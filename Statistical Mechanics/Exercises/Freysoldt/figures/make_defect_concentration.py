"""Write defect-concentration.tex: two plots for the lattice model of defects.

(a) Constrained grand potential per site against the defect concentration c,
    [Phi~(N_X) - Phi_bulk] / (N k_B T) = c E^f/k_BT - s_conf(c)/k_B,
    for E^f = 2 k_B T and g_X = 1, with the two contributions and the minimum
    at c = 1/(1 + e^2). The minimum value equals -ln(1 + e^-2), the exact
    defect part of the grand potential per site.
(b) Defect concentration against E^f/k_BT for g_X = 1 on a logarithmic scale:
    exact result c = 1/(1 + e^{E^f/k_BT}) and dilute limit e^{-E^f/k_BT}.

Usage: python3 make_defect_concentration.py > defect-concentration.tex
"""
import math

W, H = 5.6, 4.4
EF = 2.0                       # E^f / k_B T in panel (a)


def s_conf(c):                 # per site, in units of k_B, g_X = 1
    if c <= 0.0 or c >= 1.0:
        return 0.0
    return -c * math.log(c) - (1 - c) * math.log(1 - c)


def panel_a(shift):
    cmax, ymin, ymax = 0.40, -0.75, 0.90
    px = lambda c: c / cmax * W
    py = lambda y: (y - ymin) / (ymax - ymin) * H
    cs = [cmax * i / 400 for i in range(401)]
    out = [rf"\begin{{scope}}[xshift={shift}cm]"]
    # axes at the left and the bottom, with a thin zero line
    out.append(rf"\draw[->] (0,0) -- ({W + 0.35:.2f},0) node[right] {{$c$}};")
    out.append(rf"\draw[->] (0,0) -- (0,{H + 0.35:.2f});")
    out.append(rf"\draw[line width=0.4pt] (0,{py(0):.3f}) -- ({W:.3f},{py(0):.3f});")
    out.append(rf"\node[anchor=south west] at (-0.75,{H + 0.35:.2f}) "
               r"{$\big[\widetilde{\Phi}(N_X)-\Phi_{\text{bulk}}\big]/Nk_BT$};")
    for c in (0.0, 0.2, 0.4):
        out.append(rf"\draw ({px(c):.3f},-0.07) -- ({px(c):.3f},0.07);")
        out.append(rf"\node[below, font=\footnotesize] at ({px(c):.3f},-0.05) {{${c:g}$}};")
    for y in (-0.5, 0.0, 0.5):
        out.append(rf"\draw (-0.07,{py(y):.3f}) -- (0.07,{py(y):.3f});")
        out.append(rf"\node[left, font=\footnotesize] at (-0.05,{py(y):.3f}) {{${y:g}$}};")
    # contributions
    e_path = " -- ".join(f"({px(c):.3f},{py(EF * c):.3f})" for c in cs)
    s_path = " -- ".join(f"({px(c):.3f},{py(-s_conf(c)):.3f})" for c in cs)
    t_path = " -- ".join(f"({px(c):.3f},{py(EF * c - s_conf(c)):.3f})" for c in cs)
    out.append(rf"\draw[dashed, line width=0.6pt] {e_path};")
    out.append(rf"\draw[dashed, line width=0.6pt] {s_path};")
    out.append(rf"\draw[line width=1.4pt] {t_path};")
    out.append(rf"\node[anchor=south east, font=\footnotesize] at ({px(0.39):.3f},{py(EF * 0.39) - 0.05:.3f}) "
               r"{$c\,E^f/k_BT$};")
    out.append(rf"\node[anchor=south east, font=\footnotesize] at ({px(0.40):.3f},{py(-s_conf(0.40)) + 0.30:.3f}) "
               r"{$-s_{\text{conf}}/k_B$};")
    out.append(rf"\node[anchor=south, font=\footnotesize] at ({px(0.33):.3f},{py(EF * 0.33 - s_conf(0.33)) + 0.08:.3f}) "
               r"{total};")
    # minimum
    ceq = 1.0 / (1.0 + math.exp(EF))
    ymin_val = EF * ceq - s_conf(ceq)
    assert abs(ymin_val + math.log(1 + math.exp(-EF))) < 1e-12
    out.append(rf"\draw[dotted] ({px(ceq):.3f},0) -- ({px(ceq):.3f},{py(ymin_val):.3f});")
    out.append(rf"\fill ({px(ceq):.3f},{py(ymin_val):.3f}) circle (2pt);")
    out.append(rf"\node[below, font=\footnotesize] at ({px(ceq):.3f},-0.05) {{$c_{{\text{{eq}}}}$}};")
    out.append(rf"\node[anchor=north west, font=\footnotesize] at ({px(ceq) + 0.05:.3f},{py(ymin_val) - 0.08:.3f}) "
               r"{minimum, $-\ln(1+\zeta_X)$};")
    out.append(rf"\node[anchor=south] at ({W / 2:.3f},{H + 1.05:.2f}) {{(a) $E^f=2k_BT$, $g_X=1$}};")
    out.append(r"\end{scope}")
    return "\n".join(out)


def panel_b(shift):
    xmin, xmax, lmin, lmax = -4.0, 12.0, -5.5, 0.5
    px = lambda x: (x - xmin) / (xmax - xmin) * W
    py = lambda l: (l - lmin) / (lmax - lmin) * H
    xs = [xmin + (xmax - xmin) * i / 400 for i in range(401)]
    out = [rf"\begin{{scope}}[xshift={shift}cm]"]
    out.append(rf"\draw[->] (0,0) -- ({W + 0.35:.2f},0) node[right] {{$E^f/k_BT$}};")
    out.append(rf"\draw[->] (0,0) -- (0,{H + 0.35:.2f});")
    out.append(rf"\node[anchor=south west] at (-0.75,{H + 0.35:.2f}) {{$c$}};")
    for x in (-4, 0, 4, 8, 12):
        out.append(rf"\draw ({px(x):.3f},-0.07) -- ({px(x):.3f},0.07);")
        out.append(rf"\node[below, font=\footnotesize] at ({px(x):.3f},-0.05) {{${x}$}};")
    for l in (0, -2, -4):
        lab = "1" if l == 0 else rf"10^{{{l}}}"
        out.append(rf"\draw (-0.07,{py(l):.3f}) -- (0.07,{py(l):.3f});")
        out.append(rf"\node[left, font=\footnotesize] at (-0.05,{py(l):.3f}) {{${lab}$}};")
    exact = [(x, -math.log10(1 + math.exp(x))) for x in xs]
    dilute = [(x, -x / math.log(10)) for x in xs if -x / math.log(10) <= lmax]
    out.append(r"\draw[dashed, line width=0.6pt] " +
               " -- ".join(f"({px(x):.3f},{py(l):.3f})" for x, l in dilute) + ";")
    out.append(r"\draw[line width=1.4pt] " +
               " -- ".join(f"({px(x):.3f},{py(l):.3f})" for x, l in exact if l >= lmin) + ";")
    out.append(rf"\node[anchor=north west, font=\footnotesize] at ({px(-3.9):.3f},{py(-0.25):.3f}) {{exact}};")
    out.append(rf"\node[anchor=south west, font=\footnotesize] at ({px(0.3):.3f},{py(0.02):.3f}) "
               r"{dilute limit, $e^{-E^f/k_BT}$};")
    out.append(rf"\node[anchor=south] at ({W / 2:.3f},{H + 1.05:.2f}) {{(b) $g_X=1$}};")
    out.append(r"\end{scope}")
    return "\n".join(out)


print(r"""% Standalone figure for "Freysoldt's Review.tex" (Sections 5 and 7).
% Generated by make_defect_concentration.py.
\documentclass[11pt,tikz,border=2pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows.meta, positioning}
\begin{document}
\begin{tikzpicture}[font=\small, >=Latex, line width=0.8pt]""")
print(panel_a(0.0))
print(panel_b(7.7))
print(r"""\end{tikzpicture}
\end{document}""")
