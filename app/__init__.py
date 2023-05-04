from flask import Flask

from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:kevin@localhost/project"


pwd = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "loginpage"  # type: ignore
login_manager.login_message = "You are mot authorised to access this page. Please login first."
login_manager.login_message_category = "danger"

with app.app_context():
    from app.models import db

    db.init_app(app)
    db.create_all()


from app import routes
