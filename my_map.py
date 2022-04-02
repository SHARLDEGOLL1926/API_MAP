import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
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
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        delta = self.lineEdit_2.text()
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join([delta, delta]),
            "l": "map"
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        self.img = ImageQt.ImageQt(Image.open(BytesIO(response.content)))
        self.label.setPixmap(QPixmap.fromImage(self.img))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyAPP()
    ex.show()
    sys.exit(app.exec())
