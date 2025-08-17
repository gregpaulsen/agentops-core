# PaulyOps Configuration Guide

## Overview

This guide covers all configuration options for PaulyOps, including environment variables, provider setup, and examples.

## Environment Variables

### Core Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ENV` | `dev` | Environment (dev, staging, prod) |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `STORAGE_PROVIDER` | `local` | Storage provider (local, google, dropbox, s3) |
| `COMPANY_NAME` | `BigSkyAg` | Company name for folder structure |

### Path Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKUP_DIR` | `00_Admin/Backups` | Backup directory path |
| `ARCHIVE_DIR` | `00_Admin/Backups/archive` | Archive directory path |
| `INGEST_FOLDER_NAME` | `BigSkyAgDropzone` | Ingest folder name |

### Backup Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKUP_RETENTION_DAYS` | `30` | Days to keep archived backups |
| `MAX_BACKUP_SIZE_GB` | `10` | Maximum backup size in GB |

## Storage Provider Configuration

### Local Storage

**Default provider** - no additional configuration required.

```bash
STORAGE_PROVIDER=local
```

### Google Drive

#### Setup Steps

1. **Create Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project or select existing
   - Enable Google Drive API

2. **Create Service Account**
   ```bash
   # In Google Cloud Console:
   # 1. Go to IAM & Admin > Service Accounts
   # 2. Create Service Account
   # 3. Download JSON key file
   ```

3. **Configure Environment**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
   export GOOGLE_DRIVE_FOLDER_ID="your-folder-id"
   export STORAGE_PROVIDER="google"
   ```

4. **Get Folder ID**
   - Open Google Drive
   - Navigate to target folder
   - Copy ID from URL: `https://drive.google.com/drive/folders/FOLDER_ID`

#### Example Configuration
```bash
# .env file
STORAGE_PROVIDER=google
GOOGLE_DRIVE_FOLDER_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

### Dropbox

#### Setup Steps

1. **Create Dropbox App**
   - Go to [Dropbox App Console](https://www.dropbox.com/developers/apps)
   - Create new app
   - Set permissions: Files and folders (Full access)

2. **Generate Access Token**
   ```bash
   # In Dropbox App Console:
   # 1. Go to Settings > OAuth 2
   # 2. Generate access token
   # 3. Copy token
   ```

3. **Configure Environment**
   ```bash
   export DROPBOX_ACCESS_TOKEN="your-access-token"
   export DROPBOX_ROOT_PATH="/PaulyOps"
   export STORAGE_PROVIDER="dropbox"
   ```

#### Example Configuration
```bash
# .env file
STORAGE_PROVIDER=dropbox
DROPBOX_ACCESS_TOKEN=sl.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DROPBOX_ROOT_PATH=/PaulyOps
```

### Amazon S3

#### Setup Steps

1. **Create S3 Bucket**
   ```bash
   # In AWS Console:
   # 1. Go to S3
   # 2. Create bucket
   # 3. Configure permissions
   ```

2. **Create IAM User**
   ```bash
   # In AWS Console:
   # 1. Go to IAM
   # 2. Create user with S3 access
   # 3. Generate access keys
   ```

3. **Configure Environment**
   ```bash
   export AWS_ACCESS_KEY_ID="your-access-key"
   export AWS_SECRET_ACCESS_KEY="your-secret-key"
   export AWS_DEFAULT_REGION="us-east-1"
   export S3_BUCKET="your-bucket-name"
   export S3_PREFIX="paulyops/"
   export STORAGE_PROVIDER="s3"
   ```

#### Example Configuration
```bash
# .env file
STORAGE_PROVIDER=s3
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET=paulyops-backups
S3_PREFIX=paulyops/
```

## Configuration Examples

### Development Environment
```bash
# .env
ENV=dev
LOG_LEVEL=DEBUG
STORAGE_PROVIDER=local
COMPANY_NAME=BigSkyAg
BACKUP_DIR=00_Admin/Backups
INGEST_FOLDER_NAME=BigSkyAgDropzone
```

### Production Environment (Google Drive)
```bash
# .env
ENV=prod
LOG_LEVEL=INFO
STORAGE_PROVIDER=google
GOOGLE_DRIVE_FOLDER_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
BACKUP_RETENTION_DAYS=90
MAX_BACKUP_SIZE_GB=50
```

### Production Environment (S3)
```bash
# .env
ENV=prod
LOG_LEVEL=INFO
STORAGE_PROVIDER=s3
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET=paulyops-prod-backups
S3_PREFIX=paulyops/
BACKUP_RETENTION_DAYS=90
```

## Configuration Validation

### Health Check
```bash
# Validate configuration
python system_health.py
```

### Configuration Summary
```bash
# View current configuration
python -c "from config.loader import config; config.print_summary()"
```

### Provider Test
```bash
# Test specific provider
python -c "
from config.loader import config
print(f'Provider: {config.storage_provider}')
print(f'Has credentials: {config.has_provider_creds()}')
print(f'Provider config: {config.get_provider_config()}')
"
```

## Security Best Practices

### Credentials Management

1. **Never commit credentials to Git**
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   echo "*.key" >> .gitignore
   echo "*.json" >> .gitignore
   ```

2. **Use environment variables**
   ```bash
   # Instead of hardcoding
   export DROPBOX_ACCESS_TOKEN="your-token"
   
   # Or use .env file (not committed)
   echo "DROPBOX_ACCESS_TOKEN=your-token" >> .env
   ```

3. **Rotate credentials regularly**
   - Google: Regenerate service account keys
   - Dropbox: Regenerate access tokens
   - AWS: Rotate access keys

### Access Control

1. **Principle of least privilege**
   - Google: Minimal folder access
   - Dropbox: App-specific permissions
   - AWS: IAM policies with minimal permissions

2. **Monitor access**
   - Enable audit logging
   - Review access logs regularly
   - Set up alerts for unusual activity

## Troubleshooting

### Common Configuration Issues

#### 1. Missing Credentials
```bash
# Check if credentials are set
python -c "from config.loader import config; print(config.has_provider_creds())"

# Set credentials
export GOOGLE_DRIVE_FOLDER_ID="your-folder-id"
```

#### 2. Invalid Paths
```bash
# Check path configuration
python -c "from config.loader import config; print(f'Backup dir: {config.backup_dir}'); print(f'Archive dir: {config.archive_dir}')"

# Create missing directories
mkdir -p 00_Admin/Backups/archive
```

#### 3. Permission Issues
```bash
# Check file permissions
ls -la 00_Admin/Backups/
ls -la BigSkyAgDropzone/

# Fix permissions
chmod 755 00_Admin/Backups/
chmod 755 BigSkyAgDropzone/
```

### Provider-Specific Issues

#### Google Drive
```bash
# Check service account
python -c "import google.auth; print(google.auth.default())"

# Verify folder access
python -c "
from googleapiclient.discovery import build
service = build('drive', 'v3')
print(service.files().get(fileId='your-folder-id').execute())
"
```

#### Dropbox
```bash
# Test Dropbox connection
python -c "
import dropbox
dbx = dropbox.Dropbox('your-access-token')
print(dbx.users_get_current_account())
"
```

#### S3
```bash
# Test S3 connection
python -c "
import boto3
s3 = boto3.client('s3')
print(s3.list_buckets())
"
```

## Migration Between Providers

### Local to Cloud
1. **Configure cloud provider** (see setup steps above)
2. **Test configuration**: `python system_health.py`
3. **Migrate existing data**:
   ```bash
   # Backup local data
   tar -czf local_backup.tar.gz 00_Admin/Backups/
   
   # Upload to cloud
   # (Use provider-specific upload commands)
   ```
4. **Update configuration**: Change `STORAGE_PROVIDER`
5. **Verify migration**: `python system_function_check.py`

### Cloud to Cloud
1. **Configure new provider**
2. **Test both providers**
3. **Migrate data** between providers
4. **Update configuration**
5. **Verify migration**

## Advanced Configuration

### Custom File Routing
```python
# Custom routing rules
ROUTING_RULES = {
    "*.pdf": "01_Documents/PDFs",
    "*.jpg": "03_Images/Photos",
    "*.json": "02_Data/JSON",
    "*.csv": "02_Data/CSV"
}
```

### Backup Scheduling
```bash
# Cron job for automated backups
0 2 * * * cd /path/to/paulyops && python backup_script.py
```

### Monitoring Integration
```bash
# Health check monitoring
*/5 * * * * cd /path/to/paulyops && python system_health.py
```
