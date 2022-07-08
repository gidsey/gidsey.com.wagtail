## Enabling automated backups on server

This process is taken mainly from here with a couple of modifications:
[https://dev.to/sambhav2612/backup-postgres-to-s3-2nkk]()

### S3CMD
Install s3cmd as described.

Currently configured without encryption password (this could be added).

### Postgres
To install Postgres 13 on Ubuntu 18.04:

```bash
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
sudo apt update
sudo apt-get -y install postgresql-13

```

### Backup script

Access backup script via `nano backup.sh`

Create backup file at `backup.sh`:

```bash
#!/usr/bin/env bash

DB_NAME=$1
DB_USER=$2
DB_PASS=$3

BUCKET_NAME=gidsey/backups

TIMESTAMP=$(date +%F-%T | tr ':' '-')
TEMP_FILE=$(mktemp tmp.XXXXXXXXXX)
S3_FILE="s3://$BUCKET_NAME/photobase-live-db-$TIMESTAMP.backup"

PGPASSWORD=$DB_PASS pg_dump --format=c --blobs --no-owner --schema public --port 32770 -h localhost -U $DB_USER $DB_NAME > $TEMP_FILE
s3cmd put $TEMP_FILE $S3_FILE
rm "$TEMP_FILE"
```

Change file permission to be executable using chmod +x
```bash
chmod +x backup.sh
```

###Testing
Test the file using:
```bash
./backup.sh <DATABASE_NAME> <USER_NAME> <DATABASE_PASSWORD>
```

### Crontab
Create crontab on current user:

```bash
crontab -e
0 0 * * * ./backup.sh [db-name] [db-user] [PG PASSWORD]
```

List cron jobs:

```bash
crontab -l
OR
crontab -u username -l
```



