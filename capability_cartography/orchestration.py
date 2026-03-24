"""Full orchestration over intervention grids and downstream analysis."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from .agent_integration import SutskeverAgentWorkflowBridge
from .failure_atlas import FailureAtlasClassifier
from .ifme import IFMELockAnalyzer
from .notebook_runner import NotebookExecutionWrapper
from .runner import CapabilityCartographyRunner
from .schemas import ExperimentSpec, InterventionConfig
from .storage import RunStorage
from .sweeps import SweepRunner
from .visualization import CartographyVisualizer


class FullStudyOrchestrator:
    """Run the full second-generation study stack."""

    def __init__(self, runner: CapabilityCartographyRunner, *, output_root: str | Path):
        self.runner = runner
        self.output_root = Path(output_root)
        self.sweep_runner = SweepRunner(runner, self.output_root)
        self.storage = RunStorage(self.output_root)
        self.failure_atlas = FailureAtlasClassifier()
        self.ifme = IFMELockAnalyzer()
        self.visualizer = CartographyVisualizer()
        self.notebook_wrapper = NotebookExecutionWrapper(runner.substrate_adapter)
        self.agent_bridge = SutskeverAgentWorkflowBridge(runner.agent_adapter)

    def run(self, *, spec: ExperimentSpec, intervention: InterventionConfig) -> Dict[str, object]:
        sweep_result = self.sweep_runner.run_grid(
            base_spec=spec,
            base_intervention=intervention,
            text="Capability formation depends on scale, task structure, and retrieval geometry.",
            retrieval_context="Linked substrate context and retrieval passages.",
            scale_values=[32, 64, 128],
            data_token_values=[2048, 8192, 32768],
            task_family_values=["synthetic_reasoning", "retrieval_qa"],
            seeds=[1, 2],
        )
        measured_result = self.sweep_runner.run_measured_grid(
            base_spec=spec,
            base_intervention=intervention,
            task_family_values=["object_tracking", "pair_matching", "babi_simple", "retrieval_qa"],
            scale_values=[32, 64],
            data_token_values=[1024, 2048],
            seeds=[1, 2],
            train_steps=2,
        )
        measured_records = measured_result["records"]
        failure_summary = self.failure_atlas.train(measured_records)
        failure_path = self.failure_atlas.export(self.output_root / "failure_atlas" / "failure_atlas.json", failure_summary)
        ifme_bundle = self.ifme.analyze(measured_records, failure_records=failure_summary.get("records", []))
        ifme_summary_path = self.storage.save_json("ifme/ifme_summary.json", ifme_bundle.summary)
        ifme_components_path = self.storage.save_records_csv("ifme/ifme_components.csv", ifme_bundle.component_rows)
        onset_plot = self.visualizer.plot_onset_surface(measured_records, output_path=self.output_root / "plots" / "onset_surface.png")
        phase_plot = self.visualizer.plot_phase_regions(measured_records, output_path=self.output_root / "plots" / "phase_regions.png")
        try:
            notebook_report = self.notebook_wrapper.execute_notebook("22_scaling_laws", output_dir=self.output_root / "notebooks")
        except Exception as exc:
            notebook_report = {
                "notebook_name": "22_scaling_laws",
                "returncode": -1,
                "stdout": "",
                "stderr": str(exc),
                "report_path": "",
            }
        brief = self.agent_bridge.build_agent_brief(
            measured_summary=measured_result["summary"],
            failure_atlas_summary=failure_summary,
            visualization_paths=[onset_plot, phase_plot, failure_path, notebook_report["report_path"], ifme_summary_path, ifme_components_path],
        )
        agent_bundle = self.agent_bridge.export_workflow_bundle(output_dir=self.output_root / "agent", brief=brief)
        return {
            "sweep_summary": sweep_result["summary"],
            "measured_summary": measured_result["summary"],
            "failure_atlas": failure_summary,
            "ifme_summary": ifme_bundle.summary,
            "plots": [onset_plot, phase_plot],
            "notebook_report": notebook_report,
            "agent_bundle": agent_bundle,
        }
