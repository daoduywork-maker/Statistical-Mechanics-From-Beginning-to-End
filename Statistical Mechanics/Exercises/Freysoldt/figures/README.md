# Figures

Every figure of `freysoldt.tex` is pre-built as a PDF in this folder and loaded with
`\includegraphics{figures/<name>}`. Each `<name>.tex` is the standalone source of `<name>.pdf`.

    ./build.sh            # all figures
    ./build.sh <name>     # one figure

`transition-levels.pdf` (Section 2) shows the formation energy against the Fermi level for three
model defects, with the lower envelope in red.

    python3 make_transition_levels.py > transition-levels.tex
    ./build.sh transition-levels

## Figures of `Freysoldt's Review.tex`

- `defect-model.pdf` (Section 2): the lattice model with the heat bath and the reservoirs. Drawn by hand in `defect-model.tex`.
- `defect-basins.pdf` (Section 4): microstates grouped into defect configurations, with the vibrational levels of each.
- `defect-concentration.pdf` (Sections 5 and 7): constrained grand potential against the concentration, and the concentration against the formation energy.

    python3 make_defect_basins.py > defect-basins.tex
    python3 make_defect_concentration.py > defect-concentration.tex
    ./build.sh defect-model defect-basins defect-concentration
