from pathlib import Path
from dataclasses import dataclass, field
import random
import time
class CONFIG:
    base = Path(__file__).resolve().parent.parent.parent.parent
    data_path = base / 'data'
    log_path = base / 'reports'

@dataclass
class Query:
    location:str
    title:str
    start:int

    def sleep(self, start:int=1, end:int=6):
        time_to_sleep = random.randint(start, end)
        print(f"sleep for {time_to_sleep}s...")
        time.sleep(time_to_sleep)
@dataclass
class JobDesc:
    link:str
    summary:str

@dataclass
class JobInfo:
    title:str
    summarylink:str
    name:str
    location:str = "here"



if __name__ == "__main__":
    print(str(CONFIG.data_path.absolute()))
    print(str(CONFIG.log_path.absolute()))