# Figures

Every figure of the notes is pre-built as a PDF in this folder and loaded with
`\includegraphics{figures/<name>}`, so compiling `main.tex` does not redraw TikZ.
Each `<name>.tex` is the standalone source of `<name>.pdf` (11pt, same fonts as the notes).

Rebuild after editing a source:

    ./build.sh            # all figures
    ./build.sh gallery    # one figure

## Computed binary phase diagrams

`gallery.pdf` and `pressure.pdf` are computed, not drawn by hand. Each diagram is the lower
convex hull of the Gibbs free energy curves g(X) of all phases at fixed (T, P), which is the
common-tangent condition of the binary-system chapter.

- `hull_pd.py` — convex hull, two-phase segments, three-phase lines
- `make_gallery.py` — eight isobaric T–X diagrams (writes `binary_gallery.tex`)
- `make_pressure.py` — P–T projection and T–X sections at three pressures (writes `binary_pressure.tex`)
- `classify.py` — reports whether each three-phase line is of eutectic or peritectic type

Regenerate the data (needs numpy, scipy, contourpy), then rebuild the PDFs:

    python3 make_gallery.py  > binary_gallery.tex
    python3 make_pressure.py > binary_pressure.tex
    ./build.sh gallery pressure

## Computed unary figures

`unary-Pv.pdf` shows van der Waals isotherms in reduced units, with the coexisting volumes
from the equal-area rule (the common tangent of f(v)).

    python3 make_unary_Pv.py > unary-Pv.tex   # needs numpy, scipy
    ./build.sh unary-Pv

`unary-fv-triple.pdf` shows model free energy curves of a solid, a liquid and a vapor at the
triple point and below the triple point, with the common tangents computed numerically.

    python3 make_unary_fv_triple.py > unary-fv-triple.tex
    ./build.sh unary-fv-triple

`binary-three-phase.pdf` shows a eutectic from regular-solution free energies: g(X) with the
convex hull above, at and below T_e, and the T-X diagram computed from the same hull.

    python3 make_binary_three_phase.py > binary-three-phase.tex
    ./build.sh binary-three-phase
