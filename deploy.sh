#!/bin/bash
set -e

echo "Starting deployment protocol..."

# Ensure we are in the project root
cd "$(dirname "$0")"

echo "1. Syncing with repository..."
git fetch origin main
git reset --hard origin/main

echo "2. Building frontend assets..."
cd frontend
npm install
npm run build
cd ..

echo "3. Triggering database backup (if running)..."
# We attempt to run the backup script locally or inside the container.
# For simplicity, we just trigger the backup python utility.
export DATABASE_PATH="./data/goals.db"
export BACKUP_DIR="./backups"
python backup.py || echo "Warning: Backup failed or database not initialized."

echo "4. Restarting Docker containers..."
docker-compose down
docker-compose up -d --build

echo "Deployment completed successfully!"
