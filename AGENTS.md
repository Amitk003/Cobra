# Project Cobra — Agent Instructions

## Build System

```powershell
pip install -e .
python -m cobra.cli.cobrac examples/hello.cobra
```

## Project Structure

```
cobra/
├── compiler/     # Lexer → Parser → AST → Codegen
├── runtime/      # Built-in functions
├── stdlib/       # Standard library modules
├── cli/          # cobrac, cobra, cobrapkg entry points
└── pkgmgr/       # Package manager
```

## Git Workflow

- Branch per phase: `phase-0`, `phase-1`, etc.
- Commit messages: `phase-N: description`
- Push after each phase milestone

## Architecture Notes

- Compiler generates Python code (Phase 1-7), later targets standalone binary
- `print("hi")` parses as a `CALL` node to `print`
- All codegen visitors that produce expression values **return** strings
- Statement visitors **emit** via `self.emit()`
- Expression statements (like bare calls) rely on `_visit_program` checking return values
- Member access (`math.sqrt`) uses `MEMBER_ACCESS` AST node with dotted string building
- Single and double-quoted strings are both supported in the lexer
- Runtime builtins are imported via `from cobra.runtime.builtins import *` when needed
- Standard library modules are in `cobra/stdlib/` and imported as `import cobra.stdlib.<name> as <name>`
- C codegen in `codegen_c.py` uses type tracking via `_is_number_node()` to determine string vs numeric
- C codegen generates a complete C file with embedded runtime helpers (str concat, double-to-str)
- `cobrac --target c` flag switches between Python and C codegen
- Adding `*.c` and `*.exe` to .gitignore keeps generated files out of version control

## Next Phase Tasks

When building the next phase:
1. Create branch `phase-N`
2. Implement features
3. Write tests in `tests/`
4. Update `examples/`
5. Commit with `phase-N: description`
6. Push branch

## Testing

Run: `python -m cobra.cli.cobrac examples/<file>.cobra`
