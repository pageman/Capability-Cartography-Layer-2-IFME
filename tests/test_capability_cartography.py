"""Basic verification for the Capability Cartography Layer."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from capability_cartography.adapters import AgentOverlayAdapter, GPT1WindTunnelAdapter, NotebookSubstrateAdapter
from capability_cartography.failure_atlas import FailureAtlasClassifier
from capability_cartography.ifme import IFMELockAnalyzer
from capability_cartography.notebook_runner import NotebookExecutionWrapper
from capability_cartography.orchestration import FullStudyOrchestrator
from capability_cartography.boundary import BoundaryAnalyzer
from capability_cartography.compressibility import CompressibilityStack
from capability_cartography.descriptors import TaskDescriptorExtractor
from capability_cartography.runner import CapabilityCartographyRunner
from capability_cartography.schemas import CapabilitySnapshot, ExperimentSpec, InterventionConfig
from capability_cartography.sweeps import SweepRunner
from capability_cartography.validation import PredictiveLawValidator


class CapabilityCartographyTests(unittest.TestCase):
    def test_descriptor_extraction_text(self):
        extractor = TaskDescriptorExtractor()
        descriptor = extractor.extract_text_descriptor(
            "If Alice retrieves the right passage, then the answer follows.",
            task_name="qa",
            benchmark_label="unit",
            substrate="test",
            retrieval_context="retrieves answer passage",
        )
        self.assertGreaterEqual(descriptor.retrieval_geometry["retrieval_dependency_score"], 0.0)
        self.assertEqual(descriptor.cognitive_operations["logical_deduction"], 1.0)

    def test_compressibility_stack_array(self):
        stack = CompressibilityStack()
        profile = stack.profile_array([[1, 0, 1], [1, 0, 1]])
        self.assertIn("gzip_ratio", profile.surface)
        self.assertGreaterEqual(profile.structural["effective_params"], 1)

    def test_boundary_detection(self):
        analyzer = BoundaryAnalyzer()
        snapshots = [
            CapabilitySnapshot(step=1, metrics={"capability_score": 0.2}, descriptor=None, compressibility=None),  # type: ignore[arg-type]
            CapabilitySnapshot(step=2, metrics={"capability_score": 0.5}, descriptor=None, compressibility=None),  # type: ignore[arg-type]
            CapabilitySnapshot(step=3, metrics={"capability_score": 0.85}, descriptor=None, compressibility=None),  # type: ignore[arg-type]
        ]
        events = analyzer.detect_events(snapshots, metric="capability_score")
        self.assertGreaterEqual(len(events), 1)

    def test_runner_exports(self):
        runner = CapabilityCartographyRunner()
        intervention = InterventionConfig(
            architecture={"d_model": 64, "num_heads": 4, "num_layers": 2, "d_ff": 128, "vocab_size": 96},
            objective={"loss_type": "next_token"},
            retrieval={"enabled": True, "distractor_density": 0.2},
            context_geometry={"answer_position": 32, "max_seq_len": 64},
        )
        spec = ExperimentSpec(
            experiment_id="unit-demo",
            substrate="unit-test",
            task_name="qa",
            benchmark_label="unit",
            realism_level="synthetic",
            objective_type="next_token",
            model_family="unit",
        )
        with TemporaryDirectory() as temp_dir:
            bundle = runner.run_text_experiment(
                spec,
                intervention,
                text="The model must retrieve a fact and reason over it.",
                retrieval_context="fact retrieval",
                export_dir=Path(temp_dir),
            )
            self.assertIsNotNone(bundle.export_path)
            self.assertTrue(Path(bundle.export_path).exists())
            self.assertIn("linked_repositories", bundle.to_dict())
            self.assertIn("series_metrics", bundle.trajectory.aggregate_metrics)

    def test_sweep_runner_outputs_summary(self):
        runner = CapabilityCartographyRunner()
        intervention = InterventionConfig(
            architecture={"d_model": 32, "num_heads": 2, "num_layers": 2, "d_ff": 64},
            objective={"loss_type": "next_token"},
            data_regime={"data_tokens": 2048},
            retrieval={"enabled": True, "distractor_density": 0.1},
            context_geometry={"answer_position": 24},
        )
        spec = ExperimentSpec(
            experiment_id="sweep-demo",
            substrate="sutskever-30-implementations",
            task_name="qa",
            benchmark_label="unit",
            realism_level="synthetic",
            objective_type="next_token",
            model_family="unit",
        )
        with TemporaryDirectory() as temp_dir:
            sweep_runner = SweepRunner(runner, temp_dir)
            result = sweep_runner.run_grid(
                base_spec=spec,
                base_intervention=intervention,
                text="The model retrieves a lemma and performs a proof step.",
                retrieval_context="lemma retrieval context",
                scale_values=[32, 64],
                data_token_values=[2048, 4096],
                task_family_values=["retrieval_qa"],
                seeds=[1],
            )
            self.assertEqual(result["summary"]["record_count"], 4)
            self.assertIn("surface_fit", result["summary"])

    def test_adapter_explicit_roots(self):
        substrate = NotebookSubstrateAdapter("/Users/hifi/sutskever-30-implementations")
        agent = AgentOverlayAdapter("/Users/hifi/Downloads/Sutskever-Agent/sutskever-agent")
        wind_tunnel = GPT1WindTunnelAdapter("/Users/hifi/Downloads/GPT1_from_Sutskerver30/GPT1_from_Sutskever30")
        self.assertTrue(substrate.link_metadata()["available"])
        self.assertTrue(agent.link_metadata()["available"])
        self.assertTrue(wind_tunnel.link_metadata()["available"])
        self.assertIsNotNone(substrate.link_metadata()["commit"])

    def test_measured_grid_validation(self):
        runner = CapabilityCartographyRunner(
            substrate_adapter=NotebookSubstrateAdapter("/Users/hifi/sutskever-30-implementations"),
            wind_tunnel_adapter=GPT1WindTunnelAdapter("/Users/hifi/Downloads/GPT1_from_Sutskerver30/GPT1_from_Sutskever30"),
            agent_adapter=AgentOverlayAdapter("/Users/hifi/Downloads/Sutskever-Agent/sutskever-agent"),
        )
        intervention = InterventionConfig(
            architecture={"d_model": 32, "num_layers": 1},
            objective={"loss_type": "next_token", "learning_rate": 1e-4},
            data_regime={"data_tokens": 1024},
            retrieval={"enabled": True, "distractor_density": 0.2},
            context_geometry={"max_seq_len": 16, "answer_position": 12},
        )
        spec = ExperimentSpec(
            experiment_id="measured-test",
            substrate="gpt1-from-sutskever30",
            task_name="object_tracking",
            benchmark_label="unit",
            realism_level="semi_synthetic",
            objective_type="next_token",
            model_family="gpt1-measured",
        )
        with TemporaryDirectory() as temp_dir:
            sweep_runner = SweepRunner(runner, temp_dir)
            result = sweep_runner.run_measured_grid(
                base_spec=spec,
                base_intervention=intervention,
                task_family_values=["object_tracking", "retrieval_qa"],
                scale_values=[32],
                data_token_values=[512],
                seeds=[1, 2],
                train_steps=1,
            )
            self.assertEqual(result["summary"]["record_count"], 4)
            self.assertIn("laws", result["summary"]["validation"])

    def test_failure_atlas_classifier(self):
        classifier = FailureAtlasClassifier()
        summary = classifier.train(
            [
                {"capability_score": 0.19, "generalization_gap": 0.05, "retrieval_dependence": 1.0, "task_family_code": 3.0, "scale": 32.0, "data_tokens": 1024.0},
                {"capability_score": 0.24, "generalization_gap": 0.01, "retrieval_dependence": 0.0, "task_family_code": 0.0, "scale": 64.0, "data_tokens": 2048.0},
            ]
        )
        prediction = classifier.predict({"capability_score": 0.18, "generalization_gap": 0.06, "retrieval_dependence": 1.0, "task_family_code": 3.0, "scale": 32.0, "data_tokens": 1024.0})
        self.assertIn("collapse", summary["labels"])
        self.assertIn("label_counts", summary)
        self.assertEqual(summary["record_count"], 2)
        self.assertIn("label", prediction)

    def test_notebook_wrapper_exports_script(self):
        substrate = NotebookSubstrateAdapter("/Users/hifi/sutskever-30-implementations")
        wrapper = NotebookExecutionWrapper(substrate)
        with TemporaryDirectory() as temp_dir:
            path = wrapper.export_notebook_script("22_scaling_laws", output_dir=temp_dir)
            self.assertTrue(Path(path).exists())

    def test_notebook_wrapper_executes_scaling_notebook(self):
        substrate = NotebookSubstrateAdapter("/Users/hifi/sutskever-30-implementations")
        wrapper = NotebookExecutionWrapper(substrate)
        with TemporaryDirectory() as temp_dir:
            report = wrapper.execute_notebook("22_scaling_laws", output_dir=temp_dir, timeout_seconds=120)
            self.assertEqual(report["returncode"], 0)
            self.assertGreaterEqual(len(report["generated_figures"]), 1)

    def test_ifme_lock_analyzer(self):
        records = [
            {"experiment_id": "a", "capability_score": 0.20, "generalization_gap": 0.01, "retrieval_dependence": 1.0, "task_family_code": 3.0, "scale": 32.0, "data_tokens": 1024.0},
            {"experiment_id": "b", "capability_score": 0.21, "generalization_gap": 0.01, "retrieval_dependence": 1.0, "task_family_code": 3.0, "scale": 64.0, "data_tokens": 2048.0},
            {"experiment_id": "c", "capability_score": 0.23, "generalization_gap": 0.00, "retrieval_dependence": 0.0, "task_family_code": 0.0, "scale": 32.0, "data_tokens": 1024.0},
            {"experiment_id": "d", "capability_score": 0.24, "generalization_gap": 0.02, "retrieval_dependence": 0.0, "task_family_code": 1.0, "scale": 64.0, "data_tokens": 2048.0},
            {"experiment_id": "e", "capability_score": 0.25, "generalization_gap": 0.04, "retrieval_dependence": 0.0, "task_family_code": 2.0, "scale": 32.0, "data_tokens": 1024.0},
            {"experiment_id": "f", "capability_score": 0.26, "generalization_gap": 0.05, "retrieval_dependence": 0.0, "task_family_code": 2.0, "scale": 64.0, "data_tokens": 2048.0},
        ]
        failure_records = [
            {"experiment_id": "a", "actual_label": "collapse"},
            {"experiment_id": "b", "actual_label": "collapse"},
            {"experiment_id": "c", "actual_label": "stable_reasoning"},
            {"experiment_id": "d", "actual_label": "stable_reasoning"},
            {"experiment_id": "e", "actual_label": "generalization_risk"},
            {"experiment_id": "f", "actual_label": "generalization_risk"},
        ]
        bundle = IFMELockAnalyzer(random_seed=7, parallel_samples=32, bootstrap_samples=16).analyze(records, failure_records=failure_records, max_k=4)
        self.assertIn("selected_lock_count", bundle.summary)
        self.assertGreaterEqual(bundle.summary["selected_lock_count"], 1)
        self.assertGreaterEqual(len(bundle.component_rows), 1)


if __name__ == "__main__":
    unittest.main()
