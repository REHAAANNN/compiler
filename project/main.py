# main.py

from lexer import lexer
from parser_semantic import Parser
from codegen import generate


if __name__ == "__main__":

    print("Enter your algorithm in simple English")
    print("Type ENDINPUT to finish\n")

    user_input = ""

    while True:
        line = input()

        if line.strip().upper() == "ENDINPUT":
            break

        user_input += line + "\n"

    try:

        # -----------------------------
        # LEXICAL ANALYSIS
        # -----------------------------

        tokens = lexer(user_input)

        # -----------------------------
        # PARSING + SEMANTIC ANALYSIS
        # -----------------------------

        parser = Parser(tokens)
        ast = parser.parse()

        # -----------------------------
        # CODE GENERATION
        # -----------------------------

        python_code = generate(ast, target="python")

        print("\nGenerated Python Code:\n")
        print(python_code)

    except Exception as e:
        print("\nERROR:")
        print(e)