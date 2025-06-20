import sys
import os
import json

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMenu, QWidget,
    QVBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget,
    QMessageBox, QComboBox, QHBoxLayout, QCheckBox
)
from PySide6.QtGui import QAction, QIcon


# === Загрузка стилей из .qss файла ===
def load_stylesheet(file_path):
    with open(file_path, "r") as f:
        return f.read()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mouse Configurator")
        self.setGeometry(100, 100, 800, 600)

        # === Установка иконки ===
        icon_path = os.path.join(os.path.dirname(__file__), "resources", "icons", "app_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Иконка не найдена по пути: {icon_path}")

        # === Загружаем данные пользователя ===
        self.user_data = self.load_user_data()

        # === ВКЛАДКИ ===
        self.tabs = QTabWidget()

        # --- Вкладка "Авторизация" ---
        self.auth_tab = self.create_auth_tab()
        self.settings_tab = self.create_settings_tab()
        self.settings_tab.setEnabled(False)  # Заблокирована до входа

        self.tabs.addTab(self.auth_tab, "Авторизация")
        self.tabs.addTab(self.settings_tab, "Настройки")

        # === МЕНЮ СМЕНЫ ТЕМЫ ===
        self.menu_bar = QMenuBar(self)
        self.theme_menu = QMenu("Тема", self)
        self.menu_bar.addMenu(self.theme_menu)

        self.dark_action = QAction("Тёмная тема", self)
        self.light_action = QAction("Светлая тема", self)

        self.dark_action.triggered.connect(lambda: self.apply_theme("dark.qss"))
        self.light_action.triggered.connect(lambda: self.apply_theme("light.qss"))

        self.theme_menu.addAction(self.dark_action)
        self.theme_menu.addAction(self.light_action)
        self.setMenuBar(self.menu_bar)

        # === ОСНОВНОЙ ИНТЕРФЕЙС ===
        self.setCentralWidget(self.tabs)

        # Применяем начальную тему
        self.apply_theme("dark.qss")

    def create_auth_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Вход в аккаунт"))

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        self.login_input.setText(self.user_data.get("last_login", ""))  # Автозаполнение

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.remember_checkbox = QCheckBox("Запомнить меня")
        self.remember_checkbox.setChecked(bool(self.user_data.get("remember", False)))

        login_button = QPushButton("Войти")
        login_button.clicked.connect(self.handle_login)

        layout.addWidget(QLabel("Логин:"))
        layout.addWidget(self.login_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.remember_checkbox)
        layout.addWidget(login_button)
        layout.addStretch()

        tab.setLayout(layout)
        return tab

    def handle_login(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()
        remember = self.remember_checkbox.isChecked()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните логин и пароль")
            return

        # === Проверка логина ===
        if self.check_credentials(login, password):
            QMessageBox.information(self, "Успех", f"Вы вошли как {login}")
            self.save_user_data(login, remember)
            self.unlock_tabs()
        else:
            QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль")

    def check_credentials(self, login, password):
        """Проверяет логин и пароль"""
        allowed_users = {
            "admin": "12345",
            "user": "pass",
            "Danila_Gnidenko": "chess18@"
        }
        return allowed_users.get(login) == password

    def save_user_data(self, login, remember):
        """Сохраняет логин и флаг 'Запомнить меня'"""
        data = {
            "last_login": login,
            "remember": remember
        }
        with open("user.json", "w") as f:
            json.dump(data, f)

    def load_user_data(self):
        """Загружает сохранённые данные пользователя"""
        if os.path.exists("user.json"):
            try:
                with open("user.json", "r") as f:
                    return json.load(f)
            except Exception as e:
                print("Ошибка загрузки данных:", e)
        return {}

    def unlock_tabs(self):
        """Разблокирует вкладку 'Настройки' после авторизации"""
        self.tabs.setTabEnabled(1, True)
        #QMessageBox.information(self, "Доступ открыт", "Теперь вы можете настраивать мышь")

    def create_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Настройки мыши"))

        # === Выбор модели мыши ===
        layout.addWidget(QLabel("Выберите модель мыши:"))
        self.mouse_combo = QComboBox()
        mouse_models = [
            "Logitech G502 HERO",
            "Razer DeathAdder V3 Pro",
            "Corsair M65 RGB Elite",
            "SteelSeries Aerox 3",
            "Roccat Burst Pro",
            "HyperX Pulsefire Haste",
            "Redragon K552"
        ]
        self.mouse_combo.addItems(mouse_models)
        self.mouse_combo.currentIndexChanged.connect(self.on_mouse_selected)
        layout.addWidget(self.mouse_combo)

        # === Выбор профиля ===
        profile_selector_layout = QHBoxLayout()
        profile_selector_layout.addWidget(QLabel("Выберите профиль:"))
        self.profile_selector = QComboBox()
        self.profile_selector.addItems(["Профиль 1", "Профиль 2", "Профиль 3"])
        self.profile_selector.currentIndexChanged.connect(self.load_profile)
        profile_selector_layout.addWidget(self.profile_selector)
        layout.addLayout(profile_selector_layout)

        # === DPI ===
        layout.addWidget(QLabel("Выберите DPI:"))
        self.dpi_combo = QComboBox()
        self.dpi_combo.addItems(["400", "800", "1200", "1600", "2400", "3200"])
        layout.addWidget(self.dpi_combo)

        # === Цвет подсветки ===
        color_layout = QHBoxLayout()
        self.color_combo = QComboBox()
        self.color_combo.addItems(["Красный", "Зелёный", "Синий", "Белый", "Фиолетовый", "RGB-цикл"])
        color_apply = QPushButton("Применить")
        color_apply.clicked.connect(self.apply_color)
        color_layout.addWidget(self.color_combo)
        color_layout.addWidget(color_apply)
        layout.addLayout(color_layout)

        # === Кнопка сохранения ===
        save_button = QPushButton("Сохранить в профиль")
        save_button.clicked.connect(self.save_profile)
        layout.addWidget(save_button)

        layout.addStretch()  # Отодвигаем всё вверх
        tab.setLayout(layout)
        return tab

    def on_mouse_selected(self):
        selected_mouse = self.mouse_combo.currentText()
        #QMessageBox.information(self, "Мышь выбрана", f"Вы выбрали: {selected_mouse}")

    def apply_color(self):
        color = self.color_combo.currentText()
        #QMessageBox.information(self, "Подсветка", f"Цвет изменён на {color}")

    def load_profile(self):
        profile_name = self.profile_selector.currentText()
        profiles = self.load_profiles_from_file()

        profile = profiles.get(profile_name, None)
        if profile:
            self.dpi_combo.setCurrentText(profile["dpi"])
            self.color_combo.setCurrentText(profile["color"])
            #QMessageBox.information(self, "Профиль загружен", f"Настройки '{profile_name}':\nDPI: {profile['dpi']}, Цвет: {profile['color']}")
        else:
            self.dpi_combo.setCurrentIndex(0)
            self.color_combo.setCurrentIndex(0)
            #QMessageBox.information(self, "Новый профиль", "Этот профиль пустой. Установлены стандартные настройки.")

    def save_profile(self):
        profile_name = self.profile_selector.currentText()
        dpi = self.dpi_combo.currentText()
        color = self.color_combo.currentText()

        profiles = self.load_profiles_from_file()
        profiles[profile_name] = {
            "dpi": dpi,
            "color": color
        }

        with open("profiles.json", "w") as f:
            json.dump(profiles, f, indent=4)

        QMessageBox.information(self, "Сохранено", f"Профиль '{profile_name}' обновлён:\nDPI: {dpi}, Цвет: {color}")

    def load_profiles_from_file(self):
        if os.path.exists("profiles.json"):
            try:
                with open("profiles.json", "r") as f:
                    return json.load(f)
            except Exception as e:
                print("Ошибка загрузки профилей:", e)
        # Если файл не найден или повреждён — возвращаем стандартные профили
        return {
            "Профиль 1": {"dpi": "1600", "color": "Красный"},
            "Профиль 2": {"dpi": "800", "color": "Синий"},
            "Профиль 3": {"dpi": "400", "color": "RGB-цикл"}
        }

    def apply_theme(self, theme_file):
        style_path = os.path.join(os.path.dirname(__file__), "resources", "qss", theme_file)
        try:
            stylesheet = load_stylesheet(style_path)
            self.setStyleSheet(stylesheet)
            #print(f"Тема изменена на {theme_file}")
        except Exception as e:
            print("Ошибка применения темы:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())