import tkinter as tk
from automata import Automaton
import math


class Gui:
    """
    This class is a work in progress. Any function that is not commented is only here for
    testing, and will be removed or changed eventually. (This includes the initializer)
    """

    def __init__(self, canvaswidth=700, canvasheight=700):

        self.canvaswidth = canvaswidth
        self.canvasheight = canvasheight

        self.frame = tk.Frame(tk.Tk())
        self.frame.pack()

        self.canvas = tk.Canvas(master=self.frame, bg="white", borderwidth=0,
                                height=self.canvasheight, width=self.canvaswidth)
        self.canvas.pack()
        # self.arc = self.canvas.create_arc([20, 20, 120, 120], outline="red", start=0, extent=180, style=tk.ARC)

        # self.canvas.create_text([100, 600], text="(1, 6)", fill="green")
        # self.canvas.create_text([100, 100], text="(1, 1)", fill="green")
        # self.canvas.create_text([600, 100], text="(6, 1)", fill="green")

        self.quit_button = tk.Button(self.frame, text="Quit", command=self.quit)
        self.quit_button.pack(side=tk.RIGHT)

    def mainloop(self):
        self.frame.master.mainloop()
        self.frame.master.destroy()

    def quit(self):
        print("Quitting!")
        self.frame.quit()

    def drawautomaton(self, automaton: Automaton, border=200, arcangle=0.5, stateradius=20, layout=None):
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

        for state in layout:
            coords = scale(layout[state])
            self.drawstate(coords, state)

        for state_a in automaton.states:
            for state_b in automaton.states[state_a]:
                # TODO: Add the appropriate label
                self.drawarc(scale(layout[state_a]), scale(layout[state_b]), label=state_a + state_b,
                             theta=arcangle)

    def drawstate(self, coords, label, radius=20, statecolor="red", textcolor="black"):
        """
        Draws a single state on the canvas, including its label.
        :param coords: Coordinates on the canvas at which to draw the state.
        :param label: Label or name of the state.
        :param radius: Radius in pixels of the circle representing the state
        :param statecolor: Color of the state (any valid Tk color).
        :param textcolor: Color of the text label (any valid Tk color).
        :return: None
        """
        self.canvas.create_oval([coords[0] - radius, coords[1] - radius,
                                coords[0] + radius, coords[1] + radius], fill=statecolor)
        self.canvas.create_text(coords, text=label, fill=textcolor)

    def drawarc(self, a, b, label, theta=0.5, labeloffset=10):
        """
        Draws an arc between two points (to represent a state transition)
        :param a: First point, as a 2-tuple
        :param b: Second point, as a 2-tuple
        :param label: Label of this transition
        :param theta: Angle of the arc
        :param labeloffset: Number of pixels away from the arc that the label should be placed
        :return: None
        """
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

        label_dx = (r + labeloffset) * math.cos(theta_a + theta / 2)
        label_dy = (r + labeloffset) * math.sin(theta_a + theta / 2)

        self.canvas.create_text([cx + label_dx, cy - label_dy], text=label, fill="blue")
        self.canvas.create_arc([cx - r, cy - r, cx + r, cy + r], start=theta_a_degrees, extent=theta_degrees,
                               outline="red", style=tk.ARC)


if __name__ == "__main__":

    testgui = Gui()
    testautomaton = Automaton("Samples/sample4.json")
    # testgui.drawautomaton(testautomaton, arcangle=0.5)
    layout = testautomaton.layout(alignment=1.0, separation=1.2, steps=500, maxspeed=0.01, speed=5.0, generate=True)

    def test():
        global testgui
        global testautomaton
        global layout
        try:
            newlayout = layout.__next__()
            testgui.canvas.delete(tk.ALL)
            testgui.drawautomaton(testautomaton, layout=newlayout)
            testgui.frame.after(50, test)
        except StopIteration:
            pass

    test()
    testgui.mainloop()
