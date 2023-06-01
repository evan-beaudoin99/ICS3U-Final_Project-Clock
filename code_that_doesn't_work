import board
import busio
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import random
import time
import terminalio
from colors import colors
from adafruit_matrixportal.matrixportal import MatrixPortal
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
    response = requests.get(JSON_URL)
    data = response.json()
    current_time = data["datetime"].split("T")[1][:8] # extract time portion
    # print(current_time)
    response.close()

    return current_time
    
time = get_time()
print(time)
print("Done!")
    

def main() -> None:
    
    time = get_time()
    print(time)
    print("Done!")

    matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=True)

    matrixportal.add_text(
        text_font=terminalio.FONT,
        text_position=(3, (matrixportal.graphics.display.height // 2) - 1),
        scrolling=False,
        text_scale = 2)

    color_index = random.randint(0, len(colors) - 1)

    color_name = list(colors.keys())[color_index]
    color_value = colors[color_name]

    minutes = 20
    hours = 9
    
    while True:
        matrixportal.set_text(f"{hours:02d}:{minutes:02d}")

        color_index = random.randint(0, len(colors) - 1)
        color_name = list(colors.keys())[color_index]
        color_value = colors[color_name]

        matrixportal.set_text_color(color_value)

        minutes += 1
        if minutes == 60:
            hours +=1
            minutes = 0

        if hours == 24:
            hours = 0

        time.sleep(1)

if __name__ == "__main__":
    main()
