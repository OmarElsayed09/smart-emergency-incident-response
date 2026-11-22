"""Small dependency-free tests of repository contracts and authorization wording."""
import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RepositoryChecks(unittest.TestCase):
    def test_agent_modules_exist(self):
        for name in (
            "incident_agent", "map_agent", "knowledge_rag", "resource_agent",
            "decision_agent", "safety_checker", "evidence_verifier",
            "human_approval_agent", "action_plan_agent",
        ):
            self.assertTrue((ROOT / (name + ".py")).is_file())

    def test_graph_imports_are_local(self):
        source = (ROOT / "graph.py").read_text(encoding="utf-8")
        ast.parse(source)
        self.assertNotIn("from agents.", source)

    def test_rag_uses_repo_root(self):
        text = (ROOT / "knowledge_rag.py").read_text(encoding="utf-8")
        self.assertIn("os.path.dirname(os.path.abspath(__file__))", text)

    def test_action_plan_does_not_authorize_real_dispatch(self):
        # This agent only uses the Python stdlib, so it is safe to import in CI.
        import sys
        sys.path.insert(0, str(ROOT))
        from action_plan_agent import action_plan_agent
        base = dict(approval_granted=True, safety_ok=False, evidence_check_ok=True)
        plan = action_plan_agent(base)["action_plan"]
        self.assertIn("no authorization for emergency dispatch", plan)
        safe = action_plan_agent(dict(approval_granted=True, safety_ok=True, evidence_check_ok=True))["action_plan"]
        self.assertIn("SIMULATION REVIEW APPROVED", safe)
        self.assertNotIn("AUTHORIZED for deployment", safe)


if __name__ == "__main__":
    unittest.main()
