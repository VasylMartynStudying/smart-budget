import sqlite3

from app.bll.exceptions import CategoryValidationError, DuplicateCategoryError
from app.dal.category_repository import CategoryRepository
from app.models.category import Category, CategoryType


class CategoryService:
    def __init__(self, repository: CategoryRepository) -> None:
        self._repository = repository

    def get_all(self, category_type: CategoryType | None = None) -> list[Category]:
        categories = self._repository.get_all()
        if category_type is None:
            return categories
        return [category for category in categories if category.type == category_type]

    def get_by_id(self, id: int) -> Category | None:
        return self._repository.get_by_id(id)

    def add_category(self, category: Category) -> Category:
        name = self._validate_name(category.name)
        self._ensure_unique(name)
        try:
            return self._repository.add(
                Category(id=None, name=name, type=category.type)
            )
        except sqlite3.IntegrityError as exc:
            raise DuplicateCategoryError(name) from exc

    def update_category(self, category: Category) -> Category:
        if category.id is None:
            raise CategoryValidationError("Для редагування потрібен ідентифікатор")

        name = self._validate_name(category.name)
        self._ensure_unique(name, exclude_id=category.id)
        try:
            return self._repository.update(
                Category(id=category.id, name=name, type=category.type)
            )
        except sqlite3.IntegrityError as exc:
            raise DuplicateCategoryError(name) from exc

    def delete_category(self, id: int) -> None:
        self._repository.delete(id)

    def _ensure_unique(self, name: str, exclude_id: int | None = None) -> None:
        for existing in self._repository.get_all():
            if existing.name == name and existing.id != exclude_id:
                raise DuplicateCategoryError(name)

    @staticmethod
    def _validate_name(name: str) -> str:
        cleaned = name.strip()
        if not cleaned:
            raise CategoryValidationError("Назва категорії не може бути порожньою")
        return cleaned
