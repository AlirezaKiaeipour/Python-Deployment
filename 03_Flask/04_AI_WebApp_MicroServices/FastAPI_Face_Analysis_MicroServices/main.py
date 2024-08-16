from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from src.face_analysis import FaceAnalysis

app = FastAPI()
face_analysis = FaceAnalysis("models/det_10g.onnx", "models/genderage.onnx")

@app.get("/")
def read_root():
    return "Face Analysis API"

@app.post("/face-analyze")
async def face_analyze(file:UploadFile = File()):
    image = await file.read()
    image = np.frombuffer(image, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    gender, age = face_analysis.detect_age_gender(image)

    result = {
        "gender": gender,
        "age": age
    }

    return JSONResponse(result)