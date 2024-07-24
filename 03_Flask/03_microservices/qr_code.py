import requests
from flask import Flask, jsonify
import qrcode

 
app = Flask(__name__)

main_microservice_url = "http://127.0.0.1:8080/"

def main_microservice():
    response = requests.get(main_microservice_url)
    return response.json()
 
@app.route("/generate", methods=['GET'])
def generate_qrcode():
    text = main_microservice()
    text = str(text)
    img = qrcode.make(text)
    img.save("some_file.png")
    return jsonify({"Result": "QR Code Create Successfully"})
 
if __name__ == "__main__":
    app.run(port=8083)
