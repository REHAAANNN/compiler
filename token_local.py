import re

# ---------------- LEXER ----------------
TOKENS = [
    ('INT', r'int'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('NUM', r'\d+'),
    ('ASSIGN', r'='),
    ('PLUS', r'\+'),
    ('SEMI', r';'),
    ('SKIP', r'[ \t\n]+'),
]

def lexer(code):
    tokens = []
    while code:
        match = None
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                text = match.group(0)
                if token_type != 'SKIP':
                    tokens.append((token_type, text))
                code = code[len(text):]
                break
        if not match:
            raise SyntaxError(f"Invalid character: {code[0]}")
    return tokens


# ---------------- PARSE TREE NODE ----------------
class Node:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    # 🌳 Pretty Tree Printing
    def print_tree(self, prefix="", is_last=True):
        connector = "└── " if is_last else "├── "
        print(prefix + connector + f"{self.type}: {self.value if self.value else ''}")

        prefix += "    " if is_last else "│   "

        for i, child in enumerate(self.children):
            is_last_child = (i == len(self.children) - 1)
            child.print_tree(prefix, is_last_child)


# ---------------- PARSER ----------------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, token_type):
        if self.current() and self.current()[0] == token_type:
            val = self.current()
            self.pos += 1
            return val
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current()}")

    def parse(self):
        root = Node("PROGRAM")
        while self.current():
            root.add_child(self.statement())
        return root

    def statement(self):
        if self.current()[0] == 'INT':
            return self.declaration()
        else:
            return self.assignment()

    def declaration(self):
        node = Node("DECLARATION")
        self.eat('INT')
        var = self.eat('ID')
        node.add_child(Node("VAR", var[1]))

        self.eat('ASSIGN')
        expr = self.expression()
        node.add_child(expr)

        self.eat('SEMI')
        return node

    def assignment(self):
        node = Node("ASSIGNMENT")
        var = self.eat('ID')
        node.add_child(Node("VAR", var[1]))

        self.eat('ASSIGN')
        expr = self.expression()
        node.add_child(expr)

        self.eat('SEMI')
        return node

    def expression(self):
        node = Node("EXPR")
        left = self.term()
        node.add_child(left)

        while self.current() and self.current()[0] == 'PLUS':
            self.eat('PLUS')
            node.add_child(Node("PLUS", "+"))
            node.add_child(self.term())

        return node

    def term(self):
        tok = self.current()
        if tok[0] == 'NUM':
            self.eat('NUM')
            return Node("NUM", tok[1])
        elif tok[0] == 'ID':
            self.eat('ID')
            return Node("VAR", tok[1])
        else:
            raise SyntaxError("Invalid term")


# ---------------- SEMANTIC ANALYZER ----------------
class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, node):
        method_name = f"visit_{node.type}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        for child in node.children:
            self.analyze(child)

    def visit_DECLARATION(self, node):
        var_name = node.children[0].value

        if var_name in self.symbol_table:
            raise Exception(f"❌ Semantic Error: '{var_name}' already declared")

        self.symbol_table[var_name] = "int"
        self.analyze(node.children[1])

    def visit_ASSIGNMENT(self, node):
        var_name = node.children[0].value

        if var_name not in self.symbol_table:
            raise Exception(f"❌ Semantic Error: '{var_name}' not declared")

        self.analyze(node.children[1])

    def visit_VAR(self, node):
        if node.value not in self.symbol_table:
            raise Exception(f"❌ Semantic Error: '{node.value}' not declared")

    def visit_NUM(self, node):
        pass


# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("Enter your code (type 'END' on new line to finish):\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    code = "\n".join(lines)

    try:
        # Step 1: Lexer
        tokens = lexer(code)
        print("\n🔹 Tokens:")
        print(tokens)

        # Step 2: Parser
        parser = Parser(tokens)
        tree = parser.parse()

        print("\n🌳 Parse Tree:")
        tree.print_tree()

        # Step 3: Semantic Analysis
        analyzer = SemanticAnalyzer()
        analyzer.analyze(tree)

        print("\n✅ Semantic Analysis Passed!")

    except Exception as e:
        print("\n", e)