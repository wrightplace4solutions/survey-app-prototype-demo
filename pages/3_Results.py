import os
from datetime import date as _date
from typing import cast
from io import BytesIO

import altair as alt
import pandas as pd
import streamlit as st

DATA_FILE = "Updated_Training_Feedback_Survey_Template.csv"


def render_results_dashboard() -> None:
    # Unified header with improved styling
    st.markdown(
        """
        <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #2F1B14, #8B2635); color: white; border-radius: 10px; margin-bottom: 30px;'>
            <h1 style='margin: 0; font-size: 2.5em;'>📊 Training Feedback Survey Results</h1>
            <h3 style='margin: 10px 0 0 0; font-weight: 300;'>Excellence Through Training - Data Analytics Dashboard</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not os.path.exists(DATA_FILE):
        st.error("📂 No survey data file found. Please ensure survey responses have been submitted.")
        st.info("💡 **Next Steps:** Navigate to the Survey page to submit your first response!")
        st.stop()

    df: pd.DataFrame = pd.read_csv(DATA_FILE)
    
    # Check if there's actual data beyond headers
    if len(df) == 0:
        st.warning("📋 Survey data file exists but contains no responses yet.")
        st.info("💡 **Next Steps:** Navigate to the Survey page to submit your first response!")
        st.stop()
    
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

    # Sidebar Filters with improved styling
    st.sidebar.markdown("### 🔍 Filters")
    st.sidebar.markdown("---")
    
    cscs = sorted(df.get("CSC", pd.Series([])).dropna().unique().tolist())
    csc_filter = st.sidebar.multiselect(
        "🏢 Select CSC(s)", 
        options=cscs, 
        default=cscs,
        help="Filter responses by Customer Service Center"
    )

    date_min = df.get("Timestamp", pd.Series([pd.NaT])).min()
    date_max = df.get("Timestamp", pd.Series([pd.NaT])).max()
    start_date, end_date = None, None
    if pd.notna(date_min) and pd.notna(date_max):
        st.sidebar.markdown("📅 **Date Range**")
        start_date = cast(_date, st.sidebar.date_input("From", date_min.date()))
        end_date = cast(_date, st.sidebar.date_input("To", date_max.date()))

    # Apply filters
    mask = pd.Series([True] * len(df))
    if csc_filter:
        mask &= df["CSC"].isin(csc_filter)
    if start_date and end_date and "Timestamp" in df.columns:
        mask &= (df["Timestamp"] >= pd.Timestamp(start_date)) & (
            df["Timestamp"] < pd.Timestamp(end_date) + pd.Timedelta(days=1)
        )

    fdf = df[mask].copy()
    
    if len(fdf) == 0:
        st.warning("🚫 No data matches the current filters. Please adjust your filter criteria.")
        st.stop()

    # Overview with improved metrics
    st.markdown("## 📈 Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📋 Total Responses", 
            value=f"{len(fdf):,}",
            help="Total number of survey responses matching current filters"
        )
    
    with col2:
        if "CSC" in fdf.columns:
            st.metric(
                label="🏢 Unique CSCs", 
                value=f"{fdf['CSC'].nunique():,}",
                help="Number of different Customer Service Centers represented"
            )
    
    with col3:
        if "Timestamp" in fdf.columns and not fdf["Timestamp"].isna().all():
            latest_date = fdf["Timestamp"].max()
            if pd.notna(latest_date):
                st.metric(
                    label="📅 Latest Response", 
                    value=latest_date.strftime("%m/%d/%Y"),
                    help="Date of the most recent survey submission"
                )
    
    with col4:
        rating_cols = [c for c in fdf.columns if "Confidence" in c or c == "AI_Survey_Experience_Rating"]
        if rating_cols:
            overall_avg = fdf[rating_cols].mean(numeric_only=True).mean()
            if pd.notna(overall_avg):
                st.metric(
                    label="⭐ Avg Rating", 
                    value=f"{overall_avg:.1f}",
                    help="Average rating across all confidence and experience metrics"
                )

    # CSC distribution with improved styling
    if "CSC" in fdf.columns and not fdf["CSC"].dropna().empty:
        st.markdown("## 🏢 Responses by Customer Service Center")
        csc_counts = fdf["CSC"].value_counts().reset_index()
        csc_counts.columns = ["CSC", "Responses"]
        
        chart = alt.Chart(csc_counts).mark_bar(
            color='#8B2635',
            cornerRadiusTopLeft=3,
            cornerRadiusTopRight=3
        ).encode(
            x=alt.X("CSC:N", sort="-y", title="Customer Service Center"),
            y=alt.Y("Responses:Q", title="Number of Responses", axis=alt.Axis(tickMinStep=0.5)),
            tooltip=["CSC", "Responses"],
        ).properties(
            height=400,
            title="Distribution of Survey Responses by CSC"
        )
        st.altair_chart(chart, use_container_width=True)

    # Average Ratings with improved visualization
    rating_cols = [c for c in fdf.columns if "Confidence" in c or c == "AI_Survey_Experience_Rating"]
    if rating_cols:
        st.markdown("## ⭐ Average Confidence Ratings")
        avgs = fdf[rating_cols].mean(numeric_only=True).reset_index()
        avgs.columns = ["Question", "Average"]
        # Clean up column names for better display
        avgs["Question"] = avgs["Question"].str.replace("_", " ").str.replace("Ai ", "AI ").str.replace("Fdr1 And Dlid", "FDRI/DLID").str.replace("Title Class", "Title Class").str.replace("Driver Examiner", "Driver examiner").str.replace("Advanced Vdh Fdr Ii Fdr Iii", "Advanced VDH FDRII")
        # Custom sort order with Title Class first
        sort_order = {"Title Class Confidence": 0, "FDRI/DLID Confidence": 1, "Driver examiner Confidence": 2, "Compliance Confidence": 3, "Advanced VDH FDRII Confidence": 4, "AI Survey Experience Rating": 5}
        avgs["sort_key"] = avgs["Question"].map(sort_order).fillna(999)
        avgs = avgs.sort_values("sort_key").drop("sort_key", axis=1)
        
        chart = alt.Chart(avgs).mark_bar(
            color='#2F1B14',
            cornerRadiusTopLeft=3,
            cornerRadiusTopRight=3
        ).encode(
            y=alt.Y("Question:N", sort="-x", title="Training Area"),
            x=alt.X("Average:Q", title="Average Rating", scale=alt.Scale(domain=[0, 5]), axis=alt.Axis(tickMinStep=0.5)),
            tooltip=["Question", alt.Tooltip("Average:Q", format=".2f")],
        ).properties(
            height=max(300, len(avgs) * 50),
            title="Average Confidence Ratings by Training Area"
        )
        st.altair_chart(chart, use_container_width=True)

    # Skills Breakdown with improved layout
    section_skill_cols = {
        "🎯 Title Class": "Title_Class_Skills_Important",
        "🚗 FDRI/DLID": "FDR1_and_DLID_Skills_Important",
        "👨‍💼 Driver Examiner": "Driver_Examiner_Skills_Important",
        "✅ Compliance": "Compliance_Skills_Important",
        "🚀 Advanced VDH FDRII": "Advanced_VDH_FDR_II_Skills_Important",
    }
    
    skills_data_exists = False
    for section, col in section_skill_cols.items():
        if col in fdf.columns and not fdf[col].dropna().empty:
            skills_data_exists = True
            break
    
    if skills_data_exists:
        st.markdown("## 🎯 Skills Priority Analysis")
        
        tabs = st.tabs(list(section_skill_cols.keys()))
        
        for i, (section, col) in enumerate(section_skill_cols.items()):
            with tabs[i]:
                if col in fdf.columns and not fdf[col].dropna().empty:
                    counts = fdf[col].value_counts().reset_index()
                    counts.columns = ["Option", "Count"]
                    
                    chart = alt.Chart(counts).mark_bar(
                        color='#8B2635',
                        cornerRadiusTopLeft=3,
                        cornerRadiusTopRight=3
                    ).encode(
                        y=alt.Y("Option:N", sort="-x", title="Skill/Topic"),
                        x=alt.X("Count:Q", title="Number of Responses", axis=alt.Axis(tickMinStep=0.5)),
                        tooltip=["Option", "Count"],
                    ).properties(
                        height=max(200, len(counts) * 30),
                        title=f"Most Important Skills - {section.replace('🎯 ', '').replace('🚗 ', '').replace('👨‍💼 ', '').replace('✅ ', '').replace('🚀 ', '')}"
                    )
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.info(f"No data available for {section} skills yet.")

    # Audit Issues Breakdown with improved presentation
    audit_cols = [c for c in fdf.columns if c.endswith("_Audit_Issues")]
    if audit_cols:
        st.markdown("## 🔍 Audit Issues Analysis")
        
        audit_sections = []
        for col in audit_cols:
            section_name = col.replace("_Audit_Issues", "").replace("_", " ").title()
            audit_sections.append(section_name)
        
        audit_tabs = st.tabs(audit_sections)
        
        for i, col in enumerate(audit_cols):
            with audit_tabs[i]:
                section_name = audit_sections[i]
                
                # Extract Yes/No responses
                audit_split = fdf[col].fillna("").apply(lambda x: x.split(" - ")[0].strip() if x else "No Response")
                counts = audit_split.value_counts().reset_index()
                counts.columns = ["Response", "Count"]

                if not counts.empty:
                    chart = alt.Chart(counts).mark_arc(
                        innerRadius=50,
                        outerRadius=100,
                    ).encode(
                        theta=alt.Theta("Count:Q"),
                        color=alt.Color("Response:N", 
                                      scale=alt.Scale(range=["#2F1B14", "#8B2635", "#D3D3D3"])),
                        tooltip=["Response", "Count"]
                    ).properties(
                        title=f"Audit Issues Distribution - {section_name}",
                        height=300
                    )
                    st.altair_chart(chart, use_container_width=True)

                    # Show detailed issues for Yes responses
                    yes_responses = audit_split.eq("Yes").sum()
                    if yes_responses > 0:
                        st.markdown(f"### 📝 Detailed Issues ({yes_responses} responses)")
                        issues = fdf[col].dropna().apply(lambda x: x.split(" - ", 1)[1] if " - " in x else "")
                        issues = issues[issues != ""].reset_index(drop=True)
                        if not issues.empty:
                            for idx, issue in enumerate(issues, 1):
                                st.markdown(f"**{idx}.** {issue}")
                    else:
                        st.success("✅ No audit issues reported for this section!")
                else:
                    st.info("No audit issue data available for this section.")

    # Enhanced Data Export Section
    st.markdown("## 📥 Data Export & Raw Responses")
    
    # Toggle for showing raw data
    show_raw_data = st.checkbox("🔍 Show Raw Response Data", help="Display the complete survey responses in table format")
    
    if show_raw_data:
        st.markdown("### 📋 Complete Survey Responses")
        st.dataframe(
            fdf.style.highlight_max(axis=0, color='lightgreen'),
            use_container_width=True,
            height=400
        )
    
    # Export buttons with improved styling
    st.markdown("### 💾 Download Options")
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = fdf.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📄 Download as CSV",
            data=csv_data,
            file_name=f"survey_results_filtered_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download filtered results as comma-separated values file",
            use_container_width=True
        )
    
    with col2:
        # Fix Excel export using BytesIO
        excel_buffer = BytesIO()
        fdf.to_excel(excel_buffer, index=False, engine="openpyxl")
        excel_data = excel_buffer.getvalue()
        
        st.download_button(
            label="📊 Download as Excel",
            data=excel_data,
            file_name=f"survey_results_filtered_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Download filtered results as Excel spreadsheet",
            use_container_width=True
        )
    
    # Summary statistics
    st.markdown("### 📊 Summary Statistics")
    if rating_cols:
        summary_stats = fdf[rating_cols].describe()
        st.dataframe(summary_stats.round(2), use_container_width=True)


if __name__ == "__main__":
    render_results_dashboard()
