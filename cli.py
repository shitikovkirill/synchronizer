from pathlib import Path
from sync.main import run

if __name__ == "__main__":
    run(Path("source"), Path("replica"))
