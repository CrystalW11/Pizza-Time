from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.pizza import Pizza
from datetime import datetime
from decimal import Decimal


class Order:
    """This Order class represents an order in the database."""

    _db = "pizza-time"

    def __init__(self, data):
        self.id = data["id"]
        self.type = data["type"]
        self.pizzas = data["pizzas"]
        self.price = data["price"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

        self.pizza_list = self.parse_pizzas(data["pizzas"])

    def parse_pizzas(self, pizzas_str):
        """Convert the string of pizza IDs into a list of Pizza objects."""
        pizza_ids = pizzas_str.split(",")
        pizzas = [Pizza.find_by_id(int(pizza_id.strip())) for pizza_id in pizza_ids]
        return pizzas

    @classmethod
    def create(cls, form_data):
        """This method creates an order from form data."""

        # Calculate the total price based on pizza sizes
        pizzas = form_data["pizzas"].split(",")
        total_price = 0.0
        for pizza_id in pizzas:
            pizza = Pizza.find_by_id(int(pizza_id.strip()))
            if pizza.size == "small":
                total_price += 10.00
            elif pizza.size == "medium":
                total_price += 14.00
            elif pizza.size == "large":
                total_price += 18.00

        query = """
        INSERT INTO orders
        (type, pizzas, price, created_at, updated_at, user_id)
        VALUES
        (%(type)s, %(pizzas)s, %(price)s, NOW(), NOW(), %(user_id)s);
        """

        data = {
            "type": form_data["type"],
            "pizzas": form_data["pizzas"],
            "price": total_price,
            "user_id": form_data["user_id"],
        }

        order_id = connectToMySQL(Order._db).query_db(query, data)
        return order_id

    @classmethod
    def find_all(cls):
        """This method retrieves all orders from the database."""
        query = "SELECT * FROM orders;"
        results = connectToMySQL(cls._db).query_db(query)
        orders = []
        for result in results:
            orders.append(cls(result))
        return orders

    @classmethod
    def find_by_id(cls, order_id):
        """This method retrieves a single order by its ID."""
        query = "SELECT * FROM orders WHERE id = %(order_id)s;"
        data = {"order_id": order_id}
        result = connectToMySQL(cls._db).query_db(query, data)
        if result:
            return cls(result[0])
        return None

    @classmethod
    def find_all_by_user_id(cls, user_id):
        """This method retrieves all orders for a specific user."""
        query = """
        SELECT * FROM orders
        WHERE user_id = %(user_id)s
        ORDER BY created_at DESC;
        """
        data = {"user_id": user_id}
        results = connectToMySQL(cls._db).query_db(query, data)
        orders = []
        for row in results:
            order = cls(row)

            # Calculate total price including delivery fee if applicable
            delivery_fee = (
                Decimal("4.99") if order.type == "delivery" else Decimal("0.00")
            )
            order.price += delivery_fee

            orders.append(order)
        return orders

    @classmethod
    def update(cls, form_data):
        """This method updates an order in the database."""

        # Recalculate the price
        total_price = 0.0
        for pizza_id in form_data["pizzas"]:
            pizza = Pizza.find_by_id(int(pizza_id.strip()))
            if pizza.size == "small":
                total_price += 10.00
            elif pizza.size == "medium":
                total_price += 14.00
            elif pizza.size == "large":
                total_price += 18.00

        # Join the list of pizzas into a comma-separated string if storing in a single field
        pizzas_str = ",".join(form_data["pizzas"])

        query = """
        UPDATE orders
        SET type = %(type)s,
            pizzas = %(pizzas)s,
            price = %(price)s,
            updated_at = NOW()
        WHERE id = %(order_id)s;
        """

        data = {
            "type": form_data["type"],
            "pizzas": pizzas_str,
            "price": total_price,
            "order_id": form_data["order_id"],
        }

        connectToMySQL(cls._db).query_db(query, data)
        return

    @classmethod
    def delete(cls, order_id):
        """This method deletes an order from the database."""
        query = "DELETE FROM orders WHERE id = %(order_id)s;"
        data = {"order_id": order_id}
        return connectToMySQL(cls._db).query_db(query, data)
