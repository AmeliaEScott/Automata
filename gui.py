import tkinter as tk


class Gui:

    def __init__(self):

        self.frame = tk.Frame(tk.Tk())
        self.frame.pack()

        self.canvas = tk.Canvas(master=self.frame, bg="black", borderwidth=10, height=200, width=500)
        self.canvas.pack()
        self.arc = self.canvas.create_arc([20, 20, 120, 120], outline="red", start=0, extent=180, style=tk.ARC)

        self.quit_button = tk.Button(self.frame, text="Quit", command=self.quit)
        self.quit_button.pack(side=tk.RIGHT)

    def mainloop(self):
        self.frame.master.mainloop()
        self.frame.master.destroy()

    def quit(self):
        print("Quitting!")
        self.frame.quit()


Gui().mainloop()
