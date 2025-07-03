from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from ..models.expense  import Expense
from ..models.category import Category
from ..schemas         import ExpenseCreateSchema, ExpenseSchema, StatsResponseSchema
from .. import db

expense_bp = Blueprint("expenses", __name__)

@expense_bp.route("", methods=["GET"])
@jwt_required()
def list_expenses():
    user_id = get_jwt_identity()
    q = Expense.query.filter_by(user_id=user_id)
    if cat := request.args.get("category_id"):
        q = q.filter_by(category_id=int(cat))
    if mn := request.args.get("min_amount"):
        q = q.filter(Expense.amount >= float(mn))
    if mx := request.args.get("max_amount"):
        q = q.filter(Expense.amount <= float(mx))
    if sd := request.args.get("start_date"):
        q = q.filter(Expense.date >= datetime.fromisoformat(sd).date())
    if ed := request.args.get("end_date"):
        q = q.filter(Expense.date <= datetime.fromisoformat(ed).date())
    exps = q.order_by(Expense.date.desc()).all()
    return jsonify([ExpenseSchema.from_orm(e).dict() for e in exps]), 200

@expense_bp.route("", methods=["POST"])
@jwt_required()
def create_expense():
    user_id = get_jwt_identity()
    try:
        data = ExpenseCreateSchema(**(request.get_json() or {}))
    except ValidationError as ve:
        return jsonify({"errors": ve.errors()}), 400

    cat = Category.query.filter_by(id=data.category_id, user_id=user_id).first()
    if not cat:
        return jsonify({"message": "Category not found"}), 404

    exp = Expense(
        description=data.description,
        amount=data.amount,
        date=data.date or date.today(),
        category_id=cat.id,
        user_id=user_id
    )
    db.session.add(exp)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Expense conflict"}), 400

    return jsonify(ExpenseSchema.from_orm(exp).dict()), 201

@expense_bp.route("/<int:exp_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(exp_id):
    user_id = get_jwt_identity()
    exp = Expense.query.filter_by(id=exp_id, user_id=user_id).first()
    if not exp:
        return jsonify({"message": "Expense not found"}), 404

    db.session.delete(exp)
    db.session.commit()
    return "", 204

@expense_bp.route("/stats", methods=["GET"])
@jwt_required()
def stats():
    user_id = get_jwt_identity()
    today = datetime.utcnow().date()
    start = today - relativedelta(months=1)
    period = request.args.get("period")
    if period == "last_quarter":
        start = today - relativedelta(months=3)
    elif period == "last_year":
        start = today - relativedelta(years=1)

    if sd := request.args.get("start_date"):
        start = datetime.fromisoformat(sd).date()
    end = datetime.fromisoformat(request.args.get("end_date")).date() if request.args.get("end_date") else today

    exps = Expense.query.filter_by(user_id=user_id).filter(Expense.date >= start, Expense.date <= end).all()
    spent  = sum(float(e.amount) for e in exps if e.amount >= 0)
    earned = sum(-float(e.amount) for e in exps if e.amount < 0)
    result = {
        "start_date":  start,
        "end_date":    end,
        "total_spent": round(spent,  2),
        "total_earned":round(earned, 2),
        "net_flow":    round(earned - spent, 2)
    }
    return jsonify(StatsResponseSchema(**result).dict()), 200
