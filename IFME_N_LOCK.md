# From Triple-Lock to *n*-Lock in Capability Cartography Layer 2 IFME

## Purpose

Capability Cartography Layer 2 IFME already exports most of the empirical observables needed for an IFME reinterpretation:

- a measured local predictive law
- structured task-family variation
- explicit failure-atlas outputs
- onset thresholds and sweep summaries
- compressibility-related constructs
- intervention profiles
- linked substrate notebook execution reports

The IFME move is to reinterpret this capability landscape as a latent interaction field whose stable and unstable regions are governed by a small number of coupled constraints, or locks.

The key upgrade is:

- do **not** assume triple-lock in advance
- infer the lock count from the measured field

That means moving from:

- `triple-lock`

to:

- `n-lock`, where `n` is chosen by retention, stability, and behavioral sufficiency tests

## IFME State Construction

The ideal IFME state vector for a record includes:

- `capability_score`
- `generalization_gap`
- `retrieval_dependence`
- `task_family_code`
- `scale`
- `data_tokens`
- compressibility variables
- context-geometry variables
- intervention indicators

The current Layer 2 code now implements a local IFME field matrix from the measured records table plus derived interaction terms such as:

- `log_scale`
- `log_data_tokens`
- `scale_x_retrieval`
- `gap_x_retrieval`
- `capability_x_gap`

This is not yet the full ideal state vector, because the measured records table does not flatten every descriptor and compressibility field at the same richness described in the broader design documents. But it is enough to run a principled first-pass local lock selection.

## What Counts as a Lock

A lock is treated as a latent stabilizing mode that satisfies three conditions:

1. statistical retention
2. behavioral necessity
3. interpretive coherence

In practice, a retained component becomes a lock only if:

- it survives factor/component retention logic
- it contributes to preserving useful behavioral structure
- it corresponds to a meaningful capability constraint rather than numerical residue

## Data-Driven Lock Selection Rule

Layer 2 now includes a local IFME analyzer in [`capability_cartography/ifme.py`](./capability_cartography/ifme.py).

The implemented retention-and-selection logic combines:

- PCA eigenvalue structure
- Horn-style parallel analysis
- Velicer-style MAP preference
- bootstrap stability of retained counts
- behavioral sufficiency across candidate `k`

The practical selection rule is:

> choose the smallest `n` that is compatible with parallel retention, not strongly contradicted by MAP preference, reasonably stable under bootstrap resampling, and behaviorally sufficient in the current measured regime

Behavioral sufficiency is evaluated through reduced-space performance proxies, including:

- failure-label discrimination
- capability reconstruction quality
- onset-threshold consistency

This keeps lock count selection empirical rather than aesthetic.

## Current Layer 2 IFME Pipeline

The current end-to-end IFME application inside Layer 2 is:

1. Assemble the measured field matrix from `measured_records.csv`
2. Standardize the matrix
3. Residualize trivial scale/data trends
4. Run PCA on the residualized field
5. Apply parallel-analysis retention
6. Apply a Velicer-style MAP diagnostic
7. Estimate bootstrap retained-count stability
8. Evaluate candidate `k` for behavioral sufficiency
9. Select the smallest sufficient local `n`
10. Export named lock candidates with top loadings

The outputs are written to:

- [`artifacts/layer2/ifme/ifme_summary.json`](./artifacts/layer2/ifme/ifme_summary.json)
- [`artifacts/layer2/ifme/ifme_components.csv`](./artifacts/layer2/ifme/ifme_components.csv)

## Plausible Lock Families in the Current Local Regime

Given the current Layer 2 measured regime, the most plausible local lock families are:

- scale-capacity lock
- retrieval/context-integration lock
- task-family / cognitive-form lock
- generalization-gap / structural-burden lock

These should be read as candidates inferred from current loadings and measured behavior, not as final metaphysical categories.

## What This Does and Does Not Establish

What it establishes:

- Layer 2 is structurally compatible with an IFME treatment now
- the repository already has the right artifact style for local lock inference
- the lock count can be selected from measured structure rather than assumed in advance

What it does not yet establish:

- a final universal lock count
- a frontier-model theory of capability structure
- a complete compressibility-aware state vector
- a definitive proof that the local count transfers beyond the current small measured regime

So the correct conclusion is:

> Capability Cartography Layer 2 IFME can already support a principled IFME `n`-lock analysis, but the selected lock count must be treated as local and data-driven rather than assumed or universalized.

## Interpretation

The right upgrade from triple-lock is therefore not:

- default to `4`
- default to `5`

The right upgrade is:

- infer `n` from retention, bootstrap stability, behavioral sufficiency, and interpretive coherence

That is the main value of applying IFME on top of Layer 2: the empirical measurement layer is already here, and IFME adds latent interaction geometry, basin logic, and lock-count selection on top of it.
