from ..models.user import User
from .. import db

class UserRepo:
    @staticmethod
    def create(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_username(username: str) -> User | None:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_id(user_id: int) -> User | None:
        return User.query.get(user_id)
