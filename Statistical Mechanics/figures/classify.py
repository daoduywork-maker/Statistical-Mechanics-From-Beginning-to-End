import sys, numpy as np
from hull_pd import diagram, _segs, _changed
def classify(ph, Ts):
    _, three = diagram(ph, Ts)
    out = []
    for (T, xl, xr) in three:
        up = [s for s in _segs(ph, T + 2e-4) if s[1] > xl - 0.01 and s[0] < xr + 0.01]
        dn = [s for s in _segs(ph, T - 2e-4) if s[1] > xl - 0.01 and s[0] < xr + 0.01]
        typ = {(2, 1): "eutectic-type", (1, 2): "peritectic-type"}.get((len(up), len(dn)), f"?{len(up)},{len(dn)}")
        out.append((round(T, 3), round(xl, 2), round(xr, 2), typ,
                    [(round(a, 2), round(b, 2), pa, pb) for a, b, pa, pb in up],
                    [(round(a, 2), round(b, 2), pa, pb) for a, b, pa, pb in dn]))
    return out
if __name__ == "__main__":
    from make_gallery import case, compound
    trials = {
      "per A": (case(0.6, 1.6, 2.6, sf=1.0), np.linspace(0.3, 1.7, 141)),
      "per B": (case(0.5, 1.6, 3.0, sf=0.8), np.linspace(0.3, 1.7, 141)),
      "per C": (case(0.4, 1.6, 2.8, sf=1.0), np.linspace(0.3, 1.7, 141)),
      "incong A": (case(1.0, 1.6, 3.0, extra=[compound(0.5, -0.7, 0.0)]), np.linspace(0.3, 1.7, 141)),
      "incong B": (case(0.8, 1.8, 3.0, extra=[compound(0.5, -0.8, 0.0)]), np.linspace(0.3, 1.9, 161)),
    }
    for k, (ph, Ts) in trials.items():
        print(k)
        for r in classify(ph, Ts):
            print("   ", r[:4], "\n      up", r[4], "\n      dn", r[5])
