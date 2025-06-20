import pywinusb.hid as hid

class MouseController:
    def __init__(self, vendor_id=None, product_id=None):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device = None
        self.connected = False

    def connect(self):
        """Подключение к мыши"""
        if self.device is not None:
            self.disconnect()  # Закрываем предыдущее соединение, если оно было

        try:
            devices = hid.HidDeviceFilter(
                vendor_id=self.vendor_id,
                product_id=self.product_id
            ).get_devices()

            if devices:
                self.device = devices[0]
                self.device.open()
                self.connected = True
                print(f"Устройство найдено: {self.device.product_name}")
                return True
            else:
                print("Устройство не найдено")
                return False
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False

    def disconnect(self):
        """Отключение от мыши"""
        if self.device and self.connected:
            self.device.close()
            self.connected = False
            print("Устройство отключено")

    def send_report(self, data):
        """Отправка данных на устройство"""
        if not self.connected:
            print("Нет подключения к устройству")
            return False

        try:
            out_report = self.device.find_output_reports()[0]
            out_report.send(data)
            print(f"Команда отправлена: {data}")
            return True
        except Exception as e:
            print(f"Ошибка отправки команды: {e}")
            return False