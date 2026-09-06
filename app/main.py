import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

from app.bll.category_service import CategoryService
from app.dal.category_repository import CategoryRepository
from app.db.connection import connect, default_db_path, init_schema
from app.ui.category_manager_dialog import CategoryManagerDialog
from app.ui.theme import load_stylesheet


class MainWindow(QMainWindow):
    def __init__(self, category_service: CategoryService) -> None:
        super().__init__()
        self._category_service = category_service

        self.setWindowTitle("Smart Budget")
        self.resize(800, 600)

        title = QLabel("Smart Budget")
        title.setObjectName("pageTitle")

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(title)
        self.setCentralWidget(central)

        categories_action = QAction("Категорії", self)
        categories_action.triggered.connect(self._open_categories)
        catalogs_menu = self.menuBar().addMenu("Меню")
        catalogs_menu.addAction(categories_action)

    def _open_categories(self) -> None:
        dialog = CategoryManagerDialog(self._category_service, self)
        dialog.exec()


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(load_stylesheet())
    connection = connect(default_db_path())
    init_schema(connection)
    category_service = CategoryService(CategoryRepository(connection))
    window = MainWindow(category_service)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
