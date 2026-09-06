import pytest

from app.bll.category_service import CategoryService
from app.bll.exceptions import DuplicateCategoryError
from app.models.category import Category, CategoryType


def test_add_category(category_service: CategoryService) -> None:
    category = category_service.add_category(
        Category(id=None, name="Зарплата", type=CategoryType.INCOME)
    )

    assert category.id is not None
    stored = category_service.get_by_id(category.id)
    assert stored is not None
    assert stored.name == "Зарплата"
    assert stored.type == CategoryType.INCOME


def test_add_duplicate_category_raises_error(
    category_service: CategoryService,
) -> None:
    category_service.add_category(
        Category(id=None, name="Продукти", type=CategoryType.EXPENSE)
    )

    with pytest.raises(DuplicateCategoryError):
        category_service.add_category(
            Category(id=None, name="Продукти", type=CategoryType.INCOME)
        )
