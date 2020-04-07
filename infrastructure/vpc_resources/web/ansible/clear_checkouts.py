from datetime import datetime
import os
import pathlib
import shutil

base_dir = "/home/django/checkouts"

current_time = datetime.utcnow()
for folder_name in os.listdir(base_dir):
    if (
        current_time - datetime.strptime(folder_name, "%Y-%m-%d_%H-%M-%S-%Z")
    ).days >= 5:
        shutil.rmtree(pathlib.Path(base_dir, folder_name))
        print(pathlib.Path(base_dir, folder_name))
