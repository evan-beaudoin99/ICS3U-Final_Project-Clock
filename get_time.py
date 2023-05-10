import board
import busio
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi

def get_time():
    # Get wifi details and more from a secrets.py file
    try:
        from secrets import secrets
    except ImportError:
        print("WiFi secrets are kept in secrets.py, please add them there!")
        raise
    
    print("ESP32 SPI webclient test")
    
    TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
    JSON_URL = "http://worldtimeapi.org/api/timezone/America/Toronto"
    
    
    # If you are using a board with pre-defined ESP32 Pins:
    esp32_cs = DigitalInOut(board.ESP_CS)
    esp32_ready = DigitalInOut(board.ESP_BUSY)
    esp32_reset = DigitalInOut(board.ESP_RESET)
    
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
    
    requests.set_socket(socket, esp)
    
    while not esp.is_connected:
        try:
            esp.connect_AP(secrets["ssid"], secrets["password"])
        except OSError as e:
            print("could not connect to AP, retrying: ", e)
            continue
    print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
    
    print()
    print("Fetching json from", JSON_URL)
    r = requests.get(JSON_URL)
    data = r.json()
    current_time = data["datetime"].split("T")[1][:8] # extract time portion
    # print(current_time)
    r.close()
    
    return current_time
    


time = get_time()
print(time)
print("Done!")

