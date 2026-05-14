import os
import random
import subprocess
import json
from pathlib import Path
from src.shared.config import config

class FfmpegEngine:
    def __init__(self):
        config.validate()
        self.input_dir = config.INPUT_DIR
        self.output_dir = config.OUTPUT_DIR
        
        # Load transitions from JSON
        all_transitions = self._load_data("transitions.json", is_json=True)
        
        # Override with config if specified
        if config.TRANSITIONS and isinstance(config.TRANSITIONS, list):
            valid_ids = [t['id'] for t in all_transitions]
            self.transitions = [t for t in config.TRANSITIONS if t in valid_ids]
            if not self.transitions:
                print("Warning: No valid transitions found in config. Using all from file.")
                self.transitions = valid_ids
        else:
            self.transitions = [t['id'] for t in all_transitions]

        self.resolutions = self._load_data("resolutions.json", is_json=True)
        self.framerates = self._load_data("framerates.json", is_json=True)
        self.encodings = self._load_data("encodings.json", is_json=True)

    def _load_data(self, filename, is_json=False):
        path = config.get_data_file(filename)
        if not path.exists():
            return []
        with open(path, "r", encoding="utf-8") as f:
            if is_json:
                return json.load(f)
            return [line.strip() for line in f if line.strip()]

    def get_images(self, count_range=(5, 10), formats=None, reuse=True):
        if formats is None:
            formats = config.IMAGE_FORMATS
        
        all_images = []
        for ext in formats:
            all_images.extend(list(self.input_dir.glob(f"*{ext}")))
        
        if not all_images:
            raise ValueError(f"No images found in {self.input_dir} with formats {formats}")

        count = random.randint(*count_range)
        if reuse:
            selected = random.choices(all_images, k=count)
        else:
            if count > len(all_images):
                print(f"Warning: Requested {count} unique images but only {len(all_images)} available. Using all.")
                selected = all_images
                random.shuffle(selected)
            else:
                selected = random.sample(all_images, count)
        
        return selected

    def build_command(self, images, settings):
        """
        Builds a complex FFmpeg command with transitions and effects.
        settings: {
            'resolution': {'width': 1920, 'height': 1080},
            'bitrate': '5000k',
            'fps': 30,
            'codec': 'libx264',
            'duration_per_image': 3,
            'transition_duration': 1,
            'effects': {'zoom': True, 'flip': 'random'},
            'output_name': 'result.mp4'
        }
        """
    def build_command(self, images, settings):
        """
        Xây dựng lệnh FFmpeg nâng cao với hiệu ứng chuyển cảnh, zoom, và âm thanh.
        """
        fps = settings.get('fps', 30)
        res = settings.get('resolution', {'width': 1920, 'height': 1080})
        w, h = res['width'], res['height']
        codec = settings.get('codec', 'libx264')
        bitrate = settings.get('bitrate', '5000k')
        trans_dur = config.TRANSITION_DURATION
        
        # Lấy danh sách thời lượng từng ảnh (nếu có)
        img_durations = settings.get('image_durations', [config.IMAGE_DURATION] * len(images))
        
        output_path = self.output_dir / settings.get('output_name', f"video_{random.randint(1000, 9999)}.mp4")

        cmd = [config.FFMPEG_BINARY, '-y']
        
        # 1. Thêm các ảnh đầu vào
        for img in images:
            # KHÔNG dùng -loop 1 ở đây, để zoompan tự xử lý duration
            cmd.extend(['-i', str(img)])

        # 2. Thêm âm thanh nếu có
        has_audio = False
        if config.AUDIO_PATH and config.AUDIO_PATH.exists():
            cmd.extend(['-i', str(config.AUDIO_PATH)])
            has_audio = True

        # 3. Xây dựng Filter Complex
        filter_complex = []
        
        # Hiệu ứng cho từng ảnh (Scale -> ZoomPan -> Speed)
        for i in range(len(images)):
            dur = img_durations[i]
            # d trong zoompan là tổng số frame đầu ra cho 1 ảnh
            total_frames = int(dur * fps)
            
            zoom_expr = f"zoom+{config.ZOOM_SPEED}"
            
            # Filter chain cho từng clip
            # QUAN TRỌNG: zoompan phải nhận 1 frame duy nhất để tạo ra total_frames
            filters = [
                f"scale={w*2}:{h*2}:force_original_aspect_ratio=decrease",
                f"pad={w*2}:{h*2}:(ow-iw)/2:(oh-ih)/2",
                f"zoompan=z='{zoom_expr}':d={total_frames}:s={w}x{h}:fps={fps}",
                f"scale={w}:{h},setsar=1",
                f"setpts={1.0/config.VIDEO_SPEED}*PTS"
            ]
            
            filter_complex.append(f"[{i}:v]{','.join(filters)}[v{i}]")

        # Áp dụng Xfade (chuyển cảnh)
        current_v = "[v0]"
        cumulative_offset = 0.0
        for i in range(1, len(images)):
            # Offset = (tổng thời gian các ảnh trước) / speed - transition_duration
            dur_prev = img_durations[i-1] / config.VIDEO_SPEED
            cumulative_offset += (dur_prev - trans_dur)
            
            # Làm tròn offset để tránh sai số
            offset_val = round(cumulative_offset, 3)
            
            trans = random.choice(self.transitions) if self.transitions else 'fade'
            new_v = f"[vt{i}]"
            filter_complex.append(f"{current_v}[v{i}]xfade=transition={trans}:duration={trans_dur}:offset={offset_val}{new_v}")
            current_v = new_v

        # Xử lý âm thanh (Volume & Speed)
        if has_audio:
            audio_idx = len(images)
            audio_filters = [f"volume={config.AUDIO_VOLUME}"]
            if config.VIDEO_SPEED != 1.0:
                # atempo giới hạn 0.5 - 2.0
                speed = config.VIDEO_SPEED
                if 0.5 <= speed <= 2.0:
                    audio_filters.append(f"atempo={speed}")
                else:
                    # Nếu speed quá cao/thấp, cần chain nhiều atempo (tạm thời để 1 cái)
                    audio_filters.append(f"atempo={max(0.5, min(2.0, speed))}")
            
            filter_complex.append(f"[{audio_idx}:a]{','.join(audio_filters)}[afinal]")

        cmd.extend(['-filter_complex', ';'.join(filter_complex)])
        
        # Mapping đầu ra
        cmd.extend(['-map', current_v])
        if has_audio:
            cmd.extend(['-map', '[afinal]', '-shortest'])
            
        cmd.extend([
            '-c:v', codec, 
            '-b:v', bitrate, 
            '-pix_fmt', 'yuv420p',
            '-r', str(fps),
            '-fps_mode', 'cfr'
        ])
        cmd.append(str(output_path))
        
        return cmd, output_path

    def run(self, cmd, duration=None):
        """
        Chạy lệnh FFmpeg và hiển thị tiến trình (%).
        """
        import re
        import sys
        
        print(f"Running command: {' '.join(cmd)}")
        
        try:
            # Khởi tạo tiến trình
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace',
                bufsize=1 # Line buffered
            )

            time_pattern = re.compile(r"time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})")
            full_output = []
            
            # Đọc output theo từng dòng
            while True:
                line = process.stdout.readline()
                if line == '' and process.poll() is not None:
                    break
                
                if line:
                    full_output.append(line)
                    if duration and duration > 0:
                        match = time_pattern.search(line)
                        if match:
                            hours, mins, secs, ms = map(int, match.groups())
                            current_total_secs = hours * 3600 + mins * 60 + secs + ms / 100.0
                            percent = min(99.9, (current_total_secs / duration) * 100)
                            sys.stdout.write(f"\r[Progress] Rendering: {percent:.1f}%")
                            sys.stdout.flush()

            # Đợi tiến trình kết thúc thực sự
            process.wait()
            sys.stdout.write(f"\r[Progress] Rendering: 100.0% - Done!          \n")
            sys.stdout.flush()
            
            if process.returncode == 0:
                return True, "".join(full_output)
            else:
                return False, "".join(full_output)
                
        except Exception as e:
            return False, str(e)
