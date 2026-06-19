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
cobrac examples/hello.cobra
```

## Components

| Component | Description | Status |
|-----------|-------------|--------|
| Cobra Language | The programming language | 🚧 In Progress |
| Cobra Compiler | Lexer → Parser → AST → Codegen | 🚧 In Progress |
| Cobra Runtime | Built-in functions (print, input, etc.) | 📋 Planned |
| Standard Library | math, string, json, filesystem, datetime | 📋 Planned |
| Package Manager | cobrapkg — install Cobra libraries | 📋 Planned |
| Cobra Shell | Interactive REPL and script runner | 📋 Planned |
| CobraOS | Linux-based OS image with Cobra tooling | 📋 Planned |

## License

MIT
