from flask import request, jsonify
from flask_jwt_extended import create_access_token
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from ..services.user_service import UserService
from ..schemas import UserRegisterSchema, UserLoginSchema

class UserController:

    @staticmethod
    def register():
        try:
            data = UserRegisterSchema(**(request.get_json() or {}))
        except ValidationError as ve:
            return jsonify({"errors": ve.errors()}), 400

        try:
            user = UserService.register(data)
        except IntegrityError:
            return jsonify({"message": "Username already exists"}), 400
        except ValueError as ve:
            return jsonify({"message": str(ve)}), 400

        return jsonify({"id": user.id, "username": user.username}), 201

    @staticmethod
    def login():
        try:
            data = UserLoginSchema(**(request.get_json() or {}))
        except ValidationError as ve:
            return jsonify({"errors": ve.errors()}), 400

        try:
            user = UserService.authenticate(data.username, data.password)
        except ValueError:
            return jsonify({"message": "Invalid credentials"}), 401

        token = create_access_token(identity=user.id)
        return jsonify({"access_token": token}), 200
