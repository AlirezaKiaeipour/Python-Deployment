import os
import argparse
import requests
import urllib.request
import dotenv

parser = argparse.ArgumentParser()
parser.add_argument("--input_text",type=str)
arg = parser.parse_args()
env = dotenv.load_dotenv()

# Illusion Diffusion API
url_illusion_diffusion = "https://54285744-illusion-diffusion.gateway.alpha.fal.ai/"
Illusion_Diffusion_API_KEY = os.getenv("Illusion_Diffusion_API_KEY")
headers = {
    "Authorization": Illusion_Diffusion_API_KEY,
    "Content-Type": "application/json"
}
payload = {
    "image_url": "https://storage.googleapis.com/falserverless/illusion-examples/pattern.png",
    "prompt": f"(masterpiece:1.4), (best quality), (detailed), landscape, {arg.input_text}",
    "negative_prompt": "(worst quality, poor details:1.4), lowres, (artist name, signature, watermark:1.4), bad-artist-anime, bad_prompt_version2, bad-hands-5, ng_deepnegative_v1_75t"
}

try:
    response_illusion_diffusion = requests.post(url=url_illusion_diffusion,headers=headers,json=payload)
    urllib.request.urlretrieve(response_illusion_diffusion.json()["image"]["url"], "generated_image.jpg")
except:
    print(f"Error: {response_illusion_diffusion.status_code}\nThis Error Is For Illusion Diffusion API. Please Fix It")


## PlantNet API
url_plant = "https://my-api.plantnet.org/v2/identify/all"
PlantNet_API_KEY = os.getenv("PlantNet_API_KEY")
payload = {
    "api-key":PlantNet_API_KEY
}
files = {
    "images": open("generated_image.jpg","rb")
}

try:
    response_plant = requests.post(url=url_plant, params=payload, files=files)
    print(f"The name of the flower is: {response_plant.json()["results"][0]["species"]["genus"]["scientificName"]}")
except:
    print(f"Error: {response_plant.status_code}\nThis Error Is For PlantNet API. Please Fix It")
