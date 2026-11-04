"""Binary T-X phase diagrams from the lower convex hull of g-curves.

Units: k_B = 1. Each phase is a function g(X, T) per particle.
Liquid and solid solutions use the regular-solution form; a compound
is a narrow parabola.  The diagram is the set of two-phase tie lines
(hull edges spanning a composition gap) and three-phase lines.
"""
import numpy as np

NX = 801
XG = np.linspace(1e-4, 1 - 1e-4, NX)
DX = XG[1] - XG[0]


def mix(X, T):
    return T * (X * np.log(X) + (1 - X) * np.log(1 - X))


def solution(d1, d2, w):
    """g = (1-X) d1(T) + X d2(T) + T mix + w X(1-X); d_i are callables."""
    return lambda X, T: (1 - X) * d1(T) + X * d2(T) + mix(X, T) + w * X * (1 - X)


def compound(X0, e0, s0, K=60.0):
    """Line compound near X0: g = e0 - T s0 + K (X - X0)^2."""
    return lambda X, T: e0 - T * s0 + K * (X - X0) ** 2


def lower_hull(x, y):
    idx = np.argsort(x, kind="mergesort")
    hull = []
    for i in idx:
        while len(hull) >= 2:
            a, b = hull[-2], hull[-1]
            cross = (x[b] - x[a]) * (y[i] - y[a]) - (y[b] - y[a]) * (x[i] - x[a])
            if cross <= 0:
                hull.pop()
            else:
                break
        hull.append(i)
    return hull


def segments(phases, T):
    """Two-phase segments (Xa, Xb, pa, pb) of the hull at temperature T."""
    xs, ys, lab = [], [], []
    for k, g in enumerate(phases):
        xs.append(XG)
        ys.append(g(XG, T))
        lab.append(np.full(NX, k))
    x = np.concatenate(xs); y = np.concatenate(ys); lab = np.concatenate(lab)
    h = lower_hull(x, y)
    segs = []
    for a, b in zip(h[:-1], h[1:]):
        if x[b] - x[a] > 2.5 * DX or lab[a] != lab[b]:
            segs.append((x[a], x[b], int(lab[a]), int(lab[b])))
    # also report which phase is stable at each single-phase stretch
    return segs, x[h], lab[h]


def _segs(phases, T):
    segs, _, _ = segments(phases, T)
    return [sg for sg in segs if sg[1] - sg[0] > 3 * DX]


def _changed(A, B, tol=0.03):
    """Segments of A with no counterpart (same phases, close ends) in B."""
    out = []
    for a in A:
        if not any(a[2] == b[2] and a[3] == b[3] and abs(a[0] - b[0]) < tol
                   and abs(a[1] - b[1]) < tol for b in B):
            out.append(a)
    return out


def diagram(phases, Ts):
    """Boundary polylines and three-phase lines (T, X_left, X_right)."""
    tracks = {}
    dT = Ts[1] - Ts[0]
    allsegs = []
    for T in Ts:
        segs = _segs(phases, T)
        allsegs.append(segs)
        for (xa, xb, pa, pb) in segs:
            for side, xv in (("L", xa), ("R", xb)):
                lines = tracks.setdefault((pa, pb, side), [])
                best = None
                for ln in lines:
                    tl, xl = ln[-1]
                    if abs(xl - xv) < 0.05 and abs(tl - T) < 3.5 * dT:
                        best = ln
                if best is None:
                    lines.append([(T, xv)])
                else:
                    best.append((T, xv))
    sig = lambda S: tuple(sorted((g[2], g[3]) for g in S))
    three = []
    for k in range(len(Ts) - 1):
        A, B = allsegs[k], allsegs[k + 1]
        if sig(A) == sig(B):
            continue
        lo, hi, sa, sb = Ts[k], Ts[k + 1], A, B
        for _ in range(30):
            mid = 0.5 * (lo + hi)
            sm = _segs(phases, mid)
            if sig(sm) == sig(sa):
                lo, sa = mid, sm
            else:
                hi, sb = mid, sm
        ca, cb = _changed(sa, sb, 0.03), _changed(sb, sa, 0.03)
        if not ca or not cb:
            continue
        xl = min(min(c[0] for c in ca), min(c[0] for c in cb))
        xr = max(max(c[1] for c in ca), max(c[1] for c in cb))
        if xr - xl > 0.03:
            three.append((0.5 * (lo + hi), xl, xr))
    polys = [ln for lines in tracks.values() for ln in lines if len(ln) > 2]
    return polys, three


def stable_phase(phases, X, T):
    vals = [g(np.array([X]), T)[0] for g in phases]
    return int(np.argmin(vals))
