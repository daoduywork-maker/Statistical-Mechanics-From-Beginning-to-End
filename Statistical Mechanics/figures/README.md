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
