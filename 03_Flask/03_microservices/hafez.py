from flask import Flask, jsonify
import hafez
 
app = Flask(__name__)
 
@app.route("/fal", methods=['GET'])
def generate_fal():
    omen = hafez.omen()
    omen = omen["interpretation"]
    return jsonify({"fal": omen})
 
if __name__ == "__main__":
    app.run(port=8081)
    