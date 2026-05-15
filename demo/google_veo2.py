api_key = "[ENCRYPTION_KEY]"
import time
from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)  # read API key from GOOGLE_API_KEY

operation = client.models.generate_videos(
    model="veo-2.0-generate-001",
    prompt=f"""[Character Details]:
    Uga: Messy brown hair(slightly singed), banana leaf cloak soggy, shivering under a torn leaf, looking miserable in the rain.
    Toto: Chubby, in a fur vest and shorts, chewing a bone, staying dry under a rock overhang, squinting at Uga.
    [Image]:
    A rain-drenched jungle clearing with puddles and dripping vines. Uga, a lanky caveman with messy brown hair(slightly singed), big sparkling eyes, a soggy banana leaf cloak tied with vines, and a grass belt, shivers under a torn leaf, chattering teeth in the heavy rain. Toto, a short chubby caveman with a round face, small squinting eyes, a patchy fur vest, and shorts, chews a bone, dry under a rock overhang, looking skeptical. The scene is wet and vibrant, in a 3D Disney Pixar style, with a comedic, soggy vibe.
    [Video]:
    A 6-second 3D Disney Pixar-style video in a jungle clearing with heavy rain and puddles. Uga, a lanky caveman with messy brown hair(slightly singed) and a soggy banana leaf cloak, shivers under a leaf that tears with a rip, chattering teeth. Toto, a short chubby caveman with a fur vest, chews a bone, dry under a rock, grunting skeptically. Uga gestures wildly, shouting about an “umbrella.” Rain patters and Uga’s huff create a humorous, miserable atmosphere.
    """,
    config=types.GenerateVideosConfig(
        person_generation="allow_all",  # "dont_allow" or "allow_adult" "allow_all"
        aspect_ratio="9:16",  # "16:9" or "9:16"
    ),
)

while not operation.done:
    time.sleep(20)
    operation = client.operations.get(operation)

for n, generated_video in enumerate(operation.response.generated_videos):
    client.files.download(file=generated_video.video)
    generated_video.video.save(f"video{n}.mp4")  # save the video
