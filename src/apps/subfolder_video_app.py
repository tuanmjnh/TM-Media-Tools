import random
import os
from pathlib import Path
from src.shared.config import config
from src.core.ffmpeg_engine import FfmpegEngine

def run_app():
    # Load lại cấu hình mới nhất từ file
    config.load()
    
    print("\n" + "="*50)
    print("      SUBFOLDER VIDEO CREATOR")
    print("="*50)
    print(f"Input:  {config.INPUT_DIR}")
    print(f"Output: {config.OUTPUT_DIR}")
    print("-" * 50)
    
    engine = FfmpegEngine()
    
    try:
        config.validate()
        
        # 1. Identify subfolders
        input_dir = config.INPUT_DIR
        if not input_dir.exists():
            print(f"[Error] Thư mục đầu vào không tồn tại: {input_dir}")
            return

        # Lấy danh sách thư mục con, loại bỏ thư mục output nếu nó nằm trong input
        subfolders = []
        for f in input_dir.iterdir():
            if f.is_dir():
                # Kiểm tra xem có trùng với thư mục output không
                if f.resolve() == config.OUTPUT_DIR.resolve():
                    continue
                subfolders.append(f)
        
        if not subfolders:
            print(f"Không tìm thấy thư mục con nào hợp lệ trong: {input_dir}")
            print("(Lưu ý: App này tạo video cho từng THƯ MỤC CON bên trong thư mục chính)")
            
            # Kiểm tra xem chính thư mục này có ảnh không để hướng dẫn
            image_formats = config.IMAGE_FORMATS
            main_images = []
            for ext in image_formats:
                main_images.extend(list(input_dir.glob(f"*{ext}")))
            
            if main_images:
                print(f"\n[Gợi ý] Phát hiện thấy {len(main_images)} ảnh nằm trực tiếp trong thư mục '{input_dir.name}'.")
                print("-> Nếu bạn muốn tạo 1 video duy nhất từ các ảnh này, hãy dùng chức năng số '2' [Image2Video].")
            return

        print(f"Tìm thấy {len(subfolders)} thư mục con để xử lý.")
        
        # 2. Configuration Setup (Global for all videos in this run)
        # Using some random choices but keeping them consistent for this batch or randomizing each?
        # Let's randomize for each video to keep it interesting.
        
        for folder in subfolders:
            print(f"\nProcessing folder: {folder.name}")
            
            # Get images from this specific folder
            image_formats = config.IMAGE_FORMATS
            images = []
            for ext in image_formats:
                images.extend(list(folder.glob(f"*{ext}")))
            
            if not images:
                print(f"  - [Skip] Không tìm thấy ảnh trong thư mục: {folder.name}")
                continue
                
            print(f"  - Found {len(images)} images.")
            
            # Randomize order
            random.shuffle(images)
            
            # Select resolution and codec
            res = random.choice(engine.resolutions) if engine.resolutions else {"width": 1920, "height": 1080, "bitrate": "5000k"}
            fps = config.DEFAULT_FPS
            encoding = random.choice(engine.encodings) if engine.encodings else {"codec": "libx264", "extension": "mp4", "name": "H.264"}
            
            # Duration logic
            target_duration = random.randint(config.MIN_DURATION, config.MAX_DURATION)
            
            current_total_duration = 0.0
            final_images = []
            final_durations = []
            final_trans_durations = []
            
            # Loop to fill the target duration
            # If there are few images, they will be reused
            image_pool = images[:]
            while current_total_duration < target_duration:
                if not image_pool:
                    image_pool = images[:] # Refill
                
                img = image_pool.pop(random.randint(0, len(image_pool)-1))
                dur = round(random.uniform(config.MIN_IMAGE_DURATION, config.MAX_IMAGE_DURATION), 2)
                
                if not final_images:
                    current_total_duration = dur
                else:
                    t_dur = round(random.uniform(config.MIN_TRANSITION_DURATION, config.MAX_TRANSITION_DURATION), 2)
                    t_dur = min(t_dur, dur * 0.4, final_durations[-1] * 0.4)
                    final_trans_durations.append(t_dur)
                    current_total_duration += (dur - t_dur)
                
                final_images.append(img)
                final_durations.append(dur)
                
                if len(final_images) > 200: break # Safety limit

            print(f"  - Target: {target_duration}s | Actual: {round(current_total_duration, 2)}s | Images: {len(final_images)}")

            settings = {
                'resolution': {'width': res['width'], 'height': res['height']},
                'bitrate': res['bitrate'],
                'fps': fps,
                'codec': encoding['codec'],
                'image_durations': final_durations,
                'transition_durations': final_trans_durations,
                'output_name': f"{folder.name}.{encoding.get('extension', 'mp4')}"
            }
            
            # 3. Build and Run
            cmd, out_path = engine.build_command(final_images, settings)
            print(f"  - Rendering to: {out_path.name}")
            success, output = engine.run(cmd, duration=current_total_duration)
            
            if success:
                print(f"  - [Success] Video created: {out_path.name}")
            else:
                print(f"  - [Failed] {folder.name}")
                # print(output) # Print error if needed

    except Exception as e:
        print(f"\n[ERROR] {e}")

if __name__ == "__main__":
    run_app()
