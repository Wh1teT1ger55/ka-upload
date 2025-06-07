from flask import Flask, request, jsonify, send_from_directory
import jwt
import os
from werkzeug.utils import secure_filename
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

app = Flask(__name__)
SECRET_KEY = "dein_geheimer_schluessel"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "passwort":
        token = jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")
        return jsonify({"success": True, "token": token})
    else:
        return jsonify({"success": False}), 401

@app.route("/upload", methods=["POST"])
def upload():
    auth_header = request.headers.get("Authorization", None)
    if auth_header is None or not auth_header.startswith("Bearer "):
        return jsonify({"msg": "Kein Token gefunden"}), 401

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"msg": "Token abgelaufen"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"msg": "Ungültiger Token"}), 401

    if "document" not in request.files:
        return jsonify({"success": False, "msg": "Keine Datei hochgeladen"}), 400

    file = request.files["document"]
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return jsonify({"success": True, "filename": filename})

@app.route("/files", methods=["GET"])
def get_files():
    auth_header = request.headers.get("Authorization", None)
    if auth_header is None or not auth_header.startswith("Bearer "):
        return jsonify({"msg": "Kein Token gefunden"}), 401

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"msg": "Token abgelaufen"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"msg": "Ungültiger Token"}), 401

    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({"files": files})

@app.route("/uploads/<filename>")
def download_file(filename):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"msg": "Kein oder ungültiger Token"}), 401

    token = auth_header.split(" ")[1]
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except ExpiredSignatureError:
        return jsonify({"msg": "Token abgelaufen"}), 401
    except InvalidTokenError:
        return jsonify({"msg": "Ungültiger Token"}), 401

    # Falls Token gültig ist, darf Datei ausgeliefert werden
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)