import sys
from pathlib import Path

root_path = Path(__file__).parent.parent
src_path = root_path / "src"
sys.path.append(str(src_path))