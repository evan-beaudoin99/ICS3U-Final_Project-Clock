import network
import urequests

# Connect to WiFi network
ssid = "your_SSID"
password = "your_PASSWORD"
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)
while not sta_if.isconnected():
    pass

# Make a GET request to the WorldTimeAPI
url = "http://worldtimeapi.org/api/timezone/America/Toronto"
response = urequests.get(url)

if response.status_code == 200:
    data = response.json()
    current_time = data["datetime"].split("T")[1][:8]  # extract time portion
    print("Current time in Canada: ", current_time)
else:
    print
