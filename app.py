"""App de controle de dieta"""

from flask import Flask
from flask_login import LoginManager
from database import db

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


if __name__ == "__main__":
    app.run(debug=True)
