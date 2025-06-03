from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
SECRET_KEY = "dein_geheimer_schluessel"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    # Hier erfolgt die Überprüfung von Username und Passwort
    if username == "admin" and password == "passwort":  # Beispielhafte Überprüfung
        # Erstelle ein JWT-Token (mit einer sinnvollen Expiration in der Produktion)
        token = jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")
        return jsonify({"success": True, "token": token})
    else:
        return jsonify({"success": False}), 401

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

    # Token ist gültig — hier werden beispielhaft Dateinamen gesendet.
    files = ["datei1.txt", "datei2.jpg"]
    return jsonify({"files": files})