from google import genai
from google.genai import types
from PIL import Image
import time

class GeminiClient:
    def __init__(self, api_key: str, model_name: str, retry_count: int = 3, retry_delay: int = 15):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.retry_count = retry_count
        self.retry_delay = retry_delay

    def process_image(self, prompt: str, image: Image.Image):
        """
        Sends an image to Gemini and returns the processed image parts.
        """
        for attempt in range(self.retry_count + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[prompt, image],
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"]
                    )
                )
                
                image_parts = []
                if response.candidates and response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if part.inline_data:
                            image_parts.append(part.inline_data.data)
                
                return image_parts
            except Exception as e:
                if "429" in str(e) and attempt < self.retry_count:
                    print(f"    [!] Rate limit hit (429). Retrying in {self.retry_delay}s... (Attempt {attempt+1}/{self.retry_count})")
                    time.sleep(self.retry_delay)
                    continue
                print(f"Error calling Gemini API: {e}")
                return None
