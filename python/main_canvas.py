import tkinter as tk

DEFAULT_FONT = "Meiryo"

DEFAULT_HEIGHT = 450
DEFAULT_WIDTH = 800

TITLE = "共ロボタイマー"

class KyoroboTimer:
    def __init__(self):
        print("start")
    def run(self):
        root = tk.Tk()
        root.title(TITLE)
        root.geometry("{}x{}".format(DEFAULT_WIDTH, DEFAULT_HEIGHT))
        root.resizable(width=False, height=False)
        root.option_add("*font", (DEFAULT_FONT, 14))

        canvas = tk.Canvas(root, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
        canvas.place(x=0, y=0)

        canvas.create_polygon(0, 0, 100, 0, 100, 100, fill="red")

        canvas.create_text(100, 50, text="Hello World", fill="blue", font=(DEFAULT_FONT, 24))

        root.mainloop()

if __name__ == "__main__":
    timer = KyoroboTimer()
    timer.run()