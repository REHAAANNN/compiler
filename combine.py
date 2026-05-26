import re

# ---------------------------
# ROLE 1: LEXER
# ---------------------------

def lexer(input_text):
    tokens = []
    lines = input_text.strip().split('\n')

    for line in lines:
        words = line.strip().split()

        if not words:
            continue

        if words[0].lower() == "create":
            tokens.append(("CREATE", words[3]))   # variable name
            tokens.append(("VALUE", words[-1]))   # value

        elif words[0].lower() == "print":
            tokens.append(("PRINT", words[1]))

        elif words[0].lower() == "repeat":
            tokens.append(("REPEAT", words[1]))

        elif words[0].lower() == "end":
            tokens.append(("END", None))

    return tokens


# ---------------------------
# ROLE 2: PARSER + SEMANTIC
# ---------------------------

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.symbol_table = {}

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def parse(self):
        ast = []
        while self.current_token():
            stmt = self.statement()
            ast.append(stmt)
        return ast

    def statement(self):
        token = self.current_token()

        if token[0] == "CREATE":
            return self.create_statement()

        elif token[0] == "PRINT":
            return self.print_statement()

        elif token[0] == "REPEAT":
            return self.repeat_statement()

        else:
            raise Exception("Syntax Error")

    def create_statement(self):
        var_name = self.tokens[self.pos][1]
        self.pos += 1

        value = self.tokens[self.pos][1]
        self.pos += 1

        # Semantic Check: duplicate variable
        if var_name in self.symbol_table:
            raise Exception(f"Semantic Error: {var_name} already declared")

        self.symbol_table[var_name] = int(value)

        return ("CREATE", var_name, value)

    def print_statement(self):
        var_name = self.tokens[self.pos][1]
        self.pos += 1

        # Semantic Check: variable exists
        if var_name not in self.symbol_table:
            raise Exception(f"Semantic Error: {var_name} not declared")

        return ("PRINT", var_name)

    def repeat_statement(self):
        count = int(self.tokens[self.pos][1])
        self.pos += 1

        body = []

        while self.current_token() and self.current_token()[0] != "END":
            body.append(self.statement())

        if not self.current_token():
            raise Exception("Syntax Error: Missing END")

        self.pos += 1  # skip END

        return ("REPEAT", count, body)


# ---------------------------
# ROLE 3: CODE GENERATOR
# ---------------------------

def generate_code(ast):
    code = ""

    for node in ast:
        if node[0] == "CREATE":
            code += f"{node[1]} = {node[2]}\n"

        elif node[0] == "PRINT":
            code += f"print({node[1]})\n"

        elif node[0] == "REPEAT":
            code += f"for i in range({node[1]}):\n"
            for stmt in node[2]:
                if stmt[0] == "PRINT":
                    code += f"    print({stmt[1]})\n"

    return code


# ---------------------------
# MAIN DRIVER
# ---------------------------

if __name__ == "__main__":
    print("Enter your program (type ENDINPUT to stop):")

    user_input = ""
    while True:
        line = input()
        if line.strip() == "ENDINPUT":
            break
        user_input += line + "\n"

    try:
        tokens = lexer(user_input)
        parser = Parser(tokens)
        ast = parser.parse()

        print("\n--- AST ---")
        print(ast)

        output_code = generate_code(ast)

        print("\n--- Generated Python Code ---")
        print(output_code)

    except Exception as e:
        print(e)