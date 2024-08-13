import sys
import psycopg2
import time
import os
from urllib.parse import quote_plus
from config import Config
from config import Config
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

is_use_sql_error = '--error' in sys.argv

os.makedirs(Config.APP_LOG_FOLDER, exist_ok=True)

file_handler = logging.FileHandler(
    os.path.join(Config.APP_LOG_FOLDER, "applog.txt"))

file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
logger.addHandler(console_handler)



def get_warnings():

    with open("resources/sql/connect.sql") as file:
        tenant_sql = file.read().strip()

    with open("resources/sql/query.sql") as file:
        create_index_sql = file.read().strip()

    with psycopg2.connect(Config.DATABASE_URI) as conn:
        cur = conn.cursor()
        cur.execute(tenant_sql)

        conn_str_set = set()

        for item in cur:
            conn_str_set.add(item[-1])

    ans = []

    for item in conn_str_set:
        res = {}

        for pair in item.split(';')[:-1]:
            key, value = pair.split('=')
            res[key] = value

        ans.append(res)

    db_info = []

    for db in ans:
        database = db["Database"]
        user = db["User ID"]
        password = db["Password"]
        host = db["Host"]
        port = db["Port"]
        encoded_password = quote_plus(password)
        DATABASE_URI = f'postgresql://{user}:{encoded_password}@{host}:{port}/{database}'

        try:

            with psycopg2.connect(DATABASE_URI) as conn:
                cur = conn.cursor()
                cur.execute(create_index_sql)
                conn.commit()
            
            db_info.append(f"{DATABASE_URI}: Success")
        except Exception as e:

            db_info.append(f"{DATABASE_URI}: Failed - {e}")

        time.sleep(3)

    return db_info



try:
    logger.info("Starting the application")

    db = get_warnings()

    errors = '\n'.join(db)
    logger.info(errors)

    logger.info("done")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)