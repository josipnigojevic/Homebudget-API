from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from ..repos.expense_repo import ExpenseRepo

class StatsService:
    @staticmethod
    def calculate(user_id: int, period: str | None, start_date=None, end_date=None) -> dict:
        today = datetime.utcnow().date()
        if period == 'last_month':
            start = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
            end = today
        elif period == 'last_quarter':
            start = today - relativedelta(months=3)
            end = today
        elif period == 'last_year':
            start = today - relativedelta(years=1)
            end = today
        elif start_date:
            start = start_date
            end = end_date or today
        else:
            start = today - relativedelta(months=1)
            end = today

        expenses = ExpenseRepo.list_for_user(user_id, {
            'start_date': start,
            'end_date': end
        })
        total_spent = sum(float(e.amount) for e in expenses if e.amount >= 0)
        total_earned = sum(-float(e.amount) for e in expenses if e.amount < 0)
        return {
            'start_date': start,
            'end_date': end,
            'total_spent': round(total_spent, 2),
            'total_earned': round(total_earned, 2),
            'net_flow': round(total_earned - total_spent, 2)
        }
