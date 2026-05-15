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
        BASE_DIR = Path(sys.executable).parent
        BUNDLE_DIR = Path(sys._MEIPASS)
    else:
        BASE_DIR = Path(__file__).parent.parent.parent
        BUNDLE_DIR = BASE_DIR

    DATA_DIR = BUNDLE_DIR / "data"
    CONFIG_FILE = BASE_DIR / "data" / "config.json"
    MODELS_DIR = DATA_DIR
    
    _data = {}

    @classmethod
    def load(cls):
        """Load hoặc reload dữ liệu từ file config.json"""
        if not cls.CONFIG_FILE.exists():
            # Nếu chưa có file config, thử khôi phục từ mặc định
            if not cls.restore_defaults():
                # Nếu không khôi phục được (thiếu file default), dùng dữ liệu trống
                cls._data = {}
        
        if cls.CONFIG_FILE.exists():
            try:
                with open(cls.CONFIG_FILE, "r", encoding="utf-8") as f:
                    cls._data = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load config.json: {e}")
        
        # Cập nhật các thuộc tính từ dữ liệu đã load
        cls.GEMINI_API_KEY = _get_config_value(cls._data, "gemini.api_key", "")
        cls.MODEL_NAME = _get_config_value(cls._data, "gemini.model_name", "gemini-1.5-flash-002")
        cls.PROMPT = _get_config_value(cls._data, "gemini.prompt", "Optimize this image to 4K resolution.")
        
        cls.IMAGE_FORMATS = _get_config_value(cls._data, "video.image_formats", [".jpg", ".jpeg", ".png", ".webp"])
        if isinstance(cls.IMAGE_FORMATS, str): cls.IMAGE_FORMATS = cls.IMAGE_FORMATS.split(",")
        
        cls.MIN_IMAGES = int(_get_config_value(cls._data, "video.min_images", 5))
        cls.MAX_IMAGES = int(_get_config_value(cls._data, "video.max_images", 10))
        cls.MIN_DURATION = int(_get_config_value(cls._data, "video.min_duration", 15))
        cls.MAX_DURATION = int(_get_config_value(cls._data, "video.max_duration", 30))
        
        cls.MIN_IMAGE_DURATION = float(_get_config_value(cls._data, "video.min_image_duration", 2.0))
        cls.MAX_IMAGE_DURATION = float(_get_config_value(cls._data, "video.max_image_duration", 5.0))
        cls.MIN_TRANSITION_DURATION = float(_get_config_value(cls._data, "video.min_transition_duration", 0.5))
        cls.MAX_TRANSITION_DURATION = float(_get_config_value(cls._data, "video.max_transition_duration", 1.5))
        
        cls.ZOOM_SPEED = float(_get_config_value(cls._data, "video.zoom_speed", 0.0015))
        cls.VIDEO_SPEED = float(_get_config_value(cls._data, "video.video_speed", 1.0))
        
        cls.AUDIO_FILE = _get_config_value(cls._data, "video.audio_file", "")
        cls.AUDIO_VOLUME = float(_get_config_value(cls._data, "video.audio_volume", 1.0))
        
        cls.REUSE_IMAGES = str(_get_config_value(cls._data, "video.reuse_images", "true")).lower() == "true"
        cls.DEFAULT_FPS = int(_get_config_value(cls._data, "video.default_fps", 30))
        cls.TRANSITIONS = _get_config_value(cls._data, "video.transitions", [])
        cls.CODEC_ID = _get_config_value(cls._data, "video.codec_id", None)
        cls.RESOLUTION_ID = _get_config_value(cls._data, "video.resolution_id", None)
        
        _ffmpeg_env = _get_config_value(cls._data, "video.ffmpeg_binary", None)
        if _ffmpeg_env:
            _path = Path(_ffmpeg_env)
            cls.FFMPEG_BINARY = str(cls.BASE_DIR / _path) if not _path.is_absolute() else str(_path)
        else:
            _local_ffmpeg = cls.BASE_DIR / "bin" / "ffmpeg" / "ffmpeg.exe"
            cls.FFMPEG_BINARY = str(_local_ffmpeg) if _local_ffmpeg.exists() else "ffmpeg"
        
        _input_raw = _get_config_value(cls._data, "paths.input_dir", "input")
        cls.INPUT_DIR = Path(_input_raw) if Path(_input_raw).is_absolute() else cls.BASE_DIR / _input_raw
        
        _output_raw = _get_config_value(cls._data, "paths.output_dir", "output")
        cls.OUTPUT_DIR = Path(_output_raw) if Path(_output_raw).is_absolute() else cls.BASE_DIR / _output_raw
        
        _audio_raw = _get_config_value(cls._data, "video.audio_file", "")
        if _audio_raw:
            _audio_path = Path(_audio_raw)
            cls.AUDIO_PATH = _audio_path if _audio_path.is_absolute() else cls.BASE_DIR / _audio_path
        else:
            cls.AUDIO_PATH = None

        cls.RETRY_COUNT = int(_get_config_value(cls._data, "retry.count", 3))
        cls.RETRY_DELAY = int(_get_config_value(cls._data, "retry.delay", 15))

    @classmethod
    def restore_defaults(cls):
        """Khôi phục cấu hình mặc định từ data/default_config.json"""
        default_file = cls.get_data_file("default_config.json")
        if not default_file.exists():
            return False
        
        try:
            import shutil
            shutil.copy2(default_file, cls.CONFIG_FILE)
            cls.load() # Nạp lại dữ liệu mới
            return True
        except:
            return False

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

# Khởi tạo lần đầu
Config.load()
config = Config
