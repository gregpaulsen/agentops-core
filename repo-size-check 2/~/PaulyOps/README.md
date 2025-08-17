# 🚀 PaulyOps - White-Label Automation System

## 📋 Overview

PaulyOps is a comprehensive white-label automation system providing system health monitoring, nightly reporting, backup management, and safe development cleanup for any organization.

## 🏗️ Project Structure

```
~/PaulyOps/
├── Coding_Commands/         # Python scripts and command wrappers
├── Reports/                 # System health reports and logs
├── Backups/                 # Local backup archives
├── config/                  # Configuration files and paths
├── UI/                      # React/Vite dashboard (optional)
├── server/                  # Node.js backend bridge (optional)
├── System_Health_Report.md  # Latest system health summary
└── README.md               # This file
```

## 🎯 Core Features

### ✅ System Health Monitoring

- Comprehensive system health checks
- Backup status and rotation monitoring
- Git repository health
- Launchd job status
- Email system validation

### ✅ Nightly Email Reports

- Automated daily status reports
- SMTP or Apple Mail fallback
- Backup and system status summaries
- Configurable recipients

### ✅ Safe Development Cleanup

- macOS development environment cleanup
- Safe file removal and organization
- Configurable cleanup levels

### ✅ Auto-Doctor Agent

- Self-healing system that fixes common issues
- Automatic backup rotation (keeps 1 active, archives others)
- LaunchAgent validation and repair
- Flag-driven component management
- Success marker creation and tracking

### ✅ Backup Management

- Automated backup creation
- Rotation and archiving
- Exclusion of backup directories
- Size monitoring

## 🚀 Quick Start

### Desktop Shortcuts

```bash
# System Health Check
~/Desktop/PaulyOps Shortcuts/system_health.command

# Nightly Report
~/Desktop/PaulyOps Shortcuts/nightly_report.command

# Safe Cleanup
~/Desktop/PaulyOps Shortcuts/safe_dev_cleanup.command

# Auto-Doctor (Self-Healing)
~/Desktop/PaulyOps Shortcuts/autodoctor.command
```

### Direct Commands

```bash
# System Health
cd ~/PaulyOps/Coding_Commands
python3 system_health.py

# Nightly Report
cd ~/PaulyOps/Coding_Commands
python3 nightly_report.py

# Auto-Doctor (Self-Healing)
cd ~/PaulyOps/Coding_Commands
python3 system_autodoctor.py
```

## ⚙️ Configuration

### Auto-Doctor Usage

The Auto-Doctor agent automatically fixes common issues:

```bash
# Run Auto-Doctor
~/Desktop/PaulyOps Shortcuts/autodoctor.command

# Dry run (see what would be changed)
~/Desktop/PaulyOps Shortcuts/autodoctor.command --dry-run
```

**What Auto-Doctor does:**

- ✅ Ensures all required folders exist
- ✅ Rotates backups (keeps 1 active, moves others to archive)
- ✅ Validates LaunchAgent plist files
- ✅ Respects status flags for disabled components
- ✅ Creates success markers for tracking
- ✅ Logs all actions with timestamps

**Configuration:**
Edit `~/PaulyOps/config/status_flags.json` to:

- Enable/disable specific checks
- Configure which LaunchAgent jobs to monitor
- Set Git repository paths to check
- Control router and endpoint checking

### Environment Setup

1. Copy `~/PaulyOps/config/env.txt` to `~/PaulyOps/config/.env`
2. Configure your email settings:
   - SMTP host, port, username, password
   - Sender and recipient email addresses
3. Set system preferences (log level, storage provider)

### LaunchAgent Setup

The nightly report is scheduled to run at 22:00 daily via LaunchAgent:

```bash
# Check status
launchctl list | grep com.bigsky.nightlyreport

# Manual load (if needed)
launchctl load ~/Library/LaunchAgents/com.bigsky.nightlyreport.plist
```

## 📊 Reports & Logs

### System Health Reports

- **Main Report**: `~/PaulyOps/System_Health_Report.md`
- **Detailed Reports**: `~/PaulyOps/Reports/system_health_YYYYMMDD_HHMMSS.md`

### Nightly Reports

- **Reports**: `~/PaulyOps/Reports/Nightly_Update_Report_YYYY-MM-DD.md`
- **Logs**: `~/PaulyOps/Reports/nightly_report.log`

### Backup Logs

- **Backup Logs**: `~/PaulyOps/Reports/backup.log`
- **Router Logs**: `~/PaulyOps/Reports/router.log`

## 🔧 Troubleshooting

### Common Issues

1. **LaunchAgent Load Error**

   ```bash
   # Try manual load
   launchctl load ~/Library/LaunchAgents/com.bigsky.nightlyreport.plist
   ```

2. **Email Not Sending**
   - Check SMTP configuration in `~/PaulyOps/config/.env`
   - Verify app password for Gmail
   - System will fallback to Apple Mail

3. **Git Repository Not Found**
   - Ensure you're running from the correct directory
   - Check that `~/Desktop/repo-size-check` exists

4. **Missing Reports Directory**

   ```bash
   # Create missing directories
   mkdir -p ~/PaulyOps/Reports
   ```

### Log Locations

- System Health: `~/PaulyOps/Reports/system_health.log`
- Nightly Report: `~/PaulyOps/Reports/nightly_report.log`
- LaunchAgent: `~/PaulyOps/Reports/nightly_report_stdout.log`

## 🎯 Production Readiness

### ✅ Completed

- [x] Centralized path configuration
- [x] Environment-based configuration
- [x] Desktop shortcuts for easy access
- [x] Comprehensive logging
- [x] Error handling and fallbacks
- [x] Self-healing directory creation

### 🔄 Optional Enhancements

- [ ] SMTP email configuration
- [ ] UI dashboard setup
- [ ] Docker containerization
- [ ] Cloud deployment
- [ ] Multi-tenant support

## 📞 Support

For issues or questions:

1. Check the troubleshooting section above
2. Review logs in `~/PaulyOps/Reports/`
3. Run system health check for diagnostics

## 🚀 Deployment

This system is designed to be:

- **Portable**: All paths are relative to user home
- **Self-contained**: No external dependencies beyond Python
- **Configurable**: Environment-based settings
- **Safe**: Non-destructive operations only

Ready for deployment to client environments!
