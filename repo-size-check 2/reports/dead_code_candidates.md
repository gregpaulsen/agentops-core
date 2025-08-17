# Dead Code Candidates Report

**Generated**: 2024-12-12

## Analysis Summary

This report identifies potential dead code candidates in the PaulyOps codebase. These are files or functions that appear to be unused but should be reviewed before deletion.

## Candidates for Review

### 1. Test Files
- `service/test_server.py` - Simple test server, may be useful for debugging
- `tests/test_smoke.py` - Basic smoke tests, keep for CI

### 2. Legacy Scripts
- `bigsky-agent/05_Automation/Scripts/` - Multiple automation scripts
  - `system_audit.py` - May be replaced by new `system_health.py`
  - `router.py` - Core functionality, keep
  - `smart_router.py` - Enhanced router, keep
  - `mobile_api.py` - API functionality, keep

### 3. Backup Files
- `paulyops_backup_20250811_211727.tar.gz` - Old backup, can be deleted
- `bigsky-agent_cloc.txt` - Code line count report, can be deleted
- `paulyops-core_cloc.txt` - Code line count report, can be deleted

## Recommendations

### Safe to Delete
- `paulyops_backup_20250811_211727.tar.gz`
- `bigsky-agent_cloc.txt`
- `paulyops-core_cloc.txt`
- `requirements-current.txt` (generated file)

### Keep for Now
- All Python modules in `service/` and `bigsky-agent/`
- Test files
- Configuration files

### Review Later
- Legacy scripts in `bigsky-agent/05_Automation/Scripts/` - may need refactoring

## Next Steps

1. Delete safe-to-delete files
2. Review legacy scripts for integration with new config system
3. Consider consolidating router functionality
4. Update imports to use new config system
