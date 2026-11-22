"""Exercise the real LangGraph topology with stubbed external agents.

No Groq key, geocoder, GPU, or simulated dispatch is required. This test
covers state merging/fan-in, NOT real incident analysis or emergency handling.
"""
import importlib
import sys
import types
import unittest
from unittest.mock import patch

NODES = [
    "incident_agent", "map_agent", "knowledge_rag", "resource_agent",
    "decision_agent", "safety_checker", "evidence_verifier",
    "human_approval_agent", "action_plan_agent",
]


def stub_node(name):
    def run(state):
        result = {"trace": [name]}
        if name == "incident_agent":
            result.update(incident_type="test", severity="low", location="demo", people_at_risk=0)
        if name == "map_agent":
            result["map_info"] = {"resolved": False}
        if name == "knowledge_rag":
            result["procedures"] = "synthetic procedure"
        if name == "resource_agent":
            result["resources"] = {"available": False}
        if name == "decision_agent":
            assert state["map_info"] and state["procedures"] and state["resources"]
            result["decision"] = "simulation only"
        if name == "safety_checker":
            result.update(safety_ok=False, safety_notes="not validated")
        if name == "evidence_verifier":
            result.update(evidence_check_ok=False, evidence_summary="not validated")
        if name == "human_approval_agent":
            result.update(approval_status="pending", approval_granted=False)
        if name == "action_plan_agent":
            result["action_plan"] = "SIMULATION ONLY"
        return result
    return run


class GraphIntegrationTests(unittest.TestCase):
    def test_graph_fanout_fanin_and_trace(self):
        stubs = {}
        for name in NODES:
            mod = types.ModuleType(name)
            setattr(mod, name, stub_node(name))
            stubs[name] = mod
        # Our stubs are injected only during import; no external provider modules execute.
        with patch.dict(sys.modules, stubs):
            sys.modules.pop("graph", None)
            try:
                graph = importlib.import_module("graph")
                result = graph.run_incident_pipeline("synthetic test incident")
            finally:
                sys.modules.pop("graph", None)
        self.assertEqual(result["decision"], "simulation only")
        self.assertEqual(result["action_plan"], "SIMULATION ONLY")
        self.assertEqual(sorted(result["trace"]), sorted(NODES))
        self.assertEqual(len(result["trace"]), len(NODES))


if __name__ == "__main__":
    unittest.main()
