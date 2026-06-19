import sys
import argparse

from cobra.pkgmgr.manager import init, install, uninstall, list_packages


def main():
    parser = argparse.ArgumentParser(description="Cobra Package Manager")
    parser.add_argument("command", choices=["init", "install", "uninstall", "list"])
    parser.add_argument("package", nargs="?", help="Package name or URL")
    args = parser.parse_args()

    if args.command == "init":
        init()
    elif args.command == "install":
        if not args.package:
            print("Usage: cobrapkg install <package>")
            sys.exit(1)
        install(args.package)
    elif args.command == "uninstall":
        if not args.package:
            print("Usage: cobrapkg uninstall <package>")
            sys.exit(1)
        uninstall(args.package)
    elif args.command == "list":
        list_packages()


if __name__ == "__main__":
    main()
