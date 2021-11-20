import datetime
import os
from urllib.parse import quote

import dj_database_url
from invoke import run
from invoke.exceptions import Exit
from invoke.tasks import task

APP_INSTANCE_PRODUCTION = 'prod-db'


def get_db_from_url(env_string):
    return dj_database_url.parse(quote(os.getenv(env_string, Exit(f'{env_string} not set')), ':/@'))


DB_LOCAL = get_db_from_url('DATABASE_URL')
DB_PRODUCTION = get_db_from_url('DATABASE_URL_PRODUCTION')

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')


############
# Data replication
############


@task
def production_data_to_s3(c):
    origin = 'production'
    destination = 'S3 bucket'
    pull = pull_database_from_server(c, APP_INSTANCE_PRODUCTION, DB_PRODUCTION, origin, destination)
    if pull:
        push_file_to_s3(c, APP_INSTANCE_PRODUCTION)


@task
def production_data_to_local(c):
    origin = 'production'
    destination = 'local Postgres container'
    pull = pull_database_from_server(c, APP_INSTANCE_PRODUCTION, DB_PRODUCTION, origin, destination)
    if pull:
        restore_data_to_server(c, APP_INSTANCE_PRODUCTION, DB_LOCAL, origin, destination)


########
# Backup
########


def pull_database_from_server(c, app_instance, db, origin, destination):
    backup_filename = f'{app_instance}.backup'
    scratch = ' scratch' if 'scratch' in app_instance else ''
    if input(f'\nReplicate {origin}{scratch} database to {destination}? [y/N]: ') == 'y':
        print(f'Creating backup of {origin}{scratch} data')
        run(f"env PGPASSWORD='{db['PASSWORD']}' pg_dump --file '/tmp/{backup_filename}' \
                --host '{db['HOST']}' --port '{db['PORT']}' --username '{db['USER']}' \
                --format=c --blobs --no-owner --schema public '{db['NAME']}'")
        print('Backup creation complete')
        return True


########
# Restore
########

def restore_data_to_server(c, app_instance, db, origin, destination):
    backup_filename = f'{app_instance}.backup'
    scratch = ' scratch' if 'scratch' in app_instance else ''
    print(f'Restoring backup to {destination}{scratch} Postgres container')
    run(f"env PGPASSWORD='{db['PASSWORD']}' pg_restore \
                --host '{db['HOST']}' --port '{db['PORT']}' --username '{db['USER']}' \
                --dbname '{db['NAME']}' --no-owner --clean --schema public '/tmp/{backup_filename}'")
    print(f'{origin} database successfully replicated to {destination} Postgres container')


########
# Push to S3
########


def push_file_to_s3(c, app_instance):
    timestamp = str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    backup_filename = f'{app_instance}.backup'
    backup_filename_ts = f'{app_instance}-{timestamp}.backup'
    print(f'Pushing {backup_filename_ts} to S3')
    result = run(f"s3cmd \
        --access_key={AWS_ACCESS_KEY_ID} --secret_key={AWS_SECRET_ACCESS_KEY} \
        --region={AWS_S3_REGION_NAME} --host={AWS_S3_ENDPOINT_URL} \
        --host-bucket={AWS_BUCKET_NAME} --no-check-certificate \
        put /tmp/{backup_filename} s3://{AWS_BUCKET_NAME}/{backup_filename_ts}")

    if result.ok:
        print(f'{backup_filename_ts} successfully pushed to S3')
    else:
        print(result)


###########
# Utilities
###########

def make_bold(msg):
    return "\033[1m{}\033[0m".format(msg)
