import subprocess
import os
import shutil

def build():
    print("--- Building TM-Media-Tools EXE ---")
    
    # Define the command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "TM-Media-Tools",
        "--icon=public/icon.ico",
        "--add-data", "src;src",
        "--add-data", "data;data",
        "--version-file", "file_version_info.txt",
        "main.py"
    ]
    
    try:
        # Run PyInstaller
        subprocess.run(cmd, check=True)
        print("\n[SUCCESS] Build thanh cong! File EXE nam trong thu muc 'dist/'.")
        print("\n[NOTE] Hay dam bao thu muc 'data/', 'bin/', 'input/', 'output/' nam cung thu muc voi file EXE de ung dung hoat dong chinh xac.")
    except Exception as e:
        print(f"\n[ERROR] Loi khi build: {e}")

if __name__ == "__main__":
    build()
