from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import secrets  # For generating API keys

app = Flask(__name__)

# ✅ Database setup (SQLite for now, upgrade to PostgreSQL later)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ✅ Rate limiting setup (Prevents abuse)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10000 per month"]
)

# ✅ API Key Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    api_key = db.Column(db.String(50), unique=True, nullable=False)
    usage_count = db.Column(db.Integer, default=0)

# ✅ Function to check if API key is valid
def authenticate_api_key():
    api_key = request.headers.get("X-API-KEY")
    if not api_key:
        return jsonify({"error": "API Key required"}), 403
    
    user = User.query.filter_by(api_key=api_key).first()
    if not user:
        return jsonify({"error": "Invalid API Key"}), 403
    
    # ✅ Check usage limits
    if user.usage_count >= 10000:  # Adjust based on user plan
        return jsonify({"error": "API limit exceeded"}), 403
    
    # ✅ Increment usage count
    user.usage_count += 1
    db.session.commit()
    
    return user

# ✅ Route: Generate API key (for new users)
@app.route("/generate_key", methods=["POST"])
def generate_api_key():
    data = request.json
    email = data.get("email")
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    # ✅ Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"api_key": existing_user.api_key}), 200
    
    # ✅ Generate a new API key
    new_api_key = secrets.token_hex(16)
    new_user = User(email=email, api_key=new_api_key)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"api_key": new_api_key}), 201

# ✅ Route: Protected API (Requires API key)
@app.route("/protected", methods=["GET"])
@limiter.limit("1000 per month")  # Example limit
def protected():
    user = authenticate_api_key()
    if isinstance(user, dict):
        return user  # Returns error if authentication fails
    
    return jsonify({"message": "Welcome to the GlobalBlock API!"})

# ✅ Run API
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database if it doesn't exist
    app.run(host="0.0.0.0", port=5000, debug=True)

