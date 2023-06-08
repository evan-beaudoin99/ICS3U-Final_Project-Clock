import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal

# Set up where we'll be fetching data from
DATA_SOURCE = "http://worldtimeapi.org/api/timezone/America/Toronto"
DATA_LOCATION = ["datetime"]

# def text_transform(val):
#     # Parse the datetime string and extract the hour and minute components
#     date_time = val.split("T")[1].split(":")
#     hour = int(date_time[0])
#     minute = int(date_time[1])

#     # Format the hour and minute as a string
#     formatted_time = f"{hour:02d}:{minute:02d}"

#     return formatted_time

# the current working directory (where this file is)
cwd = ("/" + __file__).rsplit("/", 1)[0]

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

last_check = None

while True:
    if last_check is None or time.monotonic() > last_check + 3600:
        try:
            value = matrixportal.fetch()
            print("Response is", value)
            last_check = time.monotonic()
        except (ValueError, RuntimeError) as e:
            print("Some error occurred, retrying! -", e)
    
    # current_time = text_transform(value)
    new_time = value
    date_time = new_time.split("T")[1].split(":")
    
    hours = int(date_time[0])
    minutes = int(date_time[1])
    
    minutes += 1
    
    if minutes == 60:
        hours +=1
        minutes = 0

    if hours == 24:
        hours = 0


    # Format the hour and minute as a string
    formatted_time = f"{hours:02d}:{minutes:02d}"


    matrixportal.set_text(formatted_time)
    
    time.sleep(60)
