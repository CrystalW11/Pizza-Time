from flask_app.config.mysqlconnection import connectToMySQL
from pprint import pprint
from flask_app.models.user import User
from flask import flash


class Pizza:
    """This Pizza class."""

    _db = "pizza-time"

    def __init__(self, data):
        self.id = data["id"]
        self.method = data["method"]
        self.size = data["size"]
        self.crust = data["crust"]
        self.toppings = data.get("toppings", [])
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.order_id = data["order_id"]
        self.user_id = data["user_id"]
        self.user = None

    @staticmethod
    def form_is_valid(form_data):
        """This method validates the Pizza registration form"""
        is_valid = True

        toppings = form_data.getlist("toppings[]")
        if len(toppings) < 2:
            flash("Please select at least two toppings.")
            is_valid = False

        return is_valid

    @classmethod
    def find_all(cls):
        """This method finds all the pizzas in the database."""

        query = "SELECT * FROM pizzas:"
        list_of_dicts = connectToMySQL(Pizza._db).query_db(query)
        pprint(list_of_dicts)
        pizzas = []

        for each_dict in list_of_dicts:
            pizza = Pizza(each_dict)
            pizzas.append(pizza)

        return pizzas

    @classmethod
    def find_all_with_users(cls):
        """This method finds all the pizzas with users in the database."""

        query = """
        SELECT * FROM pizzas
        JOIN users
        ON pizzas.user_id = users.id;
        """
        list_of_dicts = connectToMySQL(Pizza._db).query_db(query)

        pizzas = []
        for each_dict in list_of_dicts:
            pizza = Pizza(each_dict)
            user_data = {
                "id": each_dict["users.id"],
                "first_name": each_dict["first_name"],
                "last_name": each_dict["last_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "address": each_dict["address"],
                "city": each_dict["city"],
                "state": each_dict["state"],
                "created_at": each_dict["users.created_at"],
                "updated_at": each_dict["users.updated_at"],
            }
            result = User(user_data)
            pizza.user = result
            pizzas.append(pizza)
        return pizzas

    @classmethod
    def find_by_id(cls, pizza_id):
        query = """SELECT * FROM pizzas WHERE id = %(pizza_id)s;"""
        data = {"pizza_id": pizza_id}
        list_of_dicts = connectToMySQL(Pizza._db).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None

        pizza = Pizza(list_of_dicts[0])
        return pizza

    @classmethod
    def find_by_id_with_user(cls, pizza_id):
        query = """SELECT * FROM pizzas JOIN users ON pizzas.user_id = users.id WHERE pizzas.id = %(pizza_id)s;"""

        data = {"pizza_id": pizza_id}
        list_of_dicts = connectToMySQL(Pizza._db).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None

        pizza = Pizza(list_of_dicts[0])
        user_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "address": list_of_dicts[0]["address"],
            "city": list_of_dicts[0]["city"],
            "state": list_of_dicts[0]["state"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }
        pizza.user = User(user_data)
        return pizza

    @classmethod
    def create(cls, form_data):
        """This method creates a pizza from a form."""

        query = """
        INSERT INTO pizzas
        (method, size, crust, toppings, created_at, updated_at, user_id)
        VALUES
        (%(method)s, %(size)s, %(crust)s, %(toppings)s, NOW(), NOW(), %(user_id)s);
        """
        pizza_id = connectToMySQL(Pizza._db).query_db(query, form_data)

        return pizza_id

    @classmethod
    def update(cls, form_data):
        """This method updates a pizza in the database."""

        query = """
        UPDATE pizzas
        SET method = %(method)s,
        size = %(size)s,
        crust = %(crust)s,
        toppings = %(toppings)s
        WHERE id = %(pizza_id)s;
        """

        connectToMySQL(Pizza._db).query_db(query, form_data)
        return

    @classmethod
    def delete(cls, pizza_id):
        """This method deletes a pizza in the database"""

        query = """
        DELETE FROM pizzas
        WHERE id = %(pizza_id)s;
        """
        data = {"pizza_id": pizza_id}
        return connectToMySQL(Pizza._db).query_db(query, data)
