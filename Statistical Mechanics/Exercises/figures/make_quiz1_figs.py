"""Write the Quiz 1 TikZ figures as standalone files in figures/.

Placeholders @KEY@ are replaced with coordinates from coords.json.
"""
import json
import re
import sys

d = json.load(open(sys.argv[1]))
OUT = sys.argv[2]

HDR = r"""%% Standalone figure for the Statistical Mechanics exercises (Quiz 1).
%% Build: pdflatex @NAME@.tex  (or run build.sh in this folder)
\documentclass[11pt,tikz,border=2pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows.meta, positioning}
\begin{document}
"""
END = "\n\\end{document}\n"


def fill(t, extra=None):
    vals = dict(d)
    vals.update(extra or {})
    return re.sub(r"@(\w+)@", lambda m: str(vals[m.group(1)]), t)


figs = {}

# ------------------------------------------------------------ Problem 2: lens
figs["quiz1_lens"] = r"""\begin{tikzpicture}[font=\small, >=Latex, line width=0.8pt]
    % frame: pure A on the left, pure B on the right
    \draw (0,5.2) -- (0,0) -- (6,0) -- (6,5.2);
    % liquidus and solidus of ideal solid and liquid solutions (computed)
    \draw plot[smooth] coordinates {@lens_liq@};
    \draw plot[smooth] coordinates {@lens_sol@};
    % isotherm T_2 and the four compositions
    \draw[dashed, line width=0.6pt] (-0.2,@T2y@) node[left] {$T_2$} -- (6,@T2y@);
    \foreach \x/\n in {1.02/x_1, 1.80/y, 3.06/z, 4.38/x_2}
        \draw[dashed, line width=0.6pt] (\x,0) node[below] {$\n$} -- (\x,4.7);
    \fill (1.80,@T2y@) circle (1.6pt);
    \fill (3.06,@T2y@) circle (1.6pt);
    % region labels
    \node at (4.9,4.3) {$L$};
    \node at (1.6,1.3) {$\alpha$};
    \node[fill=white, inner sep=0.5pt, font=\footnotesize] at (2.85,2.55) {$L+\alpha$};
    \node[rotate=-28, font=\footnotesize] at (5.25,2.08) {liquidus};
    \node[rotate=-25, font=\footnotesize] at (5.15,1.12) {solidus};
    % axes
    \node[below] at (0,-0.05) {$A$};
    \node[below] at (6,-0.05) {$B$};
    \node[below=14pt] at (3,0) {composition $X$};
    \node[rotate=90] at (-0.85,1.6) {temperature};
\end{tikzpicture}"""

# ------------------------------------------------------------ Problem 3: P-T
figs["quiz1_pt"] = r"""\begin{tikzpicture}[font=\small, >=Latex, line width=0.8pt]
    % axes
    \draw[->] (0,0) -- (10.2,0) node[below left] {$T$};
    \draw[->] (0,0) -- (0,7.0) node[above] {$P$};
    % invariant points
    \coordinate (Q)  at (1.65,2.67);   % quadruple point G alpha beta gamma
    \coordinate (A1) at (3.30,3.35);   % pure A: G alpha gamma
    \coordinate (A2) at (5.56,3.99);   % pure A: G L gamma
    \coordinate (B1) at (4.91,1.98);   % pure B: G beta gamma
    \coordinate (B2) at (6.85,2.27);   % pure B: G L gamma
    \coordinate (CA) at (8.63,4.98);   % critical point of A
    \coordinate (CB) at (9.78,2.97);   % critical point of B
    % binary three-phase curves (thick) and pure-component curves (thin)
    \begin{scope}[line width=1.1pt]
        \draw (Q) .. controls (1.76,3.6) and (1.84,4.4) .. (1.85,6.6);   % alpha beta gamma
        \draw (0,1.42) .. controls (0.6,1.80) and (1.2,2.30) .. (Q);       % G alpha beta
        \draw (Q) .. controls (2.3,2.95) and (2.8,3.15) .. (A1);           % G alpha gamma
        \draw (Q) .. controls (2.6,2.90) and (4.3,2.90) .. (B1);           % G beta gamma
        \draw (A2) .. controls (6.0,3.30) and (6.4,2.80) .. (B2);          % G L gamma
    \end{scope}
    \draw (0,0.97) .. controls (1.2,1.80) and (2.5,2.75) .. (A1);          % G alpha_A
    \draw (A1) .. controls (3.36,4.4) and (3.39,5.5) .. (3.40,6.6);        % alpha gamma_A
    \draw (A1) .. controls (4.1,3.40) and (4.9,3.70) .. (A2);              % G gamma_A
    \draw (A2) .. controls (5.60,4.9) and (5.63,5.8) .. (5.64,6.6);        % L gamma_A
    \draw (A2) .. controls (6.8,4.25) and (7.9,4.60) .. (CA);              % G L_A
    \draw (0,0.30) .. controls (1.8,0.55) and (3.5,1.30) .. (B1);          % G beta_B
    \draw (B1) .. controls (4.98,4.2) and (5.03,5.5) .. (5.05,6.6);        % beta gamma_B
    \draw (B1) .. controls (5.6,2.05) and (6.3,2.15) .. (B2);              % G gamma_B
    \draw (B2) .. controls (6.93,4.0) and (6.99,5.5) .. (7.01,6.6);        % L gamma_B
    \draw (B2) .. controls (7.9,2.45) and (8.9,2.65) .. (CB);              % G L_B
    \draw (CA) .. controls (9.3,4.30) and (9.6,3.60) .. (CB);              % critical locus
    \fill (Q) circle (1.8pt) node[below left=-1pt] {$Q$};
    % isobar p_0 and isotherm T_0
    \draw[dashed, line width=0.6pt] (-0.15,2.93) node[left] {$p_0$} -- (10.0,2.93);
    \draw[dashed, line width=0.6pt] (2.73,-0.1) node[below] {$T_0$} -- (2.73,6.8);
    % curve labels
    \begin{scope}[font=\footnotesize]
        \node[above] at (1.85,6.6) {$\alpha\beta\gamma$};
        \node[above] at (3.40,6.6) {$\alpha\gamma_A$};
        \node[above] at (5.05,6.6) {$\beta\gamma_B$};
        \node[above, yshift=9pt] at (5.64,6.6) {$L\gamma_A$};
        \node[above] at (7.01,6.6) {$L\gamma_B$};
        \node[rotate=33] at (0.60,1.98) {$G\alpha\beta$};
        \node[rotate=35] at (1.45,1.40) {$G\alpha_A$};
        \node[rotate=17] at (2.55,0.80) {$G\beta_B$};
        \node[rotate=22] at (2.25,3.38) {$G\alpha\gamma$};
        \node at (3.40,2.62) {$G\beta\gamma$};
        \node[rotate=17] at (4.35,3.76) {$G\gamma_A$};
        \node[rotate=8] at (5.85,1.84) {$G\gamma_B$};
        \node[rotate=-50] at (6.62,3.40) {$GL\gamma$};
        \node[rotate=16] at (7.45,4.62) {$GL_A$};
        \node[rotate=12] at (8.35,2.40) {$GL_B$};
    \end{scope}
\end{tikzpicture}"""

# ------------------------------------------------------------ Problem 4: Ag-Pr
figs["quiz1_agpr"] = r"""\begin{tikzpicture}[font=\small, >=Latex, line width=0.8pt]
\begin{scope}[x=9cm, y=0.0054545cm, shift={(0,-300)}]
    % frame and ticks
    \draw (0,300) rectangle (1,1400);
    \foreach \T in {300,400,...,1400}
        \draw[line width=0.5pt] (0,\T) -- (-0.012,\T) node[left, font=\footnotesize] {\T};
    \foreach \x/\l in {0/0,0.1/0.1,0.2/0.2,0.3/0.3,0.4/0.4,0.5/0.5,0.6/0.6,0.7/0.7,0.8/0.8,0.9/0.9,1/1}
        \draw[line width=0.5pt] (\x,300) -- (\x,285) node[below, font=\footnotesize] {\l};
    % liquidus
    \draw plot[smooth] coordinates {(0,1235) (0.04,1165) (0.077,1072)};
    \draw (0.077,1072) -- (0.095,1102);
    \draw plot[smooth] coordinates {(0.095,1102) (0.15,1235) (0.2154,1298)};
    \draw plot[smooth] coordinates {(0.2154,1298) (0.29,1245) (0.358,1107)};
    \draw (0.358,1107) -- (0.385,1091);
    \draw plot[smooth] coordinates {(0.385,1091) (0.44,1172) (0.5,1204)};
    \draw plot[smooth] coordinates {(0.5,1204) (0.62,1090) (0.770,848)};
    \draw (0.770,848) -- (0.787,890);
    \draw plot[smooth] coordinates {(0.787,890) (0.88,1060) (1.0,1204)};
    % Bcc solidus and Bcc/DHCP boundary
    \draw plot[smooth] coordinates {(1.0,1204) (0.962,1020) (0.942,890)};
    \draw (0.942,890) -- (1.0,1068);
    % three-phase isotherms
    \draw (0,1072) -- (0.1667,1072);
    \draw (0.095,1102) -- (0.2154,1102);
    \draw (0.2154,1107) -- (0.358,1107);
    \draw (0.3333,1091) -- (0.5,1091);
    \draw (0.5,848) -- (1.0,848);
    \draw (0.787,890) -- (1.0,890);
    % stoichiometric compounds
    \draw (0.1667,300) -- (0.1667,1102);
    \draw (0.2154,300) -- (0.2154,1298);
    \draw (0.3333,300) -- (0.3333,1107);
    \draw (0.5,300) -- (0.5,1204);
    % phase labels
    \node at (0.62,1330) {Liquid};
    \draw[line width=0.4pt] (0.985,1110) -- (1.05,1180) node[right, font=\footnotesize] {Bcc};
    \begin{scope}[font=\footnotesize]
        \node[rotate=90] at (0.035,650) {Fcc};
        \node[rotate=90] at (0.145,650) {Ag$_5$Pr};
        \node[rotate=90] at (0.240,650) {Ag$_{51}$Pr$_{14}$};
        \node[rotate=90] at (0.310,650) {Ag$_2$Pr};
        \node[rotate=90] at (0.475,650) {AgPr};
        \node[rotate=90] at (0.965,650) {DHCP};
    \end{scope}
    % axis labels
    \node[below=16pt] at (0.5,300) {$x$(Pr)};
    \node[below=4pt] at (0,280) {Ag};
    \node[below=4pt] at (1,280) {Pr};
    \node[rotate=90] at (-0.10,850) {$T$ (K)};
\end{scope}
\end{tikzpicture}"""

# ------------------------------------------------------------ ternary base
TERN_BASE = r"""    % corners and frame
    \coordinate (Ab) at (0,0);
    \coordinate (An) at (8,0);
    \coordinate (Di) at (4,6.928);
    \draw (Ab) -- (An) -- (Di) -- cycle;
    \node[below left] at (Ab) {Albite};
    \node[below right] at (An) {Anorthite};
    \node[above] at (Di) {Diopside};
    \foreach \p in {20,40,60,80}
        \draw[line width=0.5pt] (0.08*\p,0) -- (0.08*\p,-0.1) node[below, font=\footnotesize] {\p};
    % cotectic (boundary between the diopside and plagioclase fields)
    \draw[line width=1.4pt] plot[smooth] coordinates {@cot@};
"""

FAN = "\n".join(
    f"    \\draw[dashed, line width=0.5pt] (Di) -- {f['l']} -- {f['proj']};\n"
    f"    \\draw[dashed, line width=0.5pt] {f['l']} -- {f['pl']};\n"
    f"    \\node[above, font=\\scriptsize] at {f['proj']} {{{f['an']}}};"
    for f in d["fan"])

figs["quiz1_ternary"] = (r"""\begin{tikzpicture}[font=\small, >=Latex, line width=0.8pt]
""" + TERN_BASE + r"""    % diopside-liquid lines (from Di) and liquid-plagioclase tie lines;
    % numbers: An content of the plagioclase in equilibrium with each liquid
@FAN@
    % crystallization of composition A
    \draw[dotted, line width=1pt] @l2@ -- @s2@;
    \draw plot[smooth] coordinates {@A@ @l1@ @l2@};
    \foreach \P/\n/\pos in {@A@/A/above right, @l1@/l_1/left, @s3@/s_3/right}
        { \fill \P circle (1.8pt); \node[\pos] at \P {$\n$}; }
    \node[above left] at @l2@ {$l_2$};
    \node[above left] at @l3@ {$l_3$};
    \node[above left] at @l4@ {$l_4$};
    \node[below=9pt] at @s2@ {$s_2$};
\end{tikzpicture}""")

# ------------------------------------------------------------ Solution 1
figs["quiz1_sol_compound"] = r"""\begin{tikzpicture}[font=\small, >=Latex, line width=0.8pt]
    % frame: A (X=0), compound A_xB_y (gamma, at x=2.4), B (X=1); width 6 cm
    \draw (0,5.5) -- (0,0) -- (6,0) -- (6,5.5);
    % liquidus: A -> E (eutectic) -> congruent point (horizontal tangent) -> P -> B
    \draw plot[smooth] coordinates {(0,3.0) (0.6,2.6) (1.2,2.0)};
    \draw (1.2,2.0) .. controls (1.7,2.9) and (2.0,3.4) .. (2.4,3.4)
                    .. controls (2.8,3.4) and (3.0,3.6) .. (3.3,3.9);
    \draw plot[smooth] coordinates {(3.3,3.9) (4.6,4.5) (6,5.0)};
    % alpha: solidus and solvus
    \draw (0,3.0) -- (0.15,2.0);
    \draw (0.15,2.0) -- (0.10,0);
    % gamma: vertical boundary at the stoichiometric composition, solidus, solvus
    \draw (2.4,0) -- (2.4,3.4);
    \draw (2.4,3.4) .. controls (2.9,3.4) and (3.3,3.6) .. (3.7,3.9);
    \draw (3.7,3.9) .. controls (3.55,2.5) and (3.4,1.2) .. (3.3,0);
    % beta: solidus and solvus
    \draw (5.4,3.9) -- (6,5.0);
    \draw (5.4,3.9) .. controls (5.5,2.5) and (5.6,1.2) .. (5.65,0);
    % three-phase isotherms
    \draw (0.15,2.0) -- (2.4,2.0);
    \draw (3.3,3.9) -- (5.4,3.9);
    \fill (1.2,2.0) circle (1.6pt) node[below] {$E$};
    \fill (3.3,3.9) circle (1.6pt) node[below right=-1pt] {$P$};
    \fill (2.4,3.4) circle (1.6pt);
    % temperature marks
    \begin{scope}[font=\footnotesize]
        \draw[dashed, line width=0.4pt] (-0.1,2.0) node[left] {$T_E$} -- (0.15,2.0);
        \draw[dashed, line width=0.4pt] (-0.1,3.4) node[left] {$T_\gamma$} -- (2.4,3.4);
        \draw[dashed, line width=0.4pt] (-0.1,3.9) node[left] {$T_P$} -- (3.3,3.9);
    \end{scope}
    % region labels
    \node at (1.5,4.6) {$L$};
    \node[font=\footnotesize] at (0.42,2.55) {$L\!+\!\alpha$};
    \node[font=\footnotesize] at (1.85,2.35) {$L\!+\!\gamma$};
    \node[font=\footnotesize] at (4.6,4.15) {$L\!+\!\beta$};
    \node at (1.25,1.0) {$\alpha\!+\!\gamma$};
    \node at (2.85,1.4) {$\gamma$};
    \node at (4.5,1.6) {$\gamma\!+\!\beta$};
    \node at (5.85,1.6) {$\beta$};
    \node[font=\footnotesize, right=-2pt] at (0.05,1.0) {$\alpha$};
    \draw[line width=0.4pt] (3.05,3.62) -- (2.75,4.35) node[above, font=\footnotesize] {$L\!+\!\gamma$};
    % axes
    \node[below] at (0,-0.05) {$A$};
    \node[below] at (2.4,-0.05) {$A_xB_y$};
    \node[below] at (6,-0.05) {$B$};
    \node[below=14pt] at (3,0) {composition $X$};
    \node[rotate=90] at (-0.9,2.7) {temperature};
\end{tikzpicture}"""

# ------------------------------------------------------------ Solution 2
figs["quiz1_sol_profile"] = r"""\begin{tikzpicture}[font=\small, >=Latex, line width=0.8pt]
    % axes: position along the couple, composition X
    \draw[->] (0,0) -- (7.2,0) node[right] {position};
    \draw[->] (0,0) -- (0,4.4) node[above] {$X$};
    \draw[line width=0.5pt] (0,4) -- (-0.1,4) node[left] {$1$};
    \node[left] at (0,0) {$0$};
    % compositions of the tie line at T_2
    \draw[dashed, line width=0.5pt] (0,1.2) node[left] {$y$} -- (7,1.2);
    \draw[dashed, line width=0.5pt] (0,2.04) node[left] {$z$} -- (7,2.04);
    % profile: alpha layer (0 -> y), jump at the interface, liquid (z -> 1)
    \draw[line width=1.2pt] plot[smooth] coordinates {(0.2,0.02) (1.6,0.25) (2.6,0.7) (3.2,1.2)};
    \draw[line width=1.2pt] (3.2,1.2) -- (3.2,2.04);
    \draw[line width=1.2pt] plot[smooth] coordinates {(3.2,2.04) (3.9,2.9) (5.0,3.6) (6.8,3.98)};
    \draw[dashed, line width=0.5pt] (3.2,0) node[below] {interface} -- (3.2,4.2);
    \node at (1.6,3.0) {solid $\alpha$};
    \node[above] at (5.3,1.2) {liquid $L$};
    \node[below, font=\footnotesize] at (0.2,-0.35) {$A$ end};
    \node[below, font=\footnotesize] at (6.8,-0.35) {$B$ end};
\end{tikzpicture}"""

# ------------------------------------------------------------ Solution 3
figs["quiz1_sol_tx"] = r"""\begin{tikzpicture}[font=\small, >=Latex, line width=0.8pt]
    % frame; T_1 ... T_7 are the crossings of the isobar p_0 in the P-T projection
    \draw (0,5.6) -- (0,0) -- (6,0) -- (6,5.6);
    \foreach \y/\n in {1.0/T_1, 1.6/T_2, 2.1/T_3, 2.8/T_4, 3.5/T_5, 4.0/T_6, 4.8/T_7}
        \draw[dashed, line width=0.3pt] (-0.1,\y) node[left, font=\footnotesize] {$\n$} -- (0,\y);
    % alpha and beta solvus below the eutectoid
    \draw (0.30,1.0) -- (0.20,0);
    \draw (5.70,1.0) -- (5.80,0);
    % three-phase isotherms
    \draw (0.30,1.0) -- (5.70,1.0);      % alpha + gamma + beta (eutectoid)
    \draw (0.20,1.6) -- (2.40,1.6);      % alpha + G + gamma
    \draw (2.80,3.5) -- (5.40,3.5);      % G + L + gamma
    % alpha + gamma region
    \draw (0.30,1.0) -- (0.20,1.6);
    \draw plot[smooth] coordinates {(3.0,1.0) (2.65,1.3) (2.40,1.6)};
    % gamma + beta region, closing at pure B (T_4)
    \draw plot[smooth] coordinates {(3.0,1.0) (4.4,1.75) (6,2.8)};
    \draw plot[smooth] coordinates {(5.70,1.0) (5.88,1.9) (6,2.8)};
    % alpha + G region, closing at pure A (T_3)
    \draw plot[smooth] coordinates {(0.20,1.6) (0.08,1.85) (0,2.1)};
    \draw plot[smooth] coordinates {(1.30,1.6) (0.55,1.85) (0,2.1)};
    % G + gamma region
    \draw plot[smooth] coordinates {(1.30,1.6) (2.0,2.5) (2.80,3.5)};
    \draw plot[smooth] coordinates {(2.40,1.6) (4.0,2.5) (5.40,3.5)};
    % G + L region, closing at pure B (T_7)
    \draw plot[smooth] coordinates {(2.80,3.5) (4.3,4.3) (6,4.8)};
    \draw plot[smooth] coordinates {(4.20,3.5) (5.2,4.15) (6,4.8)};
    % L + gamma region, closing at pure B (T_6)
    \draw plot[smooth] coordinates {(4.20,3.5) (5.1,3.8) (6,4.0)};
    \draw plot[smooth] coordinates {(5.40,3.5) (5.75,3.75) (6,4.0)};
    % region labels
    \begin{scope}[font=\footnotesize]
        \node at (3.0,0.5) {$\alpha+\beta$};
        \node at (1.3,1.3) {$\alpha+\gamma$};
        \node at (4.9,1.35) {$\gamma+\beta$};
        \node at (3.55,1.65) {$\gamma$};
        \draw[line width=0.3pt] (0.32,1.78) -- (0.95,2.45) node[above] {$\alpha+G$};
        \node at (2.85,2.55) {$G+\gamma$};
        \node at (1.3,3.6) {$G$};
        \node at (4.7,4.15) {$G\!+\!L$};
        \draw[line width=0.3pt] (5.3,3.62) -- (6.5,3.3) node[right] {$L+\gamma$};
        \node at (5.55,4.25) {$L$};
        \node at (0.12,0.55) {$\alpha$};
        \node at (5.9,0.55) {$\beta$};
    \end{scope}
    \node[below] at (0,-0.05) {$A$};
    \node[below] at (6,-0.05) {$B$};
    \node[below=14pt] at (3,0) {composition $X$};
    \node[rotate=90] at (-1.0,2.8) {temperature};
\end{tikzpicture}"""

# ------------------------------------------------------------ Solution 5
figs["quiz1_sol_ternary"] = (r"""\begin{tikzpicture}[font=\small, >=Latex, line width=0.8pt]
""" + TERN_BASE + r"""    % three-phase tie triangle Di - l4 - plagioclase An55 (L + Di + Pl)
    \fill[gray!25] (Di) -- @l4@ -- @pl55@ -- cycle;
    \draw[line width=0.5pt] (Di) -- @l4@ -- @pl55@ -- cycle;
    \draw[line width=1.4pt] plot[smooth] coordinates {@cot@};
    % temperature falls along the cotectic from E1 to E2
    \draw[-{Latex[length=2.6mm]}, line width=1.2pt] (5.314,3.515) -- (4.903,3.162);
    \draw[-{Latex[length=2.6mm]}, line width=1.2pt] (4.135,2.684) -- (3.571,2.420);
    \draw[-{Latex[length=2.6mm]}, line width=1.2pt] (1.614,1.412) -- (1.171,1.149);
    \fill @E1@ circle (2pt) node[right] {$E_1$};
    \fill @E2@ circle (2pt) node[above left=-1pt] {$E_2$};
    % isotherm through l4: diopside-field branch and plagioclase-field branch
    \draw[line width=0.9pt, densely dashed] plot[smooth] coordinates {@iso_DiAb@ @iso_mid1@ @l4@};
    \draw[line width=0.9pt, densely dashed] plot[smooth] coordinates {@l4@ @iso_mid2@ @iso_AbAn@};
    % path of the liquid: A -> l1 -> l2 (plagioclase only), then l2 -> l4 on the cotectic
    \draw[line width=1.2pt, -{Latex[length=2.4mm]}] plot[smooth] coordinates {@A@ @l1@ @l2@};
    \draw[dotted, line width=1pt] @l2@ -- @s2@;
    \foreach \P/\n/\pos in {@A@/A/right, @l1@/l_1/left, @l2@/l_2/above, @l3@/l_3/above left, @l4@/l_4/above left}
        { \fill \P circle (1.8pt); \node[\pos] at \P {$\n$}; }
    \node[below=9pt] at @s2@ {$s_2$};
    \node[below=9pt] at @pl55@ {An$_{55}$};
    % field labels
    \begin{scope}[font=\footnotesize]
        \node at (3.55,3.2) {$L$+Di+Pl};
        \node at (2.25,3.25) {Di$\,+\,L$};
        \node at (2.55,0.45) {Pl$\,+\,L$};
        \node at (5.75,1.55) {Di$\,+\,$Pl};
        \node at (0.98,1.45) {$L$};
    \end{scope}
\end{tikzpicture}""")

for name, body in figs.items():
    with open(f"{OUT}/{name}.tex", "w") as fh:
        fh.write(fill(HDR, {"NAME": name}) + fill(body, {"FAN": fill(FAN)}) + END)
print(" ".join(figs))
