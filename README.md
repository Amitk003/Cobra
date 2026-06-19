# Project Cobra

A complete computing ecosystem — language, compiler, runtime, package manager, shell, and operating system.

> Build the ecosystem first, then build software inside it.

---

## Architecture

```
     Applications
          ↑
     Cobra Language     ← You write code here
          ↑
     Cobra Compiler     ← Transpiles to Python or C
          ↑
     Cobra Runtime      ← Built-in functions (print, input, str, ...)
          ↑
     Cobra Package Mgr  ← cobrapkg: install/remove libraries
          ↑
     Cobra Shell        ← cobra: REPL + script runner
          ↑
     CobraOS            ← Linux VPS with Cobra as the shell
```

---

## Quick Start

```bash
# Install from source
pip install -e .

# Run a Cobra file
cobrac examples/hello.cobra

# Run a file with the Cobra shell
cobra examples/features.cobra

# Start the interactive REPL
cobra

# Generate C code
cobrac -t c examples/numeric.cobra -o output.c
```

---

## Language Syntax

### Variables

```
let name = "Cobra"
let age = 25
age = age + 1                     # Reassign (no let)
```

### Conditionals

```
if score >= 90 {
    print("A")
} else {
    if score >= 80 {
        print("B")
    } else {
        print("C")
    }
}
```

### Loops

```
# While loop
let i = 0
while i < 5 {
    print(i)
    i = i + 1
}

# For loop (exclusive range)
for i in 0..5 {
    print(i)
}
```

### Functions

```
func add(a, b) {
    return a + b
}

func fib(n) {
    if n <= 1 {
        return n
    }
    return fib(n - 1) + fib(n - 2)
}

print(fib(10))                    # 55
```

### Booleans & Comparisons

```
let a = true
let b = false

if a and not b {
    print("both true")
}

if x > 5 or y < 10 {
    print("at least one")
}
```

### Comments

```
# This is a single-line comment
/*
  Multi-line
  comment
*/
```

### Imports

```
import math
import string
import json
import filesystem
import datetime
import os

print(math.sqrt(16))              # 4.0
print(string.upper("hello"))      # HELLO
```

---

## CLI Reference

### cobrac — Compiler

```bash
cobrac file.cobra                 # Compile and run
cobrac file.cobra -o output.py    # Save generated Python
cobrac -t c file.cobra -o out.c   # Generate C code
cobrac --help                     # Show help
```

### cobra — Shell

```bash
cobra                             # Start REPL
cobra file.cobra                  # Run a file
cobra --version                   # Show version
```

Inside the REPL:

```
cobra> print("Hello")
cobra> !ls                        # Run shell command
cobra> exit                       # Quit
```

### cobrapkg — Package Manager

```bash
cobrapkg init                     # Create cobra-pkg.json
cobrapkg install <name>           # Install a package
cobrapkg uninstall <name>         # Remove a package
cobrapkg list                     # List installed packages
```

### cobraos — OS Management

```bash
cobraos info                      # Show system info
cobraos neofetch                  # Display neofetch
cobraos version                   # Show version
```

---

## Standard Library

| Module     | Contents |
|------------|----------|
| `math`     | `sqrt`, `sin`, `cos`, `tan`, `abs`, `floor`, `ceil`, `round`, `pow`, `log`, `exp`, `pi`, `e`, `min`, `max` |
| `string`   | `upper`, `lower`, `split`, `join`, `replace`, `contains`, `length`, `reverse`, `repeat`, `trim`, `substring`, `starts_with`, `ends_with`, `pad_left`, `pad_right`, `is_digit`, `is_alpha`, `capitalize` |
| `json`     | `parse`, `stringify`, `read_file`, `write_file` |
| `filesystem` | `read`, `write`, `exists`, `is_file`, `is_dir`, `list_dir`, `mkdir`, `remove`, `copy`, `rename`, `cwd`, `chdir`, `size`, `abspath`, `join_path` |
| `datetime` | `now`, `today`, `parse`, `format`, `year`, `month`, `day`, `hour`, `minute`, `second`, `add_days`, `add_hours`, `seconds_between`, `days_between` |
| `os`       | `name`, `pid`, `cpu_count`, `hostname`, `user`, `env`, `exec`, `sleep`, `exit`, `args`, `cwd` |

---

## Examples

| File | Description |
|------|-------------|
| `examples/hello.cobra` | Hello World with variables |
| `examples/features.cobra` | All language features |
| `examples/edge_cases.cobra` | Nested if/else, recursion, precedence |
| `examples/numeric.cobra` | Pure numeric (for C codegen) |
| `examples/stdlib_demo.cobra` | Standard library demo |
| `examples/json_demo.cobra` | JSON parsing/stringify |
| `examples/neofetch.cobra` | CobraOS neofetch |
| `examples/cobraos-init.cobra` | OS login banner |

---

## Project Structure

```
Cobra/
├── cobra/
│   ├── compiler/        # Lexer, Parser, AST, Codegen (Python + C)
│   ├── runtime/         # Built-in functions
│   ├── stdlib/          # math, string, json, filesystem, datetime, os
│   ├── cli/             # cobrac, cobra, cobrapkg, cobraos entry points
│   ├── pkgmgr/          # Package manager logic
│   └── os/              # CobraOS deployment utilities
├── examples/            # Example .cobra files
├── scripts/             # Shell scripts (deploy, tunnel)
├── docs/                # Documentation
├── tests/               # Test files
├── pyproject.toml       # Python package config
└── cobra-pkg.json       # Cobra package manifest
```

---

## Deploying CobraOS

```bash
# Deploy to a VPS (Ubuntu Server)
./scripts/deploy.sh root@your-server-ip

# Set up an SSH tunnel
./scripts/tunnel.sh root@your-server-ip 8080 80

# SSH in and enjoy
ssh root@your-server-ip
```

See `docs/deployment.md` for details.

---

## Building From Source

```bash
git clone https://github.com/Amitk003/Cobra.git
cd Cobra
pip install -e .
```

Requires Python 3.10+. For C codegen, install GCC (MinGW on Windows, build-essential on Linux).

---

## License

MIT
