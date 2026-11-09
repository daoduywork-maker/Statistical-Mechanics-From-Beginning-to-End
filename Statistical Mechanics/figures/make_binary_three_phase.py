"""Write binary-three-phase.tex: a eutectic computed from regular-solution
free energies (k_B = 1), shown as g(X) at three temperatures and as the
isobaric T--X diagram.

Model: g = (1-X) G_A + X G_B + T[X ln X + (1-X) ln(1-X)] + Omega X(1-X)
  liquid L: G_A = G_B = 0, Omega = 0
  solid a : G_A = DS (T - TA), G_B = DS (T - TB) + D, Omega = OMS
  solid b : G_A = DS (T - TA) + D, G_B = DS (T - TB), Omega = OMS
The equilibrium g is the lower convex hull of the three curves.

Usage: python3 make_binary_three_phase.py > binary-three-phase.tex   (needs numpy)
"""
import numpy as np

TA, TB, DS, D, OMS = 1.0, 0.9, 1.0, 0.3, 1.0


def mix(X, T):
    X = np.clip(X, 1e-12, 1 - 1e-12)
    return T * (X * np.log(X) + (1 - X) * np.log(1 - X))


PH = {
    "L": lambda X, T: mix(X, T),
    "a": lambda X, T: (1 - X) * DS * (T - TA) + X * (DS * (T - TB) + D) + mix(X, T) + OMS * X * (1 - X),
    "b": lambda X, T: (1 - X) * (DS * (T - TA) + D) + X * DS * (T - TB) + mix(X, T) + OMS * X * (1 - X),
}
LABEL = {"L": "L", "a": r"\alpha", "b": r"\beta"}


def hull(T, n=6001):
    X = np.linspace(0, 1, n)
    pts = sorted(((x, g, k) for k, f in PH.items() for x, g in zip(X, f(X, T))),
                 key=lambda p: (p[0], p[1]))
    h = []
    for p in pts:
        while len(h) >= 2 and (h[-1][0] - h[-2][0]) * (p[1] - h[-2][1]) \
                - (h[-1][1] - h[-2][1]) * (p[0] - h[-2][0]) <= 0:
            h.pop()
        h.append(p)
    return [(a, b) for a, b in zip(h, h[1:])
            if (a[2] != b[2] or b[0] - a[0] > 3 / n) and a[0] < 0.999]


def kinds(T):
    return [frozenset((a[2], b[2])) for a, b in hull(T)]


lo, hi = 0.3, 0.9
for _ in range(45):
    m = (lo + hi) / 2
    lo, hi = (m, hi) if frozenset("ab") in kinds(m) else (lo, m)
TE = hi
T_ABOVE, T_BELOW = TE + 0.07, TE - 0.07

# ---------------------------------------------------------------- T--X diagram
X0, Y0, W, H = 0.0, 0.0, 8.0, 5.2
TMIN, TMAX = 0.35, 1.05
tx = lambda X: X0 + X * W
ty = lambda T: Y0 + (T - TMIN) / (TMAX - TMIN) * H

branches = {k: [] for k in ("aL_a", "aL_L", "Lb_L", "Lb_b", "ab_a", "ab_b")}
for T in np.linspace(TMIN, 1.0, 140):
    for a, b in hull(T):
        pair = frozenset((a[2], b[2]))
        if pair == frozenset("aL"):
            branches["aL_a"].append((a[0], T)); branches["aL_L"].append((b[0], T))
        elif pair == frozenset("Lb"):
            branches["Lb_L"].append((a[0], T)); branches["Lb_b"].append((b[0], T))
        elif pair == frozenset("ab") and T < TE:
            branches["ab_a"].append((a[0], T)); branches["ab_b"].append((b[0], T))
segE = {frozenset((a[2], b[2])): (a[0], b[0]) for a, b in hull(TE + 1e-6)}
XaE, XLE = segE[frozenset("aL")]
_, XbE = segE[frozenset("Lb")]
for k, pt in (("aL_a", (XaE, TE)), ("aL_L", (XLE, TE)), ("Lb_L", (XLE, TE)),
              ("Lb_b", (XbE, TE)), ("ab_a", (XaE, TE)), ("ab_b", (XbE, TE))):
    branches[k].append(pt)
branches["aL_a"].append((0.0, TA)); branches["aL_L"].append((0.0, TA))
branches["Lb_L"].append((1.0, TB)); branches["Lb_b"].append((1.0, TB))


def path(pts):
    pts = sorted(pts, key=lambda p: p[1])
    return " -- ".join(f"({tx(x):.3f},{ty(T):.3f})" for x, T in pts)


# ---------------------------------------------------------------- g(X) panels
PW, PHT = 4.6, 3.4


def panel(T, xshift, tag):
    xs = np.linspace(0.005, 0.995, 300)
    base0 = min(f(np.array([0.0]), T)[0] for f in PH.values())
    base1 = min(f(np.array([1.0]), T)[0] for f in PH.values())
    base = lambda X: base0 + (base1 - base0) * X
    segs = hull(T)
    lows = [min(PH[k](xs, T) - base(xs)) for k in PH]
    ymin = min(lows) * 1.15
    ymax = -ymin * 0.9
    sy = PHT / (ymax - ymin)
    px = lambda X: X * PW
    py = lambda g: (g - ymin) * sy
    out = [rf"\begin{{scope}}[xshift={xshift}cm, yshift=6.6cm]",
           rf"    \draw[->] (0,0) -- ({PW + 0.3:.2f},0) node[right] {{$X$}};",
           rf"    \draw[->] (0,0) -- (0,{PHT + 0.3:.2f}) node[above] {{$\tilde g$}};",
           rf"    \node[anchor=south] at ({PW / 2:.2f},{PHT + 0.35:.2f}) {{{tag}}};",
           rf"    \begin{{scope}}\clip (0,0) rectangle ({PW:.2f},{PHT:.2f});"]
    for k, f in PH.items():
        g = f(xs, T) - base(xs)
        pts = " -- ".join(f"({px(x):.3f},{py(v):.3f})" for x, v in zip(xs, g))
        out.append(rf"    \draw[line width=0.6pt] {pts};")
    for a, b in segs:
        ga = a[1] - base(np.array(a[0])); gb = b[1] - base(np.array(b[0]))
        out.append(rf"    \draw[line width=1.6pt] ({px(a[0]):.3f},{py(ga):.3f}) -- ({px(b[0]):.3f},{py(gb):.3f});")
        out.append(rf"    \fill ({px(a[0]):.3f},{py(ga):.3f}) circle (1.8pt);")
        out.append(rf"    \fill ({px(b[0]):.3f},{py(gb):.3f}) circle (1.8pt);")
    out.append(r"    \end{scope}")
    for k, xl in (("a", 0.07), ("L", 0.5), ("b", 0.93)):
        v = PH[k](np.array([xl]), T)[0] - base(xl)
        yy = min(py(v) + 0.28, PHT - 0.15)
        out.append(rf"    \node at ({px(xl):.3f},{yy:.3f}) {{${LABEL[k]}$}};")
    out.append(r"\end{scope}")
    return "\n".join(out)


print(r"""% Standalone figure for the Statistical Mechanics notes.
% Generated by make_binary_three_phase.py.
% Build: pdflatex binary-three-phase.tex  (or run build.sh in this folder)
\documentclass[11pt,tikz,border=2pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows.meta, positioning}
\begin{document}
\begin{tikzpicture}[font=\small, >=Latex, line width=0.8pt]""")
print(panel(T_ABOVE, 0.0, r"(a) $T_1>T_e$"))
print(panel(TE + 1e-6, 5.6, r"(b) $T_e$"))
print(panel(T_BELOW, 11.2, r"(c) $T_3<T_e$"))
# T--X diagram, centered below
print(r"\begin{scope}[xshift=4.0cm]")
print(rf"    \draw[->] (0,0) -- ({W + 0.3:.2f},0) node[right] {{$X$}};")
print(rf"    \draw[->] (0,0) -- (0,{H + 0.3:.2f}) node[above] {{$T$}};")
print(rf"    \draw ({W:.2f},0) -- ({W:.2f},{H:.2f});")
print(r"    \node[below] at (0,0) {$A$};")
print(rf"    \node[below] at ({W:.2f},0) {{$B$}};")
print(r"    \node[anchor=north west] at (-0.1,-0.45) {(d)};")
for k in branches:
    print(rf"    \draw {path(branches[k])};")
print(rf"    \draw[line width=1.6pt] ({tx(XaE):.3f},{ty(TE):.3f}) -- ({tx(XbE):.3f},{ty(TE):.3f});")
for x in (XaE, XLE, XbE):
    print(rf"    \fill ({tx(x):.3f},{ty(TE):.3f}) circle (1.8pt);")
for T, lab in ((T_ABOVE, "T_1"), (TE, "T_e"), (T_BELOW, "T_3")):
    print(rf"    \draw[dotted] (0,{ty(T):.3f}) -- ({W:.2f},{ty(T):.3f});")
    print(rf"    \node[left] at (0,{ty(T):.3f}) {{${lab}$}};")
for T in (T_ABOVE, T_BELOW):
    for a, b in hull(T):
        print(rf"    \draw[line width=1.0pt] ({tx(a[0]):.3f},{ty(T):.3f}) -- ({tx(b[0]):.3f},{ty(T):.3f});")
        for x in (a[0], b[0]):
            print(rf"    \fill ({tx(x):.3f},{ty(T):.3f}) circle (1.8pt);")
print(rf"    \node at ({tx(0.5):.3f},{ty(0.92):.3f}) {{$L$}};")
print(rf"    \node at ({tx(0.05):.3f},{ty(0.56):.3f}) {{$\alpha$}};")
print(rf"    \node at ({tx(0.955):.3f},{ty(0.53):.3f}) {{$\beta$}};")
print(rf"    \node at ({tx(0.5):.3f},{ty(0.45):.3f}) {{$\alpha+\beta$}};")
print(rf"    \node at ({tx(0.25):.3f},{ty(0.76):.3f}) {{$\alpha+L$}};")
print(rf"    \node at ({tx(0.78):.3f},{ty(0.76):.3f}) {{$L+\beta$}};")
print(r"\end{scope}")
print(r"""\end{tikzpicture}
\end{document}""")
