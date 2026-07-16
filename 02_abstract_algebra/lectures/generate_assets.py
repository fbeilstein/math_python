"""Generate lecture assets for the Abstract Algebra slides."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import networkx as nx
from itertools import permutations

OUT = '/data/python_scripts/math_python/02_abstract_algebra/lectures/assets'

plt.rcParams.update({
    'figure.facecolor': '#0d1117',
    'axes.facecolor': '#0d1117',
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': '#8b949e',
    'ytick.color': '#8b949e',
})

# ────────────────────────────────────────────────────────────
# 1. Z_n clock diagram
# ────────────────────────────────────────────────────────────
def draw_zn_clock(n, filename):
    fig, ax = plt.subplots(figsize=(5, 5))
    angles = [2 * np.pi * k / n - np.pi/2 for k in range(n)]
    r = 0.85
    for k in range(n):
        x, y = r * np.cos(angles[k]), r * np.sin(angles[k])
        circle = plt.Circle((x, y), 0.08, color='#58a6ff', ec='#79c0ff', lw=2, zorder=5)
        ax.add_patch(circle)
        ax.text(x, y, str(k), ha='center', va='center', fontsize=14, fontweight='bold', color='white', zorder=6)
        # Arrow to next
        x2, y2 = r * np.cos(angles[(k+1) % n]), r * np.sin(angles[(k+1) % n])
        dx, dy = x2 - x, y2 - y
        length = np.sqrt(dx**2 + dy**2)
        # Shorten arrows to not overlap circles
        shrink = 0.12
        ax.annotate('', xy=(x + dx*(1-shrink/length), y + dy*(1-shrink/length)),
                     xytext=(x + dx*(shrink/length), y + dy*(shrink/length)),
                     arrowprops=dict(arrowstyle='->', color='#ff7b72', lw=1.5), zorder=3)
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'$\\mathbb{{Z}}_{{{n}}}$', fontsize=18, color='#58a6ff', pad=10)
    fig.savefig(f'{OUT}/{filename}', dpi=150, bbox_inches='tight', transparent=True)
    plt.close(fig)

draw_zn_clock(6, 'z6_clock.png')
draw_zn_clock(8, 'z8_clock.png')
print("✓ Z_n clocks")

# ────────────────────────────────────────────────────────────
# 2. Cayley graph of D_3 (= S_3)
# ────────────────────────────────────────────────────────────
def cayley_d3():
    # D_3: <r, s | r^3 = s^2 = e, srs = r^{-1}>
    # Elements: {e, r, r^2, s, sr, sr^2}
    elems = ['e', 'r', 'r²', 's', 'sr', 'sr²']
    # r-action (rotation): e->r->r²->e, s->sr->sr²->s
    r_map = {'e':'r', 'r':'r²', 'r²':'e', 's':'sr', 'sr':'sr²', 'sr²':'s'}
    # s-action (reflection): e->s, r->sr², r²->sr, s->e, sr->r², sr²->r
    s_map = {'e':'s', 'r':'sr²', 'r²':'sr', 's':'e', 'sr':'r²', 'sr²':'r'}

    G = nx.DiGraph()
    for e in elems:
        G.add_node(e)
    for e in elems:
        G.add_edge(e, r_map[e], gen='r')
        G.add_edge(e, s_map[e], gen='s')

    # Circular layout with rotations on top, reflections on bottom
    pos = {
        'e':   (0, 1),
        'r':   (0.87, 0.5),
        'r²':  (0.87, -0.5),
        's':   (0, -1),
        'sr':  (-0.87, -0.5),
        'sr²': (-0.87, 0.5),
    }

    fig, ax = plt.subplots(figsize=(6, 5))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='#58a6ff', node_size=700, edgecolors='#79c0ff', linewidths=2)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=11, font_color='white', font_weight='bold')

    r_edges = [(u, v) for u, v, d in G.edges(data=True) if d['gen'] == 'r']
    s_edges = [(u, v) for u, v, d in G.edges(data=True) if d['gen'] == 's']
    nx.draw_networkx_edges(G, pos, edgelist=r_edges, ax=ax, edge_color='#ff7b72', arrows=True, 
                           arrowsize=18, connectionstyle='arc3,rad=0.15', width=2, label='r (rotate)')
    nx.draw_networkx_edges(G, pos, edgelist=s_edges, ax=ax, edge_color='#7ee787', arrows=True,
                           arrowsize=18, connectionstyle='arc3,rad=0.15', width=2, style='dashed', label='s (reflect)')

    ax.set_title('Cayley Graph of $D_3 \\cong S_3$', fontsize=16, color='#58a6ff')
    ax.legend(loc='lower right', facecolor='#161b22', labelcolor='white', fontsize=10)
    ax.axis('off')
    fig.savefig(f'{OUT}/cayley_d3.png', dpi=150, bbox_inches='tight', transparent=True)
    plt.close(fig)

cayley_d3()
print("✓ Cayley D_3")

# ────────────────────────────────────────────────────────────
# 3. Cayley graph of Z_6
# ────────────────────────────────────────────────────────────
def cayley_z6():
    G = nx.DiGraph()
    for i in range(6):
        G.add_node(str(i))
        G.add_edge(str(i), str((i+1) % 6))
    angles = [2 * np.pi * k / 6 - np.pi/2 for k in range(6)]
    pos = {str(k): (np.cos(angles[k]), np.sin(angles[k])) for k in range(6)}

    fig, ax = plt.subplots(figsize=(5, 5))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='#58a6ff', node_size=700, edgecolors='#79c0ff', linewidths=2)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=14, font_color='white', font_weight='bold')
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='#ff7b72', arrows=True, arrowsize=18,
                           connectionstyle='arc3,rad=0.15', width=2)
    ax.set_title('Cayley Graph of $\\mathbb{Z}_6$\n(generator: +1)', fontsize=14, color='#58a6ff')
    ax.axis('off')
    fig.savefig(f'{OUT}/cayley_z6.png', dpi=150, bbox_inches='tight', transparent=True)
    plt.close(fig)

cayley_z6()
print("✓ Cayley Z_6")

# ────────────────────────────────────────────────────────────
# 4. Cayley graph of D_4 
# ────────────────────────────────────────────────────────────
def cayley_d4():
    elems = ['e', 'r', 'r²', 'r³', 's', 'sr', 'sr²', 'sr³']
    r_map = {'e':'r', 'r':'r²', 'r²':'r³', 'r³':'e', 's':'sr³', 'sr':'s', 'sr²':'sr', 'sr³':'sr²'}
    s_map = {'e':'s', 'r':'sr³', 'r²':'sr²', 'r³':'sr', 's':'e', 'sr':'r³', 'sr²':'r²', 'sr³':'r'}

    G = nx.DiGraph()
    for e in elems: G.add_node(e)
    for e in elems:
        G.add_edge(e, r_map[e], gen='r')
        G.add_edge(e, s_map[e], gen='s')

    # Arrange in two concentric squares
    outer = 1.2
    inner = 0.55
    pos = {
        'e':   (outer, outer),   'r':   (outer, -outer),
        'r²':  (-outer, -outer), 'r³':  (-outer, outer),
        's':   (inner, inner),   'sr':  (inner, -inner),
        'sr²': (-inner, -inner), 'sr³': (-inner, inner),
    }

    fig, ax = plt.subplots(figsize=(6, 5))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='#58a6ff', node_size=600, edgecolors='#79c0ff', linewidths=2)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=9, font_color='white', font_weight='bold')

    r_edges = [(u, v) for u, v, d in G.edges(data=True) if d['gen'] == 'r']
    s_edges = [(u, v) for u, v, d in G.edges(data=True) if d['gen'] == 's']
    nx.draw_networkx_edges(G, pos, edgelist=r_edges, ax=ax, edge_color='#ff7b72', arrows=True,
                           arrowsize=15, connectionstyle='arc3,rad=0.2', width=1.8)
    nx.draw_networkx_edges(G, pos, edgelist=s_edges, ax=ax, edge_color='#7ee787', arrows=True,
                           arrowsize=15, connectionstyle='arc3,rad=0.2', width=1.8, style='dashed')

    ax.set_title('Cayley Graph of $D_4$', fontsize=16, color='#58a6ff')
    ax.axis('off')
    fig.savefig(f'{OUT}/cayley_d4.png', dpi=150, bbox_inches='tight', transparent=True)
    plt.close(fig)

cayley_d4()
print("✓ Cayley D_4")

# ────────────────────────────────────────────────────────────
# 5. Coset partition of D_3 by <s>
# ────────────────────────────────────────────────────────────
def coset_partition():
    elems = ['e', 'r', 'r²', 's', 'sr', 'sr²']
    # H = <s> = {e, s}
    cosets = [{'e', 's'}, {'r', 'sr²'}, {'r²', 'sr'}]
    colors_map = {'#ffd700': {'e', 's'}, '#58a6ff': {'r', 'sr²'}, '#7ee787': {'r²', 'sr'}}
    
    G = nx.DiGraph()
    r_map = {'e':'r', 'r':'r²', 'r²':'e', 's':'sr', 'sr':'sr²', 'sr²':'s'}
    s_map = {'e':'s', 'r':'sr²', 'r²':'sr', 's':'e', 'sr':'r²', 'sr²':'r'}
    for e in elems:
        G.add_node(e)
        G.add_edge(e, r_map[e])
        G.add_edge(e, s_map[e])

    pos = {
        'e': (0, 1), 'r': (0.87, 0.5), 'r²': (0.87, -0.5),
        's': (0, -1), 'sr': (-0.87, -0.5), 'sr²': (-0.87, 0.5),
    }

    fig, ax = plt.subplots(figsize=(6, 5))
    for color, coset in colors_map.items():
        nodelist = [n for n in elems if n in coset]
        nx.draw_networkx_nodes(G, pos, nodelist=nodelist, ax=ax, node_color=color, node_size=700, edgecolors='white', linewidths=2)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=11, font_color='#0d1117', font_weight='bold')
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='#484f58', arrows=True, arrowsize=12,
                           connectionstyle='arc3,rad=0.15', alpha=0.4, width=1.5)

    ax.set_title('Left Cosets of $H = \\langle s \\rangle$ in $D_3$\n$[D_3 : H] = 3$', fontsize=14, color='#58a6ff')
    # Legend
    handles = [
        mpatches.Patch(color='#ffd700', label='$H = \\{e, s\\}$'),
        mpatches.Patch(color='#58a6ff', label='$rH = \\{r, sr^2\\}$'),
        mpatches.Patch(color='#7ee787', label='$r^2H = \\{r^2, sr\\}$'),
    ]
    ax.legend(handles=handles, loc='lower right', facecolor='#161b22', labelcolor='white', fontsize=10)
    ax.axis('off')
    fig.savefig(f'{OUT}/coset_partition.png', dpi=150, bbox_inches='tight', transparent=True)
    plt.close(fig)

coset_partition()
print("✓ Coset partition")

# ────────────────────────────────────────────────────────────
# 6. GF(2^3) field construction table
# ────────────────────────────────────────────────────────────
def gf8_table():
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')

    data = [
        ['Power', 'Polynomial', 'Binary', 'Integer'],
        ['$\\alpha^0$', '$1$', '001', '1'],
        ['$\\alpha^1$', '$\\alpha$', '010', '2'],
        ['$\\alpha^2$', '$\\alpha^2$', '100', '4'],
        ['$\\alpha^3$', '$\\alpha + 1$', '011', '3'],
        ['$\\alpha^4$', '$\\alpha^2 + \\alpha$', '110', '6'],
        ['$\\alpha^5$', '$\\alpha^2 + \\alpha + 1$', '111', '7'],
        ['$\\alpha^6$', '$\\alpha^2 + 1$', '101', '5'],
    ]

    table = ax.table(cellText=data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.6)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#30363d')
        if row == 0:
            cell.set_facecolor('#21262d')
            cell.set_text_props(color='#58a6ff', fontweight='bold')
        else:
            cell.set_facecolor('#161b22')
            cell.set_text_props(color='white')

    ax.set_title('Elements of $GF(2^3)$ with primitive polynomial $x^3 + x + 1$',
                 fontsize=14, color='#58a6ff', pad=20)
    fig.savefig(f'{OUT}/gf8_table.png', dpi=150, bbox_inches='tight', transparent=True)
    plt.close(fig)

gf8_table()
print("✓ GF(2^3) table")

# ────────────────────────────────────────────────────────────
# 7. U(n) comparison: U(7) vs U(8)
# ────────────────────────────────────────────────────────────
def un_comparison():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    def draw_un(ax, n, title):
        from math import gcd
        elems = [k for k in range(1, n) if gcd(k, n) == 1]
        m = len(elems)
        angles = [2 * np.pi * i / m - np.pi/2 for i in range(m)]
        r = 0.85

        # Find if cyclic: check if any element has order m
        is_cyclic = False
        generator = None
        for g in elems:
            order = 1
            val = g
            while val != 1:
                val = (val * g) % n
                order += 1
            if order == m:
                is_cyclic = True
                generator = g
                break

        for i, e in enumerate(elems):
            x, y = r * np.cos(angles[i]), r * np.sin(angles[i])
            c = '#ffd700' if e == generator else '#58a6ff'
            circle = plt.Circle((x, y), 0.1, color=c, ec='#79c0ff', lw=2, zorder=5)
            ax.add_patch(circle)
            ax.text(x, y, str(e), ha='center', va='center', fontsize=13, fontweight='bold', color='#0d1117', zorder=6)

        status = f'Cyclic (gen={generator})' if is_cyclic else 'Not cyclic'
        color = '#7ee787' if is_cyclic else '#ff7b72'
        ax.set_title(f'{title}\n$|U({n})| = {m}$, {status}', fontsize=12, color=color)
        ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
        ax.set_aspect('equal'); ax.axis('off')

    draw_un(ax1, 7, '$U(7)$')
    draw_un(ax2, 8, '$U(8)$')
    fig.savefig(f'{OUT}/un_comparison.png', dpi=150, bbox_inches='tight', transparent=True)
    plt.close(fig)

un_comparison()
print("✓ U(n) comparison")

# ────────────────────────────────────────────────────────────
# 8. GF(p^n) construction analogy
# ────────────────────────────────────────────────────────────
def field_construction():
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axis('off')

    data = [
        ['Base Field', 'Polynomial', 'Quotient Ring', 'Extension Field'],
        ['$\\mathbb{R}$', '$x^2 + 1$', '$\\mathbb{R}[x]/\\langle x^2+1\\rangle$', '$\\mathbb{C}$'],
        ['$GF(2)$', '$x^2 + x + 1$', '$GF(2)[x]/\\langle x^2+x+1\\rangle$', '$GF(4)$'],
        ['$GF(2)$', '$x^3 + x + 1$', '$GF(2)[x]/\\langle x^3+x+1\\rangle$', '$GF(8)$'],
        ['$GF(2)$', '$x^8 + x^4 + x^3 + x^2 + 1$', '$GF(2)[x]/\\langle \\ldots \\rangle$', '$GF(256)$'],
    ]

    table = ax.table(cellText=data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.8)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#30363d')
        if row == 0:
            cell.set_facecolor('#21262d')
            cell.set_text_props(color='#58a6ff', fontweight='bold')
        elif row == 1:
            cell.set_facecolor('#1c2128')
            cell.set_text_props(color='#ffd700')
        else:
            cell.set_facecolor('#161b22')
            cell.set_text_props(color='white')

    ax.set_title('Field Extensions: Same Construction, Different Base', fontsize=14, color='#58a6ff', pad=15)
    fig.savefig(f'{OUT}/field_construction.png', dpi=150, bbox_inches='tight', transparent=True)
    plt.close(fig)

field_construction()
print("✓ Field construction analogy")

# ────────────────────────────────────────────────────────────
# 9. RS encoding conceptual diagram
# ────────────────────────────────────────────────────────────
def rs_encoding():
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axis('off')

    # Data block
    data_width = 0.5
    ec_width = 0.25
    y = 0.5
    h = 0.3

    # Data bytes
    ax.add_patch(plt.Rectangle((0.05, y-h/2), data_width, h, facecolor='#58a6ff', ec='white', lw=2))
    ax.text(0.05 + data_width/2, y, 'Data\n(k symbols)', ha='center', va='center', fontsize=12, fontweight='bold', color='white')

    # EC bytes
    ax.add_patch(plt.Rectangle((0.05 + data_width + 0.02, y-h/2), ec_width, h, facecolor='#ff7b72', ec='white', lw=2))
    ax.text(0.05 + data_width + 0.02 + ec_width/2, y, 'Parity\n(2t symbols)', ha='center', va='center', fontsize=11, fontweight='bold', color='white')

    # Arrow
    ax.annotate('', xy=(0.05 + data_width + ec_width + 0.08, y), xytext=(0.05 + data_width + ec_width + 0.04, y),
                arrowprops=dict(arrowstyle='->', color='white', lw=2))

    # Formula
    ax.text(0.88, y, '$m(x) \\cdot x^{2t}$  mod  $g(x)$', ha='center', va='center', fontsize=13, color='#ffd700')

    ax.text(0.05 + (data_width + ec_width + 0.02)/2, y + h/2 + 0.08,
            'Reed-Solomon Codeword (n = k + 2t symbols)', ha='center', va='top', fontsize=14, color='#58a6ff')
    ax.text(0.88, y - 0.2, 'Can correct up to $t$ errors', ha='center', va='top', fontsize=11, color='#7ee787')

    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    fig.savefig(f'{OUT}/rs_encoding.png', dpi=150, bbox_inches='tight', transparent=True)
    plt.close(fig)

rs_encoding()
print("✓ RS encoding diagram")

print("\n✅ All assets generated successfully!")
