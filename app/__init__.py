from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:kevin@localhost/project"
db = SQLAlchemy(app)
pwd = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "loginpage"  # type: ignore
login_manager.login_message = "You are mot authorised to access this page. Please login first."
login_manager.login_message_category = "danger"


@app.before_first_request
def create_tables():
    db.create_all()


from app import routes
