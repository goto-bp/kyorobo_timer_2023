import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages":[
        "pygame",
        "json",
        "sys"
    ],
    "include_files":[
        "setting.json",
        "sounds/",
        "img/",
        "font/",
        "Readme.md",
        "ReadMe.pdf"
    ]
}

base=None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="KyoroboTimer",
    version="0.5",
    description="Timer App",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
    )