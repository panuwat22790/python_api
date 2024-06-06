import cx_Freeze
import sys
from pathlib import Path
base = None
if sys.platform == "win32":
    base = "Console"
Path = str(Path(__file__).parent.resolve())
executables = [cx_Freeze.Executable("run.py",base=base)]

cx_Freeze.setup(
    name="Wash_API",
    options={
        "build_exe": {
            "packages": ["fastapi", "uvicorn", "os"],
            "include_files": [(f"{Path}\\SSL2024", "SSL2024")]
        }
    },
    executables=executables
)