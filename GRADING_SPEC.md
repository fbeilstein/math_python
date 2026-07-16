# Test & Grading Decoupling Specification

> **Purpose:** This document defines the standard procedure for separating unit tests from the student-facing UX in any problem set. Point the AI assistant to this file and say _"apply GRADING_SPEC.md to `<problem>`"_ to execute the refactoring.

---

## 1. Problem Anatomy (Target State)

After applying this spec, every problem directory should look like:

```
<problem_root>/
├── implementation_tasks.py    # Student writes code here. Has __main__ for self-testing.
├── lab_dashboard.py           # Student runs this. NO tests, NO green/red lights.
├── levels/
│   ├── base_level.py          # Graphics base class only. NO unittest.TestCase.
│   ├── level_1_<name>.py      # Graphics + sandbox. NO TestLevel* class.
│   └── ...
├── tests/                     # INSTRUCTOR ONLY. Excluded from student bundle.
│   ├── __init__.py
│   ├── test_level_1.py        # TestLevel* classes extracted from levels/
│   ├── test_level_2.py
│   └── ...
├── description/
│   └── problem.tex            # Updated: no references to unit tests in UX
└── requirements.txt
```

---

## 2. Extract Tests → `tests/`

### What to move

Every `class TestLevel*(unittest.TestCase)` from every `level_*.py` file.

### Template: `tests/test_level_N.py`

```python
import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks


class TestLevelN<Name>(unittest.TestCase):
    # Paste test methods here verbatim from the original level_*.py
    pass


if __name__ == '__main__':
    unittest.main()
```

### Template: `tests/__init__.py`

```python
# Test suite for grading. Not included in student bundle.
```

### Clean up `level_*.py`

After extracting:
1. **Remove** the `TestLevel*` class entirely.
2. **Remove** `import unittest` if no longer used.
3. **Simplify** the `if __name__ == '__main__'` block — remove the `--no-graphics` branch, keep only visual execution:

```python
if __name__ == '__main__':
    lvl = Level1Line()
    lvl.draw()
    plt.show()
```

### Special: `BaseLevel(unittest.TestCase)` pattern (QR-style)

If `base_level.py` defines `class BaseLevel(unittest.TestCase)`:
1. Change to `class BaseLevel:` (or remove if empty after change)
2. In `tests/`, each test file should inherit from `unittest.TestCase` directly

### Special: Tests in `implementation_tasks.py` (autodiff-style)

Move the test class to `tests/test_<name>.py`. Keep `__main__` block (see §3).

---

## 3. Add `__main__` to `implementation_tasks.py`

Append this block to **every** `implementation_tasks.py` (even those with no existing tests):

```python
# =============================================================================
#  SELF-TESTING (add your own tests below)
# =============================================================================
if __name__ == '__main__':
    import unittest
    # Add your own unittest.TestCase classes here, then run:
    #     python implementation_tasks.py
    unittest.main(verbosity=2)
```

**Rules:**
- Place after all function definitions, at the very bottom of the file
- Do NOT add `import unittest` at the top of the file — keep it inside the `__main__` guard so it doesn't pollute the module namespace for students who don't use it

---

## 4. Strip Tests from Dashboard

### Remove

| Element | What to delete |
|---------|---------------|
| `import unittest` | Top-level import |
| `self.status_indicators` | Dict creation + all references |
| Status indicator Canvas widgets | The `Canvas(frame, width=15, ...)` + `create_oval` for each level |
| `refresh_tests()` / `run_all_tests()` | Entire method definition |
| All calls to `self.refresh_tests()` | In `__init__`, `reload_and_retest`, `switch_sandbox` |
| "🔄 Reload & Retest" button | The `tk.Button(... text="🔄 Reload & Retest" ...)` |
| "↻ Run All Tests" button | QR dashboard variant |
| `self.status_labels` | QR dashboard variant |

### Keep

| Element | Why |
|---------|-----|
| Level-switch buttons (L1, L2, ...) | Sandbox navigation |
| `force_reload_core()` | Hot-reload during development |
| "🚀 Run Main Simulation" / "⭐ MAIN DEMO ⭐" | Main simulation launcher |
| `switch_sandbox()` / `launch_level()` | Core functionality (remove only the `refresh_tests` call inside it) |

### Simplify `reload_and_retest`

Rename to `reload_code` (or similar). Keep `force_reload_core()` + module reloads + `switch_sandbox()`. Remove the `self.refresh_tests()` call. Update the remaining button text if one exists (e.g., keep a "🔄 Reload" button but remove the "Retest" part).

---

## 5. Update `prepare_release.sh`

Add after `cd "$release_dir"`, before the zip step:

```bash
# Remove grading infrastructure from student bundle
rm -rf "$release_dir/tests"
```

The `grade.py` at the repo root is already outside the problem folder and won't be picked up by `git archive HEAD "$problem"`.

---

## 6. Update `description/problem.tex`

### File table (Problem 0)

Replace the `levels/level_*.py` description. Change from:

```latex
\lstinline|levels/level_*.py| & Unittests and graphical representation for each
specific problem. \textbf{Can be run standalone.} You can use
\lstinline|python levels/level_*.py| for the graphical debugger or
\lstinline|python levels/level_*.py --no-graphics| for unittests only. \\
```

To:

```latex
\lstinline|levels/level_*.py| & Interactive graphical sandbox for each
specific problem. \textbf{Can be run standalone} with
\lstinline|python levels/level_*.py| for visual debugging. \\
```

### `implementation_tasks.py` description

Add self-testing reminder and the optional self-testing block:

```latex
\lstinline|implementation_tasks.py| & \textcolor{red}{Here you write your code.}
You can add your own \lstinline|unittest.TestCase| classes at the bottom
and run \lstinline|python implementation_tasks.py| to execute them. \\
```

Right after the `\end{lstlisting}` for `implementation_tasks.py`, insert this standard explanation:

```latex
\subsubsection*{Self-Testing (Optional)}
At the bottom of \lstinline|implementation_tasks.py|, you will find a block that looks like this:
\begin{lstlisting}[language=Python]
if __name__ == '__main__':
    import unittest
    # Add your own unittest.TestCase classes here...
    unittest.main(verbosity=2)
\end{lstlisting}
This allows you to write your own automated unit tests to verify your code before running the visual dashboard. If you'd like to test your functions with specific inputs, simply define a class inheriting from \lstinline|unittest.TestCase| above the \lstinline|unittest.main()| call. For example, if you wanted to test simple math:
\begin{lstlisting}[language=Python]
class TestMyMath(unittest.TestCase):
    def test_addition(self):
        result = 2 + 2
        self.assertEqual(result, 4, "Addition is broken!")
\end{lstlisting}
You can run these tests anytime by executing \lstinline|python implementation_tasks.py| in your terminal. This is completely optional, but highly recommended for debugging tricky edge cases.
```

### Per-problem "Test:" paragraphs

Replace references to "Reload & Retest" and "bulb becomes green" with:

```latex
\textbf{Test:} Use the interactive sandbox to verify your implementation
visually. Drag elements on the scene and observe behavior.
```

---

## 7. Grading Script (`grade.py`)

Lives at the **repo root**. Single script for all problems.

### Usage

```bash
# Grade all students for one problem
python grade.py optical_problem submissions/optical/

# With verbose output
python grade.py optical_problem submissions/optical/ --verbose
```

### Behavior

1. Resolves the problem directory (searches `*/practice/*/`, `*/optional/*/`, `optional/*/`)
2. Finds `tests/` inside the problem directory
3. For each `implementation_tasks.py` in the submissions directory:
   - Temporarily patches `sys.modules` to use the student's file
   - Runs `unittest.TestLoader().discover('tests/')` in an isolated context
   - Collects pass/fail/error per test class (= per level)
   - Restores the original module state
4. Prints a table:

```
GRADING: optical_problem
─────────────────────────────────────────────────
Student          L1    L2    L3    L4    L5    L6    L7    TOTAL
─────────────────────────────────────────────────
alice.py         2/2   1/3   4/4   2/2   2/2   3/3   2/2   16/18
bob.py           2/2   3/3   4/4   2/2   2/2   3/3   2/2   18/18
carol.py         CRASH                                      0/18
─────────────────────────────────────────────────
```

### Error handling

- Student file with syntax error → report "CRASH" with error message in verbose mode
- Student file missing a function → individual test failures (not crash)
- Test infrastructure error → abort with clear message

---

## 8. Checklist: Applying This Spec to a Problem

Use this checklist when executing the refactoring for a specific problem:

- [ ] Create `tests/` directory with `__init__.py`
- [ ] For each `level_*.py` with a `TestLevel*` class:
  - [ ] Create `tests/test_level_*.py` with the extracted class
  - [ ] Remove the class from `level_*.py`
  - [ ] Remove `import unittest` from `level_*.py` if no longer used
  - [ ] Simplify `__main__` block in `level_*.py`
- [ ] Update dashboard:
  - [ ] Remove `import unittest`
  - [ ] Remove status indicators (Canvas + oval)
  - [ ] Remove `refresh_tests()` / `run_all_tests()` method
  - [ ] Remove all calls to the removed method
  - [ ] Remove "Reload & Retest" / "Run All Tests" button
  - [ ] Rename `reload_and_retest` → `reload_code` and simplify
- [ ] Add `__main__` block to `implementation_tasks.py`
- [ ] Update `description/problem.tex`:
  - [ ] Update file table
  - [ ] Update "Test:" paragraphs
- [ ] Verify: `python -m unittest discover tests/` passes with solution file
- [ ] Verify: dashboard launches without errors
- [ ] Verify: `prepare_release.sh` produces clean bundle without `tests/`

---

## 9. Problems Already Conforming / Exempt

| Problem | Status |
|---------|--------|
| `lsh_problem` | No levels, no tests — only needs `__main__` in tasks |
| `esher_droste_problem` | No levels, no tests — only needs `__main__` in tasks |
| `stability_problem` | No dashboard, no tests — only needs `__main__` in tasks |
| `tron_problem` | No dashboard, no tests — only needs `__main__` in tasks |
| `biochem_problem` | Has levels dir (empty), no tests — only needs `__main__` in tasks |
| `fractals_problem` | Has levels, no tests — only needs `__main__` in tasks |
| `kinematics_problem` | Has levels, no tests — only needs `__main__` in tasks |
| `evolutionary_game_problem` | Has levels, no tests — only needs `__main__` in tasks |
| `markov_chain_problem` | Has levels, no tests — only needs `__main__` in tasks |
| `spectral_graph_problem` | Has levels, no tests — only needs `__main__` in tasks |
