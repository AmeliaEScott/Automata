import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from automata import Automaton
import math
import re


class Gui:
    """
    This class is a work in progress. Any function that is not commented is only here for
    testing, and will be removed or changed eventually. (This includes the initializer)
    """

    def __init__(self, canvaswidth=700, canvasheight=400, automaton=None):

        self.canvaswidth = canvaswidth
        self.canvasheight = canvasheight
        self.automaton = automaton

        self.frame = tk.Frame(tk.Tk())
        self.frame.grid(row=0, column=0)
        # self.inputiter is an iterator that iterates over the "Test input" to the automaton.
        # For example, to test the input 'abcd', do iter('abcd')
        self.inputiter = None

        # If True, then stop auto-stepping through the automaton
        self.paused = False

        # Contains references to the circle for each state drawn on the canvas.
        # To change the configuration for a state (E.g., to turn red to be active), do this:
        # self.canvas.itemconfig(self.stateshapes[statename], fill='red')
        self.stateshapes = {}

        self.canvas = tk.Canvas(master=self.frame, bg="white", borderwidth=0,
                                height=self.canvasheight, width=self.canvaswidth)
        self.canvas.grid(row=0, column=0)

        if self.automaton is not None:
            self.drawautomaton(self.automaton)

        self.tabs = ttk.Notebook(self.frame)
        self.tabs.grid(row=1, column=0)

        ############ EDIT TAB ############

        self.edittab = tk.Frame(self.tabs)
        self.edittab.pack()
        tk.Label(self.edittab, text="State name:").grid(row=0, column=0, sticky=tk.E)
        self.stateNameEntry = tk.Entry(self.edittab)
        self.stateNameEntry.grid(row=0, column=1)
        tk.Button(self.edittab, text="Add State",
                  command=self.addstatecallback).grid(row=0, column=2, sticky=tk.EW)
        tk.Button(self.edittab, text="Remove State",
                  command=self.removestatecallback).grid(row=0, column=3, sticky=tk.EW)
        self.start = tk.IntVar()
        tk.Checkbutton(self.edittab, text="Start", var=self.start).grid(row=0, column=4)
        self.finish = tk.IntVar()
        tk.Checkbutton(self.edittab, text="Final", var=self.finish).grid(row=0, column=5)
        ttk.Separator(self.edittab, orient=tk.HORIZONTAL).grid(row=1, columnspan=5, sticky=tk.EW, pady=10)
        tk.Label(self.edittab, text="From:").grid(row=2, column=0, sticky=tk.E)
        self.fromEntry = tk.Entry(self.edittab)
        self.fromEntry.grid(row=2, column=1)
        tk.Label(self.edittab, text="To:").grid(row=3, column=0, sticky=tk.E)
        self.toEntry = tk.Entry(self.edittab)
        self.toEntry.grid(row=3, column=1)
        tk.Label(self.edittab, text="Inputs:").grid(row=4, column=0, sticky=tk.E)
        self.inputsEntry = tk.Entry(self.edittab)
        self.inputsEntry.grid(row=4, column=1)
        tk.Button(self.edittab, text="Add State Transition",
                  command=self.addtransitioncallback).grid(row=2, column=2, rowspan=3, sticky=tk.EW)
        tk.Button(self.edittab, text="Remove State Transition",
                  command=self.removetransitioncallback).grid(row=2, column=3, rowspan=3, sticky=tk.EW)
        ttk.Separator(self.edittab, orient=tk.HORIZONTAL).grid(row=5, columnspan=5, sticky=tk.EW, pady=10)
        tk.Button(self.edittab, text="Redraw",
                  command=self.redrawcallback).grid(row=6, column=0)

        self.quit_button = tk.Button(self.edittab, text="Quit", command=self.quit)
        self.load_button = tk.Button(self.edittab, text="Load", command=self.load)
        self.save_button = tk.Button(self.edittab, text="Save", command=self.save)
        self.quit_button.grid(row=6, column=1,sticky = tk.EW)
        self.load_button.grid(row=6, column=2,sticky = tk.EW)
        self.save_button.grid(row=6, column=3,sticky = tk.EW)

        ############ PLAY TAB ############

        self.playtab = tk.Frame(self.tabs)
        self.playtab.pack()
        tk.Label(self.playtab, text="Test Input:").grid(row=0, column=0, sticky=tk.E)
        self.testEntry = tk.Entry(self.playtab)
        self.testEntry.grid(row=0, column=1)
        self.testEntry.bind("<Key>", self.inputkeycallback)
        tk.Button(self.playtab, text="Play", command=self.runcallback).grid(row=1, column=0, sticky=tk.E)
        tk.Button(self.playtab, text="Pause", command=self.pausecallback).grid(row=1, column=1, sticky=tk.W)
        tk.Button(self.playtab, text="One Step", command=self.stepcallback).grid(row=1, column=1, sticky=tk.E)
        tk.Button(self.playtab, text="Restart", command=self.restartcallback).grid(row=1, column=2, sticky=tk.W)
        self.listentokeyboard = tk.IntVar()
        tk.Checkbutton(self.playtab, text="Listen to Keyboard", var=self.listentokeyboard).grid(row=1, column=3)
        self.s = tk.Scale(self.playtab, orient=tk.HORIZONTAL)
        tk.Label(self.playtab, text="Speed:").grid(row=2, column=0, sticky=tk.S)
        self.s.grid(row=2, column=1, sticky=tk.W)

        tk.Label(self.playtab, text="Current:").grid(row=3, column=0, sticky=tk.W)
        self.currentChar = tk.Label(self.playtab, text="0")
        self.currentChar.grid(row=3, column=1, sticky=tk.W)

        self.quit_button = tk.Button(self.playtab, text="Quit", command=self.quit)
        self.load_button = tk.Button(self.playtab, text="Load", command=self.load)
        self.save_button = tk.Button(self.playtab, text="Save", command=self.save)
        self.quit_button.grid(row=4, column=1, sticky=tk.EW)
        self.load_button.grid(row=4, column=2, sticky=tk.EW)
        self.save_button.grid(row=4, column=3, sticky=tk.EW)
        # End of tabs
        self.tabs.add(self.edittab, text="Edit Tab")
        self.tabs.add(self.playtab, text="Play Tab")



    def mainloop(self):
        self.frame.master.mainloop()
        self.frame.master.destroy()

    def quit(self):
        print("Quitting!")
        self.frame.quit()

    def save(self):
        f = filedialog.asksaveasfile('w',filetypes=(("JSON file", "*.json"),("All files", "*.*")))
        f.write(self.automaton.getJSON())
        f.close()

    def load(self):
        fname = filedialog.askopenfilename(filetypes=(("JSON file", "*.json"),("All files", "*.*")))
        self.automaton = Automaton(str(fname))
        self.redrawcallback()

    def addstatecallback(self):
        statename = self.stateNameEntry.get()
        self.automaton.addstate(statename)
        self.redrawcallback()

    def removestatecallback(self):
        statename = self.stateNameEntry.get()
        self.automaton.removestate(statename)
        self.redrawcallback()

    def addtransitioncallback(self):
        fromstate = self.fromEntry.get()
        tostate = self.toEntry.get()
        inputs = re.split("\s*,\s*", self.inputsEntry.get())
        self.automaton.addtransition(fromstate, tostate, inputs)
        self.redrawcallback()

    def removetransitioncallback(self):
        fromstate = self.fromEntry.get()
        tostate = self.toEntry.get()
        inputs = re.split("\s*,\s*", self.inputsEntry.get())
        self.automaton.deletetransition(fromstate, tostate, inputs)
        self.redrawcallback()

    def redrawcallback(self):
        self.canvas.delete(tk.ALL)
        self.drawautomaton(self.automaton)

    def runcallback(self):
        """
        Runs through the current test string
        """
        self.paused = False
        self.step(continuous=True)

    def pausecallback(self):
        self.paused = True

    def stepcallback(self):
        # This has to temporarily unpause, because self.step will do nothing if it is paused.
        self.paused = False
        self.step(self.automaton.currentstate)
        self.paused = True

    def inputkeycallback(self, event):
        if self.listentokeyboard.get() == 1 and event.char.isprintable():
            self.inputiter = iter(event.char)
            self.paused = False
            self.step()
            self.paused = True

    def restartcallback(self):
        self.paused = True
        self.inputiter = None
        self.setactivestate([])

    def step(self, continuous=False):
        """
        Steps the automaton based on the input.
        :param continuous: If True, then this function sets a callback to call this function again after a delay,
            and continues to do so until either it runs out of input, or it is paused. (self.paused = True)
        """
        if not self.paused:
            if self.inputiter is None:
                self.inputiter = iter(self.testEntry.get())
                self.automaton.start()
            try:
                nextInput = next(self.inputiter)
                self.currentChar.config(text=nextInput)
                self.automaton.step(nextInput)
                self.setactivestate(self.automaton.currentstate)
                if continuous:
                    self.frame.after(100*(100-self.s.get())+100, self.step, True)
            except StopIteration:
                self.inputiter = None
                self.paused = True
                # If we are done iterating, then turn off all the active states.
                self.setactivestate(set())

    def setactivestate(self, states):
        """
        Visually changes the specified states to be activated.
        :param states: An iterable of state names. (E.g., {'A', 'B'} )
        :return: None
        """
        print("Setting active state: {}".format(states))
        # First, deactivate all the states...
        for shape in self.stateshapes.values():
            self.canvas.itemconfig(shape, fill="white")
        # Then activate the new ones
        for state in states:
            self.canvas.itemconfig(self.stateshapes[state], fill="red")

    def drawautomaton(self, automaton: Automaton, border=50, arcangle=0.7, stateradius=30, layout=None):
        """
        Draws the provided automaton on the canvas.
        :param automaton: Automaton to be drawn
        :param border: Amount of empty space to be left around the edges of the canvas
        :param arcangle: Angle of arcs between states, in radians. (Bigger angle = more curve)
        :param stateradius: Radius of circles representing states, in pixels.
        :param layout: Layout to use. If None, then automaton.layout() is used.
        :return: None
        """
        border += stateradius
        if layout is None:
            layout = automaton.layout()
        minx = min(i[0] for i in layout.values())
        miny = min(i[1] for i in layout.values())
        maxx = max(i[0] for i in layout.values())
        maxy = max(i[1] for i in layout.values())

        def scale(coords):
            x = (coords[0] - minx) * (self.canvaswidth - (2 * border)) / (maxx - minx) + border
            y = (coords[1] - miny) * (self.canvasheight - (2 * border)) / (maxy - miny) + border
            return x, y

        for state_a in automaton.states:
            for state_b in automaton.states[state_a]:
                transition = automaton.states[state_a][state_b]
                label = ", ".join(transition)
                if state_a == state_b:
                    x, y = scale(layout[state_a])
                    self.canvas.create_oval([x - 1.5 * stateradius, y - 0.5 * stateradius, x, y + 0.5 * stateradius],
                                            width=3, outline="red")
                    self.canvas.create_text([x - 2 * stateradius, y], text=label, fill="black")
                    print("Arcing to self: {}".format(state_a))
                else:
                    self.drawarc(scale(layout[state_a]), scale(layout[state_b]), label=label,
                                 theta=arcangle)

        for state in layout:
            coords = scale(layout[state])
            if state is automaton.startstate:
                self.drawrect(coords, state)
            else:
                self.drawstate(coords, state, final=state in automaton.finalstates)

    def drawstate(self, coords, label, radius=30, final=False):
        """
        Draws a single state on the canvas, including its label.
        :param coords: Coordinates on the canvas at which to draw the state.
        :param label: Label or name of the state.
        :param radius: Radius in pixels of the circle representing the state
        :param final: If True, this state will be rendered as a final state (with double outline)
        :return: None
        """
        self.stateshapes[label] = self.canvas.create_oval([coords[0] - radius, coords[1] - radius,
                                                           coords[0] + radius, coords[1] + radius],
                                                          fill="white", outline="black", width=5)
        if final:
            self.canvas.create_oval([coords[0] - radius + 10, coords[1] - radius + 10,
                                     coords[0] + radius - 10, coords[1] + radius - 10],
                                    fill="white", outline="black", width=5)
        self.canvas.create_text(coords, text=label, fill="black")

    def drawrect(self, coords, label, radius=30):
        """
        Draws a single state on the canvas but a rectange, including its label.
        :param coords: Coordinates on the canvas at which to draw the state.
        :param label: Label or name of the state.
        :param radius: Radius in pixels of the circle representing the state
        :return: None
        """
        self.stateshapes[label] = self.canvas.create_rectangle([coords[0] - radius, coords[1] - radius,
                                                           coords[0] + radius, coords[1] + radius],
                                                          fill="white", outline="black", width=5)
        self.canvas.create_text(coords, text=label, fill="black")

    def drawarc(self, a, b, label, theta=0.5, labeloffset=-10, stateradius=30, arrowangle=0.4, arrowlength=25):
        """
        Draws an arc between two points (to represent a state transition)
        :param a: First point, as a 2-tuple
        :param b: Second point, as a 2-tuple
        :param label: Label of this transition
        :param theta: Angle of the arc
        :param labeloffset: Number of pixels away from the arc that the label should be placed
        :param stateradius: Radius of the states, in pixels, in order to properly draw arrow
        :param arrowangle: Angle of the arrow in radians. (Bigger angle = fatter arrow)
        :param arrowlength: Length of arrow, in pixels
        :return: None
        """
        # TODO: Deal with arcs that start and end at same state
        d = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5            # Distance between A and B
        r = d / (2 * math.sin(theta / 2))
        try:
            tanphi = (a[1] - b[1]) / (a[0] - b[0])
        except ZeroDivisionError:
            tanphi = 1 / 0.000000001
        theta_a = (math.pi / 2) - (theta / 2) - math.atan(tanphi)       # Angle between vector CA and x-axis
        if b[0] > a[0]:
            theta_a -= math.pi
        cx = a[0] - (r * math.cos(theta_a))
        cy = a[1] + (r * math.sin(theta_a))

        theta_a_degrees = theta_a * (180 / math.pi)
        theta_degrees = theta * (180 / math.pi)

        label_dx = (r + labeloffset) * math.cos(theta_a + theta * 0.55)  # Offset from center to place label
        label_dy = (r + labeloffset) * math.sin(theta_a + theta * 0.55)

        phi = 2 * math.asin(stateradius / (2 * r))
        arrowpoint_x = cx + (r * math.cos(theta_a + theta - phi))
        arrowpoint_y = cy - (r * math.sin(theta_a + theta - phi))

        arrow_x1 = arrowpoint_x + (arrowlength * math.cos(theta_a + theta - (math.pi / 2) - arrowangle))
        arrow_y1 = arrowpoint_y - (arrowlength * math.sin(theta_a + theta - (math.pi / 2) - arrowangle))

        arrow_x2 = arrowpoint_x + (arrowlength * math.cos(theta_a + theta - (math.pi / 2) + arrowangle))
        arrow_y2 = arrowpoint_y - (arrowlength * math.sin(theta_a + theta - (math.pi / 2) + arrowangle))

        self.canvas.create_arc([cx - r, cy - r, cx + r, cy + r], start=theta_a_degrees, extent=theta_degrees,
                               outline="red", style=tk.ARC, width=3)
        self.canvas.create_polygon([arrowpoint_x, arrowpoint_y, arrow_x1, arrow_y1, arrow_x2, arrow_y2], fill="red")
        self.canvas.create_text([cx + label_dx, cy - label_dy], text=label, fill="black")


if __name__ == "__main__":

    testautomaton = Automaton("Samples/sample2.json")
    testgui = Gui(automaton=testautomaton)
    # This code will no longer run, but hopefully it is at least a good reference.
    # testgui.drawautomaton(testautomaton, arcangle=0.5)
    # layout = testautomaton.layout(alignment=1.0, separation=1.2, steps=500, maxspeed=0.01, speed=5.0, generate=True)
    #
    # def test():
    #     global testgui
    #     global testautomaton
    #     global layout
    #     try:
    #         newlayout = layout.__next__()
    #         testgui.canvas.delete(tk.ALL)
    #         testgui.drawautomaton(testautomaton, layout=newlayout)
    #         # After 20 milliseconds, run the function test.
    #         # Any TK GUI element has this "after" function, and it doesn't seem important which object you use.
    #         # So I just use the frame, which encloses the entire window.
    #         testgui.frame.after(20, test)
    #     except StopIteration:
    #         pass
    #
    # test()
    testgui.mainloop()
