from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from ..services.category_service import CategoryService
from ..schemas import CategoryCreateSchema, CategorySchema

class CategoryController:

    @staticmethod
    @jwt_required()
    def list():
        user_id = get_jwt_identity()
        cats = CategoryService.list(user_id)
        return jsonify([CategorySchema.from_orm(c).dict() for c in cats]), 200

    @staticmethod
    @jwt_required()
    def create():
        user_id = get_jwt_identity()
        try:
            data = CategoryCreateSchema(**(request.get_json() or {}))
        except ValidationError as ve:
            return jsonify({"errors": ve.errors()}), 400

        try:
            cat = CategoryService.create(user_id, data)
        except ValueError as ve:
            return jsonify({"message": str(ve)}), 400
        except IntegrityError:
            return jsonify({"message": "Category conflict"}), 400

        return jsonify(CategorySchema.from_orm(cat).dict()), 201

    @staticmethod
    @jwt_required()
    def delete(cat_id):
        user_id = get_jwt_identity()
        try:
            CategoryService.delete(user_id, int(cat_id))
        except LookupError as le:
            return jsonify({"message": str(le)}), 404
        return "", 204
