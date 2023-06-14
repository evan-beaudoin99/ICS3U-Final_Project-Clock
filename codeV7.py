import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal
from colors import colors
import random
import supervisor


# Set up where we'll be fetching data from
DATA_SOURCE = "http://worldtimeapi.org/api/timezone/America/Toronto"
DATA_LOCATION = ["datetime"]

matrixportal = MatrixPortal(
    url=DATA_SOURCE,
    json_path=DATA_LOCATION,
    status_neopixel=board.NEOPIXEL,
)

# Text label for clock text
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(2, (matrixportal.graphics.display.height // 2) - 1),
    scrolling=False,
    text_scale = 2
)

# Text label for scrolling message
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(0, (matrixportal.graphics.display.height // 2) - 1),
    scrolling=True,
    text_scale = 2
)

def get_current_time():
    """
    The get_current_time() function gets the current time
    from a time API and returns the datetime.
    """
    try:
        current_time = matrixportal.fetch()
        print("Response is", current_time)
        last_check = time.monotonic()
    except (ValueError, RuntimeError) as e:
        print("Some error occurred, retrying! -", e)
    
    return current_time
    
def main() -> None:
    # The main() function runs the clock
    matrixportal.set_text("Go...")

    
    # Declaring constants
    SCROLL_DELAY = 0.03

    CONTENTS = [
        { 'text': 'Warning!',  'color': '#cf2727'},
        { 'text': 'Class is almost over!', 'color': '#0846e4'},
    ]
    
    PERIOD_END_TIMES = {
        "Period one": {
            "hour": 10,
            "minute": 4
        },
        "Period two": {
            "hour": 11,
            "minute": 24
        },
        "Period three": {
            "hour": 13,
            "minute": 29
        },
        "Period four": {
            "hour": 14,
            "minute": 49
        }
    }
    
    # Declare variables
    ticks = 0
    current_time = get_current_time()
    
    date_time = current_time.split("T")[1].split(":")
        
    hours = int(date_time[0])
    minutes = int(date_time[1])
    
    # Extract seconds and remove the fractional part if present
    seconds = int(date_time[2].split(".", 1)[0])  
    
    matrixportal.set_text("ICS3U")
    
    # This code will wait to display the clock until
    # the next minute passes
    slide = 60 - seconds 
    time.sleep(slide)
    minutes +=1
    
    while True:
        # This is the main loop
      
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
        
        # Loops through the period end time dictionary and 
        # checks if the current time equals the period end time
        # to display message
        for period, end_time in PERIOD_END_TIMES.items():
            if end_time["hour"] == hours and end_time["minute"] == minutes:
                for content in CONTENTS:
                    matrixportal.set_text_color("#000000") # clears background text
    
                    matrixportal.set_text(content['text'], 1)
                    matrixportal.set_text_color(content['color'], 1)
            
                    matrixportal.scroll_text(SCROLL_DELAY)
                    
        matrixportal.set_text_color(color_value)
        
        if ticks == 180:
            ticks = 0
            supervisor.reload()

    
        # Update minutes every minute
        minutes += 1
        ticks += 1
        time.sleep(59.7)
        

if __name__ == "__main__":
    main()
