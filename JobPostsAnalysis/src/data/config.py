from pathlib import Path

class CONFIG:
    base = Path(__file__).parent.parent.parent
    data_path = base / 'data'
    log_path = base / 'reports'

if __name__ == "__main__":
    print(str(CONFIG.data_path))
    print(str(CONFIG.log_path.absolute()))