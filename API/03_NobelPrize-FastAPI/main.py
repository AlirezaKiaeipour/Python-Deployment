import io
import json
import cv2
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse 

app = FastAPI()
data = data = json.load(open("nobel.json"))

@app.get("/")
def read_root():
    return {"Help:":"https://python-deployment-lwor.onrender.com/docs"}

@app.get("/nobel")
def read_nobel():
    return data["nobel_info"]


@app.get("/nobel/{categories}")
def read_categories(categories:str):
    if categories.lower() in data:
        return data[categories.lower()]
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Please enter the correct value: 1-physics  2-chemistry  3-medicine  4-literature")


@app.get("/image/{image_categories}")
def read_image(image_categories:str):
    if image_categories.lower() in data["image"]:
        image = cv2.imread(data["image"][image_categories.lower()])
        _,encoded_image = cv2.imencode(".png",image)
        image = StreamingResponse(io.BytesIO(encoded_image.tobytes()),media_type="image/png")
        return image
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Please enter the correct value: 1-physics  2-chemistry  3-medicine  4-literature")
