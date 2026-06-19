# Cobra Language Reference

## Overview

Cobra is a statically-scoped, imperative programming language with C-style block syntax. It compiles to Python or C.

---

## 1. Lexical Structure

### Comments

```
# Single-line comment
/* Multi-line
   comment */
```

### Identifiers

Start with a letter or underscore, followed by letters, digits, or underscores.

```
myVar
_count
fibonacci_sequence_2026
```

### Keywords

```
let, if, else, while, for, in, func, return, import,
true, false, and, or, not
```

### Literals

| Type | Examples |
|------|----------|
| Integer | `0`, `42`, `-5` |
| Float | `3.14`, `-0.5`, `10.0` |
| String | `"hello"`, `'world'` (double or single quotes) |
| Boolean | `true`, `false` |

### Operators

| Category | Operators |
|----------|-----------|
| Arithmetic | `+`, `-`, `*`, `/` |
| Comparison | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| Logical | `and`, `or`, `not` (word-style) |
| Assignment | `=` |
| Range | `..` (exclusive: `0..5` → 0,1,2,3,4) |
| Member access | `.` |

### Precedence (highest to lowest)

1. `()` — grouping, function call
2. `.` — member access
3. `not`, unary `-`
4. `*`, `/`
5. `+`, `-`
6. `==`, `!=`, `<`, `>`, `<=`, `>=`
7. `and`
8. `or`
9. `=` — assignment

---

## 2. Variables

### Declaration with `let`

```
let name = "Cobra"
let x = 10
let pi = 3.14159
let flag = true
```

### Reassignment

```
x = x + 1
name = "Python"
```

---

## 3. Control Flow

### If / Else

```
if condition {
    # body
}

if condition {
    # body
} else {
    # else body
}
```

Nested if-else:

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

### While Loop

```
let i = 0
while i < 10 {
    print(i)
    i = i + 1
}
```

### For Loop

Iterates over an exclusive range `[start, end)`:

```
for i in 0..5 {
    print(i)    # 0, 1, 2, 3, 4
}
```

---

## 4. Functions

### Definition

```
func add(a, b) {
    return a + b
}
```

### Return

```
func max(a, b) {
    if a > b {
        return a
    }
    return b
}
```

Functions without an explicit `return` return `0`.

### Recursion

```
func fib(n) {
    if n <= 1 {
        return n
    }
    return fib(n - 1) + fib(n - 2)
}
```

### Call

```
let result = add(3, 4)
print(add(10, 20))
print(fib(10))    # 55
```

---

## 5. Built-in Functions

| Function | Description |
|----------|-------------|
| `print(x)` | Print value to stdout |
| `input(prompt)` | Read a line from stdin |
| `str(x)` | Convert to string |
| `int(x)` | Convert to integer |
| `float(x)` | Convert to float |
| `bool(x)` | Convert to boolean |
| `len(x)` | Get length |
| `type(x)` | Return type name |
| `range(start, end)` | Create a range list |

---

## 6. Imports

```
import math
import string
import json
import filesystem
import datetime
import os
```

Imported modules are accessed via dot notation:

```
math.sqrt(16)
string.upper("hello")
json.parse('{"a": 1}')
filesystem.read("file.txt")
datetime.now()
os.hostname()
```

---

## 7. Grammar (EBNF)

```
program        = { statement }
statement      = let_stmt | if_stmt | while_stmt | for_stmt
               | func_stmt | return_stmt | import_stmt
               | block | assign_stmt | expr_stmt

let_stmt       = "let" ident "=" expression
assign_stmt    = ident "=" expression
if_stmt        = "if" expression block [ "else" block ]
while_stmt     = "while" expression block
for_stmt       = "for" ident "in" expression ".." expression block
func_stmt      = "func" ident "(" [ ident { "," ident } ] ")" block
return_stmt    = "return" expression
import_stmt    = "import" ident
block          = "{" { statement } "}"

expression     = or_expr
or_expr        = and_expr { "or" and_expr }
and_expr       = comparison { "and" comparison }
comparison     = addition { ("=="|"!="|"<"|">"|"<="|">=") addition }
addition       = multiplication { ("+"|"-") multiplication }
multiplication = unary { ("*"|"/") unary }
unary         = ("-"|"not") unary | primary
primary        = number | string | bool | ident [ postfix ]
               | "(" expression ")"
postfix        = "." ident | "(" [ expression { "," expression } ] ")"
```
