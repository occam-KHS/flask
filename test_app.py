import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/post_submit', methods=['POST'])
def post_submit():
    data = request.get_json()
    name = data.get('name')
    return jsonify({"message": f"Received {name}"})


@app.route('/get_submit', methods=['GET'])
def get_submit():
    name = request.args.get('name')
    return jsonify({"message": f"{name}"}) 
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

