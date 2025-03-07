import requests
import datetime as dt
import sys
import time
from Adafruit_IO import MQTTClient


class Task1:
    def __init__(self): 
        print("Init task 1")
        #define the URL
        self.BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
        self.API_KEY = "c9e9db60a93f15a43de916d49d078ae9"
        self.CITY = "Binh Duong, VN"

        self.AIO_FEED_ID = ""
        self.AIO_USERNAME = "hej_manh"
        self.AIO_KEY = open('AIO_KEY','r').read()

        #set up MQTT client and define callback function
        self.client = MQTTClient(self.AIO_USERNAME, self.AIO_KEY)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe

    def kelvin_to_celsius(self, kelvin):
        celsius = kelvin - 273.15
        return celsius

    def connected(self, client):
        print("Server connected ...")
        self.client.subscribe("cityname")
        self.client.subscribe("temperature")
        self.client.subscribe("feelslike")
        self.client.subscribe("windspeed")
        self.client.subscribe("humidity")
        self.client.subscribe("description")
        self.client.subscribe("sunrisetime")
        self.client.subscribe("sunsettime")

    def subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribe ...")

    def disconnected(self, client):
        print("Disconnect from server ...")
        sys.exit(1)

    def message(self, client, feed_id, payload):
        print("Received: " + payload)

    def Task1_Run(self):
        url = self.BASE_URL + "appid=" + self.API_KEY + "&q=" + self.CITY
        response = requests.get(url).json()

        #get data from response in API
        temp_kelvin = response['main']['temp']
        temp_celsius = self.kelvin_to_celsius(temp_kelvin)
        feels_like_kelvin = response['main']['feels_like']
        feels_like_celsius = self.kelvin_to_celsius(feels_like_kelvin)
        wind_speed = response['wind']['speed']
        humidity = response['main']['humidity']
        description = response['weather'][0]['description']
        sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
        sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
        
        #establish a connection with MQTT broker and start background loop
        self.client.connect()
        self.client.loop_background()

        start_time = time.time()

        while True:
            #send data to client
            print("Task 1 is activated")
            time.sleep(5)
            self.client.publish("cityname", self.CITY)
            self.client.publish("temperature", str(round(temp_celsius, 2)))
            self.client.publish("feelslike", str(round(feels_like_celsius, 2)))
            self.client.publish("windspeed", str(wind_speed) + "m/s")
            self.client.publish("humidity", str(humidity))
            self.client.publish("description", description)
            self.client.publish("sunrisetime", str(sunrise_time))
            self.client.publish("sunsettime", str(sunset_time))

            elapsed_time = time.time() - start_time
            if elapsed_time >= 20:  
                self.disconnected(self.client) 
            pass