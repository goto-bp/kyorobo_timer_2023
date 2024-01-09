import tkinter as tk
# import pyaudio
# import winsound

DEFAULT_FONT = "Meiryo"

DEFAULT_HEIGHT = 450
DEFAULT_WIDTH = 800

TITLE = "共ロボタイマー"

class KyoroboTimer: 
    # __point_font_size = 2.7
    # __time_font_size = 15
    # __name_font_size = 2.1

    __point_font_size = 3.1
    __time_font_size = 19
    __name_font_size = 2.5

    __point = 5

    __min = 0
    __sec = 10
    __time = __min * 60 + __sec

    __left_team_name = "大分A"
    __right_team_name = "八代B"

    def __init__(self, resolution, font, title):
        self.__resolution = resolution
        self.__font = font
        self.__title = title

        self.root = tk.Tk()
        self.root.title(self.__title)
        self.root.geometry(f"{self.__resolution[0]}x{self.__resolution[1]}")

        self.timer_screen = tk.Frame(self.root,
                                    bg="#222222")
        self.timer_screen.pack(fill=tk.BOTH,
                            expand=True)

        self.left_team_point = tk.Frame(self.timer_screen,
                                        bg="red")
        
        self.right_team_point = tk.Frame(self.timer_screen,
                                        bg="blue")
        
        self.left_team_name = tk.Frame(self.timer_screen,
                                        bg="black")
        
        self.right_team_name = tk.Frame(self.timer_screen,
                                        bg="black")
        
        self.time_label = tk.Frame(self.timer_screen,
                            bg="#222222")
        
        self.left_team_point_label = tk.Label(self.left_team_point,
                                            text="0",
                                            font=(self.__font, 0),
                                            fg="white",
                                            bg=self.left_team_point.cget("bg"))
        
        self.right_team_point_label = tk.Label(self.right_team_point,
                                            text="0",
                                            font=(self.__font, 0),
                                            fg="white",
                                            bg=self.right_team_point.cget("bg"))
        
        self.left_team_name_label = tk.Label(self.left_team_name,
                                            text=self.__left_team_name,
                                            font=self.__font,
                                            fg="white",
                                            bg=self.left_team_name.cget("bg"))
        
        self.right_team_name_label = tk.Label(self.right_team_name,
                                            text=self.__right_team_name,
                                            font=self.__font,
                                            fg="white",
                                            bg=self.right_team_name.cget("bg"))
        
        self.time_label_label = tk.Label(self.time_label,
                                            text=str(self.__min) + ":" + str(self.__sec).zfill(2),
                                            font=self.__font,
                                            fg="white",
                                            bg=self.time_label.cget("bg"))

    def count_down(self):
        if(self.__time > 0):
            self.__time -= 1
            self.__min = self.__time // 60
            self.__sec = self.__time % 60

        self.time_label_label.config(text=str(self.__min) + ":" + str(self.__sec).zfill(2))

        if(self.__time == 0):
            self.time_label_label.config(fg="red")

        if(self.__time > 0):
            self.root.after(1000, self.count_down)

    def count_up(self):
        self__time += 1

        self.time_label_label.config(text=str(self.__min) + ":" + str(self.__sec).zfill(2))

        self.root.after(1000, self.count_up)

    def on_resize(self, e):
        def update_size(): #FONT ANTIALIASING
            print(f"resize {self.root.winfo_width()}x{self.root.winfo_height()}")

            self.left_team_point_label.config(
                    font=(self.__font, int(self.root.winfo_height() / self.__point_font_size)))
            self.right_team_point_label.config(
                    font=(self.__font, int(self.root.winfo_height() / self.__point_font_size)))
            self.left_team_name_label.config(
                    font=(self.__font, int(self.root.winfo_height() / self.__time_font_size)))
            self.right_team_name_label.config(
                    font=(self.__font, int(self.root.winfo_height() / self.__time_font_size)))
            self.time_label_label.config(
                    font=(self.__font, int(self.root.winfo_height() / self.__name_font_size)))
            

        self.root.after_idle(update_size)

    def key_event(self, e):
        print(e.keysym)
        if(e.keysym == "Escape"):
            self.root.destroy()  

        if(e.keysym == "F11"):
            self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

        if(e.keysym == "r"):
            if(self.timer_screen.winfo_ismapped()):
                self.timer_screen.pack_forget()
            else:
                self.timer_screen.pack(fill=tk.BOTH,
                               expand=True)

        if(e.keysym == "w"):
            self.left_team_point_label.config(text=str(int(self.left_team_point_label.cget("text")) + 1))
        if(e.keysym == "s"):
            if(int(self.left_team_point_label.cget("text")) > 0):
                self.left_team_point_label.config(text=str(int(self.left_team_point_label.cget("text")) - 1))
        if(e.keysym == "d"):
            self.left_team_point_label.config(text=str(int(self.left_team_point_label.cget("text")) + self.__point))
        if(e.keysym == "a"):
            if(int(self.left_team_point_label.cget("text")) - self.__point < 0):
                self.left_team_point_label.config(text="0")
            else:
                self.left_team_point_label.config(text=str(int(self.left_team_point_label.cget("text")) - self.__point))
            
        
        if(e.keysym == "Up"):
            self.right_team_point_label.config(text=str(int(self.right_team_point_label.cget("text")) + 1))
        if(e.keysym == "Down"):
            if(int(self.right_team_point_label.cget("text")) > 0):
                self.right_team_point_label.config(text=str(int(self.right_team_point_label.cget("text")) - 1))
        if(e.keysym == "Right"):
            self.right_team_point_label.config(text=str(int(self.right_team_point_label.cget("text")) + self.__point))
        if(e.keysym == "Left"):
            if(int(self.right_team_point_label.cget("text")) - self.__point < 0):
                self.right_team_point_label.config(text="0")
            else:
                self.right_team_point_label.config(text=str(int(self.right_team_point_label.cget("text")) - self.__point))

    def run(self):


        self.left_team_point.grid(row=0, column=0,
                            sticky=tk.NSEW)

        self.right_team_point.grid(row=0, column=1,
                            sticky=tk.NSEW)

        self.left_team_name.grid(row=1, column=0,
                            sticky=tk.NSEW)

        self.right_team_name.grid(row=1, column=1,
                            sticky=tk.NSEW)


        self.time_label.grid(row=2, column=0,
                    columnspan=2,
                    sticky=tk.NSEW)
        

        self.left_team_point_label.place(relx=0.5, rely=0.5,
                                         anchor=tk.CENTER)
        
        self.right_team_point_label.place(relx=0.5, rely=0.5,
                                            anchor=tk.CENTER)
        
        self.left_team_name_label.place(relx=0.5, rely=0.5,
                                            anchor=tk.CENTER)
        
        self.right_team_name_label.place(relx=0.5, rely=0.5,
                                            anchor=tk.CENTER)
        
        self.time_label_label.place(relx=0.5, rely=0.5,
                                        anchor=tk.CENTER)
                                        

        self.timer_screen.grid_columnconfigure(0, weight=1)
        self.timer_screen.grid_columnconfigure(1, weight=1)

        self.timer_screen.grid_rowconfigure(0, weight=4)
        self.timer_screen.grid_rowconfigure(1, weight=1)
        self.timer_screen.grid_rowconfigure(2, weight=5)

        self.root.bind("<KeyPress>", self.key_event)

        self.root.bind("<Configure>", self.on_resize)

        self.root.after(1000, self.count_down)

        self.root.mainloop()

if __name__ == "__main__":
    timer = KyoroboTimer((DEFAULT_WIDTH, DEFAULT_HEIGHT), DEFAULT_FONT, TITLE)
    timer.run()
