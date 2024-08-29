from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL

# from flask_app.models import pizza
import re
from pprint import pprint
from flask_app.models.user import User
from flask import flash


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class Pizza:
    """This Pizza class."""

    _db = "pizza-time"

    def __init__(self, data):
        self.id = data["id"]
        self.cheese = data["cheese"]
        self.pepperoni = data["pepperoni"]
        self.supreme = data["supreme"]
        self.comment = data["comment"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.user = None

    @staticmethod
    def form_is_valid(form_data):
        """This method validates the Pizza registration form"""
        is_valid = True

        if len(form_data["cheese"].strip()) == 0:
            flash("Please enter Pizza.")
            is_valid = False
        elif len(form_data["cheese"].strip()) < 3:
            flash("Pizza must be at least three characters.")
            is_valid = False
        if len(form_data["pepperoni"].strip()) == 0:
            flash("Please enter Network.")
            is_valid = False
        elif len(form_data["pepperoni"].strip()) < 3:
            flash("Network must be at least three characters.")
            is_valid = False
        if len(form_data["supreme"].strip()) == 0:
            flash("Please enter Pizza.")
            is_valid = False
        elif len(form_data["supreme"].strip()) < 3:
            flash("Pizza must be at least three characters.")
            is_valid = False
        if len(form_data["comments"].strip()) == 0:
            flash("Please enter Comments.")
            is_valid = False
        elif len(form_data["comments"].strip()) < 3:
            flash("Comments must be at least three characters.")
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
                "created_at": each_dict["users.created_at"],
                "updated_at": each_dict["users.updated_at"],
            }
            result = User(user_data)
            pizza.user = result
            pizzas.append(pizza)

        return pizzas

    @classmethod
    def create(cls, form_data):
        """This method creates a pizza from a form."""

        query = """
        INSERT INTO pizzas
        (title, network, release_date, comment, user_id)
        VALUES
        (%(cheese)s, %(pepperoni)s, %(supreme)s, %(comment)s, %(user_id)s);
        """
        pizzas_id = connectToMySQL(Pizza._db).query_db(query, form_data)

        return pizzas_id

    @classmethod
    def find_by_email(cls, email):
        """This method finds a pizza by email."""

        query = """SELECT * FROM pizzas WHERE email = %(email)s;"""
        data = {"email": email}
        list_of_dicts = connectToMySQL(Pizza._db).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        pizza = Pizza(list_of_dicts[0])
        return pizza

    @classmethod
    def find_by_pizza_id(cls, pizza_id):
        """This method finds a pizza by pizza_id."""

        query = """SELECT * FROM pizzas WHERE id = %(pizza_id)s;"""
        data = {"pizza_id": pizza_id}
        list_of_dicts = connectToMySQL(Pizza._db).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        pizza = Pizza(list_of_dicts[0])
        return pizza

    @classmethod
    def find_by_user_id(cls, pizza_id):
        """This method finds a pizza and the user by the pizza id."""
        query = """
        SELECT * FROM pizzas
        JOIN users
        ON pizzas.user_id = users.id
        WHERE pizzas.id = %(pizza_id)s;
        """
        data = {"pizza_id": pizza_id}
        list_of_dicts = connectToMySQL(Pizza._db).query_db(query, data)
        pprint(list_of_dicts)
        pizza = Pizza(list_of_dicts[0])
        one_dict = list_of_dicts[0]
        user_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }

        user = User(user_data)
        pizza.user = user
        return pizza

    @classmethod
    def update(cls, form_data):
        """This method updates a pizza in the database."""
        print("\n\n\n\n\line247: ", form_data)
        query = """
        UPDATE pizzas
        SET cheese = %(cheese)s,
        pepperoni = %(pepperoni)s,
        supreme = %(supreme)s,
        comment = %(comment)s,
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
