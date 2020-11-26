from pathlib import Path




class CONFIG:
    file_dir = Path(__file__).resolve().parent.absolute()
    data_path = file_dir.parent / 'data' / 'raw' / 'jobpostsRaw.csv'
    report_path = file_dir.parent / 'reports'
    src_path = file_dir.parent / 'src'

if __name__ == "__main__":
    print(CONFIG.file_dir)
    print(str(CONFIG.data_path))
    print(str(CONFIG.report_path))
