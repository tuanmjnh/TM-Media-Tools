from src.shared.config import config
from src.core.ai_client import GeminiClient
from src.core.image_engine import ImageEngine

def run_app():
    print("\n--- Gemini Image Optimizer ---")
    
    try:
        # 1. Validate Config
        if not config.GEMINI_API_KEY:
             raise ValueError("GOOGLE_GEMINI_API_KEY not found in environment or .env file")
        config.validate()
        
        # 2. Initialize Components
        ai_client = GeminiClient(
            api_key=config.GEMINI_API_KEY,
            model_name=config.MODEL_NAME,
            retry_count=config.RETRY_COUNT,
            retry_delay=config.RETRY_DELAY
        )
        engine = ImageEngine(ai_client)
        
        # 3. Run Processing
        engine.run_batch_processing()
        
        print("\nProcessing complete.")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")

if __name__ == "__main__":
    run_app()
