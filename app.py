import json
import os
import shutil
import subprocess
import sys
import tempfile

from flask import Flask, jsonify, render_template, request

from project.codegen import generate
from project.lexer import lexer
from project.parser_semantic import Parser


app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


def _run_python(code):
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "main.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result


def _run_java(code):
    if not shutil.which("javac") or not shutil.which("java"):
        raise RuntimeError("javac/java not found on PATH")

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "Main.java")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        compile_result = subprocess.run(
            ["javac", file_path],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if compile_result.returncode != 0:
            return compile_result

        run_result = subprocess.run(
            ["java", "-cp", tmpdir, "Main"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return run_result


def _run_c(code):
    compiler = shutil.which("gcc") or shutil.which("clang")
    if not compiler:
        raise RuntimeError("gcc/clang not found on PATH")

    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, "main.c")
        exe_path = os.path.join(tmpdir, "main.exe")

        with open(src_path, "w", encoding="utf-8") as f:
            f.write(code)

        compile_result = subprocess.run(
            [compiler, src_path, "-o", exe_path],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if compile_result.returncode != 0:
            return compile_result

        run_result = subprocess.run(
            [exe_path],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return run_result


@app.post("/api/compile")
def compile_code():
    data = request.get_json(silent=True) or {}
    source = data.get("source", "")
    target = data.get("target", "python")
    run_code = bool(data.get("run"))

    try:
        tokens = lexer(source)
        parser = Parser(tokens)
        ast = parser.parse()
        generated = generate(ast, target=target)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    output = ""
    if run_code:
        try:
            if target == "python":
                result = _run_python(generated)
            elif target == "java":
                result = _run_java(generated)
            elif target == "c":
                result = _run_c(generated)
            else:
                return jsonify({"error": f"Unknown target: {target}"}), 400

            output = (result.stdout or "") + (result.stderr or "")
            if result.returncode != 0 and not output:
                output = f"Exited with code {result.returncode}"
        except Exception as exc:
            output = f"Runtime error: {exc}"

    return jsonify({"generated": generated, "output": output})


if __name__ == "__main__":
    app.run(debug=True)
