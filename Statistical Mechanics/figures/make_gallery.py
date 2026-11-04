"""Generate the gallery of model binary T-X diagrams as TikZ code.

Each diagram follows from the lower convex hull of the Gibbs free energy
curves g(X) of the phases at fixed (T, P): a hull edge that spans a
composition gap is a two-phase tie line, and a single-phase stretch of
the hull marks the stable phase.  Region boundaries are contours of the
resulting region map.

Run:  python3 make_gallery.py  >  binary_gallery.tex
"""
import sys
import numpy as np
from scipy import ndimage
import contourpy
from hull_pd import XG, NX, solution, compound, segments

SF = 1.2                                   # entropy of fusion / k_B


def d(Ti, sf=SF):
    return lambda T: sf * (Ti - T)         # mu_l - mu_s of pure component


zero = lambda T: 0.0


def case(T1, T2, ws, wl=0.0, extra=None, sf=SF):
    """Solid (one structure, regular, w_s) and liquid (regular, w_l)."""
    ph = [solution(zero, zero, ws), solution(d(T1, sf), d(T2, sf), wl)]
    return ph + (extra or [])


def two_solids(T1, T2, aB, aA, w, extra=None, sf=SF):
    """alpha (structure of A) and beta (structure of B) as separate solutions.

    Pure B in the alpha structure costs aB, pure A in the beta structure
    costs aA; both solids are regular solutions with parameter w.
    Phase order: alpha, liquid, beta (, extra).
    """
    alpha = solution(zero, lambda T: aB, w)
    beta = solution(lambda T: aA, zero, w)
    liq = solution(d(T1, sf), d(T2, sf), 0.0)
    return [alpha, liq, beta] + (extra or [])


# name, title, phases, T range, phase names {(phase, side): label}
CASES = [
    ("iso", "isomorphous", case(1.0, 1.5, 0.0, sf=1.0), (0.85, 1.6)),
    ("max", "congruent maximum", case(1.0, 1.15, -1.0), (0.8, 1.4)),
    ("min", "minimum with gap", case(1.0, 1.15, 1.1), (0.3, 1.2)),
    ("eut", "eutectic", case(1.0, 1.15, 2.2), (0.3, 1.2)),
    ("per", "peritectic", two_solids(1.0, 2.0, 0.2, 1.2, 1.2), (0.6, 2.05)),
    ("mono", "monotectic", case(0.6, 1.4, 3.0, 3.0), (0.3, 1.7)),
    ("cong", "congruent compound",
     two_solids(1.0, 1.15, 1.0, 1.0, 1.5, extra=[compound(0.5, -0.9, 0.0)]), (0.5, 1.4)),
    ("incong", "incongruent compound",
     two_solids(1.0, 2.0, 1.0, 1.0, 1.5, extra=[compound(0.5, -0.45, 0.0)]), (0.5, 2.05)),
]

NT = 241
W, H = 3.3, 2.6                            # panel size in cm


def region_map(phases, Ts):
    """Integer code per (T, X): 0..9 single phase, 10+ two-phase pair."""
    pairs = {}
    code = np.zeros((len(Ts), NX), dtype=int)
    for j, T in enumerate(Ts):
        G = np.array([g(XG, T) for g in phases])
        code[j] = np.argmin(G, axis=0)
        segs, _, _ = segments(phases, T)
        for (xa, xb, pa, pb) in segs:
            key = (pa, pb)
            if key not in pairs:
                pairs[key] = 10 + len(pairs)
            m = (XG > xa) & (XG < xb)
            code[j, m] = pairs[key]
    return code, pairs


def simplify(pts, tol):
    """Douglas-Peucker polyline simplification."""
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    ab = b - a
    n = np.hypot(*ab)
    if n == 0:
        dist = np.hypot(*(pts - a).T)
    else:
        dist = np.abs(ab[0] * (pts[:, 1] - a[1]) - ab[1] * (pts[:, 0] - a[0])) / n
    k = int(np.argmax(dist))
    if dist[k] > tol:
        left = simplify(pts[: k + 1], tol)
        return np.vstack([left[:-1], simplify(pts[k:], tol)])
    return np.array([a, b])


def boundaries(code, Ts):
    """Contour lines between regions, in panel coordinates (cm)."""
    xs = XG * W
    ys = (Ts - Ts[0]) / (Ts[-1] - Ts[0]) * H
    lines = []
    for c in np.unique(code):
        ind = (code == c).astype(float)
        gen = contourpy.contour_generator(xs, ys, ind)
        for ln in gen.lines(0.5):
            if len(ln) > 3:
                lines.append(simplify(np.asarray(ln), 0.012))
    return lines


def dedupe(lines):
    """Drop segments drawn twice (each boundary borders two regions)."""
    seen, out = set(), []
    for ln in lines:
        segs = []
        for p, q in zip(ln[:-1], ln[1:]):
            k = tuple(sorted([(round(p[0], 2), round(p[1], 2)),
                              (round(q[0], 2), round(q[1], 2))]))
            if k in seen:
                if segs:
                    out.append(np.array(segs))
                segs = []
                continue
            seen.add(k)
            segs = segs + [p, q] if not segs else segs + [q]
        if segs:
            out.append(np.array(segs))
    return out


def labels(code, pairs, Ts, names):
    """Label positions at the centroid of each sizeable region."""
    inv = {v: k for k, v in pairs.items()}
    out = []
    for c in np.unique(code):
        lab, n = ndimage.label(code == c)
        for r in range(1, n + 1):
            m = lab == r
            if m.sum() < 0.012 * code.size:
                continue
            jj, ii = np.nonzero(m)
            xc = XG[int(np.median(ii))]
            xl, xr = XG[ii.min()], XG[ii.max()]
            wide = xl < 0.3 and xr > 0.7
            if c < 10:
                text = names(c, None if wide else xc)
            else:
                pa, pb = inv[c]
                if pa == pb:
                    text = names(pa, 0.0, 1) + "+" + names(pb, 1.0, 2)
                else:
                    na, nb = names(pa, xl), names(pb, xr)
                    if pb == 1:
                        na, nb = nb, na
                    text = na + "+" + nb
            # pick the interior point closest to the centroid
            cj, ci = jj.mean(), ii.mean()
            k = int(np.argmin((jj - cj) ** 2 + ((ii - ci) * NT / NX) ** 2))
            out.append((XG[ii[k]] * W, (Ts[jj[k]] - Ts[0]) / (Ts[-1] - Ts[0]) * H,
                        text, m.sum()))
    return out


def namer(key):
    if key in ("per", "cong", "incong"):
        fixed = [r"\alpha", "L", r"\beta", r"\gamma"]
        return lambda p, x, k=0: fixed[p]

    def names(p, x, k=0):
        if p == 0:
            if key in ("iso", "max"):
                return r"\alpha"
            if key == "min":
                return r"\alpha" if k == 0 else rf"\alpha_{k}"
            if x is None:
                return r"\alpha"
            return r"\alpha" if x < 0.5 else r"\beta"
        if p == 1:
            if key == "mono" and x is not None:
                if k:
                    return f"L_{k}"
                return "L_1" if x < 0.5 else "L_2"
            return "L"
        return r"\gamma"
    return names


def main():
    out = sys.stdout
    out.write("% Generated by make_gallery.py -- do not edit by hand.\n")
    for idx, (key, title, ph, (t0, t1)) in enumerate(CASES):
        Ts = np.linspace(t0, t1, NT)
        code, pairs = region_map(ph, Ts)
        lines = dedupe(boundaries(code, Ts))
        from classify import classify
        for r in classify(ph, np.linspace(t0, t1, 121)):
            sys.stderr.write(f"{key}: T3={r[0]} X=[{r[1]},{r[2]}] {r[3]}\n")
        col, row = idx % 4, idx // 4
        ox, oy = col * (W + 0.9), -row * (H + 1.3)
        out.write(f"% ({chr(97 + idx)}) {title}\n")
        out.write(f"\\begin{{scope}}[shift={{({ox:.2f},{oy:.2f})}}]\n")
        out.write(f"  \\draw[line width=0.5pt] (0,0) rectangle ({W},{H});\n")
        for ln in lines:
            pts = " -- ".join(f"({p[0]:.3f},{p[1]:.3f})" for p in ln)
            out.write(f"  \\draw {pts};\n")
        for (x, y, text, size) in labels(code, pairs, Ts, namer(key)):
            out.write(f"  \\node[font=\\tiny, fill=white, inner sep=0.5pt] "
                      f"at ({x:.2f},{y:.2f}) {{${text}$}};\n")
        out.write(f"  \\node[font=\\scriptsize, below] at ({W/2},-0.05) "
                  f"{{({chr(97 + idx)}) {title}}};\n")
        out.write("\\end{scope}\n")


if __name__ == "__main__":
    main()
