"""Fast structure checks that do not call an external LLM."""
from pathlib import Path
import ast


ROOT = Path(__file__).resolve().parents[1]


def test_graph_imports_exist_at_root():
    ast.parse((ROOT / "graph.py").read_text(encoding="utf-8"))
    for module in ("incident_agent", "map_agent", "knowledge_rag", "resource_agent", "decision_agent", "safety_checker", "evidence_verifier", "human_approval_agent", "action_plan_agent"):
        assert (ROOT / (module + ".py")).exists()


def test_no_outdated_agents_package_import():
    assert "from agents." not in (ROOT / "graph.py").read_text(encoding="utf-8")


def test_knowledge_rag_uses_repo_root():
    text = (ROOT / "knowledge_rag.py").read_text(encoding="utf-8")
    assert 'os.path.dirname(os.path.abspath(__file__))' in text
