from wtforms import Form, StringField, PasswordField, SubmitField, validators, IntegerField, SelectField
from app.models import User


class RegForm(Form):
    uname = StringField(
        "Username",
        validators=[
            validators.DataRequired(),
            validators.Length(min=4, message="Username must be at least 6 characters long."),
        ],
    )
    email = StringField(
        "E-Mail",
        validators=[
            validators.DataRequired(),
            validators.Email(),
            validators.Length(min=6, message="Email Address must be at least 6 characters long."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            validators.DataRequired(),
            validators.Length(min=4, message="Password must be at least 4 characters long."),
        ],
    )
    confirm = PasswordField(
        "Confirm Password",
        validators=[validators.EqualTo("password", message="Passwords do not match."), validators.DataRequired()],
    )
    submit = SubmitField("Sign Up")

    def validate_uname(self, uname):
        present = User.query.filter_by(uname=uname.data).first()
        if present:
            raise validators.ValidationError("This username has already been taken, please choose a different one.")

    def validate_email(self, email):
        present = User.query.filter_by(email=email.data).first()
        if present:
            raise validators.ValidationError(
                "This email has already been registered with us, please enter a different one."
            )


class LoginForm(Form):
    uname = StringField("Username", validators=[validators.DataRequired(), validators.Length(min=4, max=20)])
    password = PasswordField("Password", validators=[validators.DataRequired(), validators.Length(min=4, max=20)])
    submit = SubmitField("Login")


class BmiForm(Form):
    height = IntegerField("Height", validators=[validators.DataRequired()])
    weight = IntegerField("Weight", validators=[validators.DataRequired()])
    submit = SubmitField("Update")


class WaterForm(Form):
    water = IntegerField("Water", validators=[validators.DataRequired()])
    submit = SubmitField("Update")
    delete = SubmitField("Delete")
    reset = SubmitField("Reset")


class FoodForm(Form):
    food = SelectField("Food", validate_choice=False)
    submit = SubmitField("Update")
    delete = SubmitField("Delete")
    reset = SubmitField("Reset")


class WorkoutForm(Form):
    exercises = SelectField("Exercises", validate_choice=False, validators=[validators.DataRequired()])
    trainers = SelectField("Trainer", validate_choice=False, validators=[validators.DataRequired()])
    submit = SubmitField("Update")
    delete = SubmitField("Delete")
    reset = SubmitField("Reset")
