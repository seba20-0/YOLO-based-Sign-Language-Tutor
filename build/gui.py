from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from screeninfo import get_monitors  # Import screeninfo library
from pathlib import Path


# Get the primary monitor information
primary_monitor = get_monitors()[0]
screen_width = primary_monitor.width
screen_height = primary_monitor.height

def relative_to_assets(path: str) -> Path:
  return ASSETS_PATH / Path(path)


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\sebam\Documents\GitHub\YOLO-based-Sign-Language-Tutor\build\assets\frame0")


window = Tk()

# Set window size to 80% of screen dimensions (adjust as needed)
window.geometry(f"{int(screen_width * 1)}x{int(screen_height * 1)}")
window.configure(bg="#EAFAFF")


canvas = Canvas(
    window,
    bg="#EAFAFF",
    height=1024,
    width=1800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    1300.0,
    512.0,
    image=image_image_1
)

canvas.create_text(
    92.0,
    335.0,
    anchor="nw",
    text="HandsUp\nTutor",
    fill="#000000",
    font=("Inika", 130 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=105.0,
    y=719.0,
    width=269.0,
    height=73.0
)


window.resizable(False, False)
window.mainloop()