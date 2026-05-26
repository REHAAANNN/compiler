# Project Overview

This project is a mini compiler that accepts simple English-like instructions and generates runnable code in multiple target languages. It includes a lexer, parser with semantic checks, and code generators. A Flask-based web UI lets you enter input, select a target language, and (optionally) run the generated code.

## How it works

1. **Lexical analysis**: The input text is split into tokens like ASSIGN, ARITH, PRINT, LOOP, IF, ELSE, END.
2. **Parsing + semantic checks**: Tokens are parsed into an AST and validated (variables must be declared before use).
3. **Code generation**: The AST is converted into code for the selected target language.
4. **Execution (optional)**: The generated program is run and the output is shown in the UI.

## Project structure and file responsibilities

- **app.py**
  - Flask server for the frontend UI.
  - Endpoint: `POST /api/compile` parses input, generates code, and optionally runs it.
  - Runs Python via the current interpreter, Java via `javac/java`, and C via `gcc` or `clang`.

- **templates/index.html**
  - The web UI page with input area, target selector, and output panels.

- **static/app.js**
  - Frontend logic for calling `/api/compile`.
  - Strips `ENDINPUT` lines from the input (this marker is only for the old terminal flow).
  - Renders generated code and runtime output.

- **static/style.css**
  - UI styling for the web page (layout, colors, typography, animations).

- **project/lexer.py**
  - Converts the English-like input lines into token tuples.
  - Supported features: assignments, arithmetic, print, loop, if/else/end.

- **project/parser_semantic.py**
  - Parses tokens into an AST.
  - Performs semantic checks (e.g., variables must be declared).

- **project/codegen.py**
  - Generates code for **Python**, **Java**, and **C**.
  - `generate(ast, target=...)` chooses the language backend.
  - Java and C generators emit complete programs with `main`.

- **project/main.py**
  - Original terminal-based driver.
  - Reads input until `ENDINPUT`, then runs lexer -> parser -> codegen (Python).

- **combine.py**
  - Legacy, all-in-one version (lexer + parser + codegen) for a simpler language subset.

- **token_local.py**
  - Renamed from `token.py` to avoid shadowing Python's standard library `token` module.

## Input language (English-like)

Examples of supported syntax:

- Assignment:
  - `create variable x with value 10`
  - `x = 10`

- Arithmetic:
  - `add x and y into sum`
  - `subtract x and y into diff`
  - `multiply x and y into prod`
  - `divide x and y into result`
  - `z = x + y`

- Print:
  - `print x`

- Loop:
  - `loop 3`
  - `end`

- If / else:
  - `if x > 5`
  - `else`
  - `end`

## Running the project

- **Web UI (recommended)**
  1. Install Flask: `pip install flask`
  2. Run: `python app.py`
  3. Open: `http://127.0.0.1:5000`

- **Terminal (legacy)**
  - Run: `python project/main.py`
  - End input with `ENDINPUT`

## Requirements

- Python 3.9+ (for Flask and the compiler backend)
- For running generated code:
  - Java: `javac` and `java` on PATH
  - C: `gcc` or `clang` on PATH
