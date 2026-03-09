import streamlit as st
import pandas as pd
import json
import os
from agent.graph import build_graph
from agent.state import AgentState

# --- config pagina ---
st.set_page_config(
    page_title="Autonomous Research Agent",
    page_icon="🔬",
    layout="wide"
)

# --- header ---
st.title("🔬 Autonomous Research & Report Agent")
st.caption("An LLM-powered agent that plans, searches, evaluates, and writes structured research reports autonomously.")
st.divider()

# --- input ---
task = st.text_area(
    "Research task",
    placeholder="e.g. Analyze the main trends in the European EdTech market in 2025",
    height=80
)
run_button = st.button("▶ Run Agent", type="primary", disabled=not task)

# --- session state per persistere risultati tra rerun ---
if "logs" not in st.session_state:
    st.session_state.logs = []
if "result" not in st.session_state:
    st.session_state.result = None

# --- esecuzione ---
if run_button and task:
    st.session_state.logs = []
    st.session_state.result = None

    graph = build_graph()
    initial_state: AgentState = {
        "task": task,
        "subtasks": [],
        "search_results": [],
        "report": "",
        "iterations": 0,
        "run_folder": ""
    }

    logs = []

    with st.spinner("Agent is working..."):
        for step in graph.stream(initial_state):
            node_name = list(step.keys())[0]
            node_output = step[node_name]

            if node_name == "planner":
                subtasks = node_output.get("subtasks", [])
                logs.append(("🧠", "Planner", f"Generated {len(subtasks)} search queries: {', '.join(subtasks)}"))

            elif node_name == "searcher":
                results = node_output.get("search_results", [])
                logs.append(("🔍", "Searcher", f"Retrieved {len(results)} new sources from the web"))

            elif node_name == "evaluator":
                iterations = node_output.get("iterations", 0)
                subtasks = node_output.get("subtasks", [])
                if subtasks:
                    logs.append(("⚖️", "Evaluator", f"Verdict: insufficient — starting iteration {iterations + 1}"))
                else:
                    logs.append(("⚖️", "Evaluator", "Verdict: sufficient — proceeding to report writing"))

            elif node_name == "writer":
                run_folder = node_output.get("run_folder", "outputs/")
                logs.append(("✍️", "Writer", f"Report generated and saved to {run_folder}"))
                logs.append(("✅", "Done", f"Run complete — {run_folder}"))

        st.session_state.logs = logs
        st.session_state.result = node_output  # ultimo nodo = writer

# --- mostra log ---
if st.session_state.logs:
    st.subheader("Agent Activity")
    for icon, node, message in st.session_state.logs:
        col1, col2, col3 = st.columns([0.05, 0.12, 0.83])
        with col1:
            st.write(icon)
        with col2:
            st.markdown(f"**{node}**")
        with col3:
            st.write(message)
    st.divider()

# --- output ---
if st.session_state.result:
    result = st.session_state.result
    run_folder = result.get("run_folder", "")
    report = result.get("report", "")

    tab1, tab2, tab3 = st.tabs(["📄 Report", "📊 Sources", "🗂️ Metadata"])

    with tab1:
        st.markdown(report)
        st.download_button(
            "⬇ Download report.md",
            data=report,
            file_name="report.md",
            mime="text/markdown"
        )

    with tab2:
        csv_path = f"{run_folder}/sources.csv"
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            st.dataframe(df, use_container_width=True)
            st.download_button(
                "⬇ Download sources.csv",
                data=df.to_csv(index=False),
                file_name="sources.csv",
                mime="text/csv"
            )
        else:
            st.info("Sources file not found.")

    with tab3:
        metadata_path = f"{run_folder}/run_metadata.json"
        if os.path.exists(metadata_path):
            with open(metadata_path) as f:
                metadata = json.load(f)
            col1, col2, col3 = st.columns(3)
            col1.metric("Iterations", metadata.get("iterations", "-"))
            col2.metric("Sources collected", metadata.get("sources_count", "-"))
            col3.metric("Timestamp", metadata.get("timestamp", "-"))
            st.text_input("Task", metadata.get("task", ""), disabled=True)
            st.text_input("Output folder", metadata.get("output_folder", ""), disabled=True)
        else:
            st.info("Metadata file not found.")