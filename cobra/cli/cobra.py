import sys
import os

from cobra.compiler.lexer import Lexer, LexerError
from cobra.compiler.parser import Parser, ParseError
from cobra.compiler.codegen import CodegenPy, CodegenError


def compile_source(source: str) -> str:
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    codegen = CodegenPy()
    return codegen.generate(ast)


def run_source(source: str, env: dict | None = None) -> dict:
    code = compile_source(source)
    if env is None:
        env = {}
    exec(code, env)
    return env


def run_file(path: str):
    with open(path, "r") as f:
        source = f.read()
    run_source(source)


def repl():
    try:
        import readline
        has_readline = True
    except ImportError:
        has_readline = False

    env: dict = {}
    history_file = os.path.expanduser("~/.cobra_history")
    if has_readline:
        try:
            readline.read_history_file(history_file)
        except FileNotFoundError:
            pass

    print("Cobra Shell v0.1.0")
    print("Type 'exit' or Ctrl+C to quit")
    print()

    while True:
        try:
            line = input("cobra> ")
            if line.strip() == "":
                continue
            if line.strip() == "exit":
                break
            if line.strip().startswith("!"):
                os.system(line.strip()[1:])
                continue
            run_source(line, env)
            if has_readline:
                readline.append_history_file(1, history_file)
        except (LexerError, ParseError, CodegenError, SyntaxError) as e:
            print(f"Error: {e}")
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            break
        except Exception as e:
            print(f"Runtime Error: {e}")


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h", "--help"):
            print("Usage: cobra [file.cobra]")
            return
        if sys.argv[1] in ("-v", "--version"):
            from cobra import __version__
            print(f"Cobra v{__version__}")
            return
        try:
            run_file(sys.argv[1])
        except FileNotFoundError:
            print(f"Error: file '{sys.argv[1]}' not found")
            sys.exit(1)
        except (LexerError, ParseError, CodegenError) as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        repl()


if __name__ == "__main__":
    main()
