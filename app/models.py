from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now)
    uname = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def get_id(self):
        try:
            return self.id
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`")

    def __repr__(self):
        return "User(%s , %s)" % (self.uname, self.email)


class Exercise(db.Model):
    ex_no = db.Column(db.Integer, primary_key=True)
    ex_name = db.Column(db.String(20), nullable=False)
    ex_cal = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Exercise(%s , %s)" % (self.ex_name, self.ex_cal)


class Food(db.Model):
    food_no = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(20), nullable=False)
    food_cal = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Food(%s , %s)" % (self.food_name, self.food_cal)


class WaterIntake(db.Model):
    water_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    water_ml = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return "Water(%s)" % (self.water_ml)


class UserDetails(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    bmi = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return "UserDetails(%s , %s , %s)" % (self.user_id, self.height, self.weight)


class Points(db.Model):
    points_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    action = db.Column(db.String(20), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return "Points(%s , %s)" % (self.user_id, self.points)


class FoodIntake(db.Model):
    food_intake_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    food_no = db.Column(db.Integer, db.ForeignKey("food.food_no"), nullable=False)

    def __repr__(self):
        return "FoodIntake(%s , %s)" % (self.user_id, self.food_name)


class ExerciseIntake(db.Model):
    ex_intake_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    ex_no = db.Column(db.Integer, db.ForeignKey("exercise.ex_no"), nullable=False)

    def __repr__(self):
        return "ExerciseIntake(%s , %s)" % (self.user_id, self.ex_name)
