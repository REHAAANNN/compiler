# codegen.py


def generate(ast, target="python"):
    if target == "python":
        return _generate_python(ast, 0)
    if target == "java":
        return _generate_java(ast)
    if target == "c":
        return _generate_c(ast)
    raise ValueError(f"Unknown target: {target}")


def _generate_python(ast, indent=0):

    code = ""

    for node in ast:

        space = "    " * indent

        # -----------------------------
        # Assignment
        # -----------------------------

        if node[0] == "ASSIGN":
            _, var, val = node
            code += f"{space}{var} = {val}\n"

        # -----------------------------
        # Arithmetic
        # -----------------------------

        elif node[0] == "ARITH":
            _, var, left, op, right = node
            code += f"{space}{var} = {left} {op} {right}\n"

        # -----------------------------
        # Print
        # -----------------------------

        elif node[0] == "PRINT":
            _, var = node
            code += f"{space}print({var})\n"

        # -----------------------------
        # Loop
        # -----------------------------

        elif node[0] == "LOOP":
            _, count, body = node

            code += f"{space}for i in range({count}):\n"
            code += _generate_python(body, indent + 1)

        # -----------------------------
        # IF ELSE
        # -----------------------------

        elif node[0] == "IF":
            _, left, op, right, then_body, else_body = node

            code += f"{space}if {left} {op} {right}:\n"
            code += _generate_python(then_body, indent + 1)

            if else_body:
                code += f"{space}else:\n"
                code += _generate_python(else_body, indent + 1)

    return code


def _generate_java(ast):
    declared = set()
    body = _generate_java_block(ast, declared, 2)

    return (
        "public class Main {\n"
        "    public static void main(String[] args) {\n"
        f"{body}"
        "    }\n"
        "}\n"
    )


def _generate_java_block(ast, declared, indent):
    code = ""
    space = "    " * indent

    for node in ast:
        if node[0] == "ASSIGN":
            _, var, val = node
            decl = "double " if var not in declared else ""
            declared.add(var)
            code += f"{space}{decl}{var} = {val};\n"

        elif node[0] == "ARITH":
            _, var, left, op, right = node
            decl = "double " if var not in declared else ""
            declared.add(var)
            code += f"{space}{decl}{var} = {left} {op} {right};\n"

        elif node[0] == "PRINT":
            _, var = node
            code += f"{space}System.out.println({var});\n"

        elif node[0] == "LOOP":
            _, count, body = node
            code += f"{space}for (int i = 0; i < {count}; i++) {{\n"
            code += _generate_java_block(body, declared, indent + 1)
            code += f"{space}}}\n"

        elif node[0] == "IF":
            _, left, op, right, then_body, else_body = node
            code += f"{space}if ({left} {op} {right}) {{\n"
            code += _generate_java_block(then_body, declared, indent + 1)
            if else_body:
                code += f"{space}}} else {{\n"
                code += _generate_java_block(else_body, declared, indent + 1)
            code += f"{space}}}\n"

    return code


def _generate_c(ast):
    declared = set()
    body = _generate_c_block(ast, declared, 1)

    return (
        "#include <stdio.h>\n\n"
        "int main(void) {\n"
        f"{body}"
        "    return 0;\n"
        "}\n"
    )


def _generate_c_block(ast, declared, indent):
    code = ""
    space = "    " * indent

    for node in ast:
        if node[0] == "ASSIGN":
            _, var, val = node
            decl = "double " if var not in declared else ""
            declared.add(var)
            code += f"{space}{decl}{var} = {val};\n"

        elif node[0] == "ARITH":
            _, var, left, op, right = node
            decl = "double " if var not in declared else ""
            declared.add(var)
            code += f"{space}{decl}{var} = {left} {op} {right};\n"

        elif node[0] == "PRINT":
            _, var = node
            code += f"{space}printf(\"%g\\n\", {var});\n"

        elif node[0] == "LOOP":
            _, count, body = node
            code += f"{space}for (int i = 0; i < {count}; i++) {{\n"
            code += _generate_c_block(body, declared, indent + 1)
            code += f"{space}}}\n"

        elif node[0] == "IF":
            _, left, op, right, then_body, else_body = node
            code += f"{space}if ({left} {op} {right}) {{\n"
            code += _generate_c_block(then_body, declared, indent + 1)
            if else_body:
                code += f"{space}}} else {{\n"
                code += _generate_c_block(else_body, declared, indent + 1)
            code += f"{space}}}\n"

    return code