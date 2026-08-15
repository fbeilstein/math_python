#!/usr/bin/env python3
"""Generate all network-diagram SVGs for the Systems Biochemistry course.

Outputs to:
  lectures/images/diagrams/   — used by chapter 05 markdown
  practice/biochem_problem/description/images/  — used by problem.tex (as SVG; convert to PNG externally)
"""
import os, textwrap

BASE = "/data/python_scripts/math_python/04_systems_biochemistry"
LECTURE_DIR = os.path.join(BASE, "lectures", "images", "diagrams")
PRACTICE_DIR = os.path.join(BASE, "practice", "biochem_problem", "description", "images")
os.makedirs(LECTURE_DIR, exist_ok=True)
os.makedirs(PRACTICE_DIR, exist_ok=True)

# ─── shared SVG primitives ──────────────────────────────────────────────────

DEFS = textwrap.dedent("""\
    <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
                markerWidth="6" markerHeight="6" orient="auto">
            <path d="M0 0 L10 5 L0 10 z" fill="#333"/>
        </marker>
        <marker id="activate" viewBox="0 0 10 10" refX="9" refY="5"
                markerWidth="6" markerHeight="6" orient="auto">
            <path d="M0 0 L10 5 L0 10 z" fill="#388e3c"/>
        </marker>
        <marker id="inhibit" viewBox="0 0 10 10" refX="9" refY="5"
                markerWidth="6" markerHeight="6" orient="auto">
            <line x1="9" y1="0" x2="9" y2="10" stroke="#d32f2f" stroke-width="2.5"/>
        </marker>
    </defs>""")


def _svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'style="font-family:Arial,sans-serif;background:transparent;">\n'
            f'{DEFS}\n{body}\n</svg>\n')


def circ(x, y, label, r=22, fill="#e0e0e0", stroke="#333", fsz=15):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'<text x="{x}" y="{y+5}" font-size="{fsz}" font-weight="bold" '
            f'text-anchor="middle">{label}</text>')


def rect(x, y, w, h, label, fill="#fff3e0", stroke="#e65100", fsz=13):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'<text x="{x+w/2}" y="{y+h/2+5}" font-size="{fsz}" font-weight="bold" '
            f'text-anchor="middle">{label}</text>')


def lbl(x, y, text, fsz=13, color="#555"):
    return f'<text x="{x}" y="{y}" font-size="{fsz}" fill="{color}" text-anchor="middle">{text}</text>'


def line(x1, y1, x2, y2, marker="arrow", color="#333", dash=False, sw=2):
    d = ' stroke-dasharray="6,4"' if dash else ''
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}" marker-end="url(#{marker})"{d}/>')


def curve(x1, y1, cx, cy, x2, y2, marker="arrow", color="#333", dash=False, sw=2):
    d = ' stroke-dasharray="6,4"' if dash else ''
    return (f'<path d="M{x1} {y1} Q{cx} {cy} {x2} {y2}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" marker-end="url(#{marker})"{d}/>')


def save(path, content):
    with open(path, 'w') as f:
        f.write(content)
    print(f"  ✓ {os.path.basename(path)}")


# ═══════════════════════════════════════════════════════════════════════════════
# LECTURE DIAGRAMS  (Chapter 05)
# ═══════════════════════════════════════════════════════════════════════════════

def rule1a_open_system():
    """∅ →(Vin)→ X →(k_out)→ ∅"""
    b = ""
    b += lbl(30, 80, "∅", 20)
    b += line(48, 75, 75, 75)
    b += lbl(62, 62, "V_in")
    b += circ(100, 75, "X")
    b += line(125, 75, 168, 75)
    b += lbl(147, 62, "k_out")
    b += lbl(190, 80, "∅", 20)
    return _svg(220, 120, b)


def rule1b_bimolecular():
    """X + Y →(k₁)→ Z"""
    b = ""
    b += circ(60, 50, "X")
    b += lbl(110, 55, "+", 20, "#333")
    b += circ(155, 50, "Y")
    b += line(180, 50, 230, 50)
    b += lbl(205, 37, "k₁")
    b += circ(260, 50, "Z")
    return _svg(320, 100, b)


def rule2_michaelis_menten():
    """S →(E cat)→ P"""
    b = ""
    b += circ(60, 85, "S")
    b += line(85, 85, 175, 85)
    b += lbl(130, 72, "V_max, K_M")
    b += circ(205, 85, "P")
    b += circ(130, 30, "E", fill="#e8f5e9", stroke="#388e3c")
    b += line(130, 52, 130, 73, marker="activate", color="#388e3c", dash=True)
    b += lbl(155, 52, "cat", 11, "#388e3c")
    return _svg(270, 130, b)


def rule3a_activation():
    """A activates production of B, both degrade.
    ∅ →→ B →→ ∅  with A ---(+)--→ reaction arrow"""
    b = ""
    b += lbl(25, 75, "∅", 20)
    b += line(40, 70, 80, 70)
    b += lbl(60, 57, "k₀")
    b += circ(110, 70, "B")
    b += line(135, 70, 178, 70)
    b += lbl(157, 57, "k_d")
    b += lbl(198, 75, "∅", 20)
    # Activator A boosts the production arrow
    b += circ(60, 130, "A", fill="#e8f5e9", stroke="#388e3c")
    b += line(60, 107, 60, 80, marker="activate", color="#388e3c", dash=True)
    b += lbl(80, 105, "(+)", 11, "#388e3c")
    return _svg(220, 165)


def rule3a_activation():
    b = ""
    b += lbl(25, 75, "∅", 20)
    b += line(40, 70, 80, 70)
    b += lbl(60, 57, "k₀")
    b += circ(110, 70, "B")
    b += line(135, 70, 178, 70)
    b += lbl(157, 57, "k_d")
    b += lbl(198, 75, "∅", 20)
    b += circ(60, 130, "A", fill="#e8f5e9", stroke="#388e3c")
    b += line(60, 107, 60, 82, marker="activate", color="#388e3c", dash=True)
    return _svg(220, 160, b)


def rule3b_repression():
    """I represses production of X via Hill function.
    ∅ →→ X →→ ∅  with I ---⊣--- reaction arrow"""
    b = ""
    b += lbl(25, 75, "∅", 20)
    b += line(40, 70, 80, 70)
    b += lbl(60, 57, "V₀")
    b += circ(110, 70, "X")
    b += line(135, 70, 178, 70)
    b += lbl(157, 57, "k_d")
    b += lbl(198, 75, "∅", 20)
    b += circ(60, 130, "I", fill="#ffebee", stroke="#d32f2f")
    b += line(60, 107, 60, 82, marker="inhibit", color="#d32f2f", dash=True)
    return _svg(220, 160, b)


def rule4_goldbeter():
    """W ⇌ W* with kinase K and phosphatase P"""
    b = ""
    b += circ(60, 90, "W", fill="#e0e0e0")
    b += line(90, 80, 155, 80)
    b += lbl(122, 68, "v₁")
    b += line(155, 100, 90, 100)
    b += lbl(122, 118, "v₂")
    b += circ(185, 90, "W*", fill="#e8f5e9", stroke="#388e3c")
    # Kinase
    b += circ(122, 30, "K", r=18, fill="#e3f2fd", stroke="#1565c0", fsz=13)
    b += line(122, 48, 122, 68, marker="activate", color="#388e3c", dash=True)
    # Phosphatase
    b += circ(122, 150, "P", r=18, fill="#fce4ec", stroke="#c62828", fsz=13)
    b += line(122, 132, 122, 112, marker="activate", color="#388e3c", dash=True)
    return _svg(250, 180, b)


def example1_turing():
    """Gierer-Meinhardt: A autocatalysis, A→I, I⊣A, both degrade"""
    b = ""
    # Nodes
    b += circ(100, 90, "A", r=28, fill="#e8f5e9", stroke="#388e3c", fsz=18)
    b += circ(280, 90, "I", r=28, fill="#ffebee", stroke="#d32f2f", fsz=18)
    # Autocatalysis loop on A
    b += curve(80, 65, 60, 15, 120, 65, marker="activate", color="#388e3c", dash=True)
    b += lbl(100, 30, "A²", 12, "#388e3c")
    # A activates I
    b += curve(128, 78, 190, 50, 252, 78, marker="activate", color="#388e3c", dash=True)
    b += lbl(190, 60, "+", 14, "#388e3c")
    # I inhibits A
    b += curve(252, 102, 190, 130, 128, 102, marker="inhibit", color="#d32f2f", dash=True)
    b += lbl(190, 125, "⊣", 14, "#d32f2f")
    # Basal synthesis of A
    b += lbl(25, 95, "∅", 18)
    b += line(38, 90, 68, 90)
    b += lbl(53, 78, "V₀", 11)
    # Degradation A
    b += lbl(100, 160, "∅", 16)
    b += line(100, 120, 100, 145)
    b += lbl(115, 138, "k_A", 11)
    # Degradation I
    b += lbl(280, 160, "∅", 16)
    b += line(280, 120, 280, 145)
    b += lbl(295, 138, "k_I", 11)
    return _svg(380, 175, b)


def example2_oregonator():
    """Oregonator FKN mechanism: X, Y, Z + constant pool A.
    Shows reaction channels with ± annotations."""
    b = ""
    # Constant pool A
    b += rect(155, 5, 50, 28, "A", fill="#fff3e0", stroke="#e65100")
    b += lbl(180, 50, "(pool)", 10, "#999")
    # Dynamic species triangle
    b += circ(80, 130, "X", r=25, fill="#e3f2fd", stroke="#1565c0", fsz=16)
    b += circ(280, 130, "Y", r=25, fill="#ffebee", stroke="#d32f2f", fsz=16)
    b += circ(180, 60, "Z", r=25, fill="#e8f5e9", stroke="#388e3c", fsz=16)
    # X → Z (R3 produces Z from X)
    b += line(100, 115, 155, 75)
    b += lbl(115, 85, "k₃AX", 10)
    # Z → Y (R5: recovery)
    b += line(205, 75, 258, 118)
    b += lbl(245, 88, "k₅Z", 10)
    # Y consumes X (R2: X+Y → products)
    b += line(255, 130, 110, 130)
    b += lbl(180, 148, "k₂XY", 10)
    # X autocatalysis (R3: A+X → 2X+2Z)
    b += curve(60, 110, 25, 60, 65, 108, marker="activate", color="#388e3c", dash=True)
    b += lbl(25, 100, "+", 14, "#388e3c")
    # A feeds into X via Y (R1: A+Y → X)
    b += curve(170, 33, 110, 60, 90, 105, marker="arrow", color="#333", dash=False)
    b += lbl(110, 55, "k₁AY", 10)
    # X self-degradation (R4: 2X → ...)
    b += lbl(80, 195, "∅", 16)
    b += line(80, 157, 80, 180)
    b += lbl(97, 175, "2k₄X²", 10)
    return _svg(350, 210, b)


# ═══════════════════════════════════════════════════════════════════════════════
# PRACTICE PROBLEM DIAGRAMS
# ═══════════════════════════════════════════════════════════════════════════════

def glycolysis_bier():
    """Bier glycolysis: Vin → G, G+ATP → 2ATP (with Km sat.), ATP → ADP"""
    b = ""
    # External glucose source
    b += lbl(20, 75, "∅", 18)
    b += line(35, 70, 65, 70)
    b += lbl(50, 57, "V_in")
    # G node
    b += circ(95, 70, "G", fill="#e3f2fd", stroke="#1565c0")
    # G + ATP → (reaction)
    b += line(120, 70, 175, 70)
    b += lbl(147, 57, "k₁")
    # ATP node
    b += circ(205, 70, "ATP", r=25, fill="#e8f5e9", stroke="#388e3c", fsz=13)
    # ATP degradation (Michaelis-Menten: kp·ATP/(ATP+Km))
    b += line(232, 70, 285, 70)
    b += lbl(260, 57, "k_p/(ATP+K_m)", 10)
    b += lbl(305, 75, "ADP", 14, "#333")
    # Feedback: ATP consumed in G→ATP reaction (stoichiometry: produces 2 ATP)
    b += curve(205, 95, 150, 120, 110, 90, marker="activate", color="#388e3c", dash=True)
    b += lbl(145, 115, "×2", 12, "#388e3c")
    return _svg(340, 140, b)


def bioswitch_gk():
    """Goldbeter-Koshland zero-order mutual activation switch"""
    b = ""
    # Nodes
    b += rect(20, 10, 90, 25, "stimulus, [S]", fill="#fff3e0", stroke="#e65100")
    b += rect(140, 60, 100, 25, "response, [R]", fill="#e3f2fd", stroke="#1565c0")
    b += rect(10, 120, 140, 25, "enzyme phosph., [E_p]", fill="#e8f5e9", stroke="#388e3c")
    b += rect(180, 120, 80, 25, "enzyme, [E]", fill="#e8f5e9", stroke="#388e3c")
    
    # R production/degradation
    b += line(60, 72, 137, 72)
    b += line(243, 72, 300, 72)
    b += lbl(320, 77, "∅", 20)
    
    # S activates R production
    b += line(65, 37, 65, 70, marker="activate", dash=True, color="#e65100")
    # Ep activates R production
    b += line(100, 118, 100, 74, marker="activate", dash=True, color="#388e3c")
    
    # Ep <-> E conversions
    b += line(153, 128, 178, 128)  # Ep -> E (phosphatase)
    b += line(178, 137, 153, 137)  # E -> Ep (kinase)
    
    # R activates E -> Ep (the kinase reaction)
    b += line(185, 87, 165, 135, marker="activate", dash=True, color="#1565c0")
    
    return _svg(350, 160, b)


def cusp_cell_cycle():
    """Cell cycle checkpoint: Cyclin and Wee1 control Cdc2 activation via cusp."""
    b = ""
    # Parameters as rectangular boxes
    b += rect(15, 15, 65, 28, "Cyclin", fill="#e8f5e9", stroke="#388e3c")
    b += rect(15, 100, 55, 28, "Wee1", fill="#ffebee", stroke="#d32f2f")
    # State variable
    b += circ(200, 70, "C", r=28, fill="#e3f2fd", stroke="#1565c0", fsz=20)
    b += lbl(200, 110, "(active Cdc2)", 10, "#999")
    # Cyclin → C (normal factor, drives the cell cycle)
    b += line(82, 29, 170, 60, marker="activate", color="#388e3c", dash=True)
    b += lbl(130, 30, "(+)", 11, "#388e3c")
    # Wee1 → C (splitting factor, creates bistability)
    b += line(72, 114, 170, 82, marker="activate", color="#1565c0", dash=True)
    b += lbl(125, 110, "(splitting)", 10, "#1565c0")
    # C self-interaction (cubic nonlinearity)
    b += curve(220, 48, 250, 15, 215, 42, marker="inhibit", color="#d32f2f", dash=True)
    b += lbl(255, 25, "−C³", 12, "#d32f2f")
    return _svg(290, 130, b)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generating lecture SVGs …")
    save(os.path.join(LECTURE_DIR, "rule1a_open_system.svg"), rule1a_open_system())
    save(os.path.join(LECTURE_DIR, "rule1b_bimolecular.svg"), rule1b_bimolecular())
    save(os.path.join(LECTURE_DIR, "rule2_michaelis_menten.svg"), rule2_michaelis_menten())
    save(os.path.join(LECTURE_DIR, "rule3a_activation.svg"), rule3a_activation())
    save(os.path.join(LECTURE_DIR, "rule3b_repression.svg"), rule3b_repression())
    save(os.path.join(LECTURE_DIR, "rule4_goldbeter.svg"), rule4_goldbeter())
    save(os.path.join(LECTURE_DIR, "example1_turing.svg"), example1_turing())
    save(os.path.join(LECTURE_DIR, "example2_oregonator.svg"), example2_oregonator())

    print("\nGenerating practice SVGs …")
    save(os.path.join(PRACTICE_DIR, "glycolysis_bier.svg"), glycolysis_bier())
    save(os.path.join(PRACTICE_DIR, "bioswitch_gk.svg"), bioswitch_gk())
    save(os.path.join(PRACTICE_DIR, "cusp_cell_cycle.svg"), cusp_cell_cycle())

    print("\nDone. All diagrams generated.")
