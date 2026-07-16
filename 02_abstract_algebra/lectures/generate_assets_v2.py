"""Generate additional lecture assets for expanded slides."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT = '/data/python_scripts/math_python/02_abstract_algebra/lectures/assets'

plt.rcParams.update({
    'figure.facecolor': '#0d1117',
    'axes.facecolor': '#0d1117',
    'text.color': 'white',
    'axes.labelcolor': 'white',
})

# ────────────────────────────────────────────────────────────
# 1. Cayley table for Z_4
# ────────────────────────────────────────────────────────────
def cayley_table(elements, op, labels, title, filename, highlight_zeros=False):
    n = len(elements)
    fig, ax = plt.subplots(figsize=(4 + n * 0.4, 3.5 + n * 0.35))
    ax.axis('off')

    header = ['·'] + labels
    data = [header]
    for i, a in enumerate(elements):
        row = [labels[i]]
        for j, b in enumerate(elements):
            result = op(a, b)
            idx = elements.index(result)
            row.append(labels[idx])
        data.append(row)

    table = ax.table(cellText=data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12 if n <= 6 else 10)
    table.scale(1, 1.5)

    # Color palette for element identification
    palette = ['#58a6ff', '#7ee787', '#ffa657', '#d2a8ff', '#ff7b72', '#79c0ff', '#f0e68c', '#ff69b4']

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#30363d')
        if row == 0 or col == 0:
            cell.set_facecolor('#21262d')
            cell.set_text_props(color='#58a6ff', fontweight='bold')
        else:
            val_text = data[row][col]
            val_idx = labels.index(val_text) if val_text in labels else 0
            if highlight_zeros and val_text == labels[0]:
                cell.set_facecolor('#3d1a1a')
                cell.set_text_props(color='#ff7b72', fontweight='bold')
            else:
                base = palette[val_idx % len(palette)]
                # Make it darker for table background
                r, g, b_c = int(base[1:3], 16), int(base[3:5], 16), int(base[5:7], 16)
                cell.set_facecolor(f'#{r//4:02x}{g//4:02x}{b_c//4:02x}')
                cell.set_text_props(color=base)

    ax.set_title(title, fontsize=14, color='#58a6ff', pad=15)
    fig.savefig(f'{OUT}/{filename}', dpi=150, bbox_inches='tight', transparent=True)
    plt.close(fig)

# Z_4 addition table
elems_z4 = [0, 1, 2, 3]
cayley_table(elems_z4, lambda a, b: (a + b) % 4,
             ['0', '1', '2', '3'], '$\\mathbb{Z}_4$ (addition)', 'cayley_table_z4.png')
print("✓ Z_4 table")

# U(8) multiplication table
elems_u8 = [1, 3, 5, 7]
cayley_table(elems_u8, lambda a, b: (a * b) % 8,
             ['1', '3', '5', '7'], '$U(8)$ (multiplication)', 'cayley_table_u8.png')
print("✓ U(8) table")

# Z_6 multiplication table (shows zero divisors)
elems_z6 = [0, 1, 2, 3, 4, 5]
cayley_table(elems_z6, lambda a, b: (a * b) % 6,
             ['0', '1', '2', '3', '4', '5'], '$\\mathbb{Z}_6$ multiplication', 'cayley_table_z6_mul.png',
             highlight_zeros=True)
print("✓ Z_6 mul table")

# Z_5 multiplication table (no zero divisors)
elems_z5 = [0, 1, 2, 3, 4]
cayley_table(elems_z5, lambda a, b: (a * b) % 5,
             ['0', '1', '2', '3', '4'], '$\\mathbb{Z}_5$ multiplication', 'cayley_table_z5_mul.png',
             highlight_zeros=True)
print("✓ Z_5 mul table")

print("\n✅ All additional assets generated!")
