from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
from device_connector import MouseController


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.mouse = None
        self.commands = {}
        self.mouse_profiles = []

        layout = QVBoxLayout()

        self.mouse_combo = QComboBox()
        self.mouse_combo.currentIndexChanged.connect(self.load_profile_settings)
        layout.addWidget(QLabel("Выберите модель мыши:"))
        layout.addWidget(self.mouse_combo)

        self.dpi_combo = QComboBox()
        layout.addWidget(QLabel("DPI:"))
        layout.addWidget(self.dpi_combo)

        self.apply_button = QPushButton("Применить")
        self.apply_button.clicked.connect(self.apply_settings)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

        self.load_mouse_profiles()

    def load_mouse_profiles(self):
        """Загружаем список мышей с сайта"""
        self.mouse_profiles = [
            {
                "name": "Mouse Pro X",
                "vendor_id": "0x1532",
                "product_id": "0x0097",
                "supported_features": ["dpi"],
                "commands": {
                    "set_dpi": [0x00, 0x08, "{level}", 0x00, 0x00, 0x00, 0x00, 0x00]
                }
            },
            {
                "name": "Mouse Lite Y",
                "vendor_id": "0x1234",
                "product_id": "0xABCD",
                "supported_features": ["dpi"],
                "commands": {
                    "set_dpi": [0x00, 0x0A, "{level}", 0x00, 0x00, 0x00, 0x00, 0x00]
                }
            }
        ]

        for mouse in self.mouse_profiles:
            self.mouse_combo.addItem(mouse["name"])

        if self.mouse_profiles:
            self.load_profile_settings(0)

    def load_profile_settings(self, index):
        """Загружаем настройки выбранной мыши"""
        selected = self.mouse_profiles[index]
        self.commands = selected.get("commands", {})
        self.mouse = MouseController(
            int(selected["vendor_id"], 16),
            int(selected["product_id"], 16)
        )

        # Очищаем DPI
        self.dpi_combo.clear()
        dpi_levels = ["400", "800", "1200", "1600", "3200"]
        self.dpi_combo.addItems(dpi_levels)

    def apply_settings(self):
        """Применяем настройки к мыши"""
        if not self.mouse.connect():
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к мыши")
            return

        dpi_value = self.dpi_combo.currentText()
        command_template = self.commands.get("set_dpi")

        if command_template:
            level = self.dpi_combo.currentIndex() + 1
            report_data = [int(b.replace("{level}", str(level)), 16) if "{" not in b else int(b, 16) for b in command_template]
            self.mouse.send_report(report_data)
            QMessageBox.information(self, "Готово", f"DPI установлено на {dpi_value}")