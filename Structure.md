# Project Structure - TM Media Tools

This project is a modular media processing toolset with support for multiple applications (CLI, AI-driven image optimization, and FFmpeg video generation).

## Directory Layout

```text
TM-Media-Tools/
├── bin/
│   └── ffmpeg/             # Recommended location for ffmpeg.exe
├── data/                   # Configuration data files
│   ├── encodings.json      # Video codec configurations
│   ├── framerates.txt      # List of supported FPS
│   ├── resolutions.json    # Resolution and bitrate presets
│   └── transitions.txt     # Available FFmpeg xfade transitions
├── input/                  # Source images/videos for processing
├── output/                 # Processed media results
├── src/
│   ├── apps/               # Application entry points
│   │   ├── gemini_app.py   # AI Image Optimization App
│   │   └── video_app.py    # FFmpeg Video Creator App
│   ├── core/               # Business logic engines
│   │   ├── ai_client.py    # Gemini API wrapper
│   │   ├── ffmpeg_engine.py # Video rendering engine
│   │   └── image_engine.py  # Image processing engine
│   └── shared/             # Shared utilities
│       └── config.py       # Centralized configuration manager
├── .env                    # Environment variables (API Keys, etc.)
├── config.json             # Main application configuration
├── main.py                 # Central app selector (Start here)
└── MODELS_GUIDE.md         # Guide for selecting AI models
```

## Key Components

- **main.py**: The unified entry point. Run this to select which tool to use.
- **config.json**: The primary configuration file. You can adjust AI prompts, video durations, resolutions, and FFmpeg paths here without touching the code.
- **src/core/ffmpeg_engine.py**: The "brain" of the video creator. It handles complex FFmpeg filter chains for transitions, zooming, and effects.
- **src/shared/config.py**: Handles loading configuration from both `config.json` and `.env`, providing a robust settings management system.

## Configuration Priority
The application loads settings in the following order (higher overrides lower):
1. Environment Variables (System or `.env`)
2. `config.json` file
3. Hardcoded defaults in `src/shared/config.py`
