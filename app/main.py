import sys

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Smart Budget")
        self.resize(800, 600)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(QLabel("Smart Budget"))
        self.setCentralWidget(central)


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
