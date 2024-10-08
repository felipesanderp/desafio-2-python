"""App de controle de dieta"""

import bcrypt
from flask import Flask, jsonify, request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from database import db
from models.meal import Meal
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


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Funtion to logout a user. Must be login to use this route"""
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"})


@app.route("/user/<int:id_user>", methods=["GET"])
@login_required
def read_user(id_user):
    """Funtion to get logged user."""
    user = User.query.get(id_user)

    if user:
        return {"email": user.email}

    return jsonify({"message": "Usuario não encontrado"}), 404


@app.route("/user/<string:id_user>", methods=["PUT"])
@login_required
def update_user(id_user):
    """Updtae user function"""
    data = request.json
    user = User.query.get(id_user)

    if id_user != current_user.id:
        return jsonify({"message": "Action not allowed"}), 403

    if user and data.get("password"):
        hashed_password_bytes = bcrypt.hashpw(
            data.get("password").encode(), bcrypt.gensalt()
        )
        hashed_password_string = hashed_password_bytes.decode("utf-8")

        user.password = hashed_password_string
        db.session.commit()

        return jsonify({"message": f"User {id_user} updated", "id": user.id})

    return jsonify({"message": "User not found"}), 404


@app.route("/user/<string:user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id):
    """Delete user function"""
    user = User.query.get(user_id)

    if user_id != current_user.id:
        return jsonify({"message": "Action not allowed"}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User {user_id} deleted"})

    return jsonify({"message": "User not found"}), 404


# Meals Routes


@app.route("/meal", methods=["POST"])
@login_required
def create_meal():
    """Create Meal"""
    data = request.json

    user_id = current_user.id
    name = data.get("name")
    description = data.get("description")
    inside_diet = data.get("inside_diet")

    if name and description and inside_diet:
        meal = Meal(
            user_id=user_id, name=name, description=description, inside_diet=inside_diet
        )

        db.session.add(meal)
        db.session.commit()

        return jsonify({"message": "Meal created successfully", "id": meal.id})

    return jsonify({"message": "Dados invalidos"}), 400


@app.route("/meal/<string:meal_id>", methods=["GET"])
@login_required
def read_meal(meal_id):
    """Function to read meal by id"""
    meal = Meal.query.get(meal_id)

    if meal:
        return jsonify({"message": "Meal fetched successfully", "meal": meal.to_dict()})

    return jsonify({"message": "Dados invalidos"}), 400


@app.route("/meals", methods=["GET"])
@login_required
def fetch_meals():
    """Fetch logged user meals"""
    meals = Meal.query.join(User).filter(User.id == current_user.user_id).all()

    if meals:
        return jsonify(
            {
                "message": "Meals fetched successfully",
                "meals": [meal.to_dict() for meal in meals],
            }
        )

    return jsonify({"message": "Dados invalidos"}), 400


@app.route("/meal/<string:meal_id>", methods=["PUT"])
@login_required
def update_meal(meal_id):
    """Update meal function"""
    meal = Meal.query.get(meal_id)

    if meal and meal.user_id == current_user.user_id:
        data = request.json
        meal.name = data.get("name")
        meal.description = data.get("description")
        meal.inside_diet = data.get("inside_diet")
        db.session.commit()
        return jsonify({"message": "Meal updated successfully", "id": meal.id})

    return jsonify({"message": "Dados invalidos"}), 400


@app.route("/meal/<string:meal_id>", methods=["DELETE"])
@login_required
def delete_meal(meal_id):
    """Delete meal function"""
    meal = Meal.query.get(meal_id)

    if meal and meal.user_id == current_user.user.id:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": "Meal deleted successfully"})

    return jsonify({"message": "Dados invalidos"}), 400


if __name__ == "__main__":
    app.run(debug=True)
