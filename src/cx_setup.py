import cx_Freeze
from setuptools import find_packages

# To overcome issue with Anaconda on Windows
import sys

sys.setrecursionlimit(2000)

from configs.meta import TITLE, VERSION

base = None
if sys.platform == "win32":
    base = "Win32GUI"
executables = [cx_Freeze.Executable(script="main.py", base=base)]


cx_Freeze.setup(
    name=TITLE,
    version=VERSION,
    options={
        "build_exe": {
            "packages": ["pygame", "numpy"] + find_packages(),
            "include_files": ["../assets"],
            "includes": find_packages(),
        }
    },
    executables=executables,
)
