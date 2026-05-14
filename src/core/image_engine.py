from pathlib import Path
from PIL import Image
from io import BytesIO
from src.core.ai_client import GeminiClient
from src.shared.config import config

class ImageEngine:
    def __init__(self, ai_client: GeminiClient):
        self.ai_client = ai_client
        self.image_extensions = (".jpg", ".jpeg", ".png", ".webp")

    def run_batch_processing(self):
        """
        Processes all images in the input directory.
        """
        input_dir = config.INPUT_DIR
        output_dir = config.OUTPUT_DIR
        
        files = [f for f in input_dir.iterdir() if f.suffix.lower() in self.image_extensions]
        
        if not files:
            print(f"No images found in {input_dir}")
            return

        print(f"Processing {len(files)} files...")

        for file_path in files:
            self.process_single_file(file_path, output_dir)
            # Add a small delay between requests to avoid rate limits
            import time
            time.sleep(2)

    def process_single_file(self, file_path: Path, output_dir: Path):
        print(f"[*] Processing: {file_path.name}")
        try:
            img = Image.open(file_path)
            image_data_list = self.ai_client.process_image(config.PROMPT, img)
            
            if not image_data_list:
                print(f"    [!] No image output returned for {file_path.name}")
                return

            for idx, img_bytes in enumerate(image_data_list):
                result_img = Image.open(BytesIO(img_bytes))
                output_filename = f"processed_{file_path.stem}_{idx}.png"
                save_path = output_dir / output_filename
                result_img.save(save_path)
                print(f"    [+] Saved: {output_filename}")
                
        except Exception as e:
            print(f"    [!] Error processing {file_path.name}: {e}")
