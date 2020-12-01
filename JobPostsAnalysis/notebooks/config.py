from pathlib import Path
from dataclasses import dataclass



class CONFIG:
    file_dir = Path(__file__).resolve().parent.absolute()
    data_path = file_dir.parent / 'data' 
    report_path = file_dir.parent / 'reports'
    src_path = file_dir.parent / 'src'
    models_path = file_dir.parent / 'models'
    log_path = file_dir.parent / 'reports'

@dataclass
class Query:
    location:str
    title:str
    start:int

@dataclass
class JobDesc:
    link:str
    summary:str

@dataclass
class JobInfo:
    title:str
    summarylink:str
    name:str
    location:str

if __name__ == "__main__":
    print(CONFIG.file_dir)
    print(str(CONFIG.data_path))
    print(str(CONFIG.report_path))
