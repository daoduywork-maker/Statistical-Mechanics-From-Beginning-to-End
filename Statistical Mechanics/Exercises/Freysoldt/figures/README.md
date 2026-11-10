# Figures

Every figure of `freysoldt.tex` is pre-built as a PDF in this folder and loaded with
`\includegraphics{figures/<name>}`, so compiling the document does not redraw TikZ.
Each `<name>.tex` is the standalone source of `<name>.pdf` (11pt, same fonts as the notes).

Rebuild after editing a source:

    ./build.sh            # all figures
    ./build.sh <name>     # one figure

## Arrhenius figure

`arrhenius.pdf` (Exercise 4) shows the Gibbs energy of vacancy formation
in Al and the Arrhenius plot from a model that reproduces the GGA values of Table I of
Freysoldt et al. (2014).

    python3 make_arrhenius.py > arrhenius.tex   # needs numpy, scipy
    ./build.sh arrhenius
