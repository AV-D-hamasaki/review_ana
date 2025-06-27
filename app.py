import asyncio
from pathlib import Path

import pandas as pd
import streamlit as st

from src import analytics, file_io, labeler, needs_master

st.set_page_config(page_title="Review Analyzer", layout="wide")

st.sidebar.header("Upload Reviews")
uploaded = st.sidebar.file_uploader("CSV or Excel", type=["csv", "xlsx"])
edit_master = st.sidebar.button("Edit Needs Master")
model_name = st.sidebar.text_input("Model", value="gpt-3.5-turbo")
run_label = st.sidebar.button("Run Labeling")
download_btn = st.sidebar.button("Download Labeled Data")

if edit_master:
    needs = st.session_state.get("needs", needs_master.load_master())
    edited = st.sidebar.text_area("Comma separated needs", ",".join(needs))
    if st.sidebar.button("Save Needs"):
        needs = [n.strip() for n in edited.split(",") if n.strip()]
        needs_master.save_master(needs)
        st.session_state["needs"] = needs
        st.sidebar.success("Saved")

if uploaded is not None:
    df = file_io.load_reviews(uploaded)
    st.session_state["df"] = df
    st.dataframe(df)

if run_label and "df" in st.session_state:
    needs = needs_master.load_master()
    df = st.session_state["df"]
    with st.spinner("Labeling..."):
        labeled = asyncio.run(labeler.label_reviews(df, needs, model=model_name))
    st.session_state["labeled"] = labeled
    st.success("Done")

if "labeled" in st.session_state:
    labeled = st.session_state["labeled"]
    st.subheader("Labeled Reviews")
    st.dataframe(labeled)
    metrics = analytics.calculate_metrics(labeled)
    st.subheader("Metrics")
    st.dataframe(metrics)

    if download_btn:
        tmp_path = Path("labeled.xlsx")
        file_io.save_to_excel(labeled, tmp_path)
        st.sidebar.download_button(
            "Download Excel", tmp_path.read_bytes(), file_name="labeled.xlsx"
        )
