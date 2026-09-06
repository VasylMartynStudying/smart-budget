from dataclasses import dataclass
import enum


class CategoryType(enum.StrEnum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


@dataclass
class Category:
    id: int | None
    name: str
    type: CategoryType
