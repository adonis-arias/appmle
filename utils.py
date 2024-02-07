import requests
import json
import base64
import os
from transformers import ViTFeatureExtractor, ViTForImageClassification
from PIL import Image
from googletrans import Translator

URL_API_GENERATOR = "https://stablediffusionapi.com/api/v4/dreambooth"  
KET_API_GENERATOR = "4O2uSGyVWIIKe0IoxG3y2FFnCAk3YpTDL9cXmfG0qa25ICBaV6zvH1WVDKT1"

def generate_image(input_text):

    payload = json.dumps({
        "key":  KET_API_GENERATOR,  
        "model_id":  "juggernaut-xl-v5",  
        "prompt": input_text,
        "negative_prompt":  "painting, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, skinny, glitchy, double torso, extra arms, extra hands, mangled fingers, missing lips, ugly face, distorted face, extra legs, anime",  
        "width":  "512",  
        "height":  "512",  
        "samples":  "1",  
        "num_inference_steps":  "30",  
        "safety_checker":  "no",  
        "enhance_prompt":  "yes",  
        "seed":  None,  
        "guidance_scale":  7.5,  
        "multi_lingual":  "no",  
        "panorama":  "no",  
        "self_attention":  "no",  
        "upscale":  "no",  
        "embeddings":  "embeddings_model_id",  
        "lora":  "lora_model_id",  
        "webhook":  None,  
        "track_id":  None  
    })

    headers = {
        'Content-Type':'application/json'
    }

    response = requests.request('POST', URL_API_GENERATOR, headers=headers, data=payload)
    
    print(response.json())

    url_image_generated = response.json()['future_links'][0]


    return url_image_generated


def text_to_image(input_text):

    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    body = {
    "steps": 40,
    "width": 1024,
    "height": 1024,
    "seed": 0,
    "cfg_scale": 5,
    "samples": 1,
    "text_prompts": [
        {
        "text": input_text,
        "weight": 1
        },
        {
        "text": "blurry, bad",
        "weight": -1
        }
    ],
    }

    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-YPFVMefm4LQZiGvmUn74QOjKe7iB27Zj719KInLO9OmN7gTl",
    }

    response = requests.post(
    url,
    headers=headers,
    json=body,
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    # make sure the out directory exists
    if not os.path.exists("./out"):
        os.makedirs("./out")

    for i, image in enumerate(data["artifacts"]):
        with open(f'./out/txt2img_{image["seed"]}.png', "wb") as f:
            f.write(base64.b64decode(image["base64"]))
    
    return f'./out/txt2img_{image["seed"]}.png'



def classification_image(image):
        

    # Load the feature extractor and model from Hugging Face
    feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
    model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

    # Load your own image from local storage
    # image_path = 'images/perro.jpg'  # Replace with the path to your image
    # image = Image.open(image_path)

    image = image.convert("RGB")

    # Preprocess the image and prepare it for the model
    inputs = feature_extractor(images=image, return_tensors="pt")

    # Perform the prediction
    outputs = model(**inputs)
    logits = outputs.logits

    # Retrieve the highest probability class
    predicted_class_idx = logits.argmax(-1).item()
    print("Predicted class:", model.config.id2label[predicted_class_idx])

    return model.config.id2label[predicted_class_idx]


