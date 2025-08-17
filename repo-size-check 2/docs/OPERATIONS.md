# Operations Guide

## Overview

This guide covers day-to-day operations for PaulyOps, including backups, file routing, and system maintenance.

## System Health Checks

### Health Check

Run comprehensive system health check:

```bash
python system_health.py
```

This checks:
- Environment configuration
- File system paths
- Provider credentials
- Python dependencies
- Backup status

### Function Check

Run end-to-end system function check:

```bash
python system_function_check.py --tenant bigsky
```

This tests:
- Health check
- Sample ingest (dry-run and real)
- Backup rotation
- Dashboard updates

## Backup Operations

### Manual Backup

Create manual backup:

```bash
python -c "
from utils.backup_rotation import BackupRotator
rotator = BackupRotator()
# Create backup logic here
"
```

### Backup Rotation

Rotate backups (moves old to archive):

```bash
python -c "
from utils.backup_rotation import BackupRotator
rotator = BackupRotator()
rotator.rotate_backups(new_backup_path)
"
```

### Cleanup Old Archives

Remove old archive files:

```bash
python -c "
from utils.backup_rotation import BackupRotator
rotator = BackupRotator()
rotator.cleanup_old_archives(max_age_days=30)
"
```

## File Routing

### Ingest Folder

Files are placed in the ingest folder for processing:

```bash
# Default location
BigSkyAgDropzone/

# Copy files for processing
cp document.pdf BigSkyAgDropzone/
```

### Router Operation

The router processes files in the ingest folder:

```bash
# Dry-run mode (safe testing)
python router.py --dry-run --tenant bigsky

# Real mode
python router.py --tenant bigsky
```

## Configuration Management

### Environment Variables

Set environment variables:

```bash
export TENANT=bigsky
export STORAGE_PROVIDER=local
export LOG_LEVEL=INFO
```

### Tenant Configuration

Update tenant configuration:

```yaml
# tenants/bigsky.yaml
tenant_id: bigsky
name: Big Sky Ag
plan: starter
storage:
  BACKUP_DIR: 00_Admin/Backups
  ARCHIVE_DIR: 00_Admin/Backups/archive
ingest:
  INGEST_FOLDER_NAME: BigSkyAgDropzone
```

## Monitoring

### Log Files

Check log files:

```bash
# Application logs
tail -f logs/paulyops_$(date +%Y-%m-%d).json

# Error logs
tail -f logs/errors_$(date +%Y-%m-%d).log
```

### Dashboard Status

Check dashboard status:

```bash
python -c "
from dashboards.update import get_dashboard_status
status = get_dashboard_status()
print(status)
"
```

## Troubleshooting

### Common Issues

1. **Backup Directory Missing**
   ```bash
   mkdir -p 00_Admin/Backups/archive
   ```

2. **Permission Errors**
   ```bash
   chmod 755 00_Admin/Backups
   ```

3. **Storage Provider Issues**
   ```bash
   # Check credentials
   python system_health.py
   ```

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python system_function_check.py
```

## Maintenance

### Regular Tasks

1. **Daily**: Check system health
2. **Weekly**: Review backup rotation
3. **Monthly**: Clean old archives
4. **Quarterly**: Update dependencies

### Dependency Updates

```bash
# Update Python dependencies
pip install -U -r requirements.txt

# Update development dependencies
pip install -U -r requirements-dev.txt
```

## Security

### Credential Management

- Store credentials in environment variables
- Never commit secrets to Git
- Rotate credentials regularly

### Access Control

- Use RBAC for user access
- Monitor API key usage
- Review audit logs

## Performance

### Optimization

1. **Storage**: Use appropriate storage provider
2. **Backup**: Configure retention policies
3. **Logging**: Set appropriate log levels
4. **Caching**: Enable caching where appropriate

### Monitoring

Monitor system performance:

```bash
# Check disk usage
du -sh 00_Admin/Backups/

# Check log file sizes
ls -lh logs/
```
