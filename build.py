from cx_Freeze import setup, Executable

setup(
    name="Auto-Clicker Thingies",
    version="1.0",
    description="Auto Clicker with Color Detection",
    executables=[
        Executable(
            "multi_clicker.py",
            base="Win32GUI",
            icon=None,
            target_name="Auto-Clicker.exe"
        )
    ],
    options={
        "build_exe": {
            "packages": ["tkinter", "PIL", "keyboard", "pyautogui", "win32api", "win32con"],
            "includes": ["tkinter", "PIL", "keyboard", "pyautogui", "win32api", "win32con"],
            "include_files": [],
            "excludes": [],
            "zip_include_packages": ["*"],
            "zip_exclude_packages": []
        }
    }
)