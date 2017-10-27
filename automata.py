import json
import random
import itertools
import math
import sys
import os


class Automaton:

    def __init__(self, filepath):
        """
        :param filepath: Path to the file containing the specification for this automaton
        """
        if getattr(sys, "frozen", False):
            # The application is frozen.
            datadir = os.path.dirname(sys.executable)
        else:
            # The application is not frozen.
            datadir = os.path.dirname(__file__)
        filepath = os.path.join(datadir, filepath)

        with open(filepath) as file:
            data = json.load(file)
        self.name = data["name"]
        self.description = data["description"]

        states = data["transitions"]
        # Clean up the states from the file.
        for state in states:
            for otherstate in states[state]:
                try:
                    # Just make sure everything is stored as a string, no numbers
                    states[state][otherstate] = list(map(lambda x: str(x), states[state][otherstate]))
                except TypeError:
                    # If the connection was stored as a single value instead of an array, then change it to
                    # be an array of length 1
                    states[state][otherstate] = [str(states[state][otherstate])]

        # self.states contains the information about connections between states.
        # If you are currently in state A, and receive an input x, then to check if there is a transition
        # to state B, check if x in self.states["A"]["B"]
        self.states = states

        finalstates = data["finalstates"]
        try:
            iter(finalstates)
        except TypeError:
            # If finalstates is not a list, make it a list
            finalstates = [finalstates]
        self.finalstates = finalstates

        self.startstate = data["start"]

        self.currentstate = {self.startstate}

    def start(self):
        self.currentstate = {self.startstate}

    def getnextstate(self, nextinput):
        """
        Returns the next state without actually advancing the automaton
        :param nextinput: The next input to the automaton, as a string
        :return: A set of states to which the automaton will advance on this input.
                If this automaton is deterministic, then this set will always be of length 0 or 1.
                For nondeterministic automata, this set can be of any length.
        """

        nextstate = set()
        for currentstate in self.currentstate:
            currentstate = self.states[currentstate]
            for potentialnextstate in currentstate:
                if nextinput in currentstate[potentialnextstate]:
                    nextstate.add(potentialnextstate)
        return nextstate

    def step(self, nextinput):
        """
        Advances this automaton to the next state
        :param nextinput: Next input to this automaton.
        :return: The next state(s) to which this automaton has advanced, as a set.
                Possibly the empty set if there are no states to which this automaton can advance with this input.
        """
        self.currentstate = self.getnextstate(nextinput)
        return self.currentstate

    def addstate(self, statename):
        if statename not in self.states:
            self.states[statename] = {}

    def removestate(self, statename):
        if statename in self.states:
            del self.states[statename]
        for otherstate in self.states.values():
            if statename in otherstate:
                del otherstate[statename]

    def addtransition(self, fromstate, tostate, inputs):
        try:
            inputs = list(inputs)
        except TypeError:
            inputs = [inputs]

        if fromstate in self.states:
            if tostate in self.states[fromstate]:
                self.states[fromstate][tostate] += inputs
            else:
                self.states[fromstate][tostate] = inputs

    def deletetransition(self, fromstate, tostate, inputs):
        try:
            inputs = list(inputs)
        except TypeError:
            inputs = [inputs]

        if fromstate in self.states and tostate in self.states[fromstate]:
            for input in inputs:
                self.states[fromstate][tostate].remove(input)
            if len(self.states[fromstate][tostate]) == 0:
                del self.states[fromstate][tostate]

    def layout(self, alignment=1.0, separation=1.2, steps=500, maxspeed=0.2, speed=math.e) -> dict:
        """
        Lays out the states to try and minimize overlap between states and transitions.
        This is accomplished by treating each connection between states as a spring of a certain length,
        which pushes and pulls states.
        :param alignment: Length of springs between states with transitions between them.
        :param separation: Length of springs between states without any transition between them.
        :param steps: Number of steps for which to run the simulation
        :param maxspeed: Maximum "speed" for states to be moved around during simulation.
        :param speed: A constant that just needs to be arbitrarily tweaked.
        :return: A dictionary where each state in this automaton is a key, the value for which is a 2-tuple
                    representing the coordinates of the state after the layout is complete.
        """
        # TODO: Run multiple simulations, and determine which one has the least overlap.

        # Calculates the distance between two 2-tuples
        def dist(p1, p2):
            return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

        # Initialize the location of every state to a random point in the range (-1, 1)
        result = {state: ((random.random() - 0.5) * 2, (random.random() - 0.5) * 2) for state in self.states}
        for i in range(steps):
            # Stores up the cumulative displacement on each state. Starts out at zero.
            displacements = {state: [0, 0] for state in result}
            # The following loop iterates over every pair of states that are are not the same
            for state, otherstate in filter(lambda x: x[0] != x[1], itertools.product(result.keys(), result.keys())):
                distance = dist(result[state], result[otherstate])
                if otherstate in self.states[state]:  # If these states are connected:
                    force = distance - alignment
                else:  # If they are not connected:
                    # The "min(..., 0)" ensure that if the states are already far enough apart, then
                    # no more force is exerted.
                    force = min(distance - separation, 0)
                alpha = -speed ** (-abs(force) + math.log(maxspeed, speed)) + maxspeed
                if force < 0:
                    alpha = -alpha
                # Do not yet move the state, just add the displacement to what's already there. This way,
                # for states that have multiple connections, they move based on the total net displacement
                # after all forces are calculated.
                displacements[otherstate][0] += (alpha / distance) * (result[state][0] - result[otherstate][0])
                displacements[otherstate][1] += (alpha / distance) * (result[state][1] - result[otherstate][1])
            # Here is where the forces are actually exerted.
            nextresult = {state: (result[state][0] + displacements[state][0],
                                  result[state][1] + displacements[state][1]) for state in result}
            # (This has to be two steps because you can't modify a data structure while iterating over it)
            result = nextresult
        return result


if __name__ == "__main__":

    inputsequence = "ababa"
    # inputsequence = map(lambda x: random.choice(["1", "0"]), range(1, 200))

    automaton = Automaton("Samples/sample2.json")
    for character in inputsequence:
        print(automaton.step(character))
    layout = automaton.layout(steps=1000, separation=1.0, maxspeed=0.1)
    states = sorted(layout.keys())
    x = [layout[state][0] for state in states]
    y = [layout[state][1] for state in states]
