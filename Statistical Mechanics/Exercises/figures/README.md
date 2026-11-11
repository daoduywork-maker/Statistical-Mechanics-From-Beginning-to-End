# Figures

Every figure of `exercise.tex` and `quiz1.tex` is pre-built as a PDF in this folder and loaded with
`\includegraphics{figures/<name>}`, so compiling the document does not redraw TikZ.
Each `<name>.tex` is the standalone source of `<name>.pdf` (11pt, same fonts as the notes).

Rebuild after editing a source:

    ./build.sh            # all figures
    ./build.sh <name>     # one figure

## Quiz 1 figures

The `quiz1_*` figures belong to `quiz1.tex` and Section 8 of `exercise.tex`. They redraw the
diagrams of Quiz 1 of the phase-diagram course in TikZ.

- `quiz1_lens`, `quiz1_pt`, `quiz1_agpr`, `quiz1_ternary` — the four problem diagrams
- `quiz1_sol_compound`, `quiz1_sol_profile`, `quiz1_sol_tx`, `quiz1_sol_ternary` — solution figures
- `quiz1_coords.py` — computes the lens curves and converts the ternary points to triangle
  coordinates (writes `quiz1_coords.json`)
- `make_quiz1_figs.py` — fills the coordinates into the TikZ templates

Regenerate after changing a coordinate:

    python3 quiz1_coords.py
    python3 make_quiz1_figs.py quiz1_coords.json .
    ./build.sh quiz1_lens quiz1_pt quiz1_agpr quiz1_ternary quiz1_sol_compound quiz1_sol_profile quiz1_sol_tx quiz1_sol_ternary
