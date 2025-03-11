from flask import Flask, request, jsonify
import jwt
import datetime
import os

app = Flask(__name__)

# Secret key for encoding/decoding JWT tokens
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'mysecretkey')

# Dummy user database
users = {"admin": "password123"}

# Endpoint: Home Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to GlobalBlockAPI!"})

# Endpoint: Login and Get Token
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username] == password:
        token = jwt.encode({"user": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                           app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"error": "Invalid credentials"}), 401

# Endpoint: Protected Route (Requires Authentication)
@app.route("/protected", methods=["GET"])
def protected():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token is missing"}), 403

    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return jsonify({"message": f"Welcome, {decoded_token['user']}!"})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 403

# Run the API
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

