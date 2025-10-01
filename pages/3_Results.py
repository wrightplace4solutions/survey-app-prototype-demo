import os
from datetime import date as _date
from typing import cast
from io import BytesIO

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Training Feedback Survey Results", layout="wide")

DATA_FILE = "Updated_Training_Feedback_Survey_Template.csv"


def render_results_dashboard() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(135deg, #2F1B14 0%, #8B2635 50%, #2F1B14 100%);
                min-height: 100vh;
            }

            section[data-testid="stSidebar"] {
                background: rgba(30, 15, 20, 0.85);
                backdrop-filter: blur(6px);
            }

            section[data-testid="stSidebar"] * {
                color: #F8F6F0 !important;
            }

            .main-header {
                background: linear-gradient(135deg, #2F1B14 0%, #8B2635 50%, #2F1B14 100%);
                background-size: 200% 200%;
                animation: gradientShift 4s ease infinite;
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                margin: 2rem 1rem;
                box-shadow: 
                    0 0 20px rgba(139, 38, 53, 0.4),
                    0 0 40px rgba(47, 27, 20, 0.3),
                    0 0 60px rgba(139, 38, 53, 0.2),
                    0 8px 32px rgba(0,0,0,0.2);
                border: 1px solid rgba(255,255,255,0.3);
                position: relative;
                overflow: hidden;
            }

            .main-header::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                animation: rotate 8s linear infinite;
                pointer-events: none;
            }

            .main-header h1 {
                color: white;
                margin: 0;
                font-size: 2.5em;
                text-shadow: 
                    0 0 10px rgba(255,255,255,0.5),
                    2px 2px 4px rgba(0,0,0,0.7);
                position: relative;
                z-index: 2;
            }

            .main-header h3 {
                color: rgba(255,255,255,0.95);
                margin: 10px 0 0 0;
                font-weight: 300;
                text-shadow: 
                    1px 1px 2px rgba(0,0,0,0.5);
                position: relative;
                z-index: 2;
            }

            .gradient-header {
                background: linear-gradient(135deg, #8B2635 0%, #2F1B14 50%, #8B2635 100%);
                background-size: 200% 200%;
                animation: gradientText 3s ease infinite;
                color: white;
                text-align: center;
                font-weight: 700;
                font-size: 1.3em;
                margin: 2rem 1.5rem 1rem 1.5rem;
                padding: 1.2rem 1.5rem;
                border-radius: 12px;
                box-shadow: 
                    0 0 15px rgba(139, 38, 53, 0.3),
                    0 0 30px rgba(47, 27, 20, 0.2),
                    0 4px 15px rgba(0,0,0,0.2);
                border: 1px solid rgba(255,255,255,0.2);
                text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            }

            .sub-header {
                color: #FDF6F0;
                font-weight: 600;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
                margin: 1.5rem 0 0.5rem 0;
            }

            div[data-testid="metric-container"] {
                background: rgba(255,255,255,0.08);
                border-radius: 12px;
                padding: 1rem;
                box-shadow: 0 6px 20px rgba(0,0,0,0.25);
                border: 1px solid rgba(255,255,255,0.15);
            }

            div[data-testid="metric-container"] * {
                color: #FFFFFF !important;
            }

            div[data-testid="stDataFrame"] div {
                color: #1E1E1E !important;
            }

            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            @keyframes gradientText {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            @keyframes rotate {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="main-header">
            <h1>📊 Training Feedback Survey Results</h1>
            <h3>Excellence Through Training - Data Analytics Dashboard</h3>
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
    st.markdown('<div class="gradient-header">📈 Overview</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="gradient-header">🏢 Responses by Customer Service Center</div>', unsafe_allow_html=True)
        csc_counts = fdf["CSC"].value_counts().reset_index()
        csc_counts.columns = ["CSC", "Responses"]
        
        chart = alt.Chart(csc_counts).mark_bar(
            color='#8B2635',
            cornerRadiusTopLeft=3,
            cornerRadiusTopRight=3
        ).encode(
            x=alt.X("CSC:N", sort="-y", title="Customer Service Center"),
            y=alt.Y("Responses:Q", title="Number of Responses", axis=alt.Axis(tickMinStep=1)),
            tooltip=["CSC", "Responses"],
        ).properties(
            height=400,
            title="Distribution of Survey Responses by CSC"
        )
        st.altair_chart(chart, use_container_width=True)

    # Average Ratings with improved visualization
    rating_cols = [c for c in fdf.columns if "Confidence" in c or c == "AI_Survey_Experience_Rating"]
    if rating_cols:
        st.markdown('<div class="gradient-header">⭐ Average Confidence Ratings</div>', unsafe_allow_html=True)
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
            x=alt.X("Average:Q", title="Average Rating", scale=alt.Scale(domain=[0, 5]), axis=alt.Axis(tickMinStep=1)),
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
        "🚀 Advanced VDH FDRII": "Advanced_VDH_FDR_II_FDR_III_Skills_Important",
    }
    
    skills_data_exists = False
    for section, col in section_skill_cols.items():
        if col in fdf.columns and not fdf[col].dropna().empty:
            skills_data_exists = True
            break
    
    if skills_data_exists:
        st.markdown('<div class="gradient-header">🎯 Skills Priority Analysis</div>', unsafe_allow_html=True)
        
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
                        x=alt.X("Count:Q", title="Number of Responses", axis=alt.Axis(tickMinStep=1)),
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
        st.markdown('<div class="gradient-header">🔍 Audit Issues Analysis</div>', unsafe_allow_html=True)
        
        audit_sections = []
        for col in audit_cols:
            section_name = col.replace("_Audit_Issues", "").replace("_", " ")
            # Standardize the section names to match Skills Priority Analysis
            if "Title Class" in section_name:
                section_name = "Title Class"
            elif "FDR1 and DLID" in section_name or "Fdr1 And Dlid" in section_name:
                section_name = "FDRI/DLID"
            elif "Driver Examiner" in section_name:
                section_name = "Driver Examiner"
            elif "Compliance" in section_name:
                section_name = "Compliance"
            elif "Advanced" in section_name or "FDR_II_FDR_III" in section_name:
                section_name = "Advanced VDH FDRII"
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
    st.markdown('<div class="gradient-header">📥 Data Export & Raw Responses</div>', unsafe_allow_html=True)
    
    # Toggle for showing raw data
    show_raw_data = st.checkbox("🔍 Show Raw Response Data", help="Display the complete survey responses in table format")
    
    if show_raw_data:
        st.markdown('<div class="sub-header">📋 Complete Survey Responses</div>', unsafe_allow_html=True)
        st.dataframe(
            fdf.style.highlight_max(axis=0, color='lightgreen'),
            use_container_width=True,
            height=400
        )
    
    # Export buttons with improved styling
    st.markdown('<div class="sub-header">💾 Download Options</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="sub-header">📊 Summary Statistics</div>', unsafe_allow_html=True)
    if rating_cols:
        summary_stats = fdf[rating_cols].describe()
        st.dataframe(summary_stats.round(2), use_container_width=True)


if __name__ == "__main__":
    render_results_dashboard()
