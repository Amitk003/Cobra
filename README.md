# Project Cobra

A complete computing ecosystem — language, compiler, runtime, package manager, shell, and operating system.

## Architecture

```
Applications
      ↑
Cobra Language
      ↑
Cobra Compiler
      ↑
Cobra Runtime
      ↑
Cobra Package Manager
      ↑
Cobra Shell
      ↑
CobraOS (Linux-based)
```

## Quick Start

```bash
pip install -e .
cobrac examples/hello.cobra    # Run a Cobra file
cobrac examples/features.cobra   # Run all language features
cobrac examples/stdlib_demo.cobra # Test standard library
cobrac examples/json_demo.cobra   # JSON module demo
```

## Components

| Component | Description | Status |
|-----------|-------------|--------|
| Cobra Language | Variables, if/else, loops, functions, booleans | ✅ Done (Phase 2) |
| Cobra Compiler | Lexer → Parser → AST → Python Codegen | ✅ Done (Phase 2) |
| Cobra Runtime | built-in functions (print, input, str, int, len, etc.) | ✅ Done (Phase 3) |
| Standard Library | math, string, json, filesystem, datetime, os | ✅ Done (Phase 4) |
| Package Manager | cobrapkg init, install, uninstall, list | ✅ Done (Phase 5) |
| Cobra Shell | `cobra` REPL and `cobra file.cobra` runner | ✅ Done (Phase 6) |
| C Codegen | `cobrac -t c file.cobra -o file.c` | ✅ Done (Phase 7) |
| CobraOS | Deployment scripts, neofetch, init, ssh tunnel | ✅ Done (Phase 8) |

## License

MIT
