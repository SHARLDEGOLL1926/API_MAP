import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt
from my_map_ui import Ui_MainWindow
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageQt
from io import BytesIO
import requests


class MyAPP(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyAPP, self).__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.cmd1)

    def cmd1(self):
        toponym_to_find = self.lineEdit.text()
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            pass
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        print(toponym)
        toponym_coodrinates = toponym["Point"]["pos"]
        self.toponym_longitude, self.toponym_lattitude = toponym_coodrinates.split(" ")
        self.cmd2(0)

    def cmd2(self, delta1):
        self.p = float(self.lineEdit_2.text())
        delta = str(self.p + delta1 * 0.001)
        if float(delta) >= 2:
            delta = "2.000"
        elif float(delta) <= 0.001:
            delta = "0.001"
        self.lineEdit_2.setText(delta)
        map_params = {
            "ll": ",".join([self.toponym_longitude, self.toponym_lattitude]),
            "spn": ",".join([delta, delta]),
            "l": "map"
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        self.img = ImageQt.ImageQt(Image.open(BytesIO(response.content)))
        self.label.setPixmap(QPixmap.fromImage(self.img))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            print('!')
            self.cmd2(1)
        if event.key() == Qt.Key_PageDown:
            print('!!')
            self.cmd2(-1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyAPP()
    ex.show()
    sys.exit(app.exec())
