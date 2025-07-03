from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from ..models.category import Category
from ..schemas import CategoryCreateSchema, CategorySchema
from .. import db

category_bp = Blueprint("categories", __name__)

@category_bp.route("", methods=["GET"])
@jwt_required()
def list_categories():
    user_id = get_jwt_identity()
    cats = Category.query.filter_by(user_id=user_id).all()
    return jsonify([CategorySchema.from_orm(c).dict() for c in cats]), 200

@category_bp.route("", methods=["POST"])
@jwt_required()
def create_category():
    user_id = get_jwt_identity()
    try:
        data = CategoryCreateSchema(**(request.get_json() or {}))
    except ValidationError as ve:
        return jsonify({"errors": ve.errors()}), 400

    if Category.query.filter_by(user_id=user_id, name=data.name).first():
        return jsonify({"message": "Category already exists"}), 400

    cat = Category(name=data.name, user_id=user_id)
    db.session.add(cat)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Category conflict"}), 400

    return jsonify(CategorySchema.from_orm(cat).dict()), 201

@category_bp.route("/<int:cat_id>", methods=["DELETE"])
@jwt_required()
def delete_category(cat_id):
    user_id = get_jwt_identity()
    cat = Category.query.filter_by(id=cat_id, user_id=user_id).first()
    if not cat:
        return jsonify({"message": "Category not found"}), 404

    db.session.delete(cat)
    db.session.commit()
    return "", 204
