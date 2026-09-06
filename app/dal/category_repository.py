import sqlite3

from app.models.category import Category, CategoryType


class CategoryRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def get_all(self) -> list[Category]:
        rows = self._connection.execute(
            "SELECT id, name, type FROM categories ORDER BY name"
        ).fetchall()
        return [self._row_to_category(row) for row in rows]

    def get_by_id(self, id: int) -> Category | None:
        row = self._connection.execute(
            "SELECT id, name, type FROM categories WHERE id = ?",
            (id,),
        ).fetchone()
        if row is None:
            return None
        return self._row_to_category(row)

    def add(self, category: Category) -> Category:
        cursor = self._connection.execute(
            "INSERT INTO categories (name, type) VALUES (?, ?)",
            (category.name, category.type.value),
        )
        self._connection.commit()
        return Category(id=cursor.lastrowid, name=category.name, type=category.type)

    def update(self, category: Category) -> Category:
        if category.id is None:
            raise ValueError("Category id is required for update")

        self._connection.execute(
            "UPDATE categories SET name = ?, type = ? WHERE id = ?",
            (category.name, category.type.value, category.id),
        )
        self._connection.commit()
        return category

    def delete(self, id: int) -> None:
        self._connection.execute("DELETE FROM categories WHERE id = ?", (id,))
        self._connection.commit()

    @staticmethod
    def _row_to_category(row: sqlite3.Row) -> Category:
        return Category(
            id=row["id"],
            name=row["name"],
            type=CategoryType(row["type"]),
        )
