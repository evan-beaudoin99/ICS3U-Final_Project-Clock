
import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal

# --- Display setup ---
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=True)

# Create a new label with the color and text selected
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(3, (matrixportal.graphics.display.height // 2) - 1),
    scrolling=False,
    text_scale = 2
)


seconds = 0
minutes = 30
hours = 8

while True:
    matrixportal.set_text(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    # matrixportal.set_text_color(content['color'])
    seconds += 1
    if seconds == 60:
        minutes += 1
        seconds = 0

    if minutes == 60:
        hours = 1
        minutes = 0

    time.sleep(1)
