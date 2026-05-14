# # 1. Tạo môi trường (Conda hoặc venv)
# conda create -n py310 python=3.10
# conda activate py310

# # 2. Cài thư viện CosyVoice
# pip install cosyvoice

# # 3. (Tuỳ chọn) Cài thêm Docker image nếu cần deploy:
# docker pull cosyvoice/cosyvoice:latest

from cosyvoice import CosyVoice
import os

# Danh sách ngôn ngữ hỗ trợ
LANGUAGES = [
    {"id": 0, "code": "en", "name": "English"},
    {"id": 1, "code": "fr", "name": "French"},
    {"id": 2, "code": "zh", "name": "Chinese (Mandarin)"},
    {"id": 3, "code": "ja", "name": "Japanese"},
    {"id": 4, "code": "ko", "name": "Korean"},
    {"id": 5, "code": "ru", "name": "Russian"},
    {"id": 6, "code": "de", "name": "German"},
    {"id": 7, "code": "es", "name": "Spanish"},
    {"id": 8, "code": "it", "name": "Italian"},
]

# Khởi tạo mô hình CosyVoice
model = CosyVoice(model_version="3", streaming=True)


def load_audio(path):
    if not os.path.isfile(path):
        print(f"❌ File không tồn tại: {path}")
        return None
    with open(path, "rb") as f:
        return f.read()


def synthesize(text, lang_code, speaker_audio=None):
    result = model.synthesize(
        text=text,
        lang=lang_code,
        speaker=lang_code,
        speaker_audio=speaker_audio
    )
    return result.audio


def save_audio(data, path="output.wav"):
    with open(path, "wb") as f:
        f.write(data)
    print(f"✅ Đã lưu kết quả vào {path}")


def show_languages():
    print("\n🌍 Danh sách ngôn ngữ hỗ trợ:")
    for lang in LANGUAGES:
        print(f"  [{lang['id']}] {lang['name']} ({lang['code']})")
    print()


if __name__ == "__main__":
    # Hiển thị danh sách ngôn ngữ
    show_languages()

    # Chọn ngôn ngữ qua ID
    try:
        lang_id = int(input("🔢 Nhập số ID ngôn ngữ bạn muốn dùng: "))
        selected = next((l for l in LANGUAGES if l["id"] == lang_id), None)
        if not selected:
            raise ValueError("ID không hợp lệ.")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        exit(1)

    # Nhập văn bản và giọng nói
    text = input("📝 Nhập văn bản cần đọc: ").strip()
    audio_path = input("🔊 Nhập đường dẫn tới file audio dùng để clone giọng (Enter để bỏ qua): ").strip()
    speaker_audio = load_audio(audio_path) if audio_path else None

    # Tạo giọng nói
    print(f"🔄 Đang tạo giọng nói với ngôn ngữ: {selected['name']} ({selected['code']})...")
    audio_result = synthesize(text, selected["code"], speaker_audio)

    # Lưu kết quả
    save_audio(audio_result)
