"""Shared schemas for the Capability Cartography Layer."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TaskDescriptor:
    """Descriptor vector for a single task instance or task family."""

    task_name: str
    benchmark_label: str
    substrate: str
    realism_level: str
    surface_statistics: Dict[str, float] = field(default_factory=dict)
    latent_structure: Dict[str, float] = field(default_factory=dict)
    retrieval_geometry: Dict[str, float] = field(default_factory=dict)
    perturbation_profile: Dict[str, float] = field(default_factory=dict)
    cognitive_operations: Dict[str, float] = field(default_factory=dict)
    structural_complexity: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CompressibilityProfile:
    """Surface, predictive, and structural compression proxies."""

    surface: Dict[str, float]
    predictive: Dict[str, float]
    structural: Dict[str, float]
    gaps: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CapabilitySnapshot:
    """A single checkpoint measurement."""

    step: int
    metrics: Dict[str, float]
    descriptor: TaskDescriptor
    compressibility: CompressibilityProfile
    notes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step": self.step,
            "metrics": dict(self.metrics),
            "descriptor": self.descriptor.to_dict(),
            "compressibility": self.compressibility.to_dict(),
            "notes": dict(self.notes),
        }


@dataclass
class BoundaryEvent:
    """Detected qualitative shift in a metric series."""

    metric: str
    step: int
    value: float
    delta: float
    regime_before: str
    regime_after: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BoundaryFit:
    """Threshold summary across a sweep."""

    metric: str
    threshold_value: float
    threshold_step: int
    slope: float
    lower_band: float
    upper_band: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CapabilityTrajectory:
    """Time series of capability measurements."""

    experiment_id: str
    substrate: str
    intervention_config: Dict[str, Any]
    snapshots: List[CapabilitySnapshot]
    boundary_events: List[BoundaryEvent] = field(default_factory=list)
    fitted_boundaries: List[BoundaryFit] = field(default_factory=list)
    aggregate_metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "substrate": self.substrate,
            "intervention_config": dict(self.intervention_config),
            "snapshots": [snapshot.to_dict() for snapshot in self.snapshots],
            "boundary_events": [event.to_dict() for event in self.boundary_events],
            "fitted_boundaries": [fit.to_dict() for fit in self.fitted_boundaries],
            "aggregate_metrics": dict(self.aggregate_metrics),
        }


@dataclass
class ExperimentSpec:
    """Single experiment contract."""

    experiment_id: str
    substrate: str
    task_name: str
    benchmark_label: str
    realism_level: str
    objective_type: str
    model_family: str
    intervention_axes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class InterventionConfig:
    """One-factor-at-a-time or bundled interventions."""

    architecture: Dict[str, Any] = field(default_factory=dict)
    objective: Dict[str, Any] = field(default_factory=dict)
    data_regime: Dict[str, Any] = field(default_factory=dict)
    retrieval: Dict[str, Any] = field(default_factory=dict)
    context_geometry: Dict[str, Any] = field(default_factory=dict)
    interpretability: Dict[str, Any] = field(default_factory=dict)

    def flattened(self) -> Dict[str, Any]:
        flattened: Dict[str, Any] = {}
        for section_name, section_value in asdict(self).items():
            for key, value in section_value.items():
                flattened[f"{section_name}.{key}"] = value
        return flattened

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class InterventionSweep:
    """Sweep definition for a single intervention axis."""

    axis: str
    values: List[Any]
    baseline: InterventionConfig

    def to_dict(self) -> Dict[str, Any]:
        return {
            "axis": self.axis,
            "values": list(self.values),
            "baseline": self.baseline.to_dict(),
        }


@dataclass
class ArtifactBundle:
    """Serialized outputs for downstream narration and plotting."""

    spec: ExperimentSpec
    trajectory: CapabilityTrajectory
    narrative: Optional[str] = None
    export_path: Optional[str] = None
    linked_repositories: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "spec": self.spec.to_dict(),
            "trajectory": self.trajectory.to_dict(),
            "linked_repositories": dict(self.linked_repositories),
        }
        if self.narrative is not None:
            payload["narrative"] = self.narrative
        if self.export_path is not None:
            payload["export_path"] = self.export_path
        return payload
