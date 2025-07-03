from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

from ..models.user import User
from ..models.category import Category
from ..schemas import UserRegisterSchema, UserLoginSchema
from .. import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = UserRegisterSchema(**(request.get_json() or {}))
    except ValidationError as ve:
        return jsonify({"errors": ve.errors()}), 400

    if User.query.filter_by(username=data.username).first():
        return jsonify({"message": "Username already exists"}), 400

    user = User(username=data.username, starting_budget=data.starting_budget)
    user.set_password(data.password)

    # attach default categories
    for name in ["Food","Car","Accommodation","Gifts","Health","Utilities"]:
        user.categories.append(Category(name=name))

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username conflict"}), 400

    return jsonify({"id": user.id, "username": user.username}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = UserLoginSchema(**(request.get_json() or {}))
    except ValidationError as ve:
        return jsonify({"errors": ve.errors()}), 400

    user = User.query.filter_by(username=data.username).first()
    if not user or not user.check_password(data.password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token}), 200
