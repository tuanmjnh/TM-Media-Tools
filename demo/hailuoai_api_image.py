import requests
import json
from libJson import JsonHandler
# data = read_json_file("data/hailuoai.json")
# print(data['list'][0]['key'])


url = "https://api.minimaxi.chat/v1/image_generation"
api_key = "your api key"


def create_image(url, api_key, prompt, number=1, aspect_ratio="16:9"):
    try:
        payload = json.dumps({
            "model": "image-01",
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "response_format": "url",
            "n": number,
            "prompt_optimizer": True
        })
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()
    except FileNotFoundError:
        print("API key file not found. Please create 'api_key.txt' with your API key.")
        return None


# Example usage
if __name__ == "__main__":
    # Example prompt
    prompt = "A futuristic cityscape at sunset with neon lights and flying cars, cinematic style"
    jsonHandler = JsonHandler("data/hailuoai.json")
    hailuoai = jsonHandler.read_json()
    # print(hailuoai['list'][0]['key'])
    # Generate image and save response
    result = create_image(url, hailuoai['list'][0]['key'], prompt)
    if result:
        print("Response:", result)
