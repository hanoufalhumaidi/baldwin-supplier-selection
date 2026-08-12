"""Validation of the Baldwin rotational fuzzy engine against the published
ETFE dome facade case study (Al-Humaidi, Tables 6 and 7 of the applied paper).

Reproduces:
  - The supplier-rating membership function Fmu (published Table 6 column)
  - Centroid C (program convention: discrete centroid) = (0.713, 0.599*)
  - Distance ranking (Fairly Positive closest), published Table 7

The centroid follows the original Visual Basic program (Form17):
  centroid_x = sum(x*y)/sum(y),  centroid_y = sum(x*y)/sum(x).
The published centroid "(0.713, 0.599)" contains a transcription typo:
the program computes (0.713, 0.559).

Two distance conventions are provided:
  original : d = (dx)**2 + abs(dy)  -- what the VB line
             d = ((cx-X)^2) + ((cy-Y)^2)^0.5
             actually computes under VB operator precedence; reproduces
             every published distance exactly.
  euclid   : d = sqrt(dx**2 + dy**2) -- Eq. 12 as written in the paper;
             recommended for the revised manuscript (same ranking).
"""
import numpy as np

X = np.round(np.arange(0, 1.01, 0.1), 2)

RATING_TERMS = {
    "Very Positive":   X**2,
    "Positive":        X.copy(),
    "Fairly Positive": np.sqrt(X),
    "Undecided":       np.full_like(X, 0.5),
    "Fairly Negative": np.sqrt(1 - X),
    "Negative":        1 - X,
    "Very Negative":   (1 - X)**2,
}
WEIGHT_TERMS = {
    "Very Important":   X**2,
    "Important":        X.copy(),
    "Fairly Important": np.sqrt(X),
    "Not Important":    np.zeros_like(X),
}
# Analytic area centroids of the Baldwin membership functions (Appendix 1)
BALDWIN_CENTROIDS = {
    "Very Positive":   (3/4, 3/10),
    "Positive":        (2/3, 1/3),
    "Fairly Positive": (6/10, 3/8),
    "Fairly Negative": (2/5, 3/8),
    "Negative":        (1/3, 1/3),
    "Very Negative":   (1/4, 3/10),
}

def weighted_average(pairs):
    """pairs: list of (weight_vector, rating_vector); pointwise on the x grid."""
    num = sum(w * r for w, r in pairs)
    den = sum(w for w, _ in pairs)
    out = np.zeros_like(X)
    nz = den > 0
    out[nz] = num[nz] / den[nz]
    return out

def centroid_program(y):
    sxy = (X * y).sum()
    return (sxy / y.sum(), sxy / X.sum())

def rank(y, convention="original"):
    c = centroid_program(y)
    if convention == "original":
        d = {t: float((c[0]-r[0])**2 + abs(c[1]-r[1]))
             for t, r in BALDWIN_CENTROIDS.items()}
    else:
        d = {t: float(np.hypot(c[0]-r[0], c[1]-r[1]))
             for t, r in BALDWIN_CENTROIDS.items()}
    verdict = min(d, key=d.get)
    return c, d, verdict

# ---- Published factor-rating vectors rc_1..rc_5 (paper Table 6 inputs) ----
rc = {
 1: [0,.1094,.2175,.3192,.4134,.5,.5792,.6516,.7178,.7781,.8333],
 2: [0,.255,.27,.295,.33,.375,.43,.495,.57,.655,.75],
 3: [0,.0822,.1468,.2079,.2717,.3414,.4184,.5030,.5946,.6899,.75],
 4: [0,.01,.04,.09,.16,.25,.36,.49,.64,.81,1],
 5: [0,.0404,.0834,.1372,.2055,.2904,.3935,.5155,.6570,.8185,1],
}
FMU_PUBLISHED = [0,.0994,.1515,.2099,.2761,.3514,.4362,.5310,.6359,.7503,.8667]

if __name__ == "__main__":
    vi = WEIGHT_TERMS["Very Important"]
    fmu = weighted_average([(vi, np.array(v)) for v in rc.values()])
    print("x      Fmu(computed)  Fmu(published)")
    ok = True
    for i, x in enumerate(X):
        match = abs(fmu[i] - FMU_PUBLISHED[i]) < 5e-4
        ok &= match
        print(f"{x:.1f}    {fmu[i]:.4f}         {FMU_PUBLISHED[i]:.4f}   {'OK' if match else 'MISMATCH'}")
    print("\nTable 6 Fmu column reproduced:", ok)
    D_PUB = {"Fairly Positive": .197, "Positive": .228, "Very Positive": .260,
             "Fairly Negative": .282, "Negative": .370, "Very Negative": .474}
    c, d, verdict = rank(fmu, "original")
    print(f"\nCentroid (program convention): ({c[0]:.3f}, {c[1]:.3f})")
    print("  published (0.713, 0.599): x matches; published y is a typo for %.3f" % c[1])
    print("\nOriginal-program distances vs published Table 7:")
    all_ok = True
    for t in sorted(d, key=d.get):
        ok = abs(d[t] - D_PUB[t]) < 5e-4
        all_ok &= ok
        print(f"  {t:16s} {d[t]:.3f}   published {D_PUB[t]:.3f}   {'OK' if ok else 'MISMATCH'}")
    print("All published distances reproduced exactly:", all_ok)
    print("Verdict:", verdict, " [published: Fairly Positive]")
    c2, d2, v2 = rank(fmu, "euclid")
    print("\nCorrected Euclidean (Eq. 12) distances for the revised paper:")
    for t in sorted(d2, key=d2.get):
        print(f"  {t:16s} {d2[t]:.3f}")
    print("Verdict (corrected):", v2)
