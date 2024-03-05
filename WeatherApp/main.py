import sys
import requests
import json
from datetime import datetime
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap,QIcon
  
    
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load("form.ui",None)
        self.ui.show()
        self.ui.btn_city.clicked.connect(self.weather)
        self.ui.info.triggered.connect(self.info)
        self.ui.exit.triggered.connect(exit)

        self.date_forecast = [self.ui.label_date1,self.ui.label_date2,self.ui.label_date3,self.ui.label_date4]
        self.icon_forecast = [self.ui.label_icon1,self.ui.label_icon2,self.ui.label_icon3,self.ui.label_icon4]
        self.temp_forecast = [self.ui.label_temp1,self.ui.label_temp2,self.ui.label_temp3,self.ui.label_temp4]
        

    def weather(self):
        city = self.ui.city_text.text()
        url = f"https://api.weatherbit.io/v2.0/forecast/daily?&city={city}&key=2effe1f9f06e40cc8ef77eb5be376022"
        response = requests.request("GET", url)
        json_data = json.loads(response.text)
        date_time = json_data["data"][0]["datetime"]
        normal_date = datetime.strptime(date_time, '%Y-%m-%d')
        date = normal_date.strftime('%A, %d %B')
        description_weather = json_data["data"][0]["weather"]["description"]
        self.ui.label_city.setText(str(json_data["city_name"])+" "+str(json_data["country_code"]))
        self.ui.label_date.setText(date)
        self.ui.label_c.setText("°C")
        self.ui.label_line.setText("|")
        self.ui.label_temp.setText(str(json_data["data"][0]["temp"]))
        self.ui.label_description.setText(description_weather)
        self.ui.label_wind.setText(f"Wind: {json_data['data'][0]['wind_spd']} km/h")
        self.ui.label_prec.setText(f"Precipitation: {str(json_data['data'][0]['precip'])[:3]} %")
        self.ui.label_min_temp.setText(str(json_data["data"][0]["app_min_temp"]))
        self.ui.label_max_temp.setText(str(json_data["data"][0]["app_max_temp"]))

        if "Clear" in description_weather: img = "img/sunny2.png"
        elif "Few clouds" in description_weather: img = "img/partly-cloudy2.png"
        elif "Mix snow/rain" in description_weather: img = "img/mix2.png"
        elif "rain" in description_weather: img = "img/rain2.png"
        elif "snow" in description_weather: img = "img/snow2.png"
        else : img = "img/clouds4.png"
        pixmap = QPixmap(img)
        self.ui.label_icon.setPixmap(pixmap)


        # forecast weather
        for i in range(4):
            date_time = json_data["data"][i+1]["datetime"]
            normal_date = datetime.strptime(date_time, '%Y-%m-%d')
            date = normal_date.strftime('%A')
            self.date_forecast[i].setText(date[:3])

            description_weather = json_data["data"][i+1]["weather"]["description"]
            if "Clear" in description_weather: img = "img/sunny.png"
            elif "Few clouds" in description_weather: img = "img/partly_clouds.png"
            elif "Mix snow/rain" in description_weather: img = "img/mix.png"
            elif "rain" in description_weather: img = "img/rain.png"
            elif "snow" in description_weather: img = "img/snow.png"
            else : img = "img/clouds.png"
            pixmap = QPixmap(img)
            self.icon_forecast[i].setPixmap(pixmap)

            self.temp_forecast[i].setText(str(json_data["data"][i+1]["temp"])+"°C")


    def info(self):
        msg = QMessageBox()
        msg.setText("Weather Application")
        msg.setInformativeText("GUI Weather Application using Pyside6 \nVersion 1.3\nThis program was developed by Alireza Kiaeipour\nContact developer: a.kiaipoor@gmail.com\nBuilt in 2024")
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Information")
        msg.setWindowIcon(QIcon("img/clouds.png"))
        msg.exec()
        

app = QApplication(sys.argv)
window = Main()
app.exec()