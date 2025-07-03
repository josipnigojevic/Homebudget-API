from datetime import date
from ..models.expense import Expense
from .. import db

class ExpenseRepo:
    @staticmethod
    def create(expense: Expense) -> Expense:
        db.session.add(expense)
        db.session.commit()
        return expense

    @staticmethod
    def list_for_user(user_id: int, filters: dict) -> list[Expense]:
        q = Expense.query.filter_by(user_id=user_id)
        if f := filters.get('category_id'): q = q.filter_by(category_id=f)
        if f := filters.get('min_amount'): q = q.filter(Expense.amount >= f)
        if f := filters.get('max_amount'): q = q.filter(Expense.amount <= f)
        if sd := filters.get('start_date'): q = q.filter(Expense.date >= sd)
        if ed := filters.get('end_date'): q = q.filter(Expense.date <= ed)
        return q.order_by(Expense.date.desc()).all()

    @staticmethod
    def get(user_id: int, exp_id: int) -> Expense | None:
        return Expense.query.filter_by(user_id=user_id, id=exp_id).first()

    @staticmethod
    def delete(expense: Expense) -> None:
        db.session.delete(expense)
        db.session.commit()
