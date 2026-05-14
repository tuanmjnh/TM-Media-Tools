import os
import sys
import json
from pathlib import Path

def _get_config_value(data, path, default):
    # Ưu tiên lấy từ JSON config
    keys = path.split(".")
    curr = data
    for k in keys:
        if isinstance(curr, dict) and k in curr:
            curr = curr[k]
        else:
            return default
    return curr

class Config:
    # Xác định thư mục gốc của ứng dụng
    if getattr(sys, 'frozen', False):
        # Nếu đang chạy từ file EXE
        BASE_DIR = Path(sys.executable).parent
        BUNDLE_DIR = Path(sys._MEIPASS)
    else:
        # Nếu đang chạy từ mã nguồn (script)
        BASE_DIR = Path(__file__).parent.parent.parent
        BUNDLE_DIR = BASE_DIR

    CONFIG_FILE = BASE_DIR / "config.json"
    
    _data = {}
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                _data = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load config.json: {e}")

    # API Keys
    GEMINI_API_KEY = _get_config_value(_data, "gemini.api_key", "")
    
    # Gemini App Settings
    MODEL_NAME = _get_config_value(_data, "gemini.model_name", "gemini-1.5-flash-002")
    PROMPT = _get_config_value(_data, "gemini.prompt", "Optimize this image to 4K resolution.")
    
    # Video App Settings
    IMAGE_FORMATS = _get_config_value(_data, "video.image_formats", [".jpg", ".jpeg", ".png", ".webp"])
    if isinstance(IMAGE_FORMATS, str): IMAGE_FORMATS = IMAGE_FORMATS.split(",")
    
    MIN_IMAGES = int(_get_config_value(_data, "video.min_images", 5))
    MAX_IMAGES = int(_get_config_value(_data, "video.max_images", 10))
    MIN_DURATION = int(_get_config_value(_data, "video.min_duration", 15))
    MAX_DURATION = int(_get_config_value(_data, "video.max_duration", 30))
    
    # Image Timing
    IMAGE_DURATION = float(_get_config_value(_data, "video.image_duration", 3.0))
    MIN_IMAGE_DURATION = float(_get_config_value(_data, "video.min_image_duration", 2.0))
    MAX_IMAGE_DURATION = float(_get_config_value(_data, "video.max_image_duration", 5.0))
    TRANSITION_DURATION = float(_get_config_value(_data, "video.transition_duration", 1.0))
    
    # Effects
    ZOOM_SPEED = float(_get_config_value(_data, "video.zoom_speed", 0.0015))
    VIDEO_SPEED = float(_get_config_value(_data, "video.video_speed", 1.0))
    
    # Audio
    AUDIO_FILE = _get_config_value(_data, "video.audio_file", "")
    AUDIO_VOLUME = float(_get_config_value(_data, "video.audio_volume", 1.0))
    
    REUSE_IMAGES = str(_get_config_value(_data, "video.reuse_images", "true")).lower() == "true"
    DEFAULT_FPS = int(_get_config_value(_data, "video.default_fps", 30))
    TRANSITIONS = _get_config_value(_data, "video.transitions", [])
    CODEC_ID = _get_config_value(_data, "video.codec_id", None)
    RESOLUTION_ID = _get_config_value(_data, "video.resolution_id", None)
    
    # FFmpeg Binary Path logic
    _ffmpeg_env = _get_config_value(_data, "video.ffmpeg_binary", None)
    
    if _ffmpeg_env:
        # User specified a path
        _path = Path(_ffmpeg_env)
        FFMPEG_BINARY = str(BASE_DIR / _path) if not _path.is_absolute() else str(_path)
    else:
        # Try to find in bin/ffmpeg/ffmpeg.exe
        _local_ffmpeg = BASE_DIR / "bin" / "ffmpeg" / "ffmpeg.exe"
        if _local_ffmpeg.exists():
            FFMPEG_BINARY = str(_local_ffmpeg)
        else:
            # Fallback to system path
            FFMPEG_BINARY = "ffmpeg"
    
    # Paths
    _input_raw = _get_config_value(_data, "paths.input_dir", "input")
    INPUT_DIR = BASE_DIR / _input_raw if not Path(_input_raw).is_absolute() else Path(_input_raw)
    
    _output_raw = _get_config_value(_data, "paths.output_dir", "output")
    OUTPUT_DIR = BASE_DIR / _output_raw if not Path(_output_raw).is_absolute() else Path(_output_raw)
    
    _audio_raw = _get_config_value(_data, "video.audio_file", "")
    if _audio_raw:
        _audio_path = Path(_audio_raw)
        AUDIO_PATH = BASE_DIR / _audio_path if not _audio_path.is_absolute() else _audio_path
    else:
        AUDIO_PATH = None

    DATA_DIR = BUNDLE_DIR / "data"
    MODELS_DIR = BUNDLE_DIR / "data" # Alias for convenience

    # Retry Settings
    RETRY_COUNT = int(_get_config_value(_data, "retry.count", 3))
    RETRY_DELAY = int(_get_config_value(_data, "retry.delay", 15))

    @classmethod
    def validate(cls):
        """Tự động tạo các thư mục nếu thiếu"""
        folders = [cls.INPUT_DIR, cls.OUTPUT_DIR, cls.DATA_DIR, cls.BASE_DIR / "bin" / "ffmpeg"]
        for folder in folders:
            if not folder.exists():
                print(f"Creating folder: {folder}")
                folder.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_data_file(cls, filename):
        return cls.DATA_DIR / filename

config = Config
