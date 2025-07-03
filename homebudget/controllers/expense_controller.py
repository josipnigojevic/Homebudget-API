from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from ..services.expense_service import ExpenseService
from ..services.stats_service import StatsService
from ..schemas import ExpenseCreateSchema, ExpenseSchema, StatsResponseSchema

class ExpenseController:

    @staticmethod
    @jwt_required()
    def list():
        user_id = get_jwt_identity()
        filters = {
            k: request.args[k]
            for k in request.args
            if k in ("category_id","min_amount","max_amount","start_date","end_date")
        }
        exps = ExpenseService.list(user_id, filters)
        return jsonify([ExpenseSchema.from_orm(e).dict() for e in exps]), 200

    @staticmethod
    @jwt_required()
    def create():
        user_id = get_jwt_identity()
        try:
            data = ExpenseCreateSchema(**(request.get_json() or {}))
        except ValidationError as ve:
            return jsonify({"errors": ve.errors()}), 400

        try:
            exp = ExpenseService.create(user_id, data)
        except LookupError as le:
            return jsonify({"message": str(le)}), 404
        except IntegrityError:
            return jsonify({"message": "Expense conflict"}), 400

        return jsonify(ExpenseSchema.from_orm(exp).dict()), 201

    @staticmethod
    @jwt_required()
    def delete(exp_id):
        user_id = get_jwt_identity()
        try:
            ExpenseService.delete(user_id, int(exp_id))
        except LookupError as le:
            return jsonify({"message": str(le)}), 404
        return "", 204

    @staticmethod
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
        sd = request.args.get("start_date")
        ed = request.args.get("end_date")
        if sd:
            start = datetime.fromisoformat(sd).date()
        end = datetime.fromisoformat(ed).date() if ed else today

        stats = StatsService.calculate(user_id, period, start, end)
        return jsonify(StatsResponseSchema(**stats).dict()), 200
