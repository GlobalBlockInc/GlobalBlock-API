from flask import Flask, jsonify, request

app = Flask(__name__)

# Home Route
@app.route('/')
def home():
    print("Home route was called!")  # Debugging message
    return jsonify({"message": "GlobalBlock API is running!"})

# Health Check Route
@app.route('/health', methods=['GET'])
def health():
    print(f"Health check was called! Request method: {request.method}")  # Debugging message
    response = jsonify({"status": "healthy"})
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response, 200  # Ensure HTTP 200 OK

# Run API
if __name__ == "__main__":
    print("Starting Flask API...")  # Debugging message
    app.run(host="0.0.0.0", port=5000, debug=True)

