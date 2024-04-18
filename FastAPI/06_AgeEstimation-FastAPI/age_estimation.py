import numpy as np
import cv2
from deepface import DeepFace
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()

@app.get("/")
def read_root():
    return "Age Estimation From The Image"

@app.post("/age-estimation")
async def read_image(input_image:UploadFile = File(None)):
    if not input_image.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Error in receiving the image")
    
    image = await input_image.read()
    image = np.frombuffer(image, dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
    Age_analyze = DeepFace.analyze(img_path = image, actions = ['age'])
    return f"Your age is: {Age_analyze[0]['age']}"
