"""Reusable permutation input and visualization widgets.

Provides:
- draw_perm_diagram(): draw a wiring diagram on a tkinter Canvas
- PermutationInput: Frame with text entries + interactive arrow builder
"""
import tkinter as tk
import implementation_tasks as tasks

PERM_COLORS = ['#7ee787', '#ff7b72', '#58a6ff', '#ffa657', '#d2a8ff',
               '#79c0ff', '#f0e68c', '#ff69b4', '#56d4dd', '#f78166']


def one_line_to_cycles(perm):
    """Convert one-line notation to cycle notation.
    """
    n = len(perm)
    visited = [False] * n
    cycles = []
    for i in range(n):
        if visited[i] or perm[i] == i:
            continue
        cycle = []
        j = i
        while not visited[j]:
            visited[j] = True
            cycle.append(j)
            j = perm[j]
        cycles.append(cycle)
    return cycles


def cycles_to_one_line(cycles, n):
    """Convert cycle notation to one-line notation.
    Evaluates composition right-to-left.
    """
    perm = list(range(n))
    for cycle in reversed(cycles):
        c_perm = list(range(n))
        for i in range(len(cycle)):
            c_perm[cycle[i]] = cycle[(i + 1) % len(cycle)]
        perm = [c_perm[perm[i]] for i in range(n)]
    return perm


def is_even_permutation(p):
    """Determine if a permutation is even (True) or odd (False).
    """
    n = len(p)
    visited = [False] * n
    transpositions = 0
    for i in range(n):
        if not visited[i]:
            cycle_len = 0
            j = i
            while not visited[j]:
                visited[j] = True
                j = p[j]
                cycle_len += 1
            if cycle_len > 0:
                transpositions += cycle_len - 1
    return transpositions % 2 == 0


def draw_perm_diagram(canvas, perm, n, x0, y0, w, h,
                      colors=None, show_labels=True, lw=2, tag=""):
    """Draw a permutation as a wiring diagram (top dots → bottom dots).

    Args:
        canvas: tk.Canvas to draw on.
        perm: list of int (one-line notation), or None for empty diagram.
        n: number of elements.
        x0, y0, w, h: bounding box.
        colors: list of colors per element.
        show_labels: whether to draw numeric labels.
        lw: arrow line width.
        tag: canvas tag prefix for later deletion.
    """
    if colors is None:
        colors = PERM_COLORS
    pad_x = max(14, w * 0.12)
    pad_y = max(16, h * 0.22)
    top_y = y0 + pad_y
    bot_y = y0 + h - pad_y
    r = max(3, min(5, w / (n + 1) * 0.15))
    font_sz = max(7, min(11, int(w / (n + 1) * 0.35)))

    def dot_x(i):
        if n <= 1:
            return x0 + w / 2
        return x0 + pad_x + i * (w - 2 * pad_x) / (n - 1)

    # Arrows
    if perm is not None:
        for i in range(min(n, len(perm))):
            j = perm[i]
            if j is None or not (0 <= j < n):
                continue
            c = colors[i % len(colors)]
            canvas.create_line(dot_x(i), top_y + r + 2,
                               dot_x(j), bot_y - r - 2,
                               fill=c, width=lw, arrow=tk.LAST,
                               arrowshape=(8, 10, 4), smooth=False,
                               tags=(tag,))

    # Dots and labels
    for i in range(n):
        xi = dot_x(i)
        c = colors[i % len(colors)]
        canvas.create_oval(xi - r, top_y - r, xi + r, top_y + r,
                           fill=c, outline='', tags=(tag,))
        canvas.create_oval(xi - r, bot_y - r, xi + r, bot_y + r,
                           fill=c, outline='', tags=(tag,))
        if show_labels:
            canvas.create_text(xi, top_y - r - 9, text=str(i), fill=c,
                               font=('Arial', font_sz, 'bold'), tags=(tag,))
            canvas.create_text(xi, bot_y + r + 9, text=str(i), fill=c,
                               font=('Arial', font_sz, 'bold'), tags=(tag,))


def draw_perm_stack(canvas, perms, n, x0, y0, w, h,
                    colors=None, lw=2, tag=""):
    """Draw a vertical stack of permutations (composition as braid).

    Three or more horizontal rows of colored dots. Arrows between consecutive
    rows show each permutation's mapping. The visual result is a braid where
    you can trace a path from the top row through all layers to the bottom.

    Args:
        canvas: tk.Canvas to draw on.
        perms: list of permutations (each a list of int). Applied bottom-to-top
               (perms[0] is the bottom layer, perms[-1] is the top).
        n: number of elements.
        x0, y0, w, h: bounding box.
    """
    if colors is None:
        colors = PERM_COLORS
    num_rows = len(perms) + 1
    pad_x = max(14, w * 0.10)
    pad_y = max(12, h * 0.08)
    r = max(3, min(6, w / (n + 1) * 0.18))
    row_spacing = (h - 2 * pad_y) / max(num_rows - 1, 1)

    def dot_x(i):
        if n <= 1:
            return x0 + w / 2
        return x0 + pad_x + i * (w - 2 * pad_x) / (n - 1)

    def row_y(row_idx):
        return y0 + pad_y + row_idx * row_spacing

    # Track which original element (from top row) is at each position
    # Check if mul works
    mul_works = True
    try:
        id_list = tuple(range(n))
        pg = tasks.PermutationGroup()
        p1 = pg.Element(pg, id_list)
        p2 = pg.Element(pg, id_list)
        res = (p1 * p2).value
        if res is None:
            mul_works = False
    except Exception:
        mul_works = False

    current_elements = list(range(n))

    # Draw dots for top row
    ry = row_y(0)
    for i in range(n):
        xi = dot_x(i)
        c = colors[i % len(colors)]
        canvas.create_oval(xi - r, ry - r, xi + r, ry + r,
                           fill=c, outline='', tags=(tag,))

    # Draw arrows and subsequent rows
    # Note: perms are applied bottom-to-top. So the top layer corresponds to perms[-1].
    # But wait, when we compose q then p, the stack is visually:
    # row 0 -> q -> row 1 -> p -> row 2.
    # We pass perms as [q, p], so perms[0] is q (top layer), perms[1] is p (bottom layer).
    for layer, perm in enumerate(perms):
        y_from = row_y(layer)
        y_to = row_y(layer + 1)
        next_elements = [None] * n
        
        for i in range(min(n, len(perm))):
            j = perm[i]
            if j is None or not (0 <= j < n):
                continue
            
            orig_element = current_elements[i] if mul_works else i
            c = colors[orig_element % len(colors)]
            
            canvas.create_line(dot_x(i), y_from + r + 2,
                               dot_x(j), y_to - r - 2,
                               fill=c, width=lw, arrow=tk.LAST,
                               arrowshape=(8, 10, 4), tags=(tag,))
                               
        if mul_works:
            try:
                state = tuple(range(n))
                pg = tasks.PermutationGroup()
                for p in perms[:layer+1]:
                    state = (pg.Element(pg, tuple(p)) * pg.Element(pg, state)).value
                
                next_elements = [None] * n
                for orig in range(n):
                    j = state[orig]
                    next_elements[j] = orig
                current_elements = next_elements
            except Exception:
                mul_works = False
                current_elements = list(range(n))
        else:
            current_elements = list(range(n))
        
        # Draw dots for the next row
        ry = y_to
        for i in range(n):
            if current_elements[i] is not None:
                xi = dot_x(i)
                c = colors[current_elements[i] % len(colors)]
                canvas.create_oval(xi - r, ry - r, xi + r, ry + r,
                                   fill=c, outline='', tags=(tag,))

    # Labels only on top row
    font_sz = max(7, min(12, int(w / (n + 1) * 0.4)))
    for i in range(n):
        xi = dot_x(i)
        c = colors[i % len(colors)]
        canvas.create_text(xi, row_y(0) - r - 10, text=str(i), fill=c,
                           font=('Arial', font_sz, 'bold'), tags=(tag,))


def perm_to_cycle_str(perm):
    """Convert one-line perm to cycle string like '(0 1 2)(3 4)'."""
    if perm is None:
        return ""
    cycles = one_line_to_cycles(list(perm))
    if not cycles:
        return "e"
    return ''.join(f"({' '.join(str(x) for x in c)})" for c in cycles)


class PermutationInput(tk.LabelFrame):
    """Reusable permutation input widget with three synced modes:
    1. One-line notation text entry
    2. Cycle notation text entry
    3. Interactive arrow builder (click top dot, then bottom dot)

    Args:
        parent: tk parent widget.
        n: initial number of elements.
        on_submit: callback(perm_list) fired when user presses Add.
        canvas_h: height of the arrow builder canvas.
    """

    def __init__(self, parent, n=4, on_submit=None, canvas_h=100, **kw):
        super().__init__(parent, text="Permutation Input", font=("Arial", 9, "bold"),
                         bg="#1e1e1e", fg="#58a6ff", bd=1, **kw)
        self._n = n
        self._perm = list(range(n))  # identity
        self._on_submit = on_submit
        self._selected_top = None
        self._syncing = False

        # ── n selector ──
        row0 = tk.Frame(self, bg="#1e1e1e")
        row0.pack(fill=tk.X, padx=4, pady=2)
        tk.Label(row0, text="n =", bg="#1e1e1e", fg="white",
                 font=("Arial", 9)).pack(side=tk.LEFT)
        self._n_var = tk.StringVar(value=str(n))
        self._n_spin = tk.Spinbox(row0, from_=2, to=10, width=3,
                                  font=("Courier", 10), textvariable=self._n_var,
                                  command=self._on_n_change)
        self._n_spin.pack(side=tk.LEFT, padx=4)
        self._n_spin.bind('<Return>', lambda e: self._on_n_change())

        # ── One-line entry ──
        row1 = tk.Frame(self, bg="#1e1e1e")
        row1.pack(fill=tk.X, padx=4, pady=1)
        tk.Label(row1, text="σ =", bg="#1e1e1e", fg="#8b949e",
                 font=("Arial", 9)).pack(side=tk.LEFT)
        self._ol_entry = tk.Entry(row1, font=("Courier", 10), bg="#0d1117",
                                  fg="white", insertbackground="white")
        self._ol_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        self._ol_entry.bind('<KeyRelease>', self._on_ol_change)

        # ── Cycle entry ──
        row2 = tk.Frame(self, bg="#1e1e1e")
        row2.pack(fill=tk.X, padx=4, pady=1)
        tk.Label(row2, text="  =", bg="#1e1e1e", fg="#8b949e",
                 font=("Arial", 9)).pack(side=tk.LEFT)
        self._cy_entry = tk.Entry(row2, font=("Courier", 10), bg="#0d1117",
                                  fg="white", insertbackground="white")
        self._cy_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        self._cy_entry.bind('<KeyRelease>', self._on_cy_change)

        # ── Arrow builder canvas ──
        self._canvas = tk.Canvas(self, bg="#0d1117", height=canvas_h,
                                 highlightthickness=0)
        self._canvas.pack(fill=tk.X, padx=4, pady=4)
        self._canvas.bind('<Button-1>', self._on_canvas_click)

        # ── Add button ──
        if on_submit:
            tk.Button(self, text="Add to Pool", bg="#238636", fg="white",
                      font=("Arial", 9, "bold"),
                      command=self._submit).pack(fill=tk.X, padx=4, pady=(0, 4))

        self._sync_from_perm()

    @property
    def n(self):
        return self._n

    def get_permutation(self):
        return list(self._perm)

    def set_permutation(self, perm):
        self._perm = list(perm)
        self._n = len(perm)
        self._n_var.set(str(self._n))
        self._sync_from_perm()

    def _on_n_change(self):
        try:
            new_n = int(self._n_var.get())
        except ValueError:
            return
        if new_n < 1 or new_n > 12:
            return
        self._n = new_n
        self._perm = list(range(new_n))
        self._sync_from_perm()

    def _on_ol_change(self, ev=None):
        if self._syncing:
            return
        text = self._ol_entry.get().strip()
        try:
            perm = [int(x) for x in text.replace(',', ' ').split()]
            if len(perm) == self._n and sorted(perm) == list(range(self._n)):
                self._perm = perm
                self._syncing = True
                self._cy_entry.delete(0, tk.END)
                self._cy_entry.insert(0, perm_to_cycle_str(perm))
                self._redraw()
                self._syncing = False
        except ValueError:
            pass

    def _on_cy_change(self, ev=None):
        if self._syncing:
            return
        text = self._cy_entry.get().strip()
        try:
            import re
            cycles = []
            for m in re.finditer(r'\(([^)]+)\)', text):
                tokens = re.split(r'[,\s]+', m.group(1).strip())
                if tokens and all(t.isdigit() for t in tokens):
                    cycles.append([int(x) for x in tokens])
            if not cycles and text != "":
                return
            if text == "":
                perm = list(range(self._n))
            else:
                perm = cycles_to_one_line(cycles, self._n)
            
            if sorted(perm) == list(range(self._n)):
                self._perm = perm
                self._syncing = True
                self._ol_entry.delete(0, tk.END)
                self._ol_entry.insert(0, ' '.join(str(x) for x in perm))
                self._redraw()
                self._syncing = False
        except Exception:
            pass

    def _on_canvas_click(self, ev):
        n = self._n
        cw = self._canvas.winfo_width()
        ch = self._canvas.winfo_height()
        pad_x = max(14, cw * 0.12)
        pad_y = max(16, ch * 0.22)
        top_y = pad_y
        bot_y = ch - pad_y
        hit_r = max(12, cw / (n + 1) * 0.3)

        def dot_x(i):
            if n <= 1:
                return cw / 2
            return pad_x + i * (cw - 2 * pad_x) / (n - 1)

        # Check top dots
        for i in range(n):
            if abs(ev.x - dot_x(i)) < hit_r and abs(ev.y - top_y) < hit_r:
                self._selected_top = i
                self._redraw()
                return

        # Check bottom dots
        if self._selected_top is not None:
            for j in range(n):
                if abs(ev.x - dot_x(j)) < hit_r and abs(ev.y - bot_y) < hit_r:
                    # Enforce bijection: swap destinations
                    old_dest = self._perm[self._selected_top]
                    for top_idx in range(n):
                        if self._perm[top_idx] == j:
                            self._perm[top_idx] = old_dest
                            break
                            
                    self._perm[self._selected_top] = j
                    self._selected_top = None
                    self._sync_from_perm()
                    return

        self._selected_top = None
        self._redraw()

    def _sync_from_perm(self):
        self._syncing = True
        self._ol_entry.delete(0, tk.END)
        self._ol_entry.insert(0, ' '.join(str(x) for x in self._perm))
        self._cy_entry.delete(0, tk.END)
        self._cy_entry.insert(0, perm_to_cycle_str(self._perm))
        self._syncing = False
        self._redraw()

    def _redraw(self):
        c = self._canvas
        c.delete("all")
        cw = c.winfo_width()
        ch = c.winfo_height()
        if cw < 10:
            c.after(50, self._redraw)
            return
        draw_perm_diagram(c, self._perm, self._n, 0, 0, cw, ch, tag="d")

        # Highlight selected top dot
        if self._selected_top is not None:
            pad_x = max(14, cw * 0.12)
            pad_y = max(16, ch * 0.22)
            top_y = pad_y
            n = self._n
            def dot_x(i):
                if n <= 1:
                    return cw / 2
                return pad_x + i * (cw - 2 * pad_x) / (n - 1)
            xi = dot_x(self._selected_top)
            c.create_oval(xi - 10, top_y - 10, xi + 10, top_y + 10,
                          outline='white', width=2, tags=("sel",))

    def _submit(self):
        if self._on_submit:
            self._on_submit(list(self._perm))
