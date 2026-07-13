# Understanding Python Files, Folders, Packages and Imports

## 1. A single Python file

Structure:

```text
hello.py
```

Run:

```bash
python hello.py
```

Python executes the file directly.

---

## 2. Multiple files in the same folder

Structure:

```text
A/
├── a.py
└── b.py
```

Suppose `b.py` needs code from `a.py`:

```python
# b.py
from a import greet
```

Run:

```bash
cd A
python b.py
```

Since `a.py` is in the same folder, Python can find it.

---

## 3. Files inside another folder

Structure:

```text
A/
├── a.py
└── B/
    └── b.py
```

Suppose `b.py` needs code from `a.py`:

```python
# b.py
from a import greet
```

Running:

```bash
python B/b.py
```

may fail because Python starts searching from inside folder `B`.

From Python's perspective:

```text
B/
└── b.py
```

`a.py` appears to be missing.

---

## 4. Introducing Packages

Structure:

```text
A/
├── a.py
└── B/
    ├── __init__.py
    └── b.py
```

The file:

```text
__init__.py
```

tells Python:

> "B is a Python package."

This allows Python to understand module paths.

---

## 5. Running a module

Move to the root folder:

```bash
cd A
```

Run:

```bash
python -m B.b
```

Meaning:

> Start from root folder `A`,
> enter package `B`,
> execute module `b.py`.

---

## 6. Nested packages

Structure:

```text
A/
├── a.py
└── B/
    ├── __init__.py
    ├── b.py
    └── C/
        ├── __init__.py
        └── c.py
```

To run `c.py`:

```bash
cd A
python -m B.C.c
```

Python reads this as:

```text
Root
 ↓
B package
 ↓
C package
 ↓
c module
```

---

## 7. Rule for `python -m`

General format:

```bash
python -m package.subpackage.module
```

Examples:

```bash
python -m B.b
python -m B.C.c
python -m X.Y.Z.file
```

---

## 8. The Root Folder

The root folder is the folder you stand in before running the command.

Example:

```bash
cd A
python -m B.C.c
```

Here:

```text
A
```

is the root folder.

Python starts searching from the root folder and follows the package path after `-m`.

---

## 9. Purpose of `__init__.py`

`__init__.py` tells Python:

> "This folder is a package."

Without it, Python treats the folder as an ordinary folder.

With it, Python treats the folder as something that can participate in imports and module execution.

---

## 10. Mental Model

Think of Python as navigating a building:

```text
Root/
└── Floor/
    └── Room/
        └── File.py
```

The `-m` command gives Python directions from the building entrance to the file that should be executed.
