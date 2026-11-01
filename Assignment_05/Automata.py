
class Automata:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def get_symbol(self, char):
        """
        Maps an input character to a symbol from the automaton's alphabet.
        """

        if char.isascii() and char.isalpha():
            return "letter"

        if char.isascii() and char.isdigit():
            if "digit" in self.alphabet:
                return "digit"

            if char == "0":
                return "zero"

            return "nonzero_digit"

        if char == "_":
            if "_" in self.alphabet:
                return "_"

            if "punctuation" in self.alphabet:
                return "punctuation"

        if char in " \t\r\n":
            return "whitespace"

        if char in '.,-()[]{}\'':
            return "punctuation"

        if char in r"/\:+=@#$%!?&*":
            return "special"

        if char == '"':
            return '"'

        return None

    def recognize(self, text):
        """
        Checks whether the entire text is accepted by the automaton.
        Returns True or False.
        """

        current_state = self.initial_state

        for char in text:
            symbol = self.get_symbol(char)

            if symbol not in self.alphabet:
                return False

            transition = (current_state, symbol)

            if transition not in self.transitions:
                return False

            current_state = self.transitions[transition]

        return current_state in self.final_states

    def recognize_prefix(self, source, start_position):
        """
        Reads characters from source, starting at start_position,
        and returns the longest accepted prefix.

        Returns:
            (recognized_token, next_position)

        If no valid token is found:
            (None, start_position)
        """

        current_state = self.initial_state
        position = start_position

        last_final_position = None

        while position < len(source):
            char = source[position]
            symbol = self.get_symbol(char)

            if symbol not in self.alphabet:
                break

            transition = (current_state, symbol)

            if transition not in self.transitions:
                break

            current_state = self.transitions[transition]
            position += 1

            if current_state in self.final_states:
                last_final_position = position

        if last_final_position is None:
            return None, start_position

        token = source[start_position:last_final_position]

        return token, last_final_position


# IDENTIFIER AUTOMATON
identifier_automaton = Automata(
    states=["q0", "q1"],
    alphabet=["letter", "digit", "_"],
    transitions={
        ("q0", "letter"): "q1",
        ("q1", "letter"): "q1",
        ("q1", "digit"): "q1",
        ("q1", "_"): "q1"
    },
    initial_state="q0",
    final_states=["q1"]
)


# INTEGER AUTOMATON
integer_automaton = Automata(
    states=["q0", "q1", "q2"],
    alphabet=["zero", "nonzero_digit"],
    transitions={
        ("q0", "zero"): "q1",
        ("q0", "nonzero_digit"): "q2",
        ("q2", "zero"): "q2",
        ("q2", "nonzero_digit"): "q2"
    },
    initial_state="q0",
    final_states=["q1", "q2"]
)


# STRING AUTOMATON
string_automaton = Automata(
    states=["q0", "q1", "q2"],
    alphabet=[
        '"',
        "letter",
        "digit",
        "whitespace",
        "punctuation",
        "special"
    ],
    transitions={
        ("q0", '"'): "q1",

        ("q1", "letter"): "q1",
        ("q1", "digit"): "q1",
        ("q1", "whitespace"): "q1",
        ("q1", "punctuation"): "q1",
        ("q1", "special"): "q1",

        ("q1", '"'): "q2"
    },
    initial_state="q0",
    final_states=["q2"]
)
