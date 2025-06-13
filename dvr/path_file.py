from datetime import datetime
from pathlib import Path


def dir_path() -> str:
    dir_name = 'record/' + datetime.now().strftime('%Y-%m-%d') + '/'
    Path(dir_name).mkdir(parents=True, exist_ok=True)

    return dir_name
