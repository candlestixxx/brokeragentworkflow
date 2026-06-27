# TODO

## Current Tasks (Phase 38: Automated Database Backups)
- [ ] Write `backup_db()` helper in a new module `backup.py` capturing safely snapshotting the SQLite store locally into a `backups/` directory.
- [ ] Integrate a scheduled background task inside `tasks.py` mapping Celery cron jobs triggering `backup_db()`.
- [ ] Implement robust Pytest structures validating backup generation cleanly successfully.

## Completed Tasks
- All Phase 1-37 tasks completed.
