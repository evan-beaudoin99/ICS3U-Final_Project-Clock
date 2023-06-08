import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal
from colors import colors
import random


# Set up where we'll be fetching data from
DATA_SOURCE = "http://worldtimeapi.org/api/timezone/America/Toronto"
DATA_LOCATION = ["datetime"]

def get_current_time():
    try:
        value = matrixportal.fetch()
        print("Response is", value)
        last_check = time.monotonic()
    except (ValueError, RuntimeError) as e:
        print("Some error occurred, retrying! -", e)
    
    return value
    
    
matrixportal = MatrixPortal(
    url=DATA_SOURCE,
    json_path=DATA_LOCATION,
    status_neopixel=board.NEOPIXEL,
)

matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(3, 16),
    scrolling=False,
    text_scale = 2

)


current_time = get_current_time()

date_time = current_time.split("T")[1].split(":")
    
hours = int(date_time[0])
minutes = int(date_time[1])
seconds = int(date_time[2].split(".", 1)[0])  # Extract seconds and remove the fractional part if present


# print("Hour:", hours)
# print("Minute:", minutes)
# print("Seconds:", seconds)

matrixportal.set_text("TEJ3M")

slide = 60 - seconds 
time.sleep(slide)
minutes +=1

while True:
  
    if minutes == 60:
        hours +=1
        minutes = 0

    if hours == 24:
        hours = 0
        
    # Format the hour and minute as a string
    formatted_time = f"{hours:02d}:{minutes:02d}"
   
    matrixportal.set_text(formatted_time)
    color_index = random.randint(0, len(colors) - 1)
    color_name = list(colors.keys())[color_index]
    color_value = colors[color_name]

    matrixportal.set_text_color(color_value)
    
      
    if hours == 9 and minutes == 27:
        matrixportal.set_text("Leave")

    time.sleep(60)
    
    minutes += 1
