import streamlit as st
import pandas as pd
import altair as alt
import os

st.set_page_config(page_title="Training Survey Results", layout="wide")

# Sidebar / Title
st.sidebar.title("Results")
st.title("📊 Training Survey Results Dashboard")

# Styling (match app look & feel)
st.markdown(
    """
    <style>
        body { color: #2F1B14; background-color: #FAF7F0; }
        .stApp { color: #2F1B14; background-color: #FEFCF7; }
        h1, h2, h3 { color: #8B2635; }
    </style>
    """, unsafe_allow_html=True
)

DATA_FILE = "survey_data.csv"

if not os.path.exists(DATA_FILE):
    st.warning("No survey data available yet. Submit at least one survey to view results.")
    st.stop()

# Load
df = pd.read_csv(DATA_FILE)

# Basic hygiene
if "submitted_at" in df.columns:
    df["submitted_at"] = pd.to_datetime(df["submitted_at"], errors="coerce")

# Sidebar Filters
st.sidebar.header("Filters")
cscs = sorted([c for c in df.get("csc", pd.Series([])).dropna().unique().tolist()])
default_cscs = cscs if cscs else []
csc_filter = st.sidebar.multiselect("CSC(s)", options=default_cscs, default=default_cscs)

date_min = df.get("submitted_at", pd.Series([pd.NaT])).min()
date_max = df.get("submitted_at", pd.Series([pd.NaT])).max()
if pd.notna(date_min) and pd.notna(date_max):
    start, end = st.sidebar.date_input("Date range", [date_min.date(), date_max.date()])
else:
    start = end = None

# Apply filters
mask = pd.Series([True] * len(df))
if csc_filter:
    mask &= df["csc"].isin(csc_filter)
if start and end and "submitted_at" in df.columns:
    # include whole day range
    day_mask = (df["submitted_at"] >= pd.Timestamp(start)) & (df["submitted_at"] < pd.Timestamp(end) + pd.Timedelta(days=1))
    mask &= day_mask

fdf = df[mask].copy()

st.subheader("Overview")
left, right = st.columns(2)
with left:
    st.metric("Total responses", int(len(fdf)))
with right:
    if "csc" in fdf.columns:
        st.metric("Unique CSCs", int(fdf["csc"].nunique()))

# CSC distribution
if "csc" in fdf.columns and not fdf["csc"].dropna().empty:
    st.subheader("Responses by CSC")
    csc_counts = fdf["csc"].value_counts().reset_index()
    csc_counts.columns = ["CSC", "Responses"]
    chart = alt.Chart(csc_counts).mark_bar().encode(
        x=alt.X("CSC:N", sort="-y"),
        y="Responses:Q",
        tooltip=["CSC","Responses"]
    )
    st.altair_chart(chart, use_container_width=True)

# Average ratings (columns that end with _overall or are sliders)
rating_cols = [c for c in fdf.columns if c.endswith("_overall") or c in ["ai_feedback"]]
if rating_cols:
    st.subheader("Average Ratings")
    avgs = fdf[rating_cols].mean(numeric_only=True).reset_index()
    avgs.columns = ["Question", "Average"]
    chart = alt.Chart(avgs).mark_bar().encode(
        x=alt.X("Question:N", sort="-y"),
        y=alt.Y("Average:Q"),
        tooltip=["Question","Average"]
    )
    st.altair_chart(chart, use_container_width=True)

# Skill choice counts per section
section_skill_cols = {
    "Title": "title_skill_choice",
    "FDR1/DLID": "fdr_skill_choice",
    "Driver Examiner": "de_skill_choice",
    "Compliance": "compliance_skill_choice",
    "Advanced": "advanced_skill_choice",
}
for section, col in section_skill_cols.items():
    if col in fdf.columns and not fdf[col].dropna().empty:
        st.subheader(f"{section} – Selected Skill Options")
        counts = fdf[col].value_counts().reset_index()
        counts.columns = ["Option", "Count"]
        chart = alt.Chart(counts).mark_bar().encode(
            x=alt.X("Option:N", sort="-y"),
            y="Count:Q",
            tooltip=["Option","Count"]
        )
        st.altair_chart(chart, use_container_width=True)

# Raw table (filtered)
st.subheader("Raw Responses (filtered)")
st.dataframe(fdf, use_container_width=True)

# Export buttons
st.subheader("Export")
st.download_button(
    label="Download filtered CSV",
    data=fdf.to_csv(index=False).encode("utf-8"),
    file_name="filtered_results.csv",
    mime="text/csv",
)
