# parser_semantic.py


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.symbol_table = {}

    # -----------------------------
    # Current Token
    # -----------------------------

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    # -----------------------------
    # Main Parse Function
    # -----------------------------

    def parse(self):
        ast = []

        while self.current():
            ast.append(self.statement())

        return ast

    # -----------------------------
    # Statement Selector
    # -----------------------------

    def statement(self):
        token = self.current()

        if token[0] == "ASSIGN":
            return self.assign()

        elif token[0] == "ARITH":
            return self.arith()

        elif token[0] == "PRINT":
            return self.print_stmt()

        elif token[0] == "LOOP":
            return self.loop_stmt()

        elif token[0] == "IF":
            return self.if_stmt()

        else:
            raise Exception(f"Syntax Error: Unexpected token {token}")

    # -----------------------------
    # Assignment
    # -----------------------------

    def assign(self):
        _, var, val = self.current()

        self.pos += 1

        self.symbol_table[var] = int(val)

        return ("ASSIGN", var, val)

    # -----------------------------
    # Arithmetic
    # -----------------------------

    def arith(self):
        _, var, left, op, right = self.current()

        self.pos += 1

        # Semantic Checks

        if not left.isdigit() and left not in self.symbol_table:
            raise Exception(f"Semantic Error: '{left}' not declared")

        if not right.isdigit() and right not in self.symbol_table:
            raise Exception(f"Semantic Error: '{right}' not declared")

        self.symbol_table[var] = 0

        return ("ARITH", var, left, op, right)

    # -----------------------------
    # Print Statement
    # -----------------------------

    def print_stmt(self):
        _, var = self.current()

        self.pos += 1

        if var not in self.symbol_table:
            raise Exception(f"Semantic Error: '{var}' not declared")

        return ("PRINT", var)

    # -----------------------------
    # Loop Statement
    # -----------------------------

    def loop_stmt(self):
        _, count = self.current()

        self.pos += 1

        body = []

        while self.current() and self.current()[0] != "END":
            body.append(self.statement())

        if not self.current():
            raise Exception("Syntax Error: Missing END for LOOP")

        self.pos += 1

        return ("LOOP", count, body)

    # -----------------------------
    # IF Statement
    # -----------------------------

    def if_stmt(self):
        _, left, op, right = self.current()

        self.pos += 1

        # Semantic Checks

        if not left.isdigit() and left not in self.symbol_table:
            raise Exception(f"Semantic Error: '{left}' not declared")

        if not right.isdigit() and right not in self.symbol_table:
            raise Exception(f"Semantic Error: '{right}' not declared")

        then_body = []
        else_body = []

        while self.current() and self.current()[0] not in ("ELSE", "END"):
            then_body.append(self.statement())

        # ELSE BLOCK

        if self.current() and self.current()[0] == "ELSE":
            self.pos += 1

            while self.current() and self.current()[0] != "END":
                else_body.append(self.statement())

        if not self.current():
            raise Exception("Syntax Error: Missing END for IF")

        self.pos += 1

        return ("IF", left, op, right, then_body, else_body)