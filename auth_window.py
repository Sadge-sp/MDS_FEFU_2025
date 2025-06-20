from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


class AuthWindow(QWidget):
    def __init__(self, on_login_success=None):
        """
        :param on_login_success: функция, которая вызывается при успешной авторизации
        """
        super().__init__()
        self.on_login_success = on_login_success  # Сохраняем callback

        layout = QVBoxLayout()

        self.label = QLabel("Введите номер заказа:")
        layout.addWidget(self.label)

        self.order_input = QLineEdit()
        self.order_input.setPlaceholderText("Номер заказа")
        layout.addWidget(self.order_input)

        # === Кнопки ===
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.on_login)

        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.on_clear)

        layout.addWidget(self.login_button)
        layout.addWidget(self.clear_button)

        layout.addStretch()  # Отодвигаем элементы наверх
        self.setLayout(layout)

    def on_login(self):
        order_id = self.order_input.text().strip()

        if not order_id:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите номер заказа")
            return

        if not order_id.isdigit() or len(order_id) < 4:
            QMessageBox.critical(self, "Ошибка", "Неверный формат номера заказа")
            return

        # Имитация успешного входа
        QMessageBox.information(self, "Успех", f"Вы вошли как заказ #{order_id}")

        # Вызываем callback, если он задан
        if self.on_login_success:
            self.on_login_success()

    def on_clear(self):
        self.order_input.clear()
        QMessageBox.information(self, "Очистка", "Поле ввода очищено")