import json
import random
import itertools
import matplotlib.pyplot

class Automaton:

    def __init__(self, filepath):
        """
        :param filepath: Path to the file containing the specification for this automaton
        """
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

    def layout(self, alignment=0.2, separation=0.5, steps=100, speed=0.01):
        result = {}

        def dist(p1, p2):
            return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

        def mix(p1, p2, weight):
            return (1.0 - weight) * p1[0] + weight * p2[0], (1.0 - weight) * p1[1] + weight * p2[1]
        for state in self.states:
            result[state] = ((random.random() - 0.5) * 2, (random.random() - 0.5) * 2)
        for i in range(steps):
            nextresult = result.copy()
            # The following loop iterates over every pair of states that are are not the same
            # and are connected by a transition.
            for state, otherstate in filter(lambda x: x[0] != x[1], itertools.product(result.keys(), result.keys())):
                if otherstate in self.states[state] or state in self.states[otherstate]:
                    #print("States {} and {} are connected. ".format(state, otherstate), end="")
                    if dist(nextresult[state], nextresult[otherstate]) > alignment:
                        #print("Too far away! Moving closer.")
                        nextresult[state] = mix(nextresult[state], nextresult[otherstate], speed)
                        nextresult[otherstate] = mix(nextresult[otherstate], nextresult[state], speed)
                    else:
                        #print("Too close! Moving further away.")
                        nextresult[state] = mix(nextresult[state], nextresult[otherstate], -speed)
                        nextresult[otherstate] = mix(nextresult[otherstate], nextresult[state], -speed)
                elif dist(nextresult[state], nextresult[otherstate]) < separation:
                    #print("States {} and {} are NOT connected. Too close! Moving away.".format(state, otherstate))
                    nextresult[state] = mix(nextresult[state], nextresult[otherstate], -speed)
                    nextresult[otherstate] = mix(nextresult[otherstate], nextresult[state], -speed)
                else:
                    pass
                    #print("States {} and {} are NOT connected. Far enough away, doing nothing.".format(state, otherstate))
            result = nextresult
        return result


inputsequence = "ababa"
#inputsequence = map(lambda x: random.choice(["1", "0"]), range(1, 200))

automaton = Automaton("Samples/sample2.json")
for input in inputsequence:
    print(automaton.step(input))
layout = automaton.layout(steps=1000, separation=1.0)
states = sorted(layout.keys())
x = [layout[state][0] for state in states]
y = [layout[state][1] for state in states]
matplotlib.pyplot.scatter(x, y, c=['red', 'orange', 'yellow', 'green', 'blue', 'purple'])
matplotlib.pyplot.show()
