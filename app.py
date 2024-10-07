"""App de controle de dieta"""

import bcrypt
from flask import Flask, jsonify, request
from flask_login import LoginManager, login_user
from database import db
from models.user import User

app = Flask(__name__)

app.config["SECRET_KEY"] = "your_secret_key"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet"
)

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    """Function load user"""
    return User.query.get(user_id)


# User routes


@app.route("/user", methods=["POST"])
def create_user():
    """Create user"""
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if email and password:
        hashed_password_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        hased_password_string = hashed_password_bytes.decode("utf-8")
        user = User(email=email, password=hased_password_string)

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User created sucessfully", "id": user.id})

    return jsonify({"message": "Dados invalidos"}), 400


@app.route("/login", methods=["POST"])
def login():
    """Login user"""
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if email and password:
        user = User.query.filter_by(email=email).first()
        hashed_password_bytes = user.password.encode("utf-8")

        is_hashed_true = bcrypt.checkpw(password.encode(), hashed_password_bytes)

        if user and is_hashed_true:
            login_user(user)
            return jsonify({"message": "User authenticated!"})

    return jsonify({"message": "Invalid credentials"}), 400


if __name__ == "__main__":
    app.run(debug=True)
