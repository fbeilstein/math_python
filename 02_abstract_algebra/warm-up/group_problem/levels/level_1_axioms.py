"""Level 1: Axiom Checker — interactive editable multiplication table grid.

User enters n, gets an n×n grid of entry cells. Fill it in and get
real-time feedback: closure, associativity, identity, inverses.
Preset buttons load known examples instantly.
"""
import tkinter as tk
from levels.base_level import BaseLevel
import implementation_tasks as tasks

class MissingValue(int):
    def __eq__(self, other): return True
    def __ne__(self, other): return False
    def __hash__(self): return hash(0)

MISSING = MissingValue(999)

class RobustRow(list):
    def __getitem__(self, idx):
        if isinstance(idx, MissingValue):
            return MISSING
        try:
            return super().__getitem__(idx)
        except (IndexError, TypeError):
            return MISSING

class RobustTable(list):
    def __init__(self, data):
        super().__init__([RobustRow(row) for row in data])
    def __getitem__(self, idx):
        if isinstance(idx, MissingValue):
            return RobustRow([MISSING]*len(self))
        try:
            return super().__getitem__(idx)
        except (IndexError, TypeError):
            return RobustRow([MISSING]*len(self))


# Preloaded tables: (name, n, table)
PRESETS = [
    ("Group: ℤ₄ addition", 4, [[0,1,2,3],[1,2,3,0],[2,3,0,1],[3,0,1,2]]),
    ("Group: U(8) mult", 4, [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]]),
    ("Error: Not closed", 3, [[0,1,2],[1,2,3],[2,3,4]]),
    ("Error: No associativity", 3, [[0,1,2],[1,0,2],[2,2,0]]),
    ("Error: No identity", 3, [[0,0,0],[0,1,1],[0,1,1]]),
    ("Error: No inverses", 3, [[0,1,2],[1,1,1],[2,1,2]]),
]

COLORS = ['#58a6ff', '#7ee787', '#ffa657', '#d2a8ff', '#ff7b72', '#79c0ff', '#f0e68c', '#ff69b4']
BG_COLORS = ['#16202a', '#1a2a1a', '#2a1f0a', '#221a2a', '#2a1a1a', '#1a2028', '#2a2a0a', '#2a1a20']


class Level1Axioms(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        self.entries = []
        self.n = 0

        tk.Label(self.left_panel, text="L1: Is It a Group?", font=("Arial", 13, "bold"),
                 bg="#1e1e1e", fg="white").pack(pady=4)

        # Preset buttons
        tk.Label(self.left_panel, text="Load preset:", bg="#1e1e1e", fg="#8b949e",
                 font=("Arial", 9)).pack(anchor=tk.W, padx=4)
        for name, n, table in PRESETS:
            tk.Button(self.left_panel, text=name, font=("Arial", 10), bg="#3e3e42", fg="white",
                      anchor=tk.W, command=lambda n_=n, t_=table: self._load_preset(n_, t_)
                      ).pack(fill=tk.X, padx=4, pady=2)

        # Size selector
        size_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        size_frame.pack(fill=tk.X, padx=4, pady=(12, 2))
        tk.Label(size_frame, text="Grid size n =", bg="#1e1e1e", fg="white", font=("Arial", 10)).pack(side=tk.LEFT)
        self.n_entry = tk.Entry(size_frame, width=4, font=("Courier", 10))
        self.n_entry.insert(0, "4")
        self.n_entry.pack(side=tk.LEFT, padx=4)
        tk.Button(size_frame, text="Create", bg="#007acc", fg="white",
                  font=("Arial", 9, "bold"), command=self._create_grid).pack(side=tk.LEFT, padx=4)

        # Right panel layout
        self.grid_frame = tk.Frame(self.right_panel, bg="#2d2d30")
        self.grid_frame.pack(expand=True, pady=(20, 0))

        self.error_frame = tk.Frame(self.right_panel, bg="#2d2d30")
        self.error_frame.pack(fill=tk.X, pady=20)

        self._load_preset(4, PRESETS[0][2])

    def _load_preset(self, n, table):
        self.n_entry.delete(0, tk.END)
        self.n_entry.insert(0, str(n))
        self._create_grid()
        if table is not None:
            for i in range(n):
                for j in range(n):
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, str(table[i][j]))
            self._validate()

    def _move_focus(self, r, c, event):
        if event.keysym == 'Up':
            r = max(0, r - 1)
        elif event.keysym == 'Down':
            r = min(self.n - 1, r + 1)
        elif event.keysym == 'Left':
            c = max(0, c - 1)
        elif event.keysym == 'Right':
            c = min(self.n - 1, c + 1)
        self.entries[r][c].focus_set()
        self.entries[r][c].select_range(0, tk.END)

    def _create_grid(self):
        # Clear old grid
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self.entries = []

        try:
            self.n = int(self.n_entry.get())
        except ValueError:
            return
        if self.n < 1 or self.n > 12:
            return

        n = self.n
        cell_w = 4
        font_size = 20

        # Header row
        tk.Label(self.grid_frame, text="·", font=("Arial", font_size, "bold"),
                 bg="#21262d", fg="#58a6ff", width=cell_w, relief=tk.RIDGE
                 ).grid(row=0, column=0, padx=2, pady=2)
        for j in range(n):
            tk.Label(self.grid_frame, text=str(j), font=("Arial", font_size, "bold"),
                     bg="#21262d", fg="#58a6ff", width=cell_w, relief=tk.RIDGE
                     ).grid(row=0, column=j+1, padx=2, pady=2)

        # Data rows
        for i in range(n):
            tk.Label(self.grid_frame, text=str(i), font=("Arial", font_size, "bold"),
                     bg="#21262d", fg="#58a6ff", width=cell_w, relief=tk.RIDGE
                     ).grid(row=i+1, column=0, padx=2, pady=2)
            row_entries = []
            for j in range(n):
                e = tk.Entry(self.grid_frame, width=cell_w, font=("Courier", font_size, "bold"),
                             bg="#0d1117", fg="white", insertbackground="white",
                             justify=tk.CENTER, relief=tk.FLAT, bd=2)
                e.grid(row=i+1, column=j+1, padx=2, pady=2)
                e.bind('<KeyRelease>', lambda ev: self._validate())
                e.bind('<Up>', lambda ev, r=i, c=j: self._move_focus(r, c, ev))
                e.bind('<Down>', lambda ev, r=i, c=j: self._move_focus(r, c, ev))
                e.bind('<Left>', lambda ev, r=i, c=j: self._move_focus(r, c, ev))
                e.bind('<Right>', lambda ev, r=i, c=j: self._move_focus(r, c, ev))
                row_entries.append(e)
            self.entries.append(row_entries)
            
        self._validate()

    def _read_table(self):
        """Read the table into a RobustTable. Empty cells become MISSING, which gracefully bypass false positives."""
        n = self.n
        table = []
        for i in range(n):
            row = []
            for j in range(n):
                text = self.entries[i][j].get().strip()
                if text == '':
                    row.append(MISSING)
                else:
                    try:
                        row.append(int(text))
                    except ValueError:
                        row.append(999) # Invalid entry, will trigger closure error
            table.append(row)
        return RobustTable(table)

    def _get_closure_error(self, table):
        n = self.n
        for i in range(n):
            for j in range(n):
                val = table[i][j]
                if isinstance(val, MissingValue):
                    continue
                if val < 0 or val >= n:
                    if val == 999:
                        return f"table[{i}][{j}] (invalid input) is not in {{0,...,{n-1}}}"
                    return f"table[{i}][{j}] = {val} is not in {{0,...,{n-1}}}"
        return "Not closed"

    def _get_assoc_error(self, table):
        n = self.n
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    try:
                        ab_c = table[table[a][b]][c]
                        a_bc = table[a][table[b][c]]
                        if ab_c != a_bc:
                            return f"({a}·{b})·{c} = {ab_c} ≠ {a_bc} = {a}·({b}·{c})"
                    except Exception:
                        pass
        return "Not associative"

    def _get_inverse_error(self, table, identity):
        n = self.n
        for a in range(n):
            found = False
            for b in range(n):
                try:
                    if table[a][b] == identity and table[b][a] == identity:
                        found = True
                        break
                except Exception:
                    pass
            if not found:
                return f"Element {a} has no inverse"
        return "Missing inverses"

    def _validate(self):
        """Run all axiom checks and color cells accordingly. Shows errors in field area."""
        for w in self.error_frame.winfo_children():
            w.destroy()

        table = self._read_table()
        n = self.n

        # Reset all cell colors
        for i in range(n):
            for j in range(n):
                text = self.entries[i][j].get().strip()
                if text == '':
                    self.entries[i][j].config(bg="#0d1117", fg="white")
                else:
                    try:
                        val = int(text)
                        if 0 <= val < n:
                            c = COLORS[val % len(COLORS)]
                            bg = BG_COLORS[val % len(BG_COLORS)]
                            self.entries[i][j].config(bg=bg, fg=c)
                        else:
                            self.entries[i][j].config(bg="#4a0000", fg="#ff7b72")
                    except ValueError:
                        self.entries[i][j].config(bg="#4a0000", fg="#ff7b72")

        def report_err(msg):
            tk.Label(self.error_frame, text=f"✗ {msg}", font=("Arial", 14, "bold"), fg="#ff7b72", bg="#2d2d30").pack(pady=4)

        # Build mock GridElements
        class GridElement(tasks.Group.Element):
            def __init__(self, idx, table_ref):
                self.idx = idx
                self.table_ref = table_ref
            def __mul__(self, other):
                val = self.table_ref[self.idx][other.idx]
                return GridElement(val, self.table_ref)
            def __eq__(self, other):
                return isinstance(other, GridElement) and self.idx == other.idx
            def __hash__(self):
                return hash(self.idx)
                
        elements = [GridElement(i, table) for i in range(n)]

        try:
            ok_c = tasks.check_closure(elements)
            if ok_c is None:
                report_err("check_closure not implemented")
                return
            if not ok_c:
                msg_c = self._get_closure_error(table)
                report_err(f"Closure Failed: {msg_c}")
                return
        except Exception as e:
            report_err(f"check_closure crashed: {e}")
            return

        try:
            ok_a = tasks.check_associativity(elements)
            if ok_a is None:
                report_err("check_associativity not implemented")
                return
            if not ok_a:
                msg_a = self._get_assoc_error(table)
                report_err(f"Associativity Failed: {msg_a}")
                return
        except Exception as e:
            report_err(f"check_associativity crashed: {e}")
            return

        try:
            identity = tasks.find_identity(elements)
            # find_identity could legitimately return None if not found, but if student put pass it also returns None
            # We assume if all are missing, student hasn't implemented it. But if they just return None, the UI will say "No identity exists"
            if identity is not None:
                ok_i = tasks.check_inverses(elements, identity)
                if ok_i is None:
                    report_err("check_inverses not implemented")
                    return
                if not ok_i:
                    msg_i = self._get_inverse_error(table, identity.idx)
                    report_err(f"Inverses Failed: {msg_i}")
                    return
                else:
                    partial = any(isinstance(val, MissingValue) for row in table for val in row)
                    if not partial:
                        tk.Label(self.error_frame, text="✓ Perfect! This is a valid group.", 
                                 font=("Arial", 16, "bold"), fg="#7ee787", bg="#2d2d30").pack(pady=10)
            else:
                partial = any(isinstance(val, MissingValue) for row in table for val in row)
                if not partial:
                    report_err("No identity element exists! (or find_identity not implemented)")
        except Exception as e:
            report_err(f"Identity/Inverse check crashed: {e}")
            return
