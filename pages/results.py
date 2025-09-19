import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="DMV Training Survey Results", layout="wide")
st.title("📊 DMV Training Survey Results Dashboard")

# Load data
data_file = "survey_data.csv"
if not os.path.exists(data_file):
    st.warning("No survey data available yet. Submit at least one survey to view results.")
else:
    df = pd.read_csv(data_file)

    # Sidebar filters
    st.sidebar.header("Filters")
    user_filter = st.sidebar.selectbox("Filter by User", ["All"] + sorted(df["Your Name *"].dropna().unique().tolist()))
    question_filter = st.sidebar.selectbox("Select Question", df.columns.drop(["Your Name *", "Your Role/Title *", "Your Email (optional)"]))
    chart_type = st.sidebar.radio("Chart Type", ["Bar", "Pie", "Table"])

    # Apply filter
    if user_filter != "All":
        df = df[df["Your Name *"] == user_filter]

    # Show summary stats
    st.subheader("Summary Statistics")
    col1, col2, col3 = st.columns(3)

    if pd.api.types.is_numeric_dtype(df[question_filter]):
        col1.metric("Total Responses", len(df[question_filter].dropna()))
        col2.metric("Average", round(df[question_filter].mean(), 2))
        col3.metric("Median", round(df[question_filter].median(), 2))
    else:
        counts = df[question_filter].value_counts(normalize=True) * 100
        if not counts.empty:
            col1.metric("Top Response", counts.index[0])
            col2.metric("Top %", f"{counts.iloc[0]:.1f}%")
            col3.metric("Total Responses", len(df[question_filter].dropna()))

    # Chart or Table
    st.subheader("Visualization")
    if chart_type == "Bar":
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(question_filter, type="ordinal"),
            y="count()",
            tooltip=[question_filter, "count()"]
        ).interactive()
        st.altair_chart(chart, use_container_width=True)

    elif chart_type == "Pie":
        counts = df[question_filter].value_counts().reset_index()
        counts.columns = ["Option", "Count"]
        chart = alt.Chart(counts).mark_arc().encode(
            theta="Count",
            color="Option",
            tooltip=["Option", "Count"]
        )
        st.altair_chart(chart, use_container_width=True)

    elif chart_type == "Table":
        st.dataframe(df[[question_filter]])

    # Export button
    st.subheader("Export Data")
    st.download_button(
        label="Download Filtered Data as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_results.csv",
        mime="text/csv"
    )
