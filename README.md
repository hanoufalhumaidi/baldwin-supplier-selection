# Baldwin Rotational Fuzzy Supplier Selection

Open implementation of the Multi-Attribute Decision Making (MADM) supplier
selection method on Baldwin rotational fuzzy sets (Al-Humaidi), developed to
accompany the companion papers on the theoretical framework and the ETFE dome
facade case study. Provided for the ASCE Data Availability Statement.

## Contents

- `index.html` - self-contained web application (no build step, no server, no
  external dependencies). Open it in any browser, or host with GitHub Pages.
- `validate_engine.py` - Python reproduction of the published case-study
  tables (requires `numpy`): reproduces the supplier-rating membership
  function F-mu to four decimals, the published centroid x = 0.713, and the
  published distance ranking (Fairly Positive closest).

## Model summary

- Rating terms: Very Positive (y = x^2), Positive (y = x), Fairly Positive
  (y = sqrt(x)), Undecided (y = 0.5), Fairly Negative (y = sqrt(1-x)),
  Negative (y = 1-x), Very Negative (y = (1-x)^2).
- Weight terms: Very Important = x^2, Important = x, Fairly Important =
  sqrt(x), Not Important = 0 (excluded from the weighted average).
- Aggregation: fuzzy weighted average, pointwise on the grid x = 0, 0.1, ..., 1,
  applied bottom-up (sub-sub factors -> sub-factors -> factors -> F-mu).
- Rating: Euclidean distance from the centroid of F-mu to the analytic area
  centroids of the six Baldwin membership functions; the closest function is
  the supplier rating.
- Centroid, exactly as the original Visual Basic program (Form17):
  centroid_x = sum(x*y)/sum(y), centroid_y = sum(x*y)/sum(x).
- Distance conventions (selectable in the interface):
  - "Original program": d = (dx)^2 + |dy|. This is what the VB source line
    `d = ((cx-X)^2) + ((cy-Y)^2)^0.5` computes under Visual Basic operator
    precedence, and it reproduces every published case-study distance
    exactly (0.197, 0.228, 0.260, 0.282, 0.370, 0.474).
  - "Corrected Euclidean": d = sqrt(dx^2 + dy^2), i.e. Eq. 12 as written in
    the paper; recommended for the revised manuscript. The supplier ranking
    is identical under both conventions.

## Provenance notes for the revised manuscripts

- The published centroid "(0.713, 0.599)" contains a transcription typo:
  the program computes (0.713, 0.559).
- The published distance table was produced by the original-program
  convention above; regenerating it with the corrected Euclidean Eq. 12
  gives 0.216, 0.230, 0.261, 0.363, 0.442, 0.531 with the same verdict
  (Fairly Positive).
- Zero total weight ("Not Important" everywhere) yields a zero rating here;
  the VB source divided by 1e-18 in that case, which was a guard artifact.

## Features

- Fixed three-level supplier-selection hierarchy exactly as in the original
  program and the case-study paper: Performance, Cost, Assurance of Supply,
  Technical Capability, and Quality, with their preset sub-factors and
  sub-sub factors. The structure is not editable; end users set only the
  linguistic rating and importance weight dropdowns. A branch weighted
  "Not Important" is excluded from the aggregation and greyed out, matching
  the original program's cascading enable/disable behavior.
- Rotational-model chart with the six Baldwin curves, the computed F-mu, the
  centroid, and the Baldwin centroids.
- One-click validation view against the published case-study tables.
- One-term sensitivity analysis: every leaf rating is perturbed one linguistic
  step up and down and verdict changes are reported.

## Hosting on GitHub Pages

1. Create a public repository (e.g. `baldwin-supplier-selection`).
2. Upload `index.html`, `validate_engine.py`, `README.md`, `LICENSE`.
3. Settings -> Pages -> deploy from branch `main`, root folder.
4. The app will be served at `https://<username>.github.io/baldwin-supplier-selection/`.

## License

MIT (see `LICENSE`).
