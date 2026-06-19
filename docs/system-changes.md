# System Changes Log

Records all software installations, modifications, and downloads made on this PC during the Cobra project build.

---

## 1. Pre-existing Software

The following tools were already present on the system and were **used but not installed**:

| Tool | Version | Path |
|------|---------|------|
| Git | 2.54.0.windows.1 | System PATH |
| Python | 3.11 (pythoncore-3.11-64) | `C:\Users\amitk\AppData\Local\Python\pythoncore-3.11-64\` |
| pip | 24.0 | Bundled with Python |
| PowerShell | 5.1 | Built into Windows |
| winget | Windows Package Manager | Built into Windows |

---

## 2. Python Packages Installed

### New installation

| Package | Type | Command | Location |
|---------|------|---------|----------|
| **cobra** (v0.1.0) | Editable dev install | `pip install -e .` | `C:\Users\amitk\Documents\Projects\Cobra\` (source) |

### CLI entry points registered

| Command | Installed to |
|---------|-------------|
| `cobrac.exe` | `C:\Users\amitk\AppData\Local\Python\pythoncore-3.11-64\Scripts\` |
| `cobra.exe` | Same |
| `cobrapkg.exe` | Same |
| `cobraos.exe` | Same |

**Note**: The Scripts directory is not on the system PATH. Commands are run via `python -m cobra.cli.<name>`.

---

## 3. Files Created / Modified

### Git Repository

| Action | Detail |
|--------|--------|
| Initialized | `C:\Users\amitk\Documents\Projects\Cobra\.git\` |
| Remote added | `origin → https://github.com/Amitk003/Cobra.git` |
| Branches pushed | `main`, `phase-2`, `phase-3`, `phase-5`, `phase-6`, `phase-7`, `phase-8` |

### Project Root Files

| File | Size | Description |
|------|------|-------------|
| `pyproject.toml` | ~600 B | Python package config with entry points |
| `.gitignore` | ~150 B | Git ignore rules |
| `AGENTS.md` | ~1.5 KB | Build instructions for future agent sessions |
| `README.md` | ~5 KB | Full project documentation |
| `cobra-pkg.json` | ~80 B | Cobra package manifest |

### Source Files: Compiler (`cobra/compiler/`)

| File | Lines | Description |
|------|-------|-------------|
| `ast.py` | ~140 | AST node definitions (22 node types) |
| `lexer.py` | ~120 | Tokenizer with regex patterns |
| `parser.py` | ~260 | Recursive descent parser |
| `codegen.py` | ~170 | Python code generator |
| `codegen_c.py` | ~240 | C code generator |

### Source Files: Runtime (`cobra/runtime/`)

| File | Lines | Description |
|------|-------|-------------|
| `builtins.py` | ~50 | Cobra runtime built-in functions |
| `__init__.py` | ~5 | Re-exports builtins |

### Source Files: Standard Library (`cobra/stdlib/`)

| File | Lines | Description |
|------|-------|-------------|
| `math.py` | ~85 | Mathematical functions and constants |
| `string.py` | ~95 | String manipulation functions |
| `json_.py` | ~25 | JSON parse/stringify |
| `filesystem.py` | ~90 | File system operations |
| `datetime.py` | ~85 | Date/time functions |
| `os.py` | ~50 | OS interface functions |

### Source Files: CLI (`cobra/cli/`)

| File | Lines | Description |
|------|-------|-------------|
| `cobrac.py` | ~95 | Compiler CLI |
| `cobra.py` | ~95 | Shell/REPL CLI |
| `cobrapkg.py` | ~30 | Package manager CLI |
| `cobraos.py` | ~45 | OS management CLI |

### Source Files: Package Manager (`cobra/pkgmgr/`)

| File | Lines | Description |
|------|-------|-------------|
| `manager.py` | ~130 | Package install/uninstall/list logic |

### Source Files: OS (`cobra/os/`)

| File | Lines | Description |
|------|-------|-------------|
| `deploy.py` | ~85 | VPS deployment automation |

### Example Files (`examples/`)

| File | Lines | Description |
|------|-------|-------------|
| `hello.cobra` | ~8 | Hello World with variables |
| `features.cobra` | ~40 | All language features demo |
| `edge_cases.cobra` | ~55 | Recursion, nesting, shadowing |
| `numeric.cobra` | ~20 | Pure numeric (C codegen test) |
| `stdlib_demo.cobra` | ~40 | Standard library demo |
| `json_demo.cobra` | ~8 | JSON parsing demo |
| `neofetch.cobra` | ~20 | CobraOS system info display |
| `cobraos-init.cobra` | ~25 | OS login banner |

### Documentation (`docs/`)

| File | Lines | Description |
|------|-------|-------------|
| `language.md` | ~200 | Full language reference & grammar |
| `cli.md` | ~120 | CLI commands reference |
| `stdlib.md` | ~250 | Stdlib API reference |
| `deployment.md` | ~150 | CobraOS VPS deployment guide |
| `system-changes.md` | This file | System changes log |

### Shell Scripts (`scripts/`)

| File | Lines | Description |
|------|-------|-------------|
| `deploy.sh` | ~85 | VPS deployment script |
| `tunnel.sh` | ~30 | SSH tunnel script |

---

## 4. Attempted Installations (Failed)

| Package | Method | Result |
|---------|--------|--------|
| **GCC** (MinGW) | `winget install --id GNU.GCC` | Failed — package not found in winget repository |

The C codegen target (`cobrac -t c`) requires GCC to compile `.c` files to binaries. Without GCC, the compiler still generates correct C code but cannot compile it.

---

## 5. No Uninstallations

No software was uninstalled or removed from the system during this project.

---

## 6. System State Summary

| Aspect | Before | After |
|--------|--------|-------|
| Python packages | System default | +1 (`cobra` dev install) |
| Git repos | None in Cobra dir | Initialized, linked to GitHub |
| PATH changes | None | Scripts dir not on PATH (not modified) |
| System software | Standard Windows | Unchanged |
| Files in Cobra dir | 0 (empty) | ~50 files, ~2500 lines |
