from flask_app import app, bcrypt
from flask_app.models.user import User
from flask import flash, redirect, render_template, request, session


@app.get("/")
def index():
    """This route displays the login and registration forms"""

    return render_template("index.html")


@app.post("/users/register")
def register():
    """This route processes the register form."""

    # if form not valid redirect
    if not User.register_form_is_valid(request.form):
        return redirect("/")

    # check if user already exists
    potential_user = User.find_by_email(request.form["email"])

    # if user doesn't exist, redirect
    if potential_user != None:
        flash("Email in user. Please log in.", "register")
        return redirect("/")

    # user does not exist, safe to create and hash password
    hashed_pw = bcrypt.generate_password_hash(request.form["password"])
    user_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashed_pw,
        "address": request.form["address"],
        "city": request.form["city"],
        "state": request.form["state"],
    }
    user_id = User.register(user_data)

    # save user id in session
    session["user_id"] = user_id
    return redirect("/pizzas/all")


@app.post("/users/login")
def login():
    """This route processes the login form."""

    # if form not valid redirect
    if not User.login_form_is_valid(request.form):
        return redirect("/")

    # does user exist?
    potential_user = User.find_by_email(request.form["email"])

    # user does not exist, redirect
    if potential_user == None:
        flash("Invalid credentials.", "login")
        return redirect("/")

    # user exits!
    user = potential_user

    # check the password
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid credentials.", "login")
        return redirect("/")

    # save user id in session (log them in)
    session["user_id"] = user.id
    return redirect("/pizzas/all")


@app.get("/users/logout")
def logout():
    """This route clears session."""
    session.clear()
    return redirect("/")


@app.get("/users/pizzas")
def pizzas():
    """This route displays the user pizzas."""
    if "user_id" not in session:
        flash("You must be logged in to view the page.", "login")
        return redirect("/")

    user = User.find_by_user_id(session["user_id"])

    return render_template("all_pizzas.html", user=user)
