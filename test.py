import time
import board
import busio
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
from secrets import secrets


def get_time():
    # This funcion gets the time
    print("ESP32 SPI webclient test")
    
    JSON_URL = "http://worldtimeapi.org/api/timezone/America/Toronto"
    
    # If you are using a board with pre-defined ESP32 Pins:
    esp32_cs = DigitalInOut(board.ESP_CS)
    esp32_ready = DigitalInOut(board.ESP_BUSY)
    esp32_reset = DigitalInOut(board.ESP_RESET)
    
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
    
   
    
    while not esp.is_connected:
        try:
            #print("Connect 4")
            esp.connect_AP(secrets["ssid"], secrets["password"], 10)
            print("Connection status: ", esp.is_connected)
        except OSError as e:
            print("could not connect to AP, retrying: ", e)
            continue
    
    print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
    
    
    requests.set_socket(socket, esp)
    i=1
    while i < 1000:
        #print(i)
        i += 1
        #print()
        #print("Fetching json from", JSON_URL)
        
        time.sleep(500/1000)
        try:
            response = requests.get(JSON_URL)
            data = response.json()
            current_time = data["datetime"].split("T")[1][:8] # extract time portion
        
            print(current_time)
        except:
            print("Socket error")
            continue
        
    response.close()
    print("Disconnecting")
    esp.disconnect()
    
    
    #return current_time
    


get_time()
#print(time)
print("Done!")
