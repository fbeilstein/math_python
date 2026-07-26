"""Level 2: Permutation Sandbox — build groups from permutations.

Features:
- Add permutations via the reusable PermutationInput widget
- Pool of permutation cards (small wiring diagrams)
- Perform Closure to generate the full group
- Composition viewer: stacked diagrams via drag-and-drop
- Inspect controls: inverse, powers, orbit, parity
"""
import tkinter as tk
from levels.base_level import BaseLevel
from levels.perm_widget import draw_perm_diagram, draw_perm_stack, perm_to_cycle_str, PERM_COLORS, is_even_permutation
import implementation_tasks as tasks


CARD_W = 110
CARD_H = 80
CARD_PAD = 8


class Level2Permutations(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        self.pool = []        # list of tuples
        self.selected_idx = None
        self.comp_stack = []
        self._drag_data = None

        # ── Left panel ──
        tk.Label(self.left_panel, text="L2: Permutation Sandbox",
                 font=("Arial", 13, "bold"), bg="#1e1e1e", fg="white").pack(pady=4)

        # Permutation input widget (reusable)
        from levels.perm_widget import PermutationInput
        self.perm_input = PermutationInput(self.left_panel, n=4,
                                           on_submit=self._add_to_pool,
                                           canvas_h=90)
        self.perm_input.pack(fill=tk.X, padx=2, pady=2)

        # Group actions
        act_frame = tk.LabelFrame(self.left_panel, text="Group Actions",
                                   font=("Arial", 9, "bold"),
                                   bg="#1e1e1e", fg="#58a6ff", bd=1)
        act_frame.pack(fill=tk.X, padx=2, pady=4)
        tk.Button(act_frame, text="⟨ Perform Closure ⟩", bg="#238636", fg="white",
                  font=("Arial", 10, "bold"),
                  command=self._do_closure).pack(fill=tk.X, padx=4, pady=2)
        tk.Button(act_frame, text="Clear Pool", bg="#6e3630", fg="white",
                  font=("Arial", 9), command=self._clear_pool
                  ).pack(fill=tk.X, padx=4, pady=2)

        # Inspect controls
        insp_frame = tk.LabelFrame(self.left_panel, text="Inspect (click card first)",
                                    font=("Arial", 9, "bold"),
                                    bg="#1e1e1e", fg="#58a6ff", bd=1)
        insp_frame.pack(fill=tk.X, padx=2, pady=4)

        self._highlight_mode = tk.StringVar(value="none")
        modes = [("None", "none"), ("Inverse", "inverse"),
                 ("Powers g, g², …", "powers"), ("Parity (even/odd)", "parity")]
        for label, val in modes:
            tk.Radiobutton(insp_frame, text=label, variable=self._highlight_mode,
                           value=val, bg="#1e1e1e", fg="white", selectcolor="#3e3e42",
                           activebackground="#1e1e1e", activeforeground="white",
                           font=("Arial", 9), anchor=tk.W,
                           command=self._redraw_pool
                           ).pack(fill=tk.X, padx=4)
        # ── Right panel: pool + composition ──
        
        # Composition canvas at right
        self.comp_frame = tk.Frame(self.right_panel, bg="#1a1a1a", width=280)
        self.comp_frame.pack(fill=tk.Y, side=tk.RIGHT)
        self.comp_frame.pack_propagate(False)
        self.comp_canvas = tk.Canvas(self.comp_frame, bg="#1a1a1a",
                                      highlightthickness=0)
        self.comp_canvas.pack(fill=tk.BOTH, expand=True)
        self.comp_canvas.bind('<Configure>', lambda e: self._redraw_comp())

        self.pool_canvas = tk.Canvas(self.right_panel, bg="#2d2d30",
                                      highlightthickness=0)
        self.pool_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.pool_canvas.bind('<Button-1>', self._on_pool_click)
        self.pool_canvas.bind('<B1-Motion>', self._on_pool_motion)
        self.pool_canvas.bind('<ButtonRelease-1>', self._on_pool_release)
        self.pool_canvas.bind('<Configure>', lambda e: self._redraw_pool())

    # ─── Pool management ───

    def _add_to_pool(self, perm):
        t = tuple(perm)
        if t not in self.pool:
            self.pool.append(t)
            self._redraw_pool()

    def _clear_pool(self):
        self.pool = []
        self.selected_idx = None
        self.comp_stack = []
        self._redraw_pool()
        self._redraw_comp()

    def _do_closure(self):
        if not self.pool:
            return
        n = len(self.pool[0])
        generators = [tasks.PermutationElement(list(p)) for p in self.pool]
        result = tasks.generate_group(generators)
        if result is None:
            c = self.pool_canvas
            c.delete("all")
            c.create_text(c.winfo_width() // 2, c.winfo_height() // 2,
                          text="generate_group not implemented",
                          fill="#ff7b72", font=("Arial", 12))
            return
        self.pool = [tuple(p.mapping) for p in result]
        self._redraw_pool()

    # ─── Card layout & Drag ───

    def _card_positions(self):
        cw = self.pool_canvas.winfo_width()
        cols = max(1, (cw - CARD_PAD) // (CARD_W + CARD_PAD))
        positions = []
        for idx in range(len(self.pool)):
            col = idx % cols
            row = idx // cols
            x = CARD_PAD + col * (CARD_W + CARD_PAD)
            y = CARD_PAD + row * (CARD_H + CARD_PAD + 16)
            positions.append((x, y))
        return positions

    def _idx_at(self, ex, ey):
        positions = self._card_positions()
        for idx, (x, y) in enumerate(positions):
            if x <= ex <= x + CARD_W and y <= ey <= y + CARD_H + 16:
                return idx
        return None

    def _on_pool_click(self, ev):
        idx = self._idx_at(ev.x, ev.y)
        if idx is not None:
            self.selected_idx = idx
            self._drag_data = {
                'idx': idx,
                'window': None,
                'perm': self.pool[idx]
            }
        else:
            self.selected_idx = None
            self._drag_data = None
        self._redraw_pool()

    def _on_pool_motion(self, ev):
        if not self._drag_data:
            return
        
        # Initialize floating window if it doesn't exist
        if self._drag_data['window'] is None:
            win = tk.Toplevel(self.pool_canvas)
            win.overrideredirect(True)
            win.attributes("-alpha", 0.8)
            # Create canvas to draw the card
            c = tk.Canvas(win, bg="#0d1117", highlightthickness=2, 
                          highlightbackground="#58a6ff",
                          width=CARD_W, height=CARD_H)
            c.pack()
            perm = list(self._drag_data['perm'])
            draw_perm_diagram(c, perm, len(perm), 0, 0, CARD_W, CARD_H, show_labels=False, lw=1.5)
            self._drag_data['window'] = win

        # Move floating window
        win = self._drag_data['window']
        win.geometry(f"+{ev.x_root + 15}+{ev.y_root + 15}")

    def _on_pool_release(self, ev):
        if not self._drag_data:
            return

        if self._drag_data['window']:
            self._drag_data['window'].destroy()

        # Check if dropped in comp_canvas
        cx = self.comp_canvas.winfo_rootx()
        cy = self.comp_canvas.winfo_rooty()
        cw = self.comp_canvas.winfo_width()
        ch = self.comp_canvas.winfo_height()

        if cx <= ev.x_root <= cx + cw and cy <= ev.y_root <= cy + ch:
            self.comp_stack.append(self._drag_data['perm'])
            self._redraw_comp()

        self._drag_data = None


    # ─── Drawing ───

    def _redraw_pool(self):
        c = self.pool_canvas
        c.delete("all")
        if not self.pool:
            c.create_text(c.winfo_width() // 2, c.winfo_height() // 2,
                          text="Add permutations using the input panel →",
                          fill="#8b949e", font=("Arial", 12))
            return

        n = len(self.pool[0])
        positions = self._card_positions()
        mode = self._highlight_mode.get()

        highlight = {}
        if self.selected_idx is not None and self.selected_idx < len(self.pool):
            sel_perm = list(self.pool[self.selected_idx])
            try:
                if mode == "inverse":
                    inv = tuple((~tasks.PermutationElement(sel_perm)).mapping)
                    for i, p in enumerate(self.pool):
                        if p == inv:
                            highlight[i] = "#ff7b72"
                    highlight[self.selected_idx] = "#58a6ff"
                elif mode == "powers":
                    current = sel_perm
                    k = 0
                    while True:
                        for i, p in enumerate(self.pool):
                            if p == tuple(current):
                                highlight[i] = PERM_COLORS[k % len(PERM_COLORS)]
                        current = (tasks.PermutationElement(sel_perm) * tasks.PermutationElement(current)).mapping
                        k += 1
                        if tuple(current) == tuple(sel_perm):
                            break
                elif mode == "parity":
                    for i, p in enumerate(self.pool):
                        highlight[i] = "#7ee787" if is_even_permutation(list(p)) else "#ff7b72"
            except Exception:
                pass # Silently abort highlighting if methods not implemented

        for idx, (x, y) in enumerate(positions):
            perm = self.pool[idx]
            border_c = "#3e3e42"
            if idx == self.selected_idx:
                border_c = "#58a6ff"
            if idx in highlight:
                border_c = highlight[idx]

            c.create_rectangle(x, y, x + CARD_W, y + CARD_H,
                               fill="#0d1117", outline=border_c, width=2)

            draw_perm_diagram(c, list(perm), n, x + 2, y + 2,
                              CARD_W - 4, CARD_H - 4,
                              show_labels=(n <= 6), lw=1.5,
                              tag=f"card_{idx}")

            label = perm_to_cycle_str(list(perm))
            c.create_text(x + CARD_W // 2, y + CARD_H + 8,
                          text=label, fill="#c9d1d9", font=("Courier", 8))

        if positions:
            max_y = max(y for _, y in positions) + CARD_H + 24
            c.configure(scrollregion=(0, 0, c.winfo_width(), max_y))

    def _redraw_comp(self):
        """Draw composition as vertically stacked braid."""
        c = self.comp_canvas
        c.delete("all")
        if not self.comp_stack:
            c.create_text(c.winfo_width() // 2, 80,
                          text="Drag cards here\nto multiply",
                          fill="#8b949e", font=("Arial", 10), justify=tk.CENTER)
            return

        cw = c.winfo_width()
        ch = c.winfo_height()

        n = len(self.comp_stack[0])
        
        # Clear button
        c.create_rectangle(cw - 70, 10, cw - 10, 34,
                           fill="#0d1117", outline="#ff7b72", width=1,
                           tags=("clear_btn",))
        c.create_text(cw - 40, 22, text="Clear",
                      fill="#ff7b72", font=("Arial", 9, "bold"),
                      tags=("clear_btn",))
        c.tag_bind("clear_btn", '<Button-1>', lambda e: self._clear_comp_stack())

        # Check if __mul__ is implemented before attempting to draw the braid
        try:
            id_el = tasks.PermutationElement(list(range(n)))
            res = (id_el * id_el).mapping
            if res is None:
                raise NotImplementedError
        except Exception:
            c.create_text(cw // 2, ch // 2, text="Multiplication not implemented",
                          fill="#ff7b72", font=("Arial", 12, "bold"))
            return

        # Stacked braid taking up most of the vertical space
        stack_h = min(ch - 100, int(cw * 1.5))  # Adjust for more space if needed
        c.create_rectangle(10, 40, cw - 10, 40 + stack_h,
                           fill="#0d1117", outline="#3e3e42", width=1)
        
        # Convert tuples to lists for draw_perm_stack
        perms_list = [list(p) for p in self.comp_stack]
        draw_perm_stack(c, perms_list, n, 10, 40, cw - 20, stack_h,
                        lw=2, tag="stack")

        # Labels next to the rows. Show at most first few and last few if too many.
        for layer, perm in enumerate(perms_list):
            if layer > 5 and layer < len(perms_list) - 1:
                continue
            # Calculate row y center
            pad_y = max(12, stack_h * 0.08)
            num_rows = len(perms_list) + 1
            row_spacing = (stack_h - 2 * pad_y) / max(num_rows - 1, 1)
            y_center = 40 + pad_y + layer * row_spacing + (row_spacing / 2)
            c.create_text(cw // 2, y_center, text=perm_to_cycle_str(perm),
                          fill="#c9d1d9", font=("Courier", 8))

        # Compose result
        result = list(range(n))
        for p in self.comp_stack:
            result = (tasks.PermutationElement(p) * tasks.PermutationElement(result)).mapping

        # Result label
        res_y = 40 + stack_h + 20
        c.create_text(cw // 2, res_y, text=f"Total = {perm_to_cycle_str(result)}",
                      fill="#ffa657", font=("Arial", 10, "bold"))

        # Add to pool button
        t = tuple(result)
        if t not in self.pool:
            by = res_y + 30
            c.create_rectangle(cw // 2 - 40, by - 12, cw // 2 + 40, by + 12,
                               fill="#0d1117", outline="#238636", width=1,
                               tags=("add_btn",))
            c.create_text(cw // 2, by, text="+ Add to Pool",
                          fill="#238636", font=("Arial", 9, "bold"),
                          tags=("add_btn",))
            c.tag_bind("add_btn", '<Button-1>',
                       lambda e: self._add_to_pool(result))

    def _clear_comp_stack(self):
        self.comp_stack = []
        self._redraw_comp()
