import json


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


inputsequence = "1010"

automaton = Automaton("Samples/sample.json")
for input in inputsequence:
    print(automaton.step(input))