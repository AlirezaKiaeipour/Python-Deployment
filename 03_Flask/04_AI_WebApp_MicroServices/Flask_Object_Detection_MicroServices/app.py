from flask import Flask, request, jsonify
from src.object_detection import YOLOv8
from utils.image import encode_image
from PIL import Image
import numpy as np

app = Flask("YOLO Object Detection")
object_detector = YOLOv8("models/yolov8n.onnx")

@app.route("/")
def read_root():
    return "Object Detection API"

@app.route("/object-detection", methods=["POST"])
def object_detection():
    file = request.files["file"]
    image = Image.open(file.stream)
    image = np.array(image)
    image, labels = object_detector(image)
    image_url = encode_image(image)

    result = {
        "image": image_url
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000)
