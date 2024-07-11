import time
import subprocess


def job():
    subprocess.run(["python", "main_app.py"])


while True:
    job()
    time.sleep(300)
