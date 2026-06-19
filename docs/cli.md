# Cobra CLI Reference

## cobrac — The Compiler

Compile and run Cobra source files.

### Usage

```
cobrac [options] <file>
```

### Options

| Flag | Description |
|------|-------------|
| `-o`, `--output <path>` | Save generated code to file |
| `-t`, `--target <py\|c>` | Output target: `py` (default) or `c` |
| `--help` | Show help message |

### Examples

```bash
# Compile and run
cobrac hello.cobra

# Save generated Python
cobrac hello.cobra -o output.py

# Generate C code and try to compile
cobrac -t c numeric.cobra -o program.c

# With GCC installed, also compiles to program.exe
```

### Targets

**py** (default): Generates Python code and executes it via `exec()`.  
**c**: Generates C code with embedded runtime helpers. If `-o file.c` is given, attempts to run `gcc -o file file.c -lm`.

---

## cobra — The Shell

Interactive REPL and script runner.

### Usage

```
cobra [options] [file]
```

### Options

| Flag | Description |
|------|-------------|
| `--version`, `-v` | Show version |
| `--help`, `-h` | Show help |

### REPL Commands

| Command | Description |
|---------|-------------|
| `exit` | Exit the REPL |
| `!<command>` | Run a system shell command |

### Examples

```bash
# Start REPL
cobra

# Run a file
cobra examples/hello.cobra

# With piped input
echo 'print("hi")' | cobra
```

### REPL State

The REPL maintains state between commands. Variables and functions defined in one line are available in subsequent lines.

```
cobra> let x = 10
cobra> print(x + 5)
15
cobra> x = 20
cobra> print(x)
20
cobra> exit
```

---

## cobrapkg — Package Manager

Install, remove, and list Cobra packages.

### Usage

```
cobrapkg <command> [package]
```

### Commands

| Command | Description |
|---------|-------------|
| `init` | Create `cobra-pkg.json` in current directory |
| `install <name>` | Install a package (name or GitHub URL) |
| `uninstall <name>` | Remove an installed package |
| `list` | Show installed packages |

### Examples

```bash
# Initialize project
cobrapkg init

# Install from GitHub
cobrapkg install username/repo

# List installed
cobrapkg list

# Remove
cobrapkg uninstall repo
```

### Package Storage

Packages are installed to `~/.cobra/packages/<name>/`. The compiler resolves `import <name>` by checking:
1. Standard library modules
2. Installed packages in `~/.cobra/packages/`

---

## cobraos — OS Management

System information and CobraOS utilities.

### Usage

```
cobraos <command>
```

### Commands

| Command | Description |
|---------|-------------|
| `info` | Show system info (OS, host, user) |
| `neofetch` | Display ASCII art system info |
| `version` | Show CobraOS version |

### Examples

```bash
cobraos info
cobraos neofetch
cobraos version
```

---

## Development Scripts

### Deploy to VPS

```bash
./scripts/deploy.sh user@host
```

Installs Cobra on a Ubuntu Server VPS, sets up the cobra shell, and configures the login banner. See `docs/deployment.md`.

### SSH Tunnel

```bash
./scripts/tunnel.sh user@host [local-port] [remote-port]
```

Creates a forward SSH tunnel from localhost to the VPS.
