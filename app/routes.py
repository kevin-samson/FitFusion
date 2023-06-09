from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import *
from app.models import *
from app import app, db, pwd
from sqlalchemy import text
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def homepage():
    return render_template(
        "information.html",
    )


@app.route("/signup", methods=["GET", "POST"])
def signuppage():
    if current_user.is_authenticated:  # type: ignore
        flash("You are already logged in.", "warning")
        return redirect(url_for("homepage"))
    form = RegForm(request.form)
    if request.method == "POST" and form.validate():
        hashed = pwd.generate_password_hash(form.password.data).decode("utf-8")
        element = User(uname=form.uname.data, email=form.email.data, password=hashed)  # type: ignore
        db.session.add(element)
        db.session.commit()
        flash("Account created for %s!" % (form.uname.data), "success")
        return redirect(url_for("loginpage"))
    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def loginpage():
    if current_user.is_authenticated:  # type: ignore
        flash("You are already logged in.", "warning")
        return redirect(url_for("homepage"))
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        member = User.query.filter_by(uname=form.uname.data).first()

        if member and pwd.check_password_hash(member.password, form.password.data):
            login_user(member)
            flash("Welcome, %s!" % (form.uname.data), "success")
            return redirect(url_for("homepage"))
        else:
            flash("Username or Password doesn't match, please try again.", "danger")
            return redirect(url_for("loginpage"))
    return render_template("login.html", form=form)


@app.route("/logout")
def logoutpage():
    logout_user()
    flash("Successfuly logged out.", "success")
    return redirect(url_for("homepage"))


@app.route("/member-page")
@login_required
def member():
    user_details = UserDetails.query.filter_by(user_id=current_user.id).first()  # type: ignore
    if user_details is None:
        height = 0
        weight = 0
        bmi = 0
        goal = 2000
    else:
        height = user_details.height
        weight = user_details.weight
        bmi = user_details.bmi
        goal = user_details.goal

    water_of_user = WaterIntake.query.filter_by(user_id=current_user.id).all()  # type: ignore
    if water_of_user is None:
        water = None
    else:
        water = 0
        for waters in water_of_user:
            water += waters.water_ml
    foods_of_user = db.session.execute(
        text(
            "SELECT * FROM food_intake INNER JOIN food ON food_intake.food_no = food.food_no WHERE user_id = :user_id ORDER BY date DESC"
        ),
        {"user_id": current_user.id},  # type: ignore
    ).fetchall()
    if foods_of_user is None:
        total_cal = None
    else:
        total_cal = 0
        for food in foods_of_user:
            total_cal += food.food_cal
    workouts = db.session.execute(
        text(
            "select * from user_workouts natural join exercise natural join trainer where user_id = :user_id ORDER BY date DESC"
        ),
        {"user_id": current_user.id},  # type: ignore
    ).fetchall()

    if workouts is None:
        work = None
    else:
        work = 0
        for workout in workouts:
            work += workout.exercise_cal

    return render_template(
        "tracker.html", height=height, weight=weight, water=water, total_cal=total_cal, bmi=bmi, work=work, goal=goal
    )


@app.route("/bmi", methods=["GET", "POST"])
@login_required
def bmi():
    form = BmiForm(request.form)
    data = UserDetails.query.filter_by(user_id=current_user.id).first()  # type: ignore

    if request.method == "POST" and form.validate():
        height = form.height.data
        weight = form.weight.data
        goal = form.goal.data
        if data is None:
            element = UserDetails(user_id=current_user.id, height=height, weight=weight, goal=goal)  # type: ignore
            db.session.add(element)
            db.session.commit()
        else:
            data.height = height
            data.weight = weight
            data.goal = goal
            db.session.commit()
        flash("Your BMI has been updated.", "success")
        return redirect(url_for("bmi"))

    data = UserDetails.query.filter_by(user_id=current_user.id).first()  # type: ignore

    if data is None:
        bmi = None
    else:
        bmi = data.bmi
        form.height.data = data.height
        form.weight.data = data.weight
        form.goal.data = data.goal

    return render_template("bmi.html", bmi=bmi, form=form)  # type: ignore


@app.route("/water", methods=["GET", "POST"])
@login_required
def water():
    form = WaterForm(request.form)
    # getting all water intake and sort by date
    waters = (
        WaterIntake.query.filter_by(user_id=current_user.id).order_by(WaterIntake.date.desc()).all()  # type: ignore
    )  # type: ignore
    # finding the sum of water intake
    total = 0
    for water in waters:
        total += water.water_ml
    if request.method == "POST" and form.validate():
        amount = form.water.data
        element = WaterIntake(user_id=current_user.id, water_ml=amount)  # type: ignore
        db.session.add(element)
        db.session.commit()
        flash("Your water intake has been updated.", "success")
        return redirect(url_for("water"))
    return render_template("water.html", waters=waters, form=form, total=total)  # type: ignore


@app.route("/water/delete/<int:id>", methods=["GET", "POST"])
@login_required
def water_delete(id):
    water = WaterIntake.query.filter_by(water_id=id).first()
    db.session.delete(water)
    db.session.commit()
    flash("Your water intake has been deleted.", "success")
    return redirect(url_for("water"))


@app.route("/water/delete", methods=["GET", "POST"])
@login_required
def water_delete_all():
    waters = WaterIntake.query.filter_by(user_id=current_user.id).all()  # type: ignore
    for water in waters:
        db.session.delete(water)
    db.session.commit()
    flash("Your water intake has been deleted.", "success")
    return redirect(url_for("water"))


@app.route("/water/<int:ml>", methods=["GET", "POST"])
@login_required
def water_add(ml):
    element = WaterIntake(user_id=current_user.id, water_ml=ml)  # type: ignore
    db.session.add(element)
    db.session.commit()
    return redirect(url_for("water"))


@app.route("/food", methods=["GET", "POST"])
@login_required
def food():
    food_list = Food.query.all()
    foods = db.session.execute(
        text(
            "SELECT * FROM food_intake INNER JOIN food ON food_intake.food_no = food.food_no WHERE user_id = :user_id ORDER BY date DESC"
        ),
        {"user_id": current_user.id},  # type: ignore
    ).fetchall()

    # type: ignore
    form = FoodForm(request.form)
    form.food.choices = [(food.food_no, food.food_name + " - " + str(food.food_cal) + " Kcal") for food in food_list]

    if request.method == "POST" and form.validate():
        food_no = form.food.data
        element = FoodIntake(user_id=current_user.id, food_no=food_no)  # type: ignore
        db.session.add(element)
        db.session.commit()
        flash("Your food intake has been updated.", "success")
        return redirect(url_for("food"))

    total = 0
    for food in foods:
        total += food.food_cal

    return render_template("food.html", form=form, foods=foods, total=total)  # type: ignore


@app.route("/food/delete/<int:id>", methods=["GET", "POST"])
@login_required
def food_delete(id):
    food = FoodIntake.query.filter_by(food_intake_id=id).first()
    db.session.delete(food)
    db.session.commit()
    flash("Your food intake has been deleted.", "success")
    return redirect(url_for("food"))


@app.route("/food/delete", methods=["GET", "POST"])
@login_required
def food_delete_all():
    foods = FoodIntake.query.filter_by(user_id=current_user.id).all()  # type: ignore
    for food in foods:
        db.session.delete(food)
    db.session.commit()
    flash("Your food intake has been deleted.", "success")
    return redirect(url_for("food"))


@app.route("/workout", methods=["GET", "POST"])
@login_required
def workout():
    form = WorkoutForm(request.form)
    trainer_all = Trainer.query.all()
    exercise_all = db.session.execute(
        text("select * from exercise natural join exercise_catogory"),
    ).fetchall()

    form.trainers.choices = [(trainer.trainer_id, trainer.trainer_name) for trainer in trainer_all]
    form.exercises.choices = [
        (
            exercise.exercise_id,
            exercise.exercise_name + " " + str(exercise.exercise_cal) + " " + str(exercise.exercise_catogory_name),
        )
        for exercise in exercise_all
    ]

    workouts = db.session.execute(
        text(
            "select * from user_workouts natural join exercise natural join trainer where user_id = :user_id ORDER BY date DESC"
        ),
        {"user_id": current_user.id},  # type: ignore
    ).fetchall()

    if request.method == "POST" and form.validate():
        trainer_id = form.trainers.data
        exercise_id = form.exercises.data
        element = UserWorkouts(user_id=current_user.id, trainer_id=trainer_id, exercise_id=exercise_id)  # type: ignore
        db.session.add(element)
        db.session.commit()
        return redirect(url_for("workout"))

    cal = 0
    for workout in workouts:
        cal += workout.exercise_cal

    return render_template("workout.html", form=form, workouts=workouts, cal=cal)  # type: ignore


@app.route("/workout/delete/<int:id>", methods=["GET", "POST"])
@login_required
def workout_delete(id):
    workout = UserWorkouts.query.filter_by(workout_id=id).first()
    db.session.delete(workout)
    db.session.commit()

    return redirect(url_for("workout"))


@app.route("/workout/delete", methods=["GET", "POST"])
@login_required
def workout_delete_all():
    workouts = UserWorkouts.query.filter_by(user_id=current_user.id).all()  # type: ignore
    for workout in workouts:
        db.session.delete(workout)
    db.session.commit()
    return redirect(url_for("workout"))
