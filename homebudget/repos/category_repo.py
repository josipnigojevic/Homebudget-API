from ..models.category import Category
from .. import db

class CategoryRepo:
    @staticmethod
    def create(category: Category) -> Category:
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def list_for_user(user_id: int) -> list[Category]:
        return Category.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get(user_id: int, cat_id: int) -> Category | None:
        return Category.query.filter_by(user_id=user_id, id=cat_id).first()

    @staticmethod
    def delete(category: Category) -> None:
        db.session.delete(category)
        db.session.commit()
