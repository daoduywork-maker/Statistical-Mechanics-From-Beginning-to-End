# Computed binary phase diagrams

The figures `binary_gallery.tex` and `binary_pressure.tex` are generated, not drawn by hand.
Each diagram is the lower convex hull of the Gibbs free energy curves g(X) of all phases at
fixed (T, P), which is the common-tangent condition of the binary-system chapter.

- `hull_pd.py` — convex hull, two-phase segments, three-phase lines
- `make_gallery.py` — eight isobaric T–X diagrams (lens, congruent maximum/minimum, eutectic, peritectic, monotectic, congruent and incongruent compounds)
- `make_pressure.py` — P–T projection and T–X sections at three pressures with a gas phase
- `classify.py` — reports whether each three-phase line is of eutectic or peritectic type

Regenerate (needs numpy, scipy, contourpy):

    python3 make_gallery.py  > binary_gallery.tex
    python3 make_pressure.py > binary_pressure.tex
