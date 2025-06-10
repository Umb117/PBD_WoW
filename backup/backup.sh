#!/bin/sh

DB_HOST=${DB_HOST:-haproxy}
DB_PORT=${DB_PORT:-5000}
DB_NAME=${DB_NAME:-postgres}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-postgres}
BACKUP_RETENTION_COUNT=${BACKUP_RETENTION_COUNT:-3}
BACKUP_DIR=/backups
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/wow_db_backup_${TIMESTAMP}.sql"

echo "[$(date)] Starting backup process" >> /var/log/cron.log

echo "[$(date)] Creating backup directory: ${BACKUP_DIR}" >> /var/log/cron.log
mkdir -p ${BACKUP_DIR}

echo "[$(date)] Creating backup: ${BACKUP_FILE}" >> /var/log/cron.log
PGPASSWORD=${DB_PASSWORD} pg_dump \
  -h ${DB_HOST} \
  -p ${DB_PORT} \
  -U ${DB_USER} \
  -d ${DB_NAME} \
  > ${BACKUP_FILE} 2>> /var/log/cron.log

if [ $? -eq 0 ]; then
  echo "[$(date)] Backup created successfully: ${BACKUP_FILE}" >> /var/log/cron.log
else
  echo "[$(date)] Error creating backup" >> /var/log/cron.log
  exit 1
fi

echo "[$(date)] Cleaning up old backups, keeping last ${BACKUP_RETENTION_COUNT}" >> /var/log/cron.log
ls -t ${BACKUP_DIR}/wow_db_backup_*.sql | tail -n +$((${BACKUP_RETENTION_COUNT} + 1)) | while read -r file; do
  echo "[$(date)] Removing old backup: ${file}" >> /var/log/cron.log
  rm -f "${file}"
done

echo "[$(date)] Backup process completed" >> /var/log/cron.log