from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.order import Order
from flask_app.models.pizza import Pizza
from flask_app.models.user import User
from decimal import Decimal


@app.get("/orders/all")
def all_orders():
    """This route displays all orders for the logged-in user."""

    if "user_id" not in session:
        flash("Please log in to view your orders.", "login")
        return redirect("/")

    user = User.find_by_user_id(session["user_id"])
    orders = Order.find_all_by_user_id(user.id)
    return render_template("all_orders.html", orders=orders, user=user)


@app.get("/orders/new")
def new_order():
    """This route displays the form to create a new order."""

    if "user_id" not in session:
        flash("Please log in to create an order.", "login")
        return redirect("/")

    # Retrieve all pizzas to allow the user to select them for the order
    pizzas = Pizza.find_all()
    user = User.find_by_user_id(session["user_id"])
    return render_template("new_order.html", pizzas=pizzas, user=user)


@app.post("/orders/create")
def create_order():
    """This route processes the form to create a new order."""

    if "user_id" not in session:
        flash("Please log in to create an order.", "login")
        return redirect("/")

    # Ensure at least one pizza is selected
    pizzas = request.form.getlist("pizzas[]")
    if not pizzas:
        flash("Please select at least one pizza to place an order.")
        return redirect("/orders/new")

    # Process the order
    order_data = {
        "type": request.form["type"],
        "pizzas": ",".join(
            pizzas
        ),  # Convert list of pizzas to a comma-separated string
        "user_id": session["user_id"],
    }

    order_id = Order.create(order_data)
    return redirect(f"/orders/{order_id}")


@app.get("/orders/<int:order_id>")
def view_order(order_id):
    """This route displays a specific order's details."""

    if "user_id" not in session:
        flash("Please log in to view this order.", "login")
        return redirect("/")

    order = Order.find_by_id(order_id)
    if not order:
        flash("Order not found.", "error")
        return redirect("/orders/new")

    # Calculate the total price, including the delivery fee if applicable
    delivery_fee = Decimal("4.99") if order.type == "delivery" else Decimal("0.00")
    total_price = order.price + delivery_fee

    user = User.find_by_user_id(session["user_id"])
    return render_template(
        "order_details.html", order=order, user=user, total_price=total_price
    )


@app.get("/orders/<int:order_id>/edit")
def edit_order(order_id):
    """This route displays the form to edit an existing order."""

    if "user_id" not in session:
        flash("Please log in to edit an order.", "login")
        return redirect("/")

    order = Order.find_by_id(order_id)
    if not order:
        flash("Order not found.", "error")
        return redirect("/orders/new")

    # Retrieve all pizzas to allow the user to select them for the order
    pizzas = Pizza.find_all()
    user = User.find_by_user_id(session["user_id"])

    # Calculate the total price, including the delivery fee if applicable
    delivery_fee = Decimal("4.99") if order.type == "delivery" else Decimal("0.00")
    total_price = order.price + delivery_fee

    return render_template(
        "edit_order.html",
        order=order,
        pizzas=pizzas,
        user=user,
        total_price=total_price,
    )


@app.post("/orders/update")
def update_order():
    """This route processes the form to update an existing order."""

    if "user_id" not in session:
        flash("Please log in to update your order.", "login")
        return redirect("/")

    order_data = {
        "order_id": request.form["order_id"],
        "type": request.form["type"],
        "pizzas": request.form.getlist("pizzas[]"),
        "user_id": session["user_id"],
    }

    Order.update(order_data)
    return redirect(f"/orders/{order_data['order_id']}")


@app.get("/orders/<int:order_id>/delete")
def delete_order(order_id):
    """This route deletes an order and redirects to the new order page."""

    if "user_id" not in session:
        flash("Please log in to delete an order.", "login")
        return redirect("/")

    Order.delete(order_id)
    return redirect("/orders/new")
