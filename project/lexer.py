# lexer.py

import re


def lexer(text):
    lines = text.strip().split("\n")
    tokens = []

    for line in lines:
        line = line.strip().lower()

        if not line:
            continue

        # -----------------------------
        # Variable Assignment
        # x = 10
        # create variable x with value 10
        # -----------------------------

        assign_match = re.match(
            r'(?:create variable\s+)?(\w+)\s*(?:=|equal to|equals|with value)\s*(\d+)',
            line
        )

        if assign_match:
            var, val = assign_match.groups()
            tokens.append(("ASSIGN", var, val))
            continue

        # -----------------------------
        # Arithmetic Expressions
        # z = x + y
        # add x and y into z
        # subtract x and y into z
        # multiply x and y into z
        # divide x and y into z
        # -----------------------------

        arith_match = re.match(
            r'(\w+)\s*=\s*(\w+)\s*([+\-*/])\s*(\w+)',
            line
        )

        if arith_match:
            var, left, op, right = arith_match.groups()
            tokens.append(("ARITH", var, left, op, right))
            continue

        # Natural Language Arithmetic

        add_match = re.match(r'add\s+(\w+)\s+and\s+(\w+)\s+into\s+(\w+)', line)

        if add_match:
            left, right, var = add_match.groups()
            tokens.append(("ARITH", var, left, "+", right))
            continue

        sub_match = re.match(r'subtract\s+(\w+)\s+and\s+(\w+)\s+into\s+(\w+)', line)

        if sub_match:
            left, right, var = sub_match.groups()
            tokens.append(("ARITH", var, left, "-", right))
            continue

        mul_match = re.match(r'multiply\s+(\w+)\s+and\s+(\w+)\s+into\s+(\w+)', line)

        if mul_match:
            left, right, var = mul_match.groups()
            tokens.append(("ARITH", var, left, "*", right))
            continue

        div_match = re.match(r'divide\s+(\w+)\s+and\s+(\w+)\s+into\s+(\w+)', line)

        if div_match:
            left, right, var = div_match.groups()
            tokens.append(("ARITH", var, left, "/", right))
            continue

        # -----------------------------
        # Print Statement
        # print x
        # -----------------------------

        print_match = re.match(r'print\s+(\w+)', line)

        if print_match:
            var = print_match.group(1)
            tokens.append(("PRINT", var))
            continue

        # -----------------------------
        # Loop Statement
        # loop 5
        # repeat 5 times
        # -----------------------------

        loop_match = re.match(r'(?:loop|repeat)\s+(\d+)', line)

        if loop_match:
            count = loop_match.group(1)
            tokens.append(("LOOP", count))
            continue

        # -----------------------------
        # IF Condition
        # if x > 5
        # -----------------------------

        if_match = re.match(r'if\s+(\w+)\s*(==|!=|>|<|>=|<=)\s*(\w+)', line)

        if if_match:
            left, op, right = if_match.groups()
            tokens.append(("IF", left, op, right))
            continue

        # -----------------------------
        # ELSE
        # -----------------------------

        if line == "else":
            tokens.append(("ELSE", None))
            continue

        # -----------------------------
        # END
        # -----------------------------

        if line == "end":
            tokens.append(("END", None))
            continue

        raise Exception(f"Lexer Error: Cannot understand line -> {line}")

    return tokens