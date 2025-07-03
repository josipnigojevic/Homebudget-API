from datetime import datetime
from ..repos.expense_repo import ExpenseRepo
from ..models.expense import Expense
from ..repos.category_repo import CategoryRepo
from ..schemas import ExpenseCreateSchema

class ExpenseService:
    @staticmethod
    def list(user_id: int, filters: dict) -> list[Expense]:
        return ExpenseRepo.list_for_user(user_id, filters)

    @staticmethod
    def create(user_id: int, data: ExpenseCreateSchema) -> Expense:
        cat = CategoryRepo.get(user_id, data.category_id)
        if not cat:
            raise LookupError('Category not found')
        exp = Expense(
            description=data.description,
            amount=data.amount,
            date=data.date or datetime.utcnow().date(),
            user_id=user_id,
            category_id=cat.id
        )
        return ExpenseRepo.create(exp)

    @staticmethod
    def get(user_id: int, exp_id: int) -> Expense:
        exp = ExpenseRepo.get(user_id, exp_id)
        if not exp:
            raise LookupError('Expense not found')
        return exp

    @staticmethod
    def delete(user_id: int, exp_id: int) -> None:
        exp = ExpenseService.get(user_id, exp_id)
        ExpenseRepo.delete(exp)
