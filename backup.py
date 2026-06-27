import os
import shutil
import datetime

def backup_db(source_path="goals.db", backup_dir="backups"):
    """Safely snapshot the SQLite database into a backup directory."""
    if not os.path.exists(source_path):
        print(f"Source database {source_path} does not exist. Skipping backup.")
        return False

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    basename = os.path.basename(source_path)
    backup_filename = f"{basename}.{timestamp}.bak"
    backup_path = os.path.join(backup_dir, backup_filename)

    try:
        shutil.copy2(source_path, backup_path)
        print(f"Successfully backed up {source_path} to {backup_path}")
        return True
    except Exception as e:
        print(f"Failed to backup database: {e}")
        return False
