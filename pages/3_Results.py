import os
from datetime import date as _date
from typing import cast

import altair as alt
import pandas as pd
import streamlit as st

DATA_FILE = "Updated_Training_Feedback_Survey_Template.csv"


def render_results_dashboard() -> None:
    # Unified header
    st.markdown(
        """
        <h1 style='text-align: center; color: #2F1B14;'>Training Feedback Survey</h1>
        <h3 style='text-align: center; color: #8B2635;'>Excellence Through Training</h3>
        """,
        unsafe_allow_html=True,
    )

    if not os.path.exists(DATA_FILE):
        st.warning("No survey data available yet. Submit at least one survey to view results.")
        st.stop()

    df: pd.DataFrame = pd.read_csv(DATA_FILE)
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

    # Sidebar Filters
    st.sidebar.header("Filters")
    cscs = sorted(df.get("CSC", pd.Series([])).dropna().unique().tolist())
    csc_filter = st.sidebar.multiselect("CSC(s)", options=cscs, default=cscs)

    date_min = df.get("Timestamp", pd.Series([pd.NaT])).min()
    date_max = df.get("Timestamp", pd.Series([pd.NaT])).max()
    start_date, end_date = None, None
    if pd.notna(date_min) and pd.notna(date_max):
        start_date = cast(_date, st.sidebar.date_input("Start date", date_min.date()))
        end_date = cast(_date, st.sidebar.date_input("End date", date_max.date()))

    # Apply filters
    mask = pd.Series([True] * len(df))
    if csc_filter:
        mask &= df["CSC"].isin(csc_filter)
    if start_date and end_date and "Timestamp" in df.columns:
        mask &= (df["Timestamp"] >= pd.Timestamp(start_date)) & (
            df["Timestamp"] < pd.Timestamp(end_date) + pd.Timedelta(days=1)
        )

    fdf = df[mask].copy()

    # Overview
    st.subheader("Overview")
    left, right = st.columns(2)
    with left:
        st.metric("Total responses", int(len(fdf)))
    with right:
        if "CSC" in fdf.columns:
            st.metric("Unique CSCs", int(fdf["CSC"].nunique()))

    # CSC distribution
    if "CSC" in fdf.columns and not fdf["CSC"].dropna().empty:
        st.subheader("Responses by CSC")
        csc_counts = fdf["CSC"].value_counts().reset_index()
        csc_counts.columns = ["CSC", "Responses"]
        chart = alt.Chart(csc_counts).mark_bar().encode(
            x=alt.X("CSC:N", sort="-y"),
            y="Responses:Q",
            tooltip=["CSC", "Responses"],
        )
        st.altair_chart(chart, use_container_width=True)

    # Average Ratings
    rating_cols = [c for c in fdf.columns if "Confidence" in c or c == "AI_Survey_Experience_Rating"]
    if rating_cols:
        st.subheader("Average Ratings")
        avgs = fdf[rating_cols].mean(numeric_only=True).reset_index()
        avgs.columns = ["Question", "Average"]
        chart = alt.Chart(avgs).mark_bar().encode(
            x=alt.X("Question:N", sort="-y"),
            y=alt.Y("Average:Q"),
            tooltip=["Question", "Average"],
        )
        st.altair_chart(chart, use_container_width=True)

    # Skills Breakdown
    section_skill_cols = {
        "Title": "Title_Class_Skills_Important",
        "FDR1/DLID": "FDR1_and_DLID_Skills_Important",
        "Driver Examiner": "Driver_Examiner_Skills_Important",
        "Compliance": "Compliance_Skills_Important",
        "Advanced": "Advanced_VDH_FDR_II_FDR_III_Skills_Important",
    }
    for section, col in section_skill_cols.items():
        if col in fdf.columns and not fdf[col].dropna().empty:
            st.subheader(f"{section} – Selected Skill Options")
            counts = fdf[col].value_counts().reset_index()
            counts.columns = ["Option", "Count"]
            chart = alt.Chart(counts).mark_bar().encode(
                x=alt.X("Option:N", sort="-y"),
                y="Count:Q",
                tooltip=["Option", "Count"],
            )
            st.altair_chart(chart, use_container_width=True)

    # Audit Issues Breakdown
    audit_cols = [c for c in fdf.columns if c.endswith("_Audit_Issues")]
    if audit_cols:
        st.subheader("Audit Issues Overview")
        for col in audit_cols:
            section_name = col.replace("_Audit_Issues", "").replace("_", " ")
            st.markdown(f"**{section_name}**")

            # Extract Yes/No
            audit_split = fdf[col].fillna("").apply(lambda x: x.split(" - ")[0].strip())
            counts = audit_split.value_counts().reset_index()
            counts.columns = ["Response", "Count"]

            chart = alt.Chart(counts).mark_bar().encode(
                x=alt.X("Response:N", sort="-y"),
                y="Count:Q",
                tooltip=["Response", "Count"],
            )
            st.altair_chart(chart, use_container_width=True)

            # Show common error details if any
            if audit_split.eq("Yes").any():
                st.write("Common Issues Reported:")
                issues = fdf[col].dropna().apply(lambda x: x.split(" - ")[1] if " - " in x else "")
                issues = issues[issues != ""]
                if not issues.empty:
                    st.dataframe(issues.reset_index(drop=True), use_container_width=True)

    # Raw table
    st.subheader("Raw Responses (filtered)")
    st.dataframe(fdf, use_container_width=True)

    # Export
    st.subheader("Export")
    st.download_button(
        label="Download filtered CSV",
        data=fdf.to_csv(index=False).encode("utf-8"),
        file_name="filtered_results.csv",
        mime="text/csv",
    )
    st.download_button(
        label="Download filtered Excel",
        data=fdf.to_excel(index=False, engine="openpyxl"),
        file_name="filtered_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":
    render_results_dashboard()
