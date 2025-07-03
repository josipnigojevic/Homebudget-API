from ..repos.user_repo import UserRepo
from ..models.user import User
from ..models.category import Category
from ..schemas import UserRegisterSchema

class UserService:
    @staticmethod
    def register(data: UserRegisterSchema) -> User:
        if UserRepo.get_by_username(data.username):
            raise ValueError('Username already exists')
        user = User(username=data.username, starting_budget=data.starting_budget)
        user.set_password(data.password)
        for name in ['Food','Car','Accommodation','Gifts','Health','Utilities']:
            user.categories.append(Category(name=name))
        return UserRepo.create(user)

    @staticmethod
    def authenticate(username: str, password: str) -> User:
        user = UserRepo.get_by_username(username)
        if not user or not user.check_password(password):
            raise ValueError('Invalid credentials')
        return user
