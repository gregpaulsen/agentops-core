#!/usr/bin/env python3
# Nightly automation status email (agnostic): SMTP (generic) or Apple Mail fallback
import os, sys, subprocess, shlex, pathlib, time, datetime, socket, re, smtplib, mimetypes
from email.message import EmailMessage

HOME = pathlib.Path.home()
DESKTOP = HOME / "Desktop"
REPORTS_DIR = DESKTOP / "Reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
TODAY = datetime.datetime.now().strftime("%Y-%m-%d")
REPORT_PATH = REPORTS_DIR / f"Nightly_Update_Report_{TODAY}.md"
SENT_MARKER = REPORTS_DIR / ".nightly_last_sent"

# ---------- CONFIG (edit as needed) ----------
CONFIG = {
    # Choose: "SMTP" or "APPLE_MAIL"
    "EMAIL_PROVIDER": os.environ.get("NR_EMAIL_PROVIDER", "SMTP"),
    "SENDER_NAME": os.environ.get("NR_SENDER_NAME", "Big Sky Automations"),
    "SENDER_EMAIL": os.environ.get("NR_SENDER_EMAIL", "gregpaulsen26@gmail.com"),  # from
    "RECIPIENTS": os.environ.get("NR_RECIPIENTS", "gregpaulsen26@gmail.com"),
    # SMTP settings (generic; works for Gmail w/ app password)
    "SMTP_HOST": os.environ.get("NR_SMTP_HOST", "smtp.gmail.com"),       # e.g. smtp.gmail.com
    "SMTP_PORT": int(os.environ.get("NR_SMTP_PORT", "587")),
    "SMTP_USERNAME": os.environ.get("NR_SMTP_USERNAME", "gregpaulsen26@gmail.com"),
    "SMTP_PASSWORD": os.environ.get("NR_SMTP_PASSWORD", ""),  # use app password for Gmail
    "SMTP_STARTTLS": os.environ.get("NR_SMTP_STARTTLS", "true").lower() == "true",

    # Paths and checks
    "DROPZONE": str(DESKTOP / "BigSkyAgDropzone"),
    "BACKUPS_ROOT": "/Volumes/BigSkyAgSSD/BigSkyAg/00_Admin/Backups",
    "ARCHIVE_SUBFOLDER": "Archive",
    "BACKUP_GLOB": "*.zip",
    "LOG_BACKUP_CANDIDATES": [
        "/Volumes/BigSkyAgSSD/BigSkyAg/05_Automation/Logs/backup.log",
        str(DESKTOP / "backup.log"),
        str(DESKTOP / "logs" / "backup.log"),
        "logs/backup.log",
    ],
    "LOG_ROUTER_CANDIDATES": [
        "/Volumes/BigSkyAgSSD/BigSkyAg/05_Automation/Logs/router.log",
        str(DESKTOP / "router.log"),
        str(DESKTOP / "logs" / "router.log"),
        "logs/router.log",
        "98_Tests/router_log.txt",
    ],
    "LAUNCHD_LABELS": [
        "com.bigsky.backup.10pm",
        "com.bigsky.router.watch",
        "com.bigsky.nightlyreport",
    ],
    "REPOS": [
        "/Volumes/BigSkyAgSSD/BigSkyAg",
        "/Volumes/BigSkyAgSSD/PaulyOps",
        "/Volumes/BigSkyAgSSD/agentops-core",
        str(DESKTOP / "repo-size-check"),
    ],
    "ENDPOINTS": [
        # {"name":"Make InboxCleaner","url":"https://hook.integromat.com/XXXX","method":"HEAD"}
    ],
}
# ---------------------------------------------

def run(cmd, timeout=5):
    try:
        out = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT, timeout=timeout)
        return True, out.decode("utf-8", "ignore").strip()
    except Exception as e:
        return False, str(e)

def size_fmt(bytes_val):
    try:
        import math
        units = ["B","KB","MB","GB","TB"]
        i = 0
        x = float(bytes_val)
        while x >= 1024 and i < len(units)-1:
            x /= 1024; i += 1
        return f"{x:.1f} {units[i]}"
    except: return f"{bytes_val} B"

def latest_backup():
    root = pathlib.Path(CONFIG["BACKUPS_ROOT"])
    if not root.exists():
        return False, "Backups root missing", ""
    zips = sorted(root.rglob(CONFIG["BACKUP_GLOB"]), key=lambda p: p.stat().st_mtime, reverse=True)
    if not zips:
        return False, "No backup zips found", ""
    latest = zips[0]
    age_h = (time.time() - latest.stat().st_mtime)/3600.0
    return True, f"{latest.name} — {size_fmt(latest.stat().st_size)} — {age_h:.1f}h old", str(latest)

def rotation_status():
    root = pathlib.Path(CONFIG["BACKUPS_ROOT"])
    arch = CONFIG["ARCHIVE_SUBFOLDER"]
    if not arch:
        return True, "Rotation disabled"
    archive = root / arch
    if not archive.exists():
        return False, f"Archive missing: {archive}"
    active = list(root.glob(CONFIG["BACKUP_GLOB"]))
    msg = f"Active backups: {len(active)} (expect 1), Archive entries: {len(list(archive.glob(CONFIG['BACKUP_GLOB'])))}"
    ok = len(active) <= 1
    return ok, msg

def grep_success(log_paths, pattern, hours=24):
    cutoff = time.time() - hours*3600
    for p in log_paths:
        fp = pathlib.Path(p)
        if fp.exists() and fp.stat().st_mtime >= cutoff:
            try:
                with open(fp, "r", errors="ignore") as f:
                    text = f.read()[-100000:]
                    if re.search(pattern, text, re.IGNORECASE):
                        return True, f"Success marker in {fp.name}"
            except: pass
    return False, "No recent success markers"

def router_status():
    return grep_success(CONFIG["LOG_ROUTER_CANDIDATES"], r"(route success|routed|no files)")

def backup_upload_status():
    return grep_success(CONFIG["LOG_BACKUP_CANDIDATES"], r"(upload success|backup completed|finished)")

def launchd_status():
    ok, out = run("launchctl list", timeout=8)
    if not ok: return False, f"launchctl error: {out}"
    missing = [lbl for lbl in CONFIG["LAUNCHD_LABELS"] if lbl not in out]
    if missing:
        return False, "Not loaded: " + ", ".join(missing)
    return True, "All expected jobs loaded"

def git_activity():
    lines = []
    since = '--since="24 hours ago"'
    for repo in CONFIG["REPOS"]:
        p = pathlib.Path(repo)
        if not (p.exists() and (p/".git").exists()):
            lines.append(f"- {repo}: not a repo")
            continue
        os.chdir(repo)
        ok1, log = run(f'git log {since} --pretty=format:"%h %ad %s" --date=short', timeout=10)
        ok2, push = run('git reflog show --date=short --pretty="%gD %gs" | head -50', timeout=10)
        pushed = "push" in push.lower() if ok2 else False
        cnt = len([l for l in log.splitlines() if l.strip()]) if ok1 else 0
        lines.append(f"- {repo}: {cnt} commits in 24h; push seen: {'yes' if pushed else 'no'}")
    return True, "\n".join(lines)

def endpoints_status():
    lines = []
    for ep in CONFIG["ENDPOINTS"]:
        name, url = ep["name"], ep["url"]
        method = ep.get("method", "HEAD").upper()
        curl = f'curl -I --max-time 2 -s -o /dev/null -w "%{{http_code}}" {shlex.quote(url)}' if method=="HEAD" \
            else f'curl -s -o /dev/null -w "%{{http_code}}" {shlex.quote(url)}'
        ok, code = run(curl, timeout=3)
        lines.append(f"- {name}: {'OK' if (ok and code and code[0] in '23') else f'ERR {code}'}")
    return True, "\n".join(lines) if lines else "No endpoints configured"

def build_report():
    host = socket.gethostname()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ok_bk, bk_msg, bk_path = latest_backup()
    ok_rot, rot_msg = rotation_status()
    ok_up, up_msg = backup_upload_status()
    ok_rt, rt_msg = router_status()
    ok_ld, ld_msg = launchd_status()
    ok_git, git_msg = git_activity()
    ep_ok, ep_msg = endpoints_status()

    md = []
    md.append(f"# Nightly Update Report — {now}")
    md.append(f"_Host: {host}_\n")
    md.append("## Backups")
    md.append(f"- Latest: {'✅' if ok_bk else '❌'} {bk_msg}")
    md.append(f"- Rotation: {'✅' if ok_rot else '❌'} {rot_msg}")
    md.append(f"- Uploads: {'✅' if ok_up else '❌'} {up_msg}")
    md.append("\n## Router")
    md.append(f"- Status: {'✅' if ok_rt else '❌'} {rt_msg}")
    md.append("\n## launchd")
    md.append(f"- Jobs: {'✅' if ok_ld else '❌'} {ld_msg}")
    md.append("\n## Git (last 24h)")
    md.append(git_msg)
    md.append("\n## Endpoints")
    md.append(ep_msg if isinstance(ep_msg, str) else ep_msg[1])
    md.append("\n---\n")
    overall_ok = all([ok_bk, ok_rot, ok_up, ok_rt, ok_ld])
    md.append(f"**Overall:** {'✅ PASS' if overall_ok else '❌ ATTENTION NEEDED'}")
    content = "\n".join(md)

    REPORT_PATH.write_text(content, encoding="utf-8")
    return overall_ok, content

def send_email_via_smtp(subject, body, attachment_path):
    host = CONFIG["SMTP_HOST"]
    user = CONFIG["SMTP_USERNAME"]
    pw   = CONFIG["SMTP_PASSWORD"]
    port = CONFIG["SMTP_PORT"]
    starttls = CONFIG["SMTP_STARTTLS"]

    if not (host and user and pw and port):
        return False, "SMTP not configured (host/user/password/port missing)."

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{CONFIG['SENDER_NAME']} <{user}>"
    msg["To"] = CONFIG["RECIPIENTS"]
    msg.set_content(body)

    # Add attachment if provided
    if attachment_path and pathlib.Path(attachment_path).exists():
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = pathlib.Path(attachment_path).name
            msg.add_attachment(file_data, maintype="text", subtype="markdown", filename=file_name)

    try:
        with smtplib.SMTP(host, port, timeout=10) as server:
            if starttls:
                server.starttls()
            server.login(user, pw)
            server.send_message(msg)
        return True, "Email sent successfully via SMTP"
    except Exception as e:
        return False, f"SMTP error: {e}"

def send_email_via_apple_mail(subject, body, attachment_path):
    # Create AppleScript to send email via Apple Mail
    script = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"{subject}"}}
        set content of newMessage to "{body}"
        set visible of newMessage to true
        
        tell newMessage
            make new to recipient with properties {{address:"{CONFIG['RECIPIENTS']}"}}
            set sender to "{CONFIG['SENDER_EMAIL']}"
        end tell
        
        activate
    end tell
    '''
    
    try:
        result = subprocess.run(["osascript", "-e", script], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return True, "Email opened in Apple Mail (manual send required)"
        else:
            return False, f"AppleScript error: {result.stderr}"
    except Exception as e:
        return False, f"Apple Mail error: {e}"

def send_email(subject, body, attachment_path):
    """Send email using configured provider."""
    if CONFIG["EMAIL_PROVIDER"] == "SMTP":
        success, message = send_email_via_smtp(subject, body, attachment_path)
        if not success:
            print(f"SMTP failed: {message}, falling back to Apple Mail...")
            return send_email_via_apple_mail(subject, body, attachment_path)
        return success, message
    else:
        return send_email_via_apple_mail(subject, body, attachment_path)

def main():
    """Main function to generate and send nightly report."""
    print("🌙 Generating nightly update report...")
    
    # Build the report
    overall_ok, content = build_report()
    print(f"📄 Report generated: {REPORT_PATH}")
    print(f"📊 Overall status: {'✅ PASS' if overall_ok else '❌ ATTENTION NEEDED'}")
    
    # Send email
    subject = f"Nightly Update Report — {TODAY} — {'✅ PASS' if overall_ok else '❌ ATTENTION NEEDED'}"
    print(f"📧 Sending email via {CONFIG['EMAIL_PROVIDER']}...")
    
    success, message = send_email(subject, content, str(REPORT_PATH))
    
    if success:
        print(f"✅ Email sent: {message}")
        # Update sent marker
        SENT_MARKER.write_text(str(time.time()))
        print(f"📝 Sent marker updated: {SENT_MARKER}")
    else:
        print(f"❌ Email failed: {message}")
        sys.exit(1)
    
    print("🎉 Nightly report complete!")

if __name__ == "__main__":
    main()
