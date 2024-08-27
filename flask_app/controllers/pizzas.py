from flask_app import app, bcrypt
from flask_app.models.pizza import Pizza
from flask_app.models.user import User
from flask import flash, render_template, redirect, request, session


@app.get("/pizzas/all")
def all_pizzas():
    """This route renders all pizzas"""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    pizzas = Pizza.find_all_with_users()
    user = User.find_by_user_id(session["user_id"])
    return render_template("all_pizzas.html", pizzas=pizzas, user=user)


@app.get("/pizzas/new")
def new_pizza():
    """This route displays the new pizza form."""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    user = User.find_by_user_id(session["user_id"])
    return render_template("new_pizza.html", user=user)


@app.post("/pizzas/create")
def create_pizzas():
    """This route processes the new Pizza form."""

    if not Pizza.form_is_valid(request.form):
        return redirect("/pizzas/new")

    # down here the form is valid!!
    Pizza.create(request.form)
    return redirect("/pizzas/all")


@app.get("/pizzas/dashboard")
def pizzas_dashboard():
    """This route displays the user dashboard."""
    if "user_id" not in session:
        flash("You must be logged in to view the page.", "login")
        return redirect("/")

    user = User.find_by_user_id(session["user_id"])

    return render_template("dashboard.html", user=user)


@app.get("/pizzas/<int:pizza_id>")
def pizzas_id(pizza_id):
    """This route displays one users pizzas details"""

    if "user_id" not in session:
        flash("You must be logged in to view the page.", "login")
        return redirect("/")

    pizza = Pizza.find_by_user_id(pizza_id)
    user = User.find_by_user_id(session["user_id"])

    return render_template("pizza_program.html", user=user, pizza=pizza)


@app.get("/pizzas/<int:pizza_id>/edit")
def edit_pizza(pizza_id):
    """This route displays the edit pizza form."""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    pizza = Pizza.find_by_user_id(pizza_id)
    user = User.find_by_user_id(session["user_id"])
    return render_template("edit_pizza.html", pizza=pizza, user=user)


@app.post("/pizzas/update")
def update_pizza():
    """This route displays the edit pizza form."""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    pizza_id = request.form["pizza_id"]

    if not Pizza.form_is_valid(request.form):
        return redirect(f"/pizzas/{pizza_id}/edit")

    # down here the form is valid
    Pizza.update(request.form)
    return redirect(f"/pizzas/{pizza_id}")


@app.get("/pizzas/<int:pizza_id>/delete")
def delete_pizza(pizza_id):
    """This route processes the delete form."""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    Pizza.delete(pizza_id)
    return redirect("/pizzas/all")
