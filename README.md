# Capability Cartography Layer 2 IFME

**Capability Cartography Layer 2 IFME** is the IFME-focused successor to `Capability-Cartography-Layer-2`. It keeps the Layer 2 cartography spine, but centers the repository around data-driven `n`-lock analysis on top of measured laws, failure atlases, sweep artifacts, notebook-backed substrate execution, and agent-linked exports.

This repository is designed to sit on top of three companion resources:

- `pageman/sutskever-30-implementations` as the experimental substrate
- `pageman/Sutskever-Agent` as the orchestration and explanatory layer
- `pageman/gpt1-from-sutskever30` as the first controlled transformer wind tunnel

These links are preserved explicitly in code and artifacts. The adapter layer records canonical repository URLs and configured local roots so every cartography export can retain its provenance back to those three repos rather than treating them as anonymous backends.

The central claim of this project is simple: benchmark folklore is not enough. If a model is “surprisingly strong,” “brittle,” “emergent,” or “lost in the middle,” those labels should resolve into measurable regions, descriptor profiles, compressibility signatures, and threshold estimates. This successor repo exists to push that program further than the first repository did.

## Reader Guide

If you want the shortest reader-friendly interpretation of what the current results do and do not establish, start with [`TAO_ASSESSMENT.md`](./TAO_ASSESSMENT.md). It evaluates the repository against Terence Tao’s framing of the central modern AI puzzle: we understand the machinery much better than we understand the behavior.

If you want the current IFME reinterpretation of Layer 2 as a data-driven `n`-lock system rather than a fixed triple-lock story, read [`IFME_N_LOCK.md`](./IFME_N_LOCK.md). That document is the main conceptual center of this repo.

If you want the main second-generation additions, focus on these modules:

- `capability_cartography/orchestration.py`
- `capability_cartography/failure_atlas.py`
- `capability_cartography/ifme.py`
- `capability_cartography/visualization.py`
- `capability_cartography/notebook_runner.py`
- `capability_cartography/agent_integration.py`
- `capability_cartography/compressibility.py` for live-weight estimators

## Tao and Keating Concerns

The main philosophical pressure on this repo comes from a concern articulated sharply by Terence Tao and echoed in a broader way by Prof. Brian Keating:

- the mathematics of model construction is comparatively straightforward
- the mystery is behavioral, not mechanical
- the unresolved question is why competence appears here, fails there, and remains hard to predict in advance

This IFME repo is an attempt to answer that concern in a stricter way than a normal benchmark repo.

If you want the full run-specific interpretation, read [`TAO_ASSESSMENT.md`](./TAO_ASSESSMENT.md). That file is the main reader-facing answer to the question:

- after the latest rerun, how much does this repository really explain about the gap between understandable machinery and hard-to-predict behavior?

The short version from the current run is:

- the repo now exports a real local predictive law
- it exports explicit failure categories
- it executes a linked substrate notebook successfully
- and, crucially, it adds a data-driven local IFME lock-selection result

The latest rerun currently supports:

- `11/11` tests passing
- successful demo execution
- a local law with holdout `R^2 ≈ 0.9416`
- explicit failure-atlas counts of `collapse = 8`, `generalization_risk = 1`, `stable_reasoning = 23`
- a stable linked substrate notebook run with `5` generated figures
- a local IFME result selecting a `2-lock` regime with:
  - `retrieval_context_integration_lock`
  - `generalization_gap_lock`

This does **not** mean the repo has solved the general puzzle of language-model behavior.

It **does** mean the repo now offers a more structured answer than:

- “models are weird”
- “emergence happened”
- “retrieval is brittle”

Instead, the repo is now saying:

- here is the local predictive law
- here is the local failure map
- here is the local latent lock structure
- here are the conditions under which those claims should still count as supported

That is the central reason [`TAO_ASSESSMENT.md`](./TAO_ASSESSMENT.md) matters in this repository.

## Current Results and Tao Assessment

If you want the full, run-specific interpretation of the latest IFME repo outputs, read [`TAO_ASSESSMENT.md`](./TAO_ASSESSMENT.md). That file is the best reader-oriented answer to the question:

- after the latest rerun, how much does this repository actually explain about the gap between simple model mechanics and hard-to-predict model behavior?

The short version is that the IFME repo now answers that question better than the earlier repositories, but still only within a narrow measured regime.

### What was just re-run

The current assessment is based on a fresh rerun of:

- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 -m capability_cartography.demo`

Current rerun status:

- tests: `11/11` passing
- demo: completed successfully

### Which artifacts matter most

If you only inspect a handful of outputs, inspect these:

- [`artifacts/ifme/measured/measured_summary.json`](./artifacts/ifme/measured/measured_summary.json)
- [`artifacts/ifme/measured/measured_records.csv`](./artifacts/ifme/measured/measured_records.csv)
- [`artifacts/ifme/failure_atlas/failure_atlas.json`](./artifacts/ifme/failure_atlas/failure_atlas.json)
- [`artifacts/ifme/notebooks/22_scaling_laws.execution.json`](./artifacts/ifme/notebooks/22_scaling_laws.execution.json)
- [`artifacts/ifme/ifme/ifme_summary.json`](./artifacts/ifme/ifme/ifme_summary.json)
- [`artifacts/ifme/sweeps/sweep_summary.json`](./artifacts/ifme/sweeps/sweep_summary.json)

These are the files that support the core claim that the repository is doing more than generating nice plots or abstract architecture diagrams.

### What the latest measured-law results say

The current measured-law run reports:

- `record_count = 32`
- `train_count = 16`
- `holdout_count = 16`
- model fit `R^2 ≈ 0.9919`
- holdout `MAE ≈ 0.0022`
- holdout `R^2 ≈ 0.9416`

The current local fitted law is:

`capability_score = 0.225454 - 0.000040*scale + 0.000000*data_tokens + 0.003211*task_family_code - 0.030676*retrieval_dependence`

That law is intentionally exported in falsifiable form. The artifact does not merely present coefficients. It also states the conditions under which the law should still be considered supported:

- holdout `MAE` should remain at or below roughly `0.0022`
- holdout `R^2` should remain at or above roughly `0.9416`
- the claim applies only inside the measured regime represented by the run

That is important. It means the repo is trying to behave more like an empirical instrument than a storytelling device.

### What the latest task-family split says

The current task-family means are:

- `retrieval_qa ≈ 0.2025`
- `object_tracking ≈ 0.2244`
- `pair_matching ≈ 0.2288`
- `babi_simple ≈ 0.2289`

This matters because it gives a concrete, current-run answer to one of the central concerns in Tao’s framing:

- models are not just “weirdly uneven” in the abstract
- they are measurably uneven across task families
- in this regime, retrieval-heavy work is the weakest family

That does not solve the general puzzle, but it does replace hand-waving with a measured pattern.

### What the latest failure-atlas result says

The failure-atlas artifact is now populated and explicit. The latest run reports:

- `record_count = 32`
- `collapse = 8`
- `generalization_risk = 1`
- `stable_reasoning = 23`

It also stores per-record:

- actual label
- predicted label
- centroid-distance diagnostics

This is a meaningful improvement over the weaker earlier state where failure-atlas support existed mostly as code scaffolding. The current repository now exports an inspectable failure artifact rather than only promising one.

### What the substrate notebook execution result says

The latest direct execution wrapper result for the linked scaling-laws notebook reports:

- `returncode = 0`
- empty `stderr`
- `5` generated figures

### What the IFME result adds

The IFME-specific artifact adds a new layer beyond the plain measured-law and failure-atlas exports.

The latest run reports:

- selected lock count: `2`
- selected regime: `2-lock`
- parallel retained count: `2`
- MAP preferred count: `1`
- bootstrap modal count: `2`

The current selected candidate lock families are:

- `retrieval_context_integration_lock`
- `generalization_gap_lock`

This is the core IFME-specific answer to Tao’s concern. Instead of assuming a fixed triple-lock story, the repo now infers a local latent lock structure from the measured field itself.

That matters because one of the previous weak points of Layer 2 was that richer notebook wrapping existed in concept but not as a stable execution path. The current run is better: the notebook wrapper now produces an actual execution report and saved figures rather than failing during headless execution.

### What this does and does not establish

What it does establish:

- the repo can now produce a real local predictive law
- the repo can validate that law on holdout data
- the repo can export explicit failure structure
- the repo can connect that interpretation back to a real linked substrate notebook
- the repo can infer a local data-driven lock structure rather than fixing the number of locks in advance

What it does not establish:

- a general theory of frontier LLM behavior
- a deep theory of the language “middle regime”
- globally transferable scaling laws across model families and data regimes
- a universal lock count for capability structure

So the right claim is not:

- this repository solves the mystery of language-model behavior

The right claim is:

- this repository now turns part of that mystery into a measurable, falsifiable, inspectable empirical program

That distinction is the entire point of [`TAO_ASSESSMENT.md`](./TAO_ASSESSMENT.md). Read that file if you want the full interpretation in plain language rather than only the raw JSON outputs.

## Why This Repository Exists

Most open educational model repositories are optimized for understanding how a model is built. That is useful, but incomplete. The deeper scientific question is not merely how a mechanism is implemented, but under what conditions a capability appears, stabilizes, degrades, or collapses.

That question becomes especially important when dealing with:

- retrieval-augmented models that succeed only under favorable context geometry
- reasoning benchmarks that conflate memorization with abstraction
- compact demo models whose transparency makes them ideal for causal intervention
- claims of “emergence” that are really unmeasured threshold behavior
- claims of “brittleness” that are really undocumented interactions between task structure, distractors, and objective choice

The Capability Cartography Layer reframes those issues as a mapping problem. Instead of relying on single scalar benchmark scores, it creates structured artifacts that describe:

- what kind of task the model was given
- what the intervention profile was
- how compressible the task and model behavior looked
- where capability seemed to turn on or turn off
- whether failure was gradual, abrupt, or masked by misleadingly favorable conditions

## Conceptual Model

The repository is organized around five tightly linked subsystems.

### 1. Standardized Experiment System

The system treats each experiment as a capability probe rather than a one-off training script. An experiment has:

- a substrate
- a task
- a benchmark label
- a realism level
- an intervention profile
- one or more measured trajectories

This creates a common contract across:

- educational notebook assets
- compact hand-built transformer code
- agent-generated narratives

The goal is to allow cumulative measurement rather than isolated demos.

### 2. Task Descriptor System

Every task or evaluation instance is described in structured form rather than by benchmark name alone. The descriptor system captures several families of signal:

- surface statistics
- latent structure proxies
- retrieval geometry
- perturbation profile
- cognitive-operation hints
- structural complexity proxies

That matters because a benchmark label such as “QA,” “math,” or “reasoning” is too coarse to predict success or failure. Two tasks can share a label while differing sharply in distractor density, relational depth, temporal complexity, or answer position bias.

### 3. Compressibility Stack

The compressibility layer estimates three different kinds of compression:

- surface compression using standard codecs
- predictive compression using loss-style proxies
- structural compression using description-length-like approximations

The objective is not to claim perfect MDL or Kolmogorov measurements. It is to provide practical, comparable proxies that reveal mismatch. If a task looks statistically easy at the surface level but still demands a structurally costly representation, that gap is informative. If predictive loss is low but structural compression remains poor, that is also informative.

### 4. Intervention System

Capabilities should not be described only after they appear. They should be stress-tested and moved. The intervention system therefore exposes knobs over:

- architecture
- objective
- data regime
- retrieval
- context geometry
- interpretability-related settings

This is where the GPT-1 companion project becomes especially useful. A compact, inspectable transformer is the right place to run one-factor-at-a-time sweeps before moving to larger or less transparent systems.

### 5. Boundary Analysis System

The end product of the framework is not just a log file. It is a map. The boundary layer looks for:

- changepoints
- threshold estimates
- competence regimes
- phase-like transitions

This makes it possible to say more than “the model got better.” Instead, one can say:

- capability score crossed from collapse into partial competence at a particular step
- the median threshold for a sweep sits at a specific value
- retrieval dependence remains high even after apparent capability gains
- a success region is narrow and bordered by rapid collapse under perturbation

## What Is In This Repository

### `capability_cartography/`

The main Python package.

- [`capability_cartography/schemas.py`](./capability_cartography/schemas.py)
  Defines the shared dataclasses for descriptors, trajectories, interventions, artifacts, and boundary summaries.

- [`capability_cartography/descriptors.py`](./capability_cartography/descriptors.py)
  Extracts task descriptors from text or arrays.

- [`capability_cartography/compressibility.py`](./capability_cartography/compressibility.py)
  Computes surface, predictive, and structural compression proxies plus gap measures.

- [`capability_cartography/boundary.py`](./capability_cartography/boundary.py)
  Detects abrupt regime shifts and fits lightweight threshold summaries.

- [`capability_cartography/adapters.py`](./capability_cartography/adapters.py)
  Integrates with external repos through configurable roots rather than hardcoded local assumptions.

- [`capability_cartography/runner.py`](./capability_cartography/runner.py)
  Provides the shared runner that ties descriptors, compressibility, interventions, wind-tunnel probing, and export together.

- [`capability_cartography/demo.py`](./capability_cartography/demo.py)
  Demonstrates the full pipeline and writes JSON artifacts to `./artifacts/`.

- [`capability_cartography/sweeps.py`](./capability_cartography/sweeps.py)
  Runs scale/data/task-family grids and builds a sweep registry suitable for onset-surface analysis.

- [`capability_cartography/surfaces.py`](./capability_cartography/surfaces.py)
  Fits lightweight predictive surfaces and onset thresholds across sweep records.

- [`capability_cartography/storage.py`](./capability_cartography/storage.py)
  Persists per-run artifacts and tabular sweep summaries.

- [`capability_cartography/metrics.py`](./capability_cartography/metrics.py)
  Computes aggregate metrics, calibration-style error, and capability proxies for measured synthetic trajectories.

- [`capability_cartography/execution.py`](./capability_cartography/execution.py)
  Runs measured tiny-model experiments against the linked GPT-1 wind tunnel and exports live-run signals including weight-oriented compressibility summaries.

- [`capability_cartography/datasets.py`](./capability_cartography/datasets.py)
  Defines the small measured task families used for local predictive-law studies and task-family differentiation.

- [`capability_cartography/validation.py`](./capability_cartography/validation.py)
  Fits local predictive laws, performs holdout validation, and computes bootstrap coefficient intervals.

- [`capability_cartography/provenance.py`](./capability_cartography/provenance.py)
  Captures repository commit, branch, dirty-state, and local-root provenance for linked companion repositories.

- [`capability_cartography/orchestration.py`](./capability_cartography/orchestration.py)
  Coordinates the Layer 2 study stack across measured runs, sweep exports, failure-atlas generation, notebook execution, plotting, and agent-bundle export.

- [`capability_cartography/failure_atlas.py`](./capability_cartography/failure_atlas.py)
  Trains and exports the current explicit failure-atlas artifact, including label counts and per-record predictions.

- [`capability_cartography/visualization.py`](./capability_cartography/visualization.py)
  Generates static onset-surface and phase-region plots from exported records.

- [`capability_cartography/notebook_runner.py`](./capability_cartography/notebook_runner.py)
  Wraps linked substrate notebooks into executable Python scripts, runs them in headless mode, and captures reports plus generated figures.

- [`capability_cartography/agent_integration.py`](./capability_cartography/agent_integration.py)
  Produces Sutskever-Agent-oriented briefs and workflow bundles from the exported Layer 2 study outputs.

- [`capability_cartography/ifme.py`](./capability_cartography/ifme.py)
  Builds a local IFME field matrix from measured IFME-repo records and selects a data-driven local `n`-lock solution using retention, bootstrap, and sufficiency criteria.

### `tests/`

Basic unit tests using the Python standard library’s `unittest` module.

## Repository Positioning Relative to the Companion Repos

This repository is intentionally separate from the educational substrate. That separation is deliberate for several reasons:

- the measurement layer evolves on different timescales than the underlying notebooks
- the cartography layer should be reusable across multiple substrates, not only one
- it should be publishable and versioned independently
- it should be able to depend on external local paths or clones without requiring those repos to absorb measurement-specific logic

In practical terms:

- `sutskever-30-implementations` remains the transparent experimental substrate
- `gpt1-from-sutskever30` remains the compact wind tunnel
- `Sutskever-Agent` remains the orchestration and explanatory layer
- this repository becomes the measurement spine that links them

## Installation

### Minimal installation

```bash
git clone https://github.com/pageman/Capability-Cartography-Layer-2-IFME
cd Capability-Cartography-Layer-2-IFME
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

This installs the package itself with its currently declared dependencies:

- `matplotlib`
- `numpy`
- `PyYAML`

If you want to execute linked substrate notebooks directly, you may also need notebook-specific scientific Python dependencies used by those notebooks. For the currently exercised `22_scaling_laws` path, that includes `scipy`.

### Optional companion repositories

If you want live integration with the three companion repos rather than fallback behavior, clone them somewhere on disk and then point this repository at them via environment variables:

```bash
export SUTSKEVER30_ROOT=/path/to/sutskever-30-implementations
export GPT1_WIND_TUNNEL_ROOT=/path/to/gpt1-from-sutskever30
export SUTSKEVER_AGENT_ROOT=/path/to/Sutskever-Agent/sutskever-agent
```

The adapters are designed so that:

- if the substrate repo is configured, notebook metadata can be discovered directly
- if the GPT-1 repo is configured, the runner can import and probe the actual GPT-1 implementation
- if the agent repo is configured, skill metadata can be read from the agent manifest
- if some repos are missing, the framework still works in reduced mode

They also try a small set of likely local clone locations automatically. On a machine with the repos cloned in common places under `~` or `~/Downloads`, linked mode can work without exporting any environment variables.

Every exported artifact now includes `linked_repositories` metadata referencing:

- `https://github.com/pageman/Sutskever-30-implementations`
- `https://github.com/pageman/Sutskever-Agent`
- `https://github.com/pageman/gpt1-from-Sutskever30`

## Quick Start

Run the demo:

```bash
python3 -m capability_cartography.demo
```

This will:

1. define a small intervention profile
2. construct a descriptor-bearing text experiment
3. compute compressibility proxies
4. detect boundary events
5. generate a narrative summary
6. export artifacts to `./artifacts/`
7. run a GPT-1 wind tunnel profile using the configured adapter or a fallback dry-run approximation
8. run a multi-axis sweep over scale, data volume, and task family
9. export sweep records and surface summaries to `./artifacts/sweeps/`
10. run a measured study using actual tiny GPT-1 training loops on task families derived from the linked substrate
11. export held-out validation, bootstrap intervals, and falsifiable law statements to `./artifacts/measured/`
12. run the IFME orchestration stack and export failure-atlas, plot, notebook, IFME, and agent-workflow outputs to `./artifacts/ifme/`

## Linked Mode

If the companion repositories already exist in standard local locations, this is enough:

```bash
cd Capability-Cartography-Layer-2-IFME
python3 -m capability_cartography.demo
```

If you want to force specific linked roots, use:

```bash
SUTSKEVER30_ROOT=/path/to/sutskever-30-implementations \
SUTSKEVER_AGENT_ROOT=/path/to/Sutskever-Agent/sutskever-agent \
GPT1_WIND_TUNNEL_ROOT=/path/to/gpt1-from-Sutskever30 \
python3 -m capability_cartography.demo
```

When linked mode is active, the exported artifacts will show `available: true` in `linked_repositories` and will record the configured local roots for:

- `pageman/Sutskever-30-implementations`
- `pageman/Sutskever-Agent`
- `pageman/gpt1-from-Sutskever30`

## Example Output Artifacts

The exported JSON artifacts are designed to be:

- machine-readable
- easy to diff
- easy for agents to narrate
- stable enough to serve as research audit trail records

An artifact contains:

- the experiment spec
- the full capability trajectory
- descriptor payloads
- compressibility summaries
- boundary events
- fitted boundary statistics
- aggregate series metrics
- linked companion-repository metadata
- an optional narrative layer

The measured study outputs also contain:

- repeated-seed records
- holdout validation metrics
- bootstrap coefficient intervals
- provenance with linked repository commits
- falsifiable law statements with explicit validation error

## IFME Artifact Tree

The current IFME orchestration exports a second-generation artifact bundle under [`artifacts/ifme/`](./artifacts/ifme/). At the time of writing, the exact current tree includes:

```text
artifacts/ifme/
├── agent/
│   ├── agent_brief.json
│   └── agent_workflow.yaml
├── failure_atlas/
│   └── failure_atlas.json
├── ifme/
│   ├── ifme_components.csv
│   └── ifme_summary.json
├── measured/
│   ├── measured_laws.json
│   ├── measured_records.csv
│   └── measured_summary.json
├── notebooks/
│   ├── 22_scaling_laws.execution.json
│   ├── 22_scaling_laws.py
│   └── 22_scaling_laws_figures/
│       ├── figure_01.png
│       ├── figure_02.png
│       ├── figure_03.png
│       ├── figure_04.png
│       └── figure_05.png
├── plots/
│   ├── onset_surface.png
│   └── phase_regions.png
└── sweeps/
    ├── sweep_records.csv
    ├── sweep_records.jsonl
    └── sweep_summary.json
```

The most important IFME repo outputs are:

- [`artifacts/ifme/measured/measured_summary.json`](./artifacts/ifme/measured/measured_summary.json)
  The current local predictive-law summary with train/holdout split metrics and bootstrap intervals.
- [`artifacts/ifme/measured/measured_records.csv`](./artifacts/ifme/measured/measured_records.csv)
  The measured run table used for current local-law fitting and task-family analysis.
- [`artifacts/ifme/failure_atlas/failure_atlas.json`](./artifacts/ifme/failure_atlas/failure_atlas.json)
  The exported failure-atlas artifact with label counts, centroids, and per-record predictions.
- [`artifacts/ifme/ifme/ifme_summary.json`](./artifacts/ifme/ifme/ifme_summary.json)
  The current local IFME `n`-lock selection summary with retention tests, bootstrap stability, sufficiency metrics, and selected lock count.
- [`artifacts/ifme/ifme/ifme_components.csv`](./artifacts/ifme/ifme/ifme_components.csv)
  The named candidate lock rows and top-loading features for the current selected local lock regime.
- [`artifacts/ifme/notebooks/22_scaling_laws.execution.json`](./artifacts/ifme/notebooks/22_scaling_laws.execution.json)
  The linked substrate notebook execution report, including runtime status and generated figures.
- [`artifacts/ifme/plots/onset_surface.png`](./artifacts/ifme/plots/onset_surface.png)
  The current static onset-surface visualization.
- [`artifacts/ifme/plots/phase_regions.png`](./artifacts/ifme/plots/phase_regions.png)
  The current static phase-region visualization.
- [`artifacts/ifme/agent/agent_workflow.yaml`](./artifacts/ifme/agent/agent_workflow.yaml)
  The exported Sutskever-Agent workflow bundle for the current orchestration result.

## Configuration Model

The principal control object is `InterventionConfig`. It groups settings into six domains:

- `architecture`
- `objective`
- `data_regime`
- `retrieval`
- `context_geometry`
- `interpretability`

This makes it possible to specify sweeps and runs in a way that is legible both to humans and to downstream orchestration systems.

## Design Philosophy

### Separate measurement from pedagogy

Educational code is excellent for transparency but often weak as instrumentation. This repository does not replace pedagogical implementations. It upgrades them into a measurement surface.

### Prefer transparent proxies over ornate black boxes

Many of the estimates here are proxies rather than mathematically exact quantities. That is acceptable if the proxies are:

- explicit
- reproducible
- comparable across runs
- useful for ordering and diagnosis

### Keep the coupling loose

The repository does not require invasive edits to companion repos. It consumes them through adapters and environment-variable configuration.

### Build toward cumulative science

A useful research layer should not only produce one interesting notebook screenshot. It should produce artifacts that can accumulate over time, compare across runs, and support explanation.

## Current Capabilities

At the current version, the repository provides:

- a shared experiment contract
- text and array descriptor extraction
- multi-view compressibility estimation
- lightweight boundary and regime analysis
- a GPT-1 wind tunnel bridge
- a Sutskever-Agent narration bridge
- a sweep runner over scale, data, and task family
- persistent storage for sweep registries
- lightweight response-surface fitting
- measured tiny-run execution against the linked GPT-1 implementation
- repeated-seed measured studies across differentiated task families
- held-out predictive validation and bootstrap uncertainty intervals
- provenance capture with companion-repo commits and dirty state
- falsifiable law statements exported as machine-readable artifacts
- full Layer 2 orchestration over measured studies, sweeps, plotting, notebook execution, and agent export
- explicit failure-atlas exports with label counts and per-record predictions
- a local IFME `n`-lock analysis layer with retention, bootstrap, and sufficiency-based lock-count selection
- static onset-surface and phase-region visualizations
- direct linked notebook execution with saved figure capture
- Sutskever-Agent workflow bundle export
- JSON artifact export
- a runnable demo
- basic tests

## Current Limitations

This repository is an early measurement spine, not a complete mature research platform yet.

Important limitations:

- boundary fitting is intentionally lightweight and heuristic
- the descriptor schema currently uses proxies rather than fully learned latent estimators
- the current failure atlas is still simple and centroid-based rather than a strong probabilistic classifier
- notebook execution is now working for the current linked path, but it is not yet a comprehensive, notebook-by-notebook execution framework across the whole substrate
- the GPT-1 integration currently emphasizes small measured studies and instrumentation rather than large-scale sweep automation
- visualization is currently static rather than interactive
- the current response-surface fitting is still lightweight and should be replaced by stronger uncertainty-aware models
- the measured studies are still small-scale and should be expanded before making strong external claims

These are appropriate next targets, not hidden problems.

## Suggested Next Steps

If you are extending this repository, the highest-value next additions are:

1. replace the current centroid-based failure atlas with a stronger classifier that supports calibrated probabilities and richer failure taxonomies
2. expand notebook execution from the current proven path to a broader, more resilient substrate execution matrix with checkpoint capture
3. replace lightweight surface fitting with stronger uncertainty-aware statistical models
4. broaden measured studies beyond tiny local regimes so the law statements cover more than narrow toy settings
5. add interactive atlas exploration on top of the current static visualizations
6. deepen agent integration so the exported workflow bundle can drive comparative reruns and narrative synthesis across multiple Layer 2 studies

## Development

Run the tests with:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

Run the demo with:

```bash
python3 -m capability_cartography.demo
```

## Suggested GitHub Description

If you are publishing this as `github.com/pageman/Capability-Cartography-Layer-2-IFME`, a strong short description would be:

> An IFME-focused capability cartography framework for data-driven n-lock selection, measured laws, failure atlases, notebook-backed substrate execution, and agent-linked capability research.

## Citation

```bibtex
@misc{capability-cartography-layer-2-ifme-2026,
  author    = {Paul "The Pageman" Pajo, pageman@gmail.com},
  title     = {Capability-Cartography-Layer-2-IFME: an IFME-focused empirical framework for data-driven n-lock capability mapping, failure atlases, and notebook-backed cartography},
  year      = {2026},
  url       = {https://github.com/pageman/Capability-Cartography-Layer-2-IFME},
  note      = {IFME-focused successor to Capability-Cartography-Layer-2, extending the cartography spine with
               data-driven n-lock selection, retention/stability analysis, failure-atlas exports, and notebook-backed substrate execution.}
}
```

## License

This repository is released under the MIT License. See [`LICENSE`](./LICENSE).

## Final Framing

Capability Cartography Layer 2 IFME is meant to convert vague claims into map-like artifacts.

Instead of:

- “emergence”
- “brittleness”
- “surprisingly strong”
- “lost in the middle”
- “probably memorizing”

the repository pushes toward:

- onset surfaces
- threshold estimates
- descriptor-conditioned failure prediction
- compressibility gap analysis
- intervention-sensitive region shifts

That is the shift from anecdote to cartography, and from cartography toward an empirical science of model behavior.
