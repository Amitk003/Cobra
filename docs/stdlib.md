# Cobra Standard Library Reference

## Usage

```cobra
import math
import string
import json
import filesystem
import datetime
import os
```

All modules are accessed via dot notation:

```cobra
math.sqrt(16)
string.upper("hello")
```

---

## `math` — Mathematical Functions

### Constants

| Name | Value |
|------|-------|
| `math.pi` | 3.141592653589793 |
| `math.e` | 2.718281828459045 |
| `math.tau` | 6.283185307179586 |
| `math.inf` | Infinity |
| `math.nan` | NaN |

### Functions

| Function | Description |
|----------|-------------|
| `sqrt(x)` | Square root |
| `sin(x)` | Sine (radians) |
| `cos(x)` | Cosine (radians) |
| `tan(x)` | Tangent (radians) |
| `abs(x)` | Absolute value |
| `floor(x)` | Round down |
| `ceil(x)` | Round up |
| `round(x, n)` | Round to n decimals |
| `pow(x, y)` | x raised to y |
| `log(x, base)` | Logarithm (base defaults to e) |
| `log10(x)` | Base-10 logarithm |
| `exp(x)` | e raised to x |
| `degrees(x)` | Radians to degrees |
| `radians(x)` | Degrees to radians |
| `min(a, *args)` | Minimum value |
| `max(a, *args)` | Maximum value |
| `is_nan(x)` | Check if NaN |
| `is_inf(x)` | Check if infinite |

### Examples

```cobra
print(math.sqrt(16))        # 4.0
print(math.floor(3.7))      # 3
print(math.ceil(3.2))       # 4
print(math.pow(2, 10))      # 1024
print(math.pi)              # 3.141592653589793
```

---

## `string` — String Operations

### Functions

| Function | Description |
|----------|-------------|
| `upper(s)` | Convert to uppercase |
| `lower(s)` | Convert to lowercase |
| `split(s, sep)` | Split string into list |
| `join(parts, glue)` | Join list with glue |
| `replace(s, old, new)` | Replace substrings |
| `contains(s, substr)` | Check if substring exists |
| `starts_with(s, prefix)` | Check prefix |
| `ends_with(s, suffix)` | Check suffix |
| `trim(s)` | Remove whitespace |
| `trim_left(s)` | Remove leading whitespace |
| `trim_right(s)` | Remove trailing whitespace |
| `length(s)` | String length |
| `substring(s, start, end)` | Extract substring |
| `index_of(s, substr)` | Find substring position |
| `to_chars(s)` | Convert to character list |
| `capitalize(s)` | Capitalize first letter |
| `reverse(s)` | Reverse string |
| `repeat(s, count)` | Repeat string |
| `is_digit(s)` | Check if all digits |
| `is_alpha(s)` | Check if all letters |
| `is_alnum(s)` | Check if alphanumeric |
| `is_space(s)` | Check if whitespace |
| `pad_left(s, width, char)` | Left-pad string |
| `pad_right(s, width, char)` | Right-pad string |

### Examples

```cobra
print(string.upper("hello"))            # HELLO
print(string.contains("hello", "ell"))  # true
print(string.reverse("cobra"))          # arboc
print(string.repeat("hi ", 3))          # hi hi hi
print(string.trim("  hello  "))         # hello
```

---

## `json` — JSON Processing

### Functions

| Function | Description |
|----------|-------------|
| `parse(s)` | Parse JSON string to object |
| `stringify(obj, pretty)` | Convert object to JSON string |
| `read_file(path)` | Read and parse JSON file |
| `write_file(path, obj, pretty)` | Write object as JSON file |

### Examples

```cobra
import json

let data = json.parse('{"name": "Cobra", "year": 2026}')
print(json.stringify(data))
```

---

## `filesystem` — File Operations

### Functions

| Function | Description |
|----------|-------------|
| `read(path)` | Read file contents |
| `write(path, content)` | Write to file |
| `read_lines(path)` | Read lines into list |
| `write_lines(path, lines)` | Write list of lines |
| `append(path, content)` | Append to file |
| `exists(path)` | Check if path exists |
| `is_file(path)` | Check if path is a file |
| `is_dir(path)` | Check if path is a directory |
| `list_dir(path)` | List directory contents |
| `mkdir(path)` | Create directory (recursive) |
| `remove(path)` | Delete file or directory |
| `rename(src, dst)` | Rename/move |
| `copy(src, dst)` | Copy file |
| `size(path)` | Get file size in bytes |
| `abspath(path)` | Get absolute path |
| `basename(path)` | Get file name |
| `dirname(path)` | Get directory name |
| `join_path(*parts)` | Join path components |
| `cwd()` | Get current working directory |
| `chdir(path)` | Change directory |

### Examples

```cobra
import filesystem

let content = filesystem.read("file.txt")
filesystem.write("output.txt", "Hello")
print(filesystem.cwd())
print(filesystem.exists("."))  # true
```

---

## `datetime` — Date & Time

### Functions

| Function | Description |
|----------|-------------|
| `now()` | Current datetime as ISO string |
| `today()` | Current date as ISO string |
| `timestamp()` | Unix timestamp |
| `parse(s, fmt)` | Parse date string |
| `format(s, fmt)` | Format datetime string |
| `year(s)` | Extract year |
| `month(s)` | Extract month (1-12) |
| `day(s)` | Extract day (1-31) |
| `hour(s)` | Extract hour (0-23) |
| `minute(s)` | Extract minute (0-59) |
| `second(s)` | Extract second (0-59) |
| `add_days(s, n)` | Add n days |
| `add_hours(s, n)` | Add n hours |
| `add_minutes(s, n)` | Add n minutes |
| `seconds_between(a, b)` | Seconds between two datetimes |
| `days_between(a, b)` | Days between two dates |

### Examples

```cobra
import datetime

print(datetime.now())             # 2026-06-19T16:00:00.000000
print(datetime.year())            # 2026
print(datetime.month())           # 6
print(datetime.day())             # 19
```

---

## `os` — Operating System

### Functions

| Function | Description |
|----------|-------------|
| `name()` | OS name (posix, nt, etc.) |
| `pid()` | Current process ID |
| `cpu_count()` | Number of CPU cores |
| `hostname()` | System hostname |
| `user()` | Current username |
| `env(key, default)` | Get environment variable |
| `set_env(key, value)` | Set environment variable |
| `exec(cmd)` | Execute shell command |
| `exit(code)` | Exit process |
| `sleep(seconds)` | Sleep for N seconds |
| `args()` | Command-line arguments |
| `getenv(key, default)` | Alias for env |

### Examples

```cobra
import os

print(os.name())                  # nt, posix, etc.
print(os.hostname())              # my-pc
print(os.cpu_count())             # 12
print(os.user())                  # amitk
os.exec("echo hello from cobra")
```
