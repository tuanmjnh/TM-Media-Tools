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
        "--add-data", "CONFIG_GUIDE.md;.",
        "main.py"
    ]
    
    try:
        # Run PyInstaller
        subprocess.run(cmd, check=True)
        print("\n✅ Build thành công! File EXE nằm trong thư mục 'dist/'.")
        print("\n⚠️ Lưu ý: Hãy đảm bảo copy file 'config.json' và thư mục 'bin/', 'input/', 'output/' vào cùng thư mục với file EXE để ứng dụng hoạt động chính xác.")
    except Exception as e:
        print(f"\n❌ Lỗi khi build: {e}")

if __name__ == "__main__":
    build()
