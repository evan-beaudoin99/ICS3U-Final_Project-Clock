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

matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(0, (matrixportal.graphics.display.height // 2) - 1),
    scrolling=True,
    text_scale = 2

)
        


SCROLL_DELAY = 0.03

# PERIOD_END_TIMES = []

CONTENTS = [
    { 'text': 'Class is over',  'color': '#cf2727'},
    { 'text': 'Time to Leave', 'color': '#0846e4'},
    { 'text': 'Do not be Late!', 'color': '#7fffd4'}
]


period_end_times = {
    "Period one": {
        "hour": 10,
        "minute": 5
    },
    "Period two": {
        "hour": 11,
        "minute": 25
    },
    "Period three": {
        "hour": 13,
        "minute": 30
    },
    "Period four": {
        "hour": 22,
        "minute": 9
    }
}


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
    
      
    for end_time in period_end_times.items():
        if end_time["hour"] == hours and end_time["minute"] == minutes:
            for content in CONTENTS:

                matrixportal.set_text(content['text'], 1)
                matrixportal.set_text_color(content['color'], 1)
        
                matrixportal.scroll_text(SCROLL_DELAY)

    time.sleep(60)
    
    minutes += 1
