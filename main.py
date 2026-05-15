import sys
import argparse
from pathlib import Path
from src.apps import gemini_app, video_app, subfolder_video_app

def show_guide():
    """Hiển thị nội dung từ CONFIG_GUIDE.md"""
    from src.shared.config import config
    guide_path = config.DATA_DIR / "CONFIG_GUIDE.md"
    if guide_path.exists():
        try:
            with open(guide_path, "r", encoding="utf-8") as f:
                content = f.read()
                print("\n" + "="*50)
                print("         CONFIGURATION GUIDE")
                print("="*50)
                print(content)
                print("="*50)
        except Exception as e:
            print(f"\n[Error] Could not display guide: {e}")
    else:
        print("\n[Error] CONFIG_GUIDE.md not found.")

def main():
    # Reconfigure stdout to handle UTF-8 on Windows
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass

    # Khởi tạo và kiểm tra thư mục hệ thống
    from src.shared.config import config
    config.validate()

    # Khởi tạo bộ parse đối số
    parser = argparse.ArgumentParser(
        description="TM Media Tools - Bộ công cụ xử lý media đa năng (AI Optimizer & FFmpeg Video Creator).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  python main.py              # Chạy ở chế độ menu tương tác
  python main.py gemini       # Chạy trực tiếp Gemini Image Optimizer
  python main.py video        # Chạy trực tiếp FFmpeg Video Creator
  python main.py guide        # Xem hướng dẫn cấu hình chi tiết
        """
    )
    
    # Thêm các lệnh con (subcommands)
    subparsers = parser.add_subparsers(dest="command", help="Chọn lệnh để thực thi")
    
    # Lệnh gemini
    subparsers.add_parser("gemini", help="Chạy ứng dụng tối ưu hóa hình ảnh bằng AI Gemini")
    
    # Lệnh video
    subparsers.add_parser("video", help="Chạy ứng dụng tạo video từ hình ảnh bằng FFmpeg")
    
    # Lệnh guide
    subparsers.add_parser("guide", help="Xem hướng dẫn chi tiết về các thông số cấu hình trong config.json")
    
    # Lệnh subfolder-video
    subparsers.add_parser("subfolder-video", help="Tạo video từ các thư mục con trong input_dir")
    
    # Lệnh transitions
    subparsers.add_parser("transitions", help="Liệt kê danh sách các hiệu ứng chuyển cảnh (xfade) được FFmpeg hỗ trợ")
    
    # Lệnh models
    subparsers.add_parser("models", help="Liệt kê danh sách các model AI được hỗ trợ")
    
    # Parse các đối số từ dòng lệnh
    args = parser.parse_args()

    # Xử lý theo lệnh đã chọn
    if args.command == "gemini":
        gemini_app.run_app()
    elif args.command == "video":
        video_app.run_app()
    elif args.command == "guide":
        show_guide()
    elif args.command == "subfolder-video":
        subfolder_video_app.run_app()
    elif args.command == "transitions":
        show_transitions()
    elif args.command == "models":
        show_models()
    else:
        # Nếu không có lệnh nào, hiển thị menu tương tác truyền thống
        interactive_menu()

def show_models():
    """Hiển thị danh sách các model AI hỗ trợ"""
    from src.shared.config import config
    import json
    
    models_file = config.DATA_DIR / "models.json"
    if not models_file.exists():
        print(f"\n[Error] Không tìm thấy file: {models_file}")
        return

    try:
        with open(models_file, "r", encoding="utf-8") as f:
            models = json.load(f)
            
        print("\n" + "="*85)
        print(f"{'GROUP':<12} {'TYPE':<20} {'ID':<25} {'DESCRIPTION'}")
        print("-" * 85)
        for m in models:
            print(f"{m.get('group', 'N/A'):<12} {m.get('type', 'N/A'):<20} {m.get('id', 'N/A'):<25} {m.get('description', '')}")
        print("="*85)
    except Exception as e:
        print(f"\n[Error] Lỗi đọc danh sách model: {e}")

def show_transitions():
    """Chạy lệnh ffmpeg để liệt kê các hiệu ứng xfade hỗ trợ và định dạng JSON"""
    from src.shared.config import config
    import subprocess
    import re
    import json
    
    print(f"\n--- Phân tích hiệu ứng từ: {config.FFMPEG_BINARY} ---")
    cmd = [config.FFMPEG_BINARY, "-h", "filter=xfade"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        output = result.stdout
        
        # 1. Trích xuất danh sách Transitions
        transitions = []
        # Tìm phần danh sách giữa các tên transition (thường thụt đầu dòng sau 'transition')
        # Format: "     name            ID            ..FV....... description"
        pattern = re.compile(r"^\s{5}([a-z0-9_]+)\s+\d+\s+\.\.FV\.\.\.\.\.\.\.\s+(.*)$", re.MULTILINE)
        matches = pattern.findall(output)
        
        for name, desc in matches:
            if name == "custom": continue # Bỏ qua custom
            transitions.append({
                "id": name,
                "name": name.capitalize().replace("_", " "),
                "description": desc.strip()
            })
            
        # 2. Trích xuất các tham số khác (duration, offset, expr)
        params = []
        param_pattern = re.compile(r"^\s{3}(duration|offset|expr)\s+<[^>]+>\s+\.\.FV\.\.\.\.\.\.\.\s+(.*)$", re.MULTILINE)
        param_matches = param_pattern.findall(output)
        for p_name, p_desc in param_matches:
            params.append({
                "parameter": p_name,
                "description": p_desc.strip()
            })

        # 3. Hiển thị kết quả dạng JSON để copy
        print("\n[ COPY DỮ LIỆU DƯỚI ĐÂY VÀO transitions.json ]")
        print("="*50)
        print(json.dumps(transitions, indent=2, ensure_ascii=False))
        print("="*50)
        
        print("\n[ THÔNG SỐ CẤU HÌNH XFADE ]")
        for p in params:
            print(f"- {p['parameter']}: {p['description']}")
            
    except Exception as e:
        print(f"\n[Error] Không thể phân tích FFmpeg: {e}")

def interactive_menu():
    """Menu tương tác khi không truyền đối số"""
    while True:
        print("\n" + "="*40)
        print("      TM MEDIA TOOLS - SELECT APP")
        print("="*40)
        print("1. [Image2Image] - Gemini Image Optimizer 4K")
        print("2. [Image2Video] - FFmpeg Video Creator (from Images)")
        print("3. [Image2Video] - Subfolder Video Creator (One video per subfolder)")
        print("4. [Help - Config] - View Configuration Guide")
        print("5. [Help - Video] - List Supported Video Transitions (xfade)")
        print("6. [Help - AI] - List Supported AI Models")
        print("7. [System] - Restore Default Configuration")
        print("0. Exit")
        print("="*40)

        try:
            choice = input("\nEnter your choice (0-5): ").strip()
            if choice == '1':
                gemini_app.run_app()
            elif choice == '2':
                video_app.run_app()
            elif choice == '3':
                subfolder_video_app.run_app()
            elif choice == '4':
                show_guide()
            elif choice == '5':
                show_transitions()
            elif choice == '6':
                show_models()
            elif choice == '7':
                confirm = input("Bạn có chắc chắn muốn khôi phục cấu hình mặc định? (y/n): ").strip().lower()
                if confirm == 'y':
                    from src.shared.config import config
                    config.restore_defaults()
            elif choice == '0':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
