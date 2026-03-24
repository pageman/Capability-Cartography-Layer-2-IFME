"""IFME-style n-lock analysis over Layer 2 measured artifacts."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

import numpy as np


@dataclass
class IFMEAnalysisBundle:
    """Container for IFME analysis outputs."""

    summary: Dict[str, object]
    component_rows: List[Dict[str, object]]


class IFMELockAnalyzer:
    """Select a local n-lock solution from measured Layer 2 records."""

    def __init__(self, *, random_seed: int = 0, parallel_samples: int = 200, bootstrap_samples: int = 64):
        self.random_seed = random_seed
        self.parallel_samples = parallel_samples
        self.bootstrap_samples = bootstrap_samples

    def analyze(
        self,
        records: Sequence[Dict[str, object]],
        *,
        failure_records: Sequence[Dict[str, object]] | None = None,
        max_k: int = 8,
    ) -> IFMEAnalysisBundle:
        matrix, feature_names = self._build_field_matrix(records)
        standardized = self._standardize(matrix)
        residualized, residual_feature_names = self._residualize_scale_data(standardized, feature_names)

        pca = self._pca(residualized)
        max_k = min(max_k, residualized.shape[1])
        parallel = self._parallel_analysis(residualized, max_k=max_k)
        map_result = self._velicer_map(residualized, max_k=max_k)
        labels = self._resolve_labels(records, failure_records)
        sufficiency = self._behavioral_sufficiency(residualized, labels, np.asarray([float(r["capability_score"]) for r in records]), max_k=max_k)
        bootstrap = self._bootstrap_lock_stability(residualized, max_k=max_k)
        selected_k, rationale = self._select_lock_count(
            parallel_count=parallel["retained_count"],
            map_count=map_result["preferred_count"],
            sufficiency=sufficiency,
            bootstrap=bootstrap,
            max_k=max_k,
        )
        lock_rows = self._lock_rows(
            pca["loadings"],
            residual_feature_names,
            selected_k,
        )

        summary = {
            "record_count": len(records),
            "field_definition": {
                "raw_feature_names": feature_names,
                "residual_feature_names": residual_feature_names,
                "state_interpretation": (
                    "The current IFME local chart is built from measured Layer 2 observables and derived interaction terms. "
                    "This is a local field construction, not a universal final state space."
                ),
            },
            "retention": {
                "parallel_analysis": parallel,
                "velicer_map": map_result,
                "bootstrap_stability": bootstrap,
            },
            "sufficiency": sufficiency,
            "selected_lock_count": selected_k,
            "selected_lock_regime": f"{selected_k}-lock",
            "selection_rationale": rationale,
            "candidate_lock_families": [row["lock_name"] for row in lock_rows],
            "local_law_interpretation": (
                "Treat the fitted Layer 2 predictive law as a local chart on the IFME manifold. "
                "The selected lock count is valid only inside the current measured regime."
            ),
            "limitations": [
                "Current IFME selection is based on the present small measured Layer 2 regime.",
                "Compressibility and context-geometry variables are not yet flattened into the measured records table at the same richness described in the full IFME state construction.",
                "The present solution should be read as a local empirical lock count, not a final universal capability structure.",
            ],
        }
        return IFMEAnalysisBundle(summary=summary, component_rows=lock_rows)

    def _build_field_matrix(self, records: Sequence[Dict[str, object]]) -> Tuple[np.ndarray, List[str]]:
        rows: List[List[float]] = []
        feature_names = [
            "capability_score",
            "generalization_gap",
            "retrieval_dependence",
            "task_family_code",
            "scale",
            "data_tokens",
            "log_scale",
            "log_data_tokens",
            "scale_x_retrieval",
            "gap_x_retrieval",
            "capability_x_gap",
        ]
        for record in records:
            capability = float(record.get("capability_score", 0.0))
            gap = float(record.get("generalization_gap", 0.0))
            retrieval = float(record.get("retrieval_dependence", 0.0))
            task_family_code = float(record.get("task_family_code", 0.0))
            scale = float(record.get("scale", 0.0))
            data_tokens = float(record.get("data_tokens", 0.0))
            rows.append(
                [
                    capability,
                    gap,
                    retrieval,
                    task_family_code,
                    scale,
                    data_tokens,
                    float(np.log1p(scale)),
                    float(np.log1p(data_tokens)),
                    scale * retrieval,
                    gap * retrieval,
                    capability * gap,
                ]
            )
        return np.asarray(rows, dtype=float), feature_names

    @staticmethod
    def _standardize(matrix: np.ndarray) -> np.ndarray:
        mean = np.mean(matrix, axis=0)
        std = np.std(matrix, axis=0)
        std[std == 0] = 1.0
        return (matrix - mean) / std

    def _residualize_scale_data(self, matrix: np.ndarray, feature_names: Sequence[str]) -> Tuple[np.ndarray, List[str]]:
        control_names = ["scale", "data_tokens", "log_scale", "log_data_tokens"]
        control_idx = [feature_names.index(name) for name in control_names]
        keep_idx = [i for i in range(len(feature_names)) if i not in control_idx]
        controls = matrix[:, control_idx]
        design = np.column_stack([np.ones(len(matrix)), controls])
        residual_cols = []
        residual_names = []
        for idx in keep_idx:
            y = matrix[:, idx]
            beta, *_ = np.linalg.lstsq(design, y, rcond=None)
            residual = y - design @ beta
            residual_cols.append(residual)
            residual_names.append(f"{feature_names[idx]}_residual")
        residualized = np.column_stack(residual_cols)
        return self._standardize(residualized), residual_names

    def _pca(self, matrix: np.ndarray) -> Dict[str, np.ndarray]:
        corr = np.corrcoef(matrix, rowvar=False)
        corr = np.nan_to_num(corr, nan=0.0)
        eigvals, eigvecs = np.linalg.eigh(corr)
        order = np.argsort(eigvals)[::-1]
        eigvals = eigvals[order]
        eigvecs = eigvecs[:, order]
        loadings = eigvecs * np.sqrt(np.clip(eigvals, 0.0, None))
        return {"eigenvalues": eigvals, "eigenvectors": eigvecs, "loadings": loadings}

    def _parallel_analysis(self, matrix: np.ndarray, *, max_k: int) -> Dict[str, object]:
        rng = np.random.default_rng(self.random_seed)
        empirical = self._pca(matrix)["eigenvalues"][:max_k]
        random_eigenvalues = []
        for _ in range(self.parallel_samples):
            random_matrix = rng.normal(size=matrix.shape)
            random_matrix = self._standardize(random_matrix)
            random_eigenvalues.append(self._pca(random_matrix)["eigenvalues"][:max_k])
        random_eigenvalues = np.asarray(random_eigenvalues)
        percentile_95 = np.percentile(random_eigenvalues, 95, axis=0)
        retained_count = int(np.sum(empirical > percentile_95))
        return {
            "empirical_eigenvalues": empirical.tolist(),
            "random_95th_percentile": percentile_95.tolist(),
            "retained_count": max(retained_count, 1),
        }

    def _velicer_map(self, matrix: np.ndarray, *, max_k: int) -> Dict[str, object]:
        centered = self._standardize(matrix)
        u, s, vt = np.linalg.svd(centered, full_matrices=False)
        scores = u * s
        avg_sq_partial = []
        for k in range(0, max_k + 1):
            if k == 0:
                residual = centered
            else:
                reconstructed = scores[:, :k] @ vt[:k, :]
                residual = centered - reconstructed
            corr = np.corrcoef(residual, rowvar=False)
            corr = np.nan_to_num(corr, nan=0.0)
            mask = ~np.eye(corr.shape[0], dtype=bool)
            avg_sq_partial.append(float(np.mean(np.square(corr[mask]))))
        search_values = avg_sq_partial[:-1] if len(avg_sq_partial) > 1 else avg_sq_partial
        preferred_count = int(np.argmin(search_values))
        return {
            "avg_squared_partial_correlations": avg_sq_partial,
            "preferred_count": preferred_count,
        }

    def _resolve_labels(
        self,
        records: Sequence[Dict[str, object]],
        failure_records: Sequence[Dict[str, object]] | None,
    ) -> List[str]:
        if failure_records:
            label_map = {
                str(record.get("experiment_id", "")): str(record.get("actual_label") or record.get("predicted_label") or "stable_reasoning")
                for record in failure_records
            }
            labels = [label_map.get(str(record.get("experiment_id", "")), "stable_reasoning") for record in records]
            if any(label != "stable_reasoning" for label in labels):
                return labels
        labels = []
        for record in records:
            score = float(record.get("capability_score", 0.0))
            gap = float(record.get("generalization_gap", 0.0))
            retrieval = float(record.get("retrieval_dependence", 0.0))
            if score < 0.21:
                labels.append("collapse")
            elif retrieval > 0.5 and gap > 0.02:
                labels.append("brittle_retrieval")
            elif gap > 0.03:
                labels.append("generalization_risk")
            else:
                labels.append("stable_reasoning")
        return labels

    def _behavioral_sufficiency(
        self,
        matrix: np.ndarray,
        labels: Sequence[str],
        capability_scores: np.ndarray,
        *,
        max_k: int,
    ) -> Dict[str, object]:
        pca = self._pca(matrix)
        scores = matrix @ pca["eigenvectors"]
        label_set = sorted(set(labels))
        results = []
        threshold = float(np.median(capability_scores))
        for k in range(1, max_k + 1):
            reduced = scores[:, :k]
            predicted_labels = []
            predicted_caps = []
            for i in range(len(reduced)):
                train_mask = np.ones(len(reduced), dtype=bool)
                train_mask[i] = False
                x_train = reduced[train_mask]
                y_train = capability_scores[train_mask]
                label_train = [labels[j] for j in range(len(labels)) if j != i]
                centroids = {
                    label: np.mean(x_train[[idx for idx, value in enumerate(label_train) if value == label]], axis=0)
                    for label in label_set
                    if any(value == label for value in label_train)
                }
                distances = {label: float(np.linalg.norm(reduced[i] - centroid)) for label, centroid in centroids.items()}
                predicted_labels.append(min(distances, key=distances.get))

                design = np.column_stack([np.ones(len(x_train)), x_train])
                beta, *_ = np.linalg.lstsq(design, y_train, rcond=None)
                predicted_caps.append(float(np.dot(np.concatenate([[1.0], reduced[i]]), beta)))
            accuracy = float(np.mean([predicted_labels[i] == labels[i] for i in range(len(labels))]))
            macro_f1 = self._macro_f1(labels, predicted_labels)
            capability_r2 = self._r2(capability_scores, np.asarray(predicted_caps))
            onset_accuracy = float(
                np.mean(
                    [
                        (predicted_caps[i] >= threshold) == (capability_scores[i] >= threshold)
                        for i in range(len(predicted_caps))
                    ]
                )
            )
            results.append(
                {
                    "k": k,
                    "failure_accuracy": accuracy,
                    "failure_macro_f1": macro_f1,
                    "capability_r2": capability_r2,
                    "onset_accuracy": onset_accuracy,
                }
            )
        for index, row in enumerate(results):
            next_row = results[index + 1] if index + 1 < len(results) else None
            if next_row is None:
                row["next_k_improvement"] = 0.0
            else:
                row["next_k_improvement"] = float(
                    max(
                        next_row["failure_macro_f1"] - row["failure_macro_f1"],
                        next_row["capability_r2"] - row["capability_r2"],
                        next_row["onset_accuracy"] - row["onset_accuracy"],
                    )
                )
        return {"candidate_metrics": results}

    def _bootstrap_lock_stability(self, matrix: np.ndarray, *, max_k: int) -> Dict[str, object]:
        rng = np.random.default_rng(self.random_seed + 17)
        counts = Counter()
        for _ in range(self.bootstrap_samples):
            indices = rng.integers(0, len(matrix), size=len(matrix))
            sample = matrix[indices]
            retained = self._parallel_analysis(sample, max_k=max_k)["retained_count"]
            counts[int(retained)] += 1
        frequencies = {str(k): counts.get(k, 0) / float(self.bootstrap_samples) for k in range(1, max_k + 1)}
        modal_count = max(counts, key=counts.get) if counts else 1
        return {"modal_count": int(modal_count), "retained_count_frequencies": frequencies}

    def _select_lock_count(
        self,
        *,
        parallel_count: int,
        map_count: int,
        sufficiency: Dict[str, object],
        bootstrap: Dict[str, object],
        max_k: int,
    ) -> Tuple[int, str]:
        metrics = {int(row["k"]): row for row in sufficiency["candidate_metrics"]}  # type: ignore[index]
        start_k = max(1, min(parallel_count, max_k))
        modal_count = int(bootstrap.get("modal_count", start_k))
        frequencies = bootstrap.get("retained_count_frequencies", {})
        chosen = start_k
        for k in range(start_k, max_k + 1):
            row = metrics[k]
            stable = float(frequencies.get(str(k), 0.0)) >= 0.2 or k == modal_count
            sufficient = (
                float(row["failure_macro_f1"]) >= 0.75
                and float(row["capability_r2"]) >= 0.7
                and float(row["onset_accuracy"]) >= 0.75
            )
            marginal = float(row["next_k_improvement"]) <= 0.03
            if stable and sufficient and marginal:
                chosen = k
                break
            if stable and sufficient:
                chosen = k
        map_clause = (
            f"MAP preferred {map_count}, which does not force a smaller solution than {chosen}."
            if map_count >= chosen
            else f"MAP preferred a smaller solution ({map_count}), so {chosen} should be read as a conservative behavioral-sufficiency choice."
        )
        rationale = (
            f"Selected the smallest local {chosen}-lock solution starting from parallel retention ({parallel_count}), "
            f"checking bootstrap mode ({modal_count}), and requiring behavioral sufficiency plus diminishing gain. {map_clause}"
        )
        return chosen, rationale

    def _lock_rows(self, loadings: np.ndarray, feature_names: Sequence[str], k: int) -> List[Dict[str, object]]:
        rows = []
        for component_index in range(min(k, loadings.shape[1])):
            component = loadings[:, component_index]
            order = np.argsort(np.abs(component))[::-1][:4]
            top_features = [(feature_names[idx], float(component[idx])) for idx in order]
            rows.append(
                {
                    "component": component_index + 1,
                    "lock_name": self._name_lock(top_features),
                    "top_loadings": [
                        {"feature": feature, "loading": loading}
                        for feature, loading in top_features
                    ],
                }
            )
        return rows

    @staticmethod
    def _name_lock(top_features: Sequence[Tuple[str, float]]) -> str:
        scores = {
            "retrieval_context_integration_lock": 0,
            "task_family_cognitive_form_lock": 0,
            "scale_capacity_lock": 0,
            "generalization_gap_lock": 0,
            "capability_threshold_lock": 0,
            "data_regime_lock": 0,
        }
        for feature, loading in top_features:
            weight = abs(float(loading))
            if "retrieval" in feature:
                scores["retrieval_context_integration_lock"] += weight
            if "task_family" in feature:
                scores["task_family_cognitive_form_lock"] += weight
            if "scale" in feature:
                scores["scale_capacity_lock"] += weight
            if "gap" in feature:
                scores["generalization_gap_lock"] += weight
            if "capability_score" in feature or "capability_x_gap" in feature:
                scores["capability_threshold_lock"] += weight
            if "data_tokens" in feature:
                scores["data_regime_lock"] += weight
        best = max(scores, key=scores.get)
        if scores[best] > 0:
            return best
        return "capability_interaction_lock"

    @staticmethod
    def _macro_f1(true_labels: Sequence[str], pred_labels: Sequence[str]) -> float:
        labels = sorted(set(true_labels) | set(pred_labels))
        f1_scores = []
        for label in labels:
            tp = sum(1 for t, p in zip(true_labels, pred_labels) if t == label and p == label)
            fp = sum(1 for t, p in zip(true_labels, pred_labels) if t != label and p == label)
            fn = sum(1 for t, p in zip(true_labels, pred_labels) if t == label and p != label)
            if tp == 0 and fp == 0 and fn == 0:
                f1_scores.append(1.0)
                continue
            precision = tp / max(tp + fp, 1)
            recall = tp / max(tp + fn, 1)
            if precision + recall == 0:
                f1_scores.append(0.0)
            else:
                f1_scores.append(2 * precision * recall / (precision + recall))
        return float(np.mean(f1_scores))

    @staticmethod
    def _r2(true_values: np.ndarray, pred_values: np.ndarray) -> float:
        ss_res = float(np.sum(np.square(true_values - pred_values)))
        ss_tot = float(np.sum(np.square(true_values - np.mean(true_values))))
        if ss_tot == 0:
            return 0.0
        return 1.0 - ss_res / ss_tot
