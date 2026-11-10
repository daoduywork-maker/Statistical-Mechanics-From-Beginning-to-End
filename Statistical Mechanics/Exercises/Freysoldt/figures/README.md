# Figures

Every figure of `freysoldt.tex` is pre-built as a PDF in this folder and loaded with
`\includegraphics{figures/<name>}`. Each `<name>.tex` is the standalone source of `<name>.pdf`.

    ./build.sh            # all figures
    ./build.sh <name>     # one figure

`transition-levels.pdf` (Section 2) shows the formation energy against the Fermi level for three
model defects, with the lower envelope in red.

    python3 make_transition_levels.py > transition-levels.tex
    ./build.sh transition-levels
