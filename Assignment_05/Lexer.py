
from HashTable import HashTable

from Automata import (
    identifier_automaton,
    integer_automaton,
    string_automaton
)


# 1. Reserved keywords

KEYWORDS = {
    "album", "load", "into", "add", "to",
    "grayscale", "blur", "resize", "rotate", "crop",
    "output", "save", "if", "else", "end",
    "for", "in", "width", "height", "size",
    "true", "false"
}


# 2. Token codes

TOKEN_CODES = {}

for keyword in sorted(KEYWORDS):
    TOKEN_CODES[keyword] = "KW_" + keyword.upper()

TOKEN_CODES.update({
    "=": "ASSIGN",
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLY",
    "/": "DIVIDE",
    "==": "EQUAL",
    "!=": "NOT_EQUAL",
    "<": "LESS",
    ">": "GREATER",
    "<=": "LESS_EQUAL",
    ">=": "GREATER_EQUAL",
    "[": "LBRACKET",
    "]": "RBRACKET",
    ",": "COMMA",
    "(": "LPAREN",
    ")": "RPAREN",
    "ID": "ID",
    "CONST": "CONST",
    "NEWLINE": "NEWLINE",
})


# 3. Lexer

class Lexer:

    def __init__(self):
        self.pif = []
        self.symbol_table = HashTable()
        self.errors = []

    def add_symbol(self, value, category):
        """
        Adds a token to the symbol table and returns its position.
        """
        position = self.symbol_table.insert(category, value)
        return position

    def add_pif(self, token, position=-1):
        """
        Adds an entry to the Program Internal Form.
        """
        self.pif.append((TOKEN_CODES[token], position))

    def tokenize(self, source):

        self.pif = []
        self.symbol_table = HashTable()
        self.errors = []

        position = 0
        line = 1
        column = 1

        while position < len(source):

            char = source[position]

            # 1. Ignore spaces and tabs
            if char in " \t":
                position += 1
                column += 1
                continue

            # 2. Handle newlines
            if char == "\n":
                self.add_pif("NEWLINE")
                position += 1
                line += 1
                column = 1
                continue

            if char == "\r":
                position += 1
                continue

            # 3. Recognize strings using the string automaton
            if char == '"':

                token, end = string_automaton.recognize_prefix(
                    source, position
                )

                if token is None:
                    self.errors.append(
                        f"Lexical error at line {line}, column {column}: "
                        "Invalid or unterminated string"
                    )

                    # Skip until the end of the line
                    while position < len(source) and source[position] != "\n":
                        position += 1
                        column += 1

                    continue

                index = self.add_symbol(token, "CONST")
                self.add_pif("CONST", index)

                column += end - position
                position = end
                continue

            # 4. Recognize identifiers using the identifier automaton
            if char.isascii() and char.isalpha():

                token, end = identifier_automaton.recognize_prefix(
                    source, position
                )

                if token is None:
                    self.errors.append(
                        f"Lexical error at line {line}, column {column}: "
                        "Invalid identifier"
                    )
                    position += 1
                    column += 1
                    continue

                # Check that the identifier is not followed by
                # a digit or underscore that belongs to a malformed token.
                if end < len(source) and (
                    source[end].isascii()
                    and (source[end].isalnum() or source[end] == "_")
                ):

                    while end < len(source) and (
                        source[end].isascii()
                        and (source[end].isalnum() or source[end] == "_")
                    ):
                        end += 1

                    invalid_token = source[position:end]

                    self.errors.append(
                        f"Lexical error at line {line}, column {column}: "
                        f"Invalid identifier '{invalid_token}'"
                    )

                    column += end - position
                    position = end
                    continue

                if token in KEYWORDS:
                    self.add_pif(token)

                else:
                    index = self.add_symbol(token, "ID")
                    self.add_pif("ID", index)

                column += end - position
                position = end
                continue

            # 5. Recognize integers using the integer automaton
            if char.isascii() and char.isdigit():

                token, end = integer_automaton.recognize_prefix(
                    source, position
                )

                # First check whether the automaton recognized a number
                if token is None:
                    self.errors.append(
                        f"Lexical error at line {line}, column {column}: "
                        "Invalid number"
                    )
                    position += 1
                    column += 1
                    continue

                # Check for malformed numbers such as 03 or 123abc
                if end < len(source) and (
                    source[end].isascii()
                    and (source[end].isalnum() or source[end] == "_")
                ):

                    while end < len(source) and (
                        source[end].isascii()
                        and (source[end].isalnum() or source[end] == "_")
                    ):
                        end += 1

                    invalid_token = source[position:end]

                    self.errors.append(
                        f"Lexical error at line {line}, column {column}: "
                        f"Invalid number '{invalid_token}'"
                    )

                    column += end - position
                    position = end
                    continue

                index = self.add_symbol(token, "CONST")
                self.add_pif("CONST", index)

                column += end - position
                position = end
                continue

            # 6. Recognize operators (check two-character operators first)
            two_char = source[position:position + 2]

            if two_char in ("==", "!=", "<=", ">="):
                self.add_pif(two_char)
                position += 2
                column += 2
                continue

            if char in ("+", "-", "*", "/", "=", "<", ">"):
                self.add_pif(char)
                position += 1
                column += 1
                continue

            # 7. Recognize delimiters
            if char in ("[", "]", "(", ")", ","):
                self.add_pif(char)
                position += 1
                column += 1
                continue

            # 8. Invalid character
            self.errors.append(
                f"Lexical error at line {line}, column {column}: "
                f"Invalid character '{char}'"
            )

            position += 1
            column += 1

    def print_results(self):
        """Display the PIF, symbol table, and lexical errors."""
        print("\n=== PIF (Program Internal Form) ===")
        print(f"{'Token code':<20} Symbol table position")
        print("-" * 42)

        for token_code, st_position in self.pif:
            print(f"{token_code:<20} {st_position}")

        print("\n=== Symbol Table (ST) ===")
        print(f"{'Position':<12} {'Category':<12} Value")
        print("-" * 45)

        for (category, value), pos in sorted(
                self.symbol_table.items(),
                key=lambda item: item[1]
        ):
            print(f"{pos:<12} {category:<12} {value}")

        print("\n=== Lexical Errors ===")

        if self.errors:
            for error in self.errors:
                print(error)
        else:
            print("No lexical errors.")


# 4. Example source program

if __name__ == "__main__":

    source_code = """load "beach.jpg" into beach
load "mountain.jpg" into mountain
load "sunset.jpg" into sunset

album vacation = [beach, mountain, sunset]

resize beach 1200 800
crop beach 100 100
rotate beach 90
grayscale beach

resize mountain 1000 700
blur mountain 3

resize mountain 300 400

resize sunset 1200 800
grayscale sunset

load "kayak.jpg" into kayak
add kayak to vacation

if width(beach) > 1000
    resize beach 800 700
end

if height(mountain) < 2000
    resize mountain 400 300
else
    if width(sunset) > 100
        resize sunset 300 300
    end
end
"""

    lexer = Lexer()
    lexer.tokenize(source_code)
    lexer.print_results()
