import sqlite3
from collections.abc import Generator

import pytest

from app.bll.category_service import CategoryService
from app.dal.category_repository import CategoryRepository
from app.db.connection import connect, init_schema


@pytest.fixture
def connection() -> Generator[sqlite3.Connection, None, None]:
    db_connection = connect(":memory:")
    init_schema(db_connection)
    yield db_connection
    db_connection.close()


@pytest.fixture
def category_service(connection: sqlite3.Connection) -> CategoryService:
    return CategoryService(CategoryRepository(connection))
