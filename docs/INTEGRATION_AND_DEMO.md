# Integration evidence and demos

`langgraph-integration.yml` exercises the **actual LangGraph execution framework** using deterministic stub agents in place of network/LLM operations. It verifies fan-out/fan-in and trace merging, plus the repository's simulation authorization rules.

This does **not** establish that Groq output, map geocoding, the local Chroma corpus, or an actual emergency process works. Those require separately tested integrations, reviewed procedure documents and qualified supervision. The system is strictly an educational demonstration.

## Repeat locally

```bash
python -m pip install "langgraph>=1,<2"
python -m unittest discover -s tests -p 'test_graph_integration.py' -v
python -m unittest discover -s tests -p 'test_repository_layout.py' -v
```

## Evidence artifacts

Download test logs from GitHub Actions to substantiate the topology test. The Streamlit UI may be captured as a **real** screenshot after launching `python -m streamlit run app.py`, but never fake a functioning emergency dispatch or publish real incident reports. UI screenshots are not evidence of operational fitness.
