"""CobraOS CLI — cobraos command for OS-level operations."""

import sys
import argparse
import os as _os


def main():
    parser = argparse.ArgumentParser(description="CobraOS — OS management")
    parser.add_argument("command", nargs="?", choices=["info", "neofetch", "version"], default="info")
    args = parser.parse_args()

    from cobra import __version__

    if args.command == "version":
        print(f"CobraOS v{__version__}")
    elif args.command == "neofetch":
        from cobra.compiler.lexer import Lexer
        from cobra.compiler.parser import Parser
        from cobra.compiler.codegen import CodegenPy

        src = (
            'import os\n'
            'print("  _______________")\n'
            f'print(" | CobraOS v{__version__}    |")\n'
            f'print(" | Host: " + os.hostname() + "       |")\n'
            f'print(" | User: " + os.user() + "         |")\n'
            f'print(" | Shell: Cobra        |")\n'
            f'print(" | Cores: " + str(os.cpu_count()) + "          |")\n'
            'print(" |_______________|")\n'
        )
        lexer = Lexer(src)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = CodegenPy()
        output = codegen.generate(ast)
        exec(output, {})
    else:
        print(f"CobraOS v{__version__}")
        print(f"Host: {_os.name}")
        print(f"User: {_os.environ.get('USER', _os.environ.get('USERNAME', 'unknown'))}")


if __name__ == "__main__":
    main()
