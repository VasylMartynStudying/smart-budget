from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from app.bll.category_service import CategoryService
from app.bll.exceptions import CategoryError
from app.models.category import Category, CategoryType


class CategoryManagerDialog(QDialog):
    def __init__(
        self,
        service: CategoryService,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._service = service

        self.setWindowTitle("Категорії")
        self.resize(480, 420)

        self._tabs = QTabWidget()
        self._income_table = self._create_table()
        self._expense_table = self._create_table()
        self._tabs.addTab(self._income_table, "Доходи")
        self._tabs.addTab(self._expense_table, "Витрати")

        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("Назва категорії")
        self._name_edit.returnPressed.connect(self._on_add)

        self._add_button = QPushButton("Додати")
        self._edit_button = QPushButton("Редагувати")
        self._delete_button = QPushButton("Видалити")
        self._add_button.setObjectName("primaryButton")
        self._delete_button.setObjectName("dangerButton")
        self._edit_button.setEnabled(False)
        self._delete_button.setEnabled(False)

        self._add_button.clicked.connect(self._on_add)
        self._edit_button.clicked.connect(self._on_edit)
        self._delete_button.clicked.connect(self._on_delete)
        self._tabs.currentChanged.connect(self._on_tab_changed)
        self._income_table.itemSelectionChanged.connect(self._on_selection_changed)
        self._expense_table.itemSelectionChanged.connect(self._on_selection_changed)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self._add_button)
        buttons_layout.addWidget(self._edit_button)
        buttons_layout.addWidget(self._delete_button)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Назва:"))
        form_layout.addWidget(self._name_edit)

        layout = QVBoxLayout(self)
        layout.addWidget(self._tabs)
        layout.addLayout(form_layout)
        layout.addLayout(buttons_layout)

        self._reload()

    def _create_table(self) -> QTableWidget:
        table = QTableWidget(0, 1)
        table.setHorizontalHeaderLabels(["Назва"])
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setAlternatingRowColors(True)
        return table

    def _current_type(self) -> CategoryType:
        if self._tabs.currentIndex() == 0:
            return CategoryType.INCOME
        return CategoryType.EXPENSE

    def _current_table(self) -> QTableWidget:
        if self._current_type() is CategoryType.INCOME:
            return self._income_table
        return self._expense_table

    def _selected_category_id(self) -> int | None:
        items = self._current_table().selectedItems()
        if not items:
            return None
        category_id = items[0].data(Qt.ItemDataRole.UserRole)
        if category_id is None:
            return None
        return int(category_id)

    def _reload(self) -> None:
        self._fill_table(
            self._income_table,
            self._service.get_all(CategoryType.INCOME),
        )
        self._fill_table(
            self._expense_table,
            self._service.get_all(CategoryType.EXPENSE),
        )
        self._on_selection_changed()

    def _fill_table(self, table: QTableWidget, categories: list[Category]) -> None:
        table.setRowCount(len(categories))
        for row, category in enumerate(categories):
            item = QTableWidgetItem(category.name)
            item.setData(Qt.ItemDataRole.UserRole, category.id)
            table.setItem(row, 0, item)

    def _on_tab_changed(self) -> None:
        self._name_edit.clear()
        self._on_selection_changed()

    def _on_selection_changed(self) -> None:
        category_id = self._selected_category_id()
        has_selection = category_id is not None
        self._edit_button.setEnabled(has_selection)
        self._delete_button.setEnabled(has_selection)

        if category_id is None:
            return

        category = self._service.get_by_id(category_id)
        if category is not None:
            self._name_edit.setText(category.name)

    def _on_add(self) -> None:
        try:
            self._service.add_category(
                Category(
                    id=None,
                    name=self._name_edit.text(),
                    type=self._current_type(),
                )
            )
        except CategoryError as exc:
            QMessageBox.warning(self, "Помилка", str(exc))
            return

        self._name_edit.clear()
        self._reload()

    def _on_edit(self) -> None:
        category_id = self._selected_category_id()
        if category_id is None:
            QMessageBox.information(
                self, "Категорії", "Оберіть категорію для редагування"
            )
            return

        category = self._service.get_by_id(category_id)
        if category is None:
            QMessageBox.warning(self, "Помилка", "Категорію не знайдено")
            return

        try:
            self._service.update_category(
                Category(
                    id=category.id,
                    name=self._name_edit.text(),
                    type=category.type,
                )
            )
        except CategoryError as exc:
            QMessageBox.warning(self, "Помилка", str(exc))
            return

        self._reload()

    def _on_delete(self) -> None:
        category_id = self._selected_category_id()
        if category_id is None:
            QMessageBox.information(
                self, "Категорії", "Оберіть категорію для видалення"
            )
            return

        answer = QMessageBox.question(
            self,
            "Видалення категорії",
            "Видалити вибрану категорію?",
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            self._service.delete_category(category_id)
        except CategoryError as exc:
            QMessageBox.warning(self, "Помилка", str(exc))
            return

        self._name_edit.clear()
        self._reload()
