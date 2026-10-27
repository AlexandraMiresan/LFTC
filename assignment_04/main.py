
def fa_to_rg(states, alphabet, transitions,
             initial_state, final_states):
    """
    Convert a finite automaton into a regular grammar.

    Parameters:
        states: list of states
        alphabet: list of input symbols
        transitions: dictionary mapping (state, symbol)
                     to destination state
        initial_state: initial state
        final_states: list of accepting states

    Returns:
        A dictionary representing the regular grammar.
    """

    # 1. Validate the automaton

    if not states:
        raise ValueError("The automaton must have states.")

    if len(states) != len(set(states)):
        raise ValueError("States must be unique.")

    if len(alphabet) != len(set(alphabet)):
        raise ValueError("Alphabet symbols must be unique.")

    if initial_state not in states:
        raise ValueError("The initial state does not exist.")

    for state in final_states:
        if state not in states:
            raise ValueError(
                f"Final state '{state}' does not exist."
            )

    for (source, symbol), destination in transitions.items():

        if source not in states:
            raise ValueError(
                f"Unknown source state: {source}"
            )

        if destination not in states:
            raise ValueError(
                f"Unknown destination state: {destination}"
            )

        if symbol not in alphabet:
            raise ValueError(
                f"Symbol '{symbol}' is not in the alphabet."
            )

    # 2. Create one nonterminal per state

    grammar = {
        state: [] for state in states
    }

    # 3. Transform transitions into productions

    for (source, symbol), destination in transitions.items():

        production = f"{symbol} {destination}"

        grammar[source].append(production)

    # 4. Add epsilon productions to final states

    for state in final_states:
        grammar[state].append("ε")

    # 5. Return the resulting grammar

    return {
        "nonterminals": list(states),
        "terminals": list(alphabet),
        "start_symbol": initial_state,
        "productions": grammar
    }


def display_grammar(name, grammar):
    """Display the resulting regular grammar."""

    print("\n" + "=" * 55)
    print(name)
    print("=" * 55)

    print("\nNonterminals (V):")
    print(grammar["nonterminals"])

    print("\nTerminals (T):")
    print(grammar["terminals"])

    print("\nStart symbol (S):")
    print(grammar["start_symbol"])

    print("\nProduction rules (P):")

    for state, productions in grammar["productions"].items():

        if productions:
            alternatives = " | ".join(productions)
            print(f"{state} -> {alternatives}")

# AUTOMATON 1: IDENTIFIERS

identifier_states = ["q0", "q1"]

identifier_alphabet = [
    "letter",
    "digit",
    "_"
]

identifier_transitions = {
    ("q0", "letter"): "q1",

    ("q1", "letter"): "q1",
    ("q1", "digit"): "q1",
    ("q1", "_"): "q1"
}

identifier_initial = "q0"

identifier_finals = ["q1"]

# AUTOMATON 2: INTEGER CONSTANTS

integer_states = ["q0", "q1"]

integer_alphabet = [
    "digit"
]

integer_transitions = {
    ("q0", "digit"): "q1",
    ("q1", "digit"): "q1"
}

integer_initial = "q0"

integer_finals = ["q1"]


# AUTOMATON 3: STRING CONSTANTS

string_states = ["q0", "q1", "q2"]

string_alphabet = [
    '"',
    "letter",
    "digit",
    "whitespace",
    "punctuation",
    "special"
]

string_transitions = {
    # Opening quotation mark
    ("q0", '"'): "q1",

    # Permitted characters inside the string
    ("q1", "letter"): "q1",
    ("q1", "digit"): "q1",
    ("q1", "whitespace"): "q1",
    ("q1", "punctuation"): "q1",
    ("q1", "special"): "q1",

    # Closing quotation mark
    ("q1", '"'): "q2"
}

string_initial = "q0"

string_finals = ["q2"]


if __name__ == "__main__":

    # Transform the identifier automaton
    identifier_grammar = fa_to_rg(
        identifier_states,
        identifier_alphabet,
        identifier_transitions,
        identifier_initial,
        identifier_finals
    )

    display_grammar(
        "IDENTIFIER REGULAR GRAMMAR",
        identifier_grammar
    )

    # Transform the integer constant automaton
    integer_grammar = fa_to_rg(
        integer_states,
        integer_alphabet,
        integer_transitions,
        integer_initial,
        integer_finals
    )

    display_grammar(
        "INTEGER CONSTANT REGULAR GRAMMAR",
        integer_grammar
    )

    # Transform the string constant automaton
    string_grammar = fa_to_rg(
        string_states,
        string_alphabet,
        string_transitions,
        string_initial,
        string_finals
    )

    display_grammar(
        "STRING CONSTANT REGULAR GRAMMAR",
        string_grammar
    )
