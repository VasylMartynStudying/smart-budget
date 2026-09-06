class CategoryError(Exception):
    pass


class CategoryValidationError(CategoryError):
    pass


class DuplicateCategoryError(CategoryValidationError):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Категорія «{name}» вже існує")
