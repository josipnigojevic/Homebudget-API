from ..repos.category_repo import CategoryRepo
from ..models.category import Category
from ..schemas import CategoryCreateSchema

class CategoryService:
    @staticmethod
    def list(user_id: int) -> list[Category]:
        return CategoryRepo.list_for_user(user_id)

    @staticmethod
    def create(user_id: int, data: CategoryCreateSchema) -> Category:
        existing = CategoryRepo.list_for_user(user_id)
        if any(c.name == data.name for c in existing):
            raise ValueError('Category already exists')
        cat = Category(name=data.name, user_id=user_id)
        return CategoryRepo.create(cat)

    @staticmethod
    def get(user_id: int, cat_id: int) -> Category:
        cat = CategoryRepo.get(user_id, cat_id)
        if not cat:
            raise LookupError('Category not found')
        return cat

    @staticmethod
    def delete(user_id: int, cat_id: int) -> None:
        cat = CategoryService.get(user_id, cat_id)
        CategoryRepo.delete(cat)
