import sys
from cx_Freeze import setup, Executable

sys.setrecursionlimit(67108864)

build_exe_options = {
    "packages":[
        "pygame",
        "json",
        "sys",
        "random"
    ],
    "include_files":[
        "setting.json",
        "sounds/",
        "img/",
        "font/",
        "Readme.md",
        "ReadMe.pdf",
        "ReadMe.html"
    ]
}

base=None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="KyoroboTimer",
    version="0.95",
    description="Timer App",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
    )

# python setup.py bdist_msi