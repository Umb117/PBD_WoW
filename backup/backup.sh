#!/bin/sh

# Environment variables
POSTGRES_HOST=${POSTGRES_HOST:-postgres}
POSTGRES_PORT=${POSTGRES_PORT:-5432}
POSTGRES_DB=${POSTGRES_DB:-wow_db}
POSTGRES_USER=${POSTGRES_USER:-migrator_user}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-admin123}
BACKUP_RETENTION_COUNT=${BACKUP_RETENTION_COUNT:-5}
BACKUP_DIR=/backups
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/wow_db_backup_${TIMESTAMP}.sql"

# Log start time
echo "[$(date)] Starting backup process" >> /var/log/cron.log

# Ensure backup directory exists
echo "[$(date)] Creating backup directory: ${BACKUP_DIR}" >> /var/log/cron.log
mkdir -p ${BACKUP_DIR}

# Perform backup using pg_dump
echo "[$(date)] Creating backup: ${BACKUP_FILE}" >> /var/log/cron.log
PGPASSWORD=${POSTGRES_PASSWORD} pg_dump \
  -h ${POSTGRES_HOST} \
  -p ${POSTGRES_PORT} \
  -U ${POSTGRES_USER} \
  -d ${POSTGRES_DB} \
  > ${BACKUP_FILE} 2>> /var/log/cron.log

if [ $? -eq 0 ]; then
  echo "[$(date)] Backup created successfully: ${BACKUP_FILE}" >> /var/log/cron.log
else
  echo "[$(date)] Error creating backup" >> /var/log/cron.log
  exit 1
fi

# Remove old backups, keep only BACKUP_RETENTION_COUNT
echo "[$(date)] Cleaning up old backups, keeping last ${BACKUP_RETENTION_COUNT}" >> /var/log/cron.log
ls -t ${BACKUP_DIR}/wow_db_backup_*.sql | tail -n +$((${BACKUP_RETENTION_COUNT} + 1)) | while read -r file; do
  echo "[$(date)] Removing old backup: ${file}" >> /var/log/cron.log
  rm -f "${file}"
done

echo "[$(date)] Backup process completed" >> /var/log/cron.log