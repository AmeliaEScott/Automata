import tkinter as tk


class Gui:

    def __init__(self):

        self.frame = tk.Frame(tk.Tk())
        self.frame.pack()

        self.canvas = tk.Canvas(master=self.frame, bg="white", borderwidth=10, height=200, width=500)
        self.canvas.pack()
        self.polygon = self.canvas.create_polygon([30, 10, 30, 30, 10, 30, 40, 50, 80, 30, 50, 30, 50, 10], fill='red')

        self.quit_button = tk.Button(self.frame, text="Quit", command=self.quit)
        self.quit_button.pack(side=tk.RIGHT)

    def mainloop(self):
        self.frame.master.mainloop()
        self.frame.master.destroy()

    def quit(self):
        print("Quitting!")
        self.frame.quit()


Gui().mainloop()
