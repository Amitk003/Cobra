import sys
import argparse

from cobra.compiler.lexer import Lexer
from cobra.compiler.parser import Parser
from cobra.compiler.codegen import CodegenPy

def main():
    parser = argparse.ArgumentParser(description="Cobra Compiler")
    parser.add_argument("file", help="Path to .cobra source file")
    parser.add_argument("-o", "--output", help="Output file path")
    args = parser.parse_args()

    with open(args.file, "r") as f:
        source = f.read()

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    codegen = CodegenPy()
    output = codegen.generate(ast)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
    else:
        exec(output, {})

if __name__ == "__main__":
    main()
