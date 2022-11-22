from flask import Flask, make_response, request
from flask_restful import Api, Resource
from sqlalchemy import *
from marshmallow import ValidationError
import bcrypt
from models import *
from shemas import *

from flask_httpauth import HTTPBasicAuth
from flask_jwt import current_identity
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)
api = Api(app)

auth = HTTPBasicAuth()
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "HS256"
class Error():
    @staticmethod
    def invalid_id():
        invalid_id = make_response({"Error": "Invalid id"})
        invalid_id.status_code = 400
        return invalid_id

    @staticmethod
    def not_found():
        not_found = make_response({"Error": "Not found"})
        not_found.status_code = 404
        return not_found

    @staticmethod
    def invalid_input():
        invalid_input = make_response({"Error": "Invalid input"})
        invalid_input.status_code = 405
        return invalid_input


class methods():
    def maxId(obj):
        res = connection.execute(select([func.count()]).select_from(obj))
        for row in res:
            for id in row:
                return id


class TrainersAPI(Resource):
    @staticmethod
    def requestTrainers():
        cTrainer = {
            "idtrainer": request.form["idtrainer"],
            "name": request.form["name"],
            "size": request.form["size"],
            "price": request.form["price"],
            "img_urls": request.form.getlist("img_urls")
        }

        try:
            schema = TrainersSchema()
            result = schema.load(cTrainer)
        except ValidationError:
            return None

        urls = ""
        for i in cTrainer["img_urls"]:
            urls += i + " "

        cTrainer["img_urls"] = urls
        return cTrainer


    def post(self):
        cTrainer = TrainersAPI.requestTrainers()

        if cTrainer == None:
            return Error.invalid_input()

        cTrainer["idtrainer"] = methods.maxId(trainer) + 1

        insert_trainer = insert(trainer).values(idtrainer = cTrainer["idtrainer"],
                                                name = cTrainer["name"],
                                                size = cTrainer["size"],
                                                price = cTrainer["price"],
                                                img_urls = cTrainer["img_urls"]
        )

        connection.execute(insert_trainer)
        return cTrainer


class TrainersWithParamAPI(Resource):
    def getTrainers(id):
        cTrainer = connection.execute(select(trainer).where(trainer.c.idtrainer == id))

        if cTrainer == None:
            return None

        for id, name, size, price, img_urls in cTrainer:
            return {"idtrainer": id, "name": name, "size": size, "price": price, "img_urls": img_urls.split()}


    def get(self, id):
        if id < 1 or id > methods.maxId(trainer):
            return Error.invalid_id()
        else:
            return TrainersWithParamAPI.getTrainers(id)


    def put(self, id):
        if id < 1 or id > methods.maxId(trainer):
            return Error.invalid_id()

        cTrainer = TrainersAPI.requestTrainers()

        if cTrainer == None:
            return Error.invalid_input()

        update_trainer = update(trainer).where(trainer.c.idtrainer == id).values(idtrainer = cTrainer["idtrainer"],
                                                                                  name = cTrainer["name"],
                                                                                  size = cTrainer["size"],
                                                                                  price = cTrainer["price"],
                                                                                  img_urls = cTrainer["img_urls"]
        )

        connection.execute(update_trainer)
        return cTrainer


    def delete(self, id):
        if id < 1 or id > methods.maxId(trainer):
            return Error.invalid_id()

        connection.execute(delete(trainer).where(trainer.c.idtrainer == id))
        return "Succesful operation", 200


class OrderAPI(Resource):
    @staticmethod
    def requestOrder():
        cOrder = {
            "idorder": request.form["idorder"],
            "delivery_adress": request.form["delivery_adress"],
            "status": request.form["status"],
            "user_id": request.form["user_id"]
        }

        print("cOrder =", cOrder)

        try:
            schema = OrderSchema()
            result = schema.load(cOrder)
        except ValidationError as err:
            print("data =", err.data)
            return None

        return cOrder


    def post(self):
        cOrder = OrderAPI.requestOrder()

        if cOrder == None:
            return Error.invalid_input()

        cOrder["idorder"] = methods.maxId(order) + 1

        insert_order = insert(order).values(idorder = cOrder["idorder"],
                                            delivery_adress = cOrder["delivery_adress"],
                                            status = cOrder["status"],
                                            user_id = cOrder["user_id"]
        )

        connection.execute(insert_order)
        return cOrder


class OrderWithParamAPI(Resource):
    def getOrder(id):
        cOrder = connection.execute(select(order).where(order.c.idorder == id))

        if cOrder == None:
            return None

        for id, adress, status, user in cOrder:
            return {"idorder": id, "delivery_adress": adress, "status": status, "user_id": user}


    def get(self, id):
        if id < 1 or id > methods.maxId(order):
            return Error.invalid_id()
        else:
            return OrderWithParamAPI.getOrder(id)


    def delete(self, id):
        if id < 1 or id > methods.maxId(order):
            return Error.invalid_id()

        connection.execute(delete(order).where(order.c.idorder == id))
        return "Succesful operation", 200


class InventoryAPI(Resource):
    def get(self):
        orders = []
        for i in range(1, methods.maxId(order) + 1):
            orders.append(OrderWithParamAPI.getOrder(i))
        return orders


class UserAPI(Resource):
    @staticmethod
    def requestUser():
        cUser = {
            "iduser": request.form["iduser"],
            "username": request.form["username"],
            "full_name": request.form["full_name"],
            "phone_number": request.form["phone_number"],
            "email": request.form["email"],
            "password": request.form["password"]
        }

        try:
            schema = UserSchema()
            result = schema.load(cUser)
        except ValidationError:
            return None

        hashed = bcrypt.hashpw(cUser["password"].encode("utf-8"), bcrypt.gensalt())

        cUser["password"] = hashed
        return cUser


    def post(self):
        cUser = UserAPI.requestUser()

        if cUser == None:
            return Error.invalid_input()

        cUser["iduser"] = methods.maxId(user) + 1

        insert_user = insert(user).values(iduser = cUser["iduser"],
                                          username = cUser["username"],
                                          full_name = cUser["full_name"],
                                          phone_number = cUser["phone_number"],
                                          email = cUser["email"],
                                          password = cUser["password"]
        )

        connection.execute(insert_user)
        return UserWithParamAPI.getUser(cUser["username"])


class UserWithParamAPI(Resource):
    def getUser(username):
        cUser = connection.execute(select(user).where(user.c.username == username))

        if cUser == None:
            return None

        for id, name, fN, phone, email, password in cUser:
            return {"iduser": id, "username": name, "full_name": fN, "phone_number": phone, "email": email, "password": password}

    def get(self, username):
        cUser = UserWithParamAPI.getUser(username)
        if cUser == None:
            return Error.invalid_id()
        else:
            return cUser


    def put(self, username):
        if UserWithParamAPI.getUser(username) == None:
            return Error.invalid_id()

        cUser = UserAPI.requestUser()

        if cUser == None:
            return Error.invalid_input()

        update_user = update(user).where(user.c.username == username).values(iduser = cUser["iduser"],
                                                                             username = cUser["username"],
                                                                             full_name = cUser["full_name"],
                                                                             phone_number = cUser["phone_number"],
                                                                             email = cUser["email"],
                                                                             password = cUser["password"]
        )

        connection.execute(update_user)
        return UserWithParamAPI.getUser(cUser["username"])

    @jwt_required()
    def delete(self, username):
        if UserWithParamAPI.getUser(username) == None:
            return Error.invalid_id()

        connection.execute(delete(user).where(user.c.username == username))
        return "Succesful operation", 200


class LoginAPI(Resource):
    @staticmethod
    def requestLogin():
        loginData = {
            "username": request.form["username"],
            "password": request.form["password"]
        }

        return loginData
    def post(self):
        log = LoginAPI.requestLogin()
        user = UserWithParamAPI.getUser(log.get("username"))

        if not user:
            return "User doesn`t exist"

        if log.get("password") == user.get("password") :
            access_token = create_access_token(identity=user.get("username"))
            return access_token
        else:
            return "False password"

        return "Not avaible"

"""
    def put(self):
        loginData = LoginAPI.requestLogin()

        correctData = UserWithParamAPI.getUser(loginData["login"])
        if correctData == None:
            return Error.invalid_input()

        if not bcrypt.checkpw(loginData["password"].encode("utf-8") , correctData["password"].encode("utf-8")):
            return Error.invalid_input()

        return correctData
"""

class LogoutAPI(Resource):
    def get(self):
        return "Succesful operation"


api.add_resource(TrainersAPI, "/trainers")
api.add_resource(TrainersWithParamAPI, "/trainers/<int:id>")
api.add_resource(InventoryAPI, "/store/inventory")
api.add_resource(OrderAPI, "/store/order")
api.add_resource(OrderWithParamAPI, "/store/order/<int:id>")
api.add_resource(UserAPI, "/user")
api.add_resource(UserWithParamAPI, "/user/<string:username>")
api.add_resource(LoginAPI, "/login")
api.add_resource(LogoutAPI, "/logout")


if __name__ == "__main__":
    app.run(debug = True, port = 5000, host = "127.0.0.1")
