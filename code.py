
import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal

def main() -> None:

    matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=True)

    matrixportal.add_text(
        text_font=terminalio.FONT,
        text_position=(3, (matrixportal.graphics.display.height // 2) - 1),
        scrolling=False,
        text_scale = 2
    )

    color_index = random.randint(0, len(colors) - 1)

    color_name = list(colors.keys())[color_index]
    color_value = colors[color_name]




    minutes = 40
    hours = 3
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
