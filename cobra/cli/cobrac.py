import sys
import argparse
import os
import subprocess
import tempfile

from cobra.compiler.lexer import Lexer, LexerError
from cobra.compiler.parser import Parser, ParseError
from cobra.compiler.codegen import CodegenPy, CodegenError
from cobra.compiler.codegen_c import CodegenC


def compile_to_python(source, output_path=None):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    codegen = CodegenPy()
    output = codegen.generate(ast)

    if output_path:
        with open(output_path, "w") as f:
            f.write(output)
        print(f"Generated {output_path}")
    else:
        exec(output, {})
    return output


def compile_to_c(source, output_path=None):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    codegen = CodegenC()
    output = codegen.generate(ast)

    if output_path:
        with open(output_path, "w") as f:
            f.write(output)
        print(f"Generated {output_path}")
    else:
        print(output)
    return output


def try_compile_c(c_path):
    binary = c_path[:-2]
    if os.name == "nt":
        binary += ".exe"
    try:
        result = subprocess.run(
            ["gcc", "-o", binary, c_path, "-lm"],
            check=True, capture_output=True, text=True
        )
        print(f"Compiled to {binary}")
        return binary
    except FileNotFoundError:
        print("Warning: gcc not found. Install GCC to compile the C output.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Compilation error:\n{e.stderr}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Cobra Compiler")
    parser.add_argument("file", help="Path to .cobra source file")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument(
        "-t", "--target", choices=["py", "c"], default="py",
        help="Target output (py=Python, c=C)"
    )
    args = parser.parse_args()

    try:
        with open(args.file, "r") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: file '{args.file}' not found")
        sys.exit(1)

    try:
        if args.target == "c":
            output = compile_to_c(source, args.output)
            if args.output and args.output.endswith(".c"):
                try_compile_c(args.output)
        else:
            compile_to_python(source, args.output)
    except (LexerError, ParseError, CodegenError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
