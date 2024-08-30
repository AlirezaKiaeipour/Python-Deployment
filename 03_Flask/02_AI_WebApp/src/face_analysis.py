import argparse
import cv2
from src.face_detection import RetinaFace
from src.age_gender_estimation import AgeGenderEstimator


class FaceAnalysis:
    def __init__(self, face_detection_onnx_model_path, age_gender_estimation_onnx_model_path):
        self.face_detection_model = RetinaFace(face_detection_onnx_model_path)
        self.age_gender_estimation_model = AgeGenderEstimator(age_gender_estimation_onnx_model_path)

    def detect_age_gender(self, image):
        faces = self.face_detection_model(image)
        genders = []
        ages = []
        for face in faces:
            gender, age = self.age_gender_estimation_model(image, face)
            genders.append(gender)
            ages.append(age)
            # Draw bounding box and labels on the image
        gender = 'Male' if genders[0] == 1 else 'Female'
        age = int(ages[0])
        return gender, age


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image", type=str, required=True ,help="Input image path",
    )
    parser.add_argument(
        "--face-detection-model", type=str, default="models/det_10g.onnx", help="ONNX model path"
    )
    parser.add_argument(
        "--age-gender-estimation-model", type=str, default="models/genderage.onnx", help="ONNX model path"
    )
    args = parser.parse_args()

    input_image = cv2.imread(args.image)
    if input_image is not None:
        face_analysis = FaceAnalysis(args.face_detection_model, args.age_gender_estimation_model)
        gender, age = face_analysis.detect_age_gender(input_image)
    else:
        print("Could not read image:", args.image)
