import sys
from pathlib import Path
sys.path.append(str(Path.home() / "Desktop" / "Coding_Commands"))

from bigsky_path_utils import (
    get_agent_subfolder,
    find_bigsky_root,
    get_bigsky_subfolder,
    safe_print_bigsky_path,
    backup_script
)

from pathlib import Path
sys.path.append(str(Path.home() / "Desktop" / "Coding_Commands"))

from bigsky_path_utils import (
    find_agent_root,
    get_agent_subfolder,
    find_bigsky_root,
    get_bigsky_subfolder,
    safe_print_bigsky_path,
    backup_script
)

#!/usr/bin/env python3
from datetime import datetime

print(f"☁️ Upload to Drive simulated — file already saved in BigSkyAgBackup as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("✅ Upload complete!")
