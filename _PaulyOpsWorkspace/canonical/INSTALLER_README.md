# PaulyOps Desktop Installer

Welcome to the PaulyOps Desktop Installer! This installer will set up PaulyOps on your desktop with all the necessary components for intelligent document processing and workflow automation.

## 🚀 What Gets Installed

### Desktop Folders
- **`~/Desktop/PaulyOps/`** - Complete PaulyOps application with all components
- **`~/Desktop/Dropzone/`** - Intelligent file processing dropzone
- **`~/PaulyOpsHome/`** - Hidden home directory for caches and logs

### Components
- **Next.js 14 Application** - Main PaulyOps web interface
- **Dropzone Watcher** - Background service for file monitoring
- **Agent Framework** - Modular processing agents
- **Security System** - RBAC, audit logging, and sandboxing
- **Configuration Files** - Routing rules and settings

## 📋 System Requirements

### Minimum Requirements
- **macOS**: 10.15 (Catalina) or later
- **Windows**: Windows 10 or later
- **Linux**: Ubuntu 18.04 or later
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB available space
- **Network**: Internet connection for initial setup

### Recommended Requirements
- **RAM**: 16GB or more
- **Storage**: 10GB available space
- **Processor**: Multi-core processor
- **Network**: Stable internet connection

## 🔧 Installation Options

### Option 1: Quick Install (Recommended)
1. Download the installer for your platform
2. Run the installer
3. Choose "Quick Install" when prompted
4. The installer will:
   - Create all necessary folders
   - Set up background services
   - Configure default settings
   - Start the application

### Option 2: Custom Install
1. Download the installer for your platform
2. Run the installer
3. Choose "Custom Install" when prompted
4. Configure options:
   - **Installation Directory**: Choose where to install PaulyOps
   - **Create Desktop Shortcut**: Add shortcut to desktop
   - **Create Dropzone**: Set up file processing dropzone
   - **Start on Boot**: Automatically start services on system boot

## 📁 Folder Structure After Installation

```
~/Desktop/
├── PaulyOps/                    # Main application
│   ├── apps/
│   │   ├── ui/                  # Next.js web application
│   │   └── dropzone-watcher/    # File monitoring service
│   ├── agents/                  # Processing agents
│   │   ├── inbox-cleaner/       # Email processing
│   │   ├── ndvi-processor/      # Agricultural data
│   │   └── vendor-router/       # Vendor documents
│   ├── packages/                # Shared libraries
│   │   ├── shared/              # Common utilities
│   │   └── security/            # Security components
│   ├── configs/                 # Configuration files
│   │   └── routing/             # Dropzone routing rules
│   ├── docs/                    # Documentation
│   └── scripts/                 # Utility scripts
│
├── Dropzone/                    # File processing dropzone
│   ├── Processed/               # Successfully processed files
│   ├── Pending/                 # Files being processed
│   └── Error/                   # Files with processing errors
│
└── PaulyOpsHome/                # Hidden home directory
    ├── logs/                    # Application logs
    ├── cache/                   # Temporary files
    ├── config/                  # User configuration
    └── install-manifest.json    # Installation details
```

## 🎯 Getting Started

### 1. First Launch
1. Navigate to `~/Desktop/PaulyOps/apps/ui/`
2. Open terminal/command prompt
3. Run: `npm install`
4. Run: `npm run dev`
5. Open browser to `http://localhost:3000`

### 2. Initial Setup
1. **Connect Gmail**: Link your Gmail account for email processing
2. **Choose Plan**: Select a plan (7-day free trial included)
3. **Generate First Digest**: Process your first email digest
4. **Configure Dropzone**: Set up file routing rules

### 3. Using the Dropzone
1. Drop files into `~/Desktop/Dropzone/`
2. Files are automatically classified and processed
3. Check `~/Desktop/Dropzone/Processed/` for results
4. View processing logs in the web interface

## ⚙️ Configuration

### Dropzone Routing Rules
Edit `~/Desktop/PaulyOps/configs/routing/rules.yaml` to customize:
- Company detection patterns
- File classification rules
- Processing workflows
- Agent routing

### Application Settings
- **Environment Variables**: Edit `.env` in the UI directory
- **Database**: PostgreSQL connection settings
- **Authentication**: Google OAuth configuration
- **Billing**: Stripe integration settings

## 🔄 Background Services

### Dropzone Watcher
- **Purpose**: Monitors the Dropzone folder for new files
- **Status**: Automatically started during installation
- **Logs**: Located in `~/PaulyOpsHome/logs/dropzone-watcher.log`

### Agent Services
- **Purpose**: Process files based on classification
- **Status**: Started on-demand when files are detected
- **Logs**: Located in `~/PaulyOpsHome/logs/agents.log`

## 🛠️ Troubleshooting

### Common Issues

**1. Dropzone Not Processing Files**
- Check if dropzone watcher is running
- Verify file permissions
- Check logs in `~/PaulyOpsHome/logs/`

**2. Application Won't Start**
- Verify Node.js is installed (version 18+)
- Check port 3000 is available
- Review error logs

**3. Gmail Connection Issues**
- Verify Google OAuth credentials
- Check internet connection
- Review browser console for errors

### Log Files
- **Application Logs**: `~/PaulyOpsHome/logs/app.log`
- **Dropzone Logs**: `~/PaulyOpsHome/logs/dropzone-watcher.log`
- **Agent Logs**: `~/PaulyOpsHome/logs/agents.log`
- **Error Logs**: `~/PaulyOpsHome/logs/errors.log`

### Support
- **Documentation**: `~/Desktop/PaulyOps/docs/`
- **Community**: [PaulyOps Community Forum]
- **Support**: [support@paulyops.com]

## 🗑️ Uninstallation

### Option 1: Keep Home Folder (Recommended)
- Uninstaller removes application files
- Keeps `~/PaulyOpsHome/` for future reinstallation
- Preserves user data and configuration

### Option 2: Complete Removal
- Removes all PaulyOps files and folders
- Deletes `~/PaulyOpsHome/` directory
- Removes all user data and configuration

### Uninstall Process
1. Run the uninstaller
2. Choose whether to keep home folder
3. Confirm removal
4. Restart computer (recommended)

## 🔒 Security & Privacy

### Data Storage
- **Local Processing**: Files processed locally on your machine
- **Cloud Sync**: Optional cloud backup of processed results
- **Privacy**: No file content sent to servers without permission

### Permissions
- **File System**: Read/write access to Dropzone and PaulyOps folders
- **Network**: Internet access for Gmail integration and updates
- **Background**: System permissions for background services

### Audit Logging
- All file processing activities are logged
- User actions are tracked for compliance
- Logs stored locally in `~/PaulyOpsHome/logs/`

## 📈 Performance Tips

### Optimization
- **SSD Storage**: Install on SSD for better performance
- **Sufficient RAM**: 8GB+ recommended for large file processing
- **Regular Cleanup**: Clear processed files periodically
- **Background Services**: Close unnecessary applications

### Monitoring
- Check `~/PaulyOpsHome/logs/` for performance issues
- Monitor disk space usage
- Review processing times in web interface

## 🔄 Updates

### Automatic Updates
- Check for updates on application startup
- Download and install updates automatically
- Preserve user data during updates

### Manual Updates
1. Download latest installer
2. Run installer (will update existing installation)
3. Restart application

## 📞 Support & Resources

### Documentation
- **User Guide**: `~/Desktop/PaulyOps/docs/user-guide.md`
- **API Reference**: `~/Desktop/PaulyOps/docs/api-reference.md`
- **Configuration**: `~/Desktop/PaulyOps/docs/configuration.md`

### Community
- **Forum**: [PaulyOps Community Forum]
- **Discord**: [PaulyOps Discord Server]
- **GitHub**: [PaulyOps GitHub Repository]

### Support
- **Email**: support@paulyops.com
- **Phone**: +1 (555) 123-4567
- **Hours**: Monday-Friday, 9AM-6PM EST

---

**Thank you for choosing PaulyOps!** 🚀

For the latest information and updates, visit [paulyops.com](https://paulyops.com)
