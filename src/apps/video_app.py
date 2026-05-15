import random
from src.shared.config import config
from src.core.ffmpeg_engine import FfmpegEngine

def run_app():
    # Load lại cấu hình mới nhất từ file
    config.load()
    
    print("\n--- FFmpeg Video Creator ---")
    
    engine = FfmpegEngine()
    
    try:
        config.validate()
        
        # 1. Image Selection
        print("Selecting images...")
        images = engine.get_images(
            count_range=(config.MIN_IMAGES, config.MAX_IMAGES),
            reuse=config.REUSE_IMAGES
        )
        print(f"Selected {len(images)} images.")
        
        # 2. Configuration Setup
        res = None
        if config.RESOLUTION_ID:
            res = next((r for r in engine.resolutions if r['id'] == config.RESOLUTION_ID), None)
        if not res:
            res = random.choice(engine.resolutions) if engine.resolutions else {"width": 1920, "height": 1080, "bitrate": "5000k"}
        
        selected_fps_obj = random.choice(engine.framerates) if engine.framerates else {"fps": 30}
        fps = int(selected_fps_obj.get('fps', 30))
        
        encoding = None
        if config.CODEC_ID:
            encoding = next((e for e in engine.encodings if e['id'] == config.CODEC_ID), None)
        if not encoding:
            encoding = random.choice(engine.encodings) if engine.encodings else {"codec": "libx264", "extension": "mp4", "name": "H.264"}
        
        print(f"Configuration:")
        print(f"  - Resolution: {res.get('name', 'Custom')} ({res['width']}x{res['height']})")
        print(f"  - Bitrate: {res['bitrate']}")
        print(f"  - Framerate: {fps} FPS")
        print(f"  - Codec: {encoding['name']} ({encoding['codec']})")
        
        # Calculate total duration and select images with random duration
        target_duration = random.randint(config.MIN_DURATION, config.MAX_DURATION)
        
        current_total_duration = 0.0
        final_images = []
        final_durations = []
        final_trans_durations = []
        
        while current_total_duration < target_duration:
            img = random.choice(images)
            dur = round(random.uniform(config.MIN_IMAGE_DURATION, config.MAX_IMAGE_DURATION), 2)
            
            if not final_images:
                # First image
                current_total_duration = dur
            else:
                # Subsequent images with transition
                t_dur = round(random.uniform(config.MIN_TRANSITION_DURATION, config.MAX_TRANSITION_DURATION), 2)
                # Ensure transition is not longer than images
                t_dur = min(t_dur, dur * 0.5, final_durations[-1] * 0.5)
                
                final_trans_durations.append(t_dur)
                current_total_duration += (dur - t_dur)
                
            final_images.append(img)
            final_durations.append(dur)
            
            if len(final_images) > 100: break

        print(f"Total video duration (est): {round(current_total_duration, 2)}s")
        print(f"Final image sequence length: {len(final_images)}")

        settings = {
            'resolution': {'width': res['width'], 'height': res['height']},
            'bitrate': res['bitrate'],
            'fps': fps,
            'codec': encoding['codec'],
            'image_durations': final_durations,
            'transition_durations': final_trans_durations,
            'output_name': f"video_{random.randint(1000, 9999)}.{encoding.get('extension', 'mp4')}"
        }
        
        # 3. Build and Run
        cmd, out_path = engine.build_command(final_images, settings)
        print(f"\nRendering video to: {out_path}")
        success, output = engine.run(cmd, duration=current_total_duration)
        
        if success:
            print(f"Success! Video created at {out_path}")
        else:
            print(f"Failed to create video:\n{output}")
            
    except Exception as e:
        print(f"\n[ERROR] {e}")

if __name__ == "__main__":
    run_app()
