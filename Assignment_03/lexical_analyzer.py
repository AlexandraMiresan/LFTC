
import re

from HashTable import HashTable

# 1. Reserved keywords
KEYWORDS = {
    "album", "load", "into", "add", "to",
    "grayscale", "blur", "resize", "rotate", "crop",
    "output", "save", "if", "else", "end",
    "for", "in", "width", "height", "size",
    "true", "false"
}


# 2. Token codes
# Keywords and operators have fixed token codes.
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
    "\n": "NEWLINE",
})


# 3. Regular expressions
TOKEN_REGEX = re.compile(
    r'(?P<WHITESPACE>[ \t\r]+)'
    r'|(?P<STRING>"[A-Za-z0-9 _.]+")'
    r'|(?P<NUMBER>[0-9]+)'
    r'|(?P<IDENTIFIER>[A-Za-z][A-Za-z0-9_]*)'
    r'|(?P<OPERATOR>==|!=|<=|>=|[=+\-*/<>])'
    r'|(?P<DELIMITER>[\[\],()])'
    r'|(?P<NEWLINE>\r\n|\n|\r)'
)


class Lexer:
    def __init__(self):
        self.pif = []
        self.symbol_table = HashTable()
        self.errors = []
        self.next_position = 0

    def add_symbol(self, category, value):
        return self.symbol_table.insert(category, value)

    def add_pif(self, token_code, position=-1):
        """Add an entry to the Program Internal Form."""
        self.pif.append((token_code, position))

    def tokenize(self, source):
        """Perform lexical analysis on the source program."""
        self.pif = []
        self.symbol_table = HashTable()
        self.errors = []
        self.next_position = 0

        position = 0
        line = 1
        column = 1

        while position < len(source):
            # Handle invalid or unsupported characters
            match = TOKEN_REGEX.match(source, position)

            if not match:
                char = source[position]

                # Give an informative error for an invalid string.
                if char == '"':
                    end = source.find('"', position + 1)
                    newline = source.find('\n', position + 1)

                    if end == -1 or (
                        newline != -1 and newline < end
                    ):
                        self.errors.append(
                            f"Line {line}, column {column}: "
                            "unterminated string"
                        )

                        position += 1
                        column += 1
                        continue

                    invalid_string = source[position:end + 1]

                    self.errors.append(
                        f"Line {line}, column {column}: "
                        f"invalid string {invalid_string!r}"
                    )

                    position = end + 1
                    column += len(invalid_string)
                    continue

                self.errors.append(
                    f"Line {line}, column {column}: "
                    f"invalid character {char!r}"
                )

                position += 1
                column += 1
                continue

            token_type = match.lastgroup
            value = match.group()
            length = len(value)

            # Ignore spaces and tabs.
            if token_type == "WHITESPACE":
                position += length
                column += length
                continue

            # Preserve newlines in the PIF.
            if token_type == "NEWLINE":
                self.add_pif("NEWLINE")
                position += length
                line += 1
                column = 1
                continue

            # Classify identifiers and keywords.
            if token_type == "IDENTIFIER":
                if value in KEYWORDS:
                    self.add_pif(TOKEN_CODES[value])
                else:
                    st_position = self.add_symbol("ID", value)
                    self.add_pif("ID", st_position)

            # Store numbers in the symbol table.
            elif token_type == "NUMBER":
                st_position = self.add_symbol("CONST", value)
                self.add_pif("CONST", st_position)

            # Store strings in the symbol table.
            elif token_type == "STRING":
                st_position = self.add_symbol("CONST", value)
                self.add_pif("CONST", st_position)

            # Operators and delimiters have fixed token codes.
            elif token_type in ("OPERATOR", "DELIMITER"):
                self.add_pif(TOKEN_CODES[value])

            position += length
            column += length

        return self.pif, self.symbol_table, self.errors

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
