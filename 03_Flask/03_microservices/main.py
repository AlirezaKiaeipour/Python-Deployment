import requests
from flask import Flask, jsonify

 
app = Flask(__name__)

hafez_microservice_url = "http://127.0.0.1:8081/fal"
khayyam_microservice_url = "http://127.0.0.1:8082/today"

def hafez_microservice():
    response = requests.get(hafez_microservice_url)
    return response.json().get("fal")

def khayyam_microservice():
    response = requests.get(khayyam_microservice_url)
    return response.json().get("today")
 
@app.route("/", methods=['GET'])
def main():
    hafez = hafez_microservice()
    today = khayyam_microservice()
    return jsonify({"fal": hafez, "today": today})
 
if __name__ == "__main__":
    app.run(port=8080)
    