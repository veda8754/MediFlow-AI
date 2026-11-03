from pathlib import Path
from modules.demo_mode import get_demo_analysis
from modules.followup import get_followup_recommendations
from modules.analytics import (
    get_category_chart,
    get_sentiment_chart,
    get_priority_chart
)
import streamlit as st
import pandas as pd

from database.db import (
    create_table,
    get_all_enquiries,
    update_enquiry,
    update_status
)

from modules.classifier import classify_enquiry

from modules.analytics import (
    get_category_chart,
    get_sentiment_chart,
    get_priority_chart
)


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="MediFlow AI",
    page_icon="🏥",
    layout="wide"
)
import streamlit as st
import pandas as pd
from pathlib import Path



# Page Configuration
st.set_page_config(
    page_title="MediFlow AI",
    page_icon="🏥",
    layout="wide"
)

from pathlib import Path

def load_css():

    css_path = Path(__file__).parent / "assets" / "style.css"

    if css_path.exists():

        with open(css_path, encoding="utf-8") as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

    else:

        st.warning(f"CSS file not found: {css_path}")


load_css()






# ==========================================
# 2. DATABASE INITIALIZATION
# ==========================================

create_table()


# ==========================================
# 3. APPLICATION HEADER
# ==========================================

st.title("🏥 MediFlow AI")

st.caption(
    "AI-Powered Healthcare Enquiry Management System"
)

st.divider()


# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================

with st.sidebar:

    # Application Branding

    st.markdown(
        """
        <div style="text-align:center; padding:15px 5px;">
            <h1 style="color:#2E86C1;">🏥 MediFlow AI</h1>
            <p style="font-size:13px; color:gray;">
                Smart Healthcare Enquiry Management
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("Navigation")

    page = st.radio(
        "Go to",
        [
            "Dashboard",
            "All Enquiries",
            "AI Enquiry Analyzer"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    # Project Information

    st.markdown("### 💡 About MediFlow")

    st.caption(
        "An AI-powered healthcare enquiry management "
        "and automation system."
    )

    st.divider()

    st.caption("Built with Python | Streamlit | Gemini AI")


# ==========================================
# 5. LOAD DATABASE RECORDS
# ==========================================

records = get_all_enquiries()

df = pd.DataFrame(records)


# ==========================================
# 6. DASHBOARD
# ==========================================

if page == "Dashboard":

    if df.empty:

        st.info("No enquiries available.")

    else:

        # Calculate metrics

        total = len(df)

        open_count = len(
            df[df["status"] == "Open"]
        )

        high_priority = len(
            df[df["priority"] == "High"]
        )

        followups = len(
            df[df["requires_followup"] == 1]
        )

        resolved_count = len(
            df[df["status"] == "Resolved"]
        )

        # KPI Cards

        st.subheader("📈 Clinic Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Enquiries",
            total
        )

        col2.metric(
            "Open Enquiries",
            open_count
        )

        col3.metric(
            "High Priority",
            high_priority
        )

        col4.metric(
            "Follow-ups Required",
            followups
        )

        st.divider()

        # Recent Enquiries

        st.subheader("📋 Recent Enquiries")

        recent_df = df[
            [
                "enquiry_id",
                "patient_name",
                "category",
                "priority",
                "status"
            ]
        ].tail(10)

        st.dataframe(
            recent_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # Analytics Section

        st.subheader("📊 Enquiry Analytics")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:

            st.plotly_chart(
                get_category_chart(df),
                use_container_width=True
            )

        with chart_col2:

            st.plotly_chart(
                get_sentiment_chart(df),
                use_container_width=True
            )

        st.plotly_chart(
            get_priority_chart(df),
            use_container_width=True
        )

        st.divider()

        # Clinic Performance

        st.subheader("🏥 Enquiry Resolution Overview")

        resolved_percentage = (
            (resolved_count / total) * 100
            if total > 0 else 0
        )

        st.metric(
            "Resolved Enquiries",
            f"{resolved_count} / {total}",
            f"{resolved_percentage:.1f}% resolved"
        )

        st.progress(
            resolved_percentage / 100
        )

        st.caption(
            "Percentage of enquiries marked as resolved."
        )

        st.divider()

        # Follow-up Recommendations

        st.subheader("📌 Follow-up Recommendations")

        followup_df = get_followup_recommendations(df)

        if not followup_df.empty:

            st.dataframe(
                followup_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "No pending follow-ups. Great job!"
            )

        # ==================================
        # ADVANCED ANALYTICS
        # ==================================

        st.header("📈 Advanced Analytics")


        # Category chart

        st.subheader("Enquiry Category Analysis")

        st.plotly_chart(
    get_category_chart(df),
    use_container_width=True,
    key="category_chart"
)


        # Sentiment and priority charts

        col1, col2 = st.columns(2)


        with col1:

            st.subheader("Sentiment Distribution")

            st.plotly_chart(
    get_sentiment_chart(df),
    use_container_width=True,
    key="sentiment_chart"
)


        with col2:

            st.subheader("Priority Distribution")

            st.plotly_chart(
    get_priority_chart(df),
    use_container_width=True,
    key="priority_chart"
)
    st.divider()

    st.subheader("📌 Follow-up Recommendations")

    followup_df = get_followup_recommendations(df)

    if not followup_df.empty:

        st.write(
            "These enquiries may require additional attention."
        )

        st.dataframe(
            followup_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.success("No pending follow-ups. Great job!")


# ==========================================
# 7. ALL ENQUIRIES
# ==========================================
elif page == "All Enquiries":

    st.title("📋 All Patient Enquiries")

    st.write("Search, filter and manage clinic enquiries.")

    # Search
    search_query = st.text_input(
        "🔍 Search by patient name or enquiry",
        placeholder="Enter patient name or keyword..."
    )

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Open", "In Progress", "Resolved"]
        )

    with col2:
        priority_filter = st.selectbox(
            "Filter by Priority",
            ["All", "High", "Medium", "Low", "Not Analysed"]
        )

    with col3:
        category_options = ["All"] + sorted(
            df["category"].dropna().unique().tolist()
        )

        category_filter = st.selectbox(
            "Filter by Category",
            category_options
        )

    # Create filtered dataframe
    filtered_df = df.copy()

    # Apply search
    if search_query:
        filtered_df = filtered_df[
            filtered_df["patient_name"].str.contains(
                search_query, case=False, na=False
            )
            |
            filtered_df["enquiry_text"].str.contains(
                search_query, case=False, na=False
            )
        ]

    # Apply status filter
    if status_filter != "All":
        filtered_df = filtered_df[
            filtered_df["status"] == status_filter
        ]

    # Apply priority filter
    if priority_filter == "Not Analysed":
        filtered_df = filtered_df[
            filtered_df["priority"].isna()
            |
            (filtered_df["priority"] == "")
        ]
    elif priority_filter != "All":
        filtered_df = filtered_df[
            filtered_df["priority"] == priority_filter
        ]

    # Apply category filter
    if category_filter != "All":
        filtered_df = filtered_df[
            filtered_df["category"] == category_filter
        ]

    # Display results
    st.subheader(f"Search Results: {len(filtered_df)} enquiries")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )
    st.divider()

    st.subheader("📥 Export Enquiries")

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Enquiries (CSV)",
        data=csv_data,
        file_name="mediflow_filtered_enquiries.csv",
        mime="text/csv"
    )
    all_csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download All Enquiries (CSV)",
        data=all_csv_data,
        file_name="mediflow_all_enquiries.csv",
        mime="text/csv"
    )

    st.divider()

    # Update enquiry status
    st.subheader("✏️ Update Enquiry Status")

    if not filtered_df.empty:

        selected_id = st.selectbox(
            "Select Enquiry ID",
            filtered_df["enquiry_id"].tolist()
        )

        new_status = st.selectbox(
            "Select New Status",
            ["Open", "In Progress", "Resolved"]
        )

        if st.button("Update Status"):

            update_status(selected_id, new_status)

            st.success("Enquiry status updated successfully!")

            st.rerun()

    else:
        st.info("No enquiries match your selected filters.")



# ==========================================
# 8. AI ENQUIRY ANALYZER
# ==========================================

elif page == "AI Enquiry Analyzer":

    st.header("🤖 AI Enquiry Analyzer")

    st.write(
        "Analyse healthcare enquiries using Google Gemini AI."
    )
    analysis_mode = st.radio(
        "Choose Analysis Mode",
        ["Demo Mode (No API)", "Gemini AI"],
        horizontal=True
    )

    if df.empty:

        st.warning("No enquiries available.")

    else:

        # Select enquiry
        enquiry_id = st.selectbox(
            "Select Enquiry",
            df["enquiry_id"].tolist()
        )

        selected = df[
            df["enquiry_id"] == enquiry_id
        ].iloc[0]

        # Patient information
        st.subheader("Patient Information")

        st.write("**Patient:**", selected["patient_name"])

        st.info(selected["enquiry_text"])

        # Run combined AI analysis
    if st.button("Analyse Enquiry"):

        try:

                with st.spinner("Analysing enquiry..."):

                    if analysis_mode == "Gemini AI":

                        result = classify_enquiry(
                            selected["enquiry_text"]
                        )

                    else:

                        result = get_demo_analysis(
                            selected["enquiry_text"]
                        )

                classification = {
                    "category": result["category"],
                    "sentiment": result["sentiment"],
                    "priority": result["priority"],
                    "summary": result["summary"],
                    "requires_followup": result["requires_followup"]
                }

                response = result["suggested_response"]

                update_enquiry(
                    enquiry_id,
                    classification,
                    response
                )

                st.session_state["classification"] = classification
                st.session_state["response"] = response
                st.session_state["selected_id"] = enquiry_id
                st.session_state["analysis_id"] = enquiry_id
                st.session_state["analysis_mode"] = analysis_mode

                st.success("Analysis completed successfully!")

        except Exception as e:

                st.error(
                    f"Analysis failed: {type(e).__name__}: {e}"
                )
        
                # Display analysis results
                        # Display analysis results

        if (
            st.session_state.get("selected_id") == enquiry_id
            and "classification" in st.session_state
        ):

            classification = st.session_state["classification"]

            st.divider()

            st.subheader("📊 AI Classification")

            st.caption(
                f"Analysis Mode: {st.session_state.get('analysis_mode', 'Unknown')}"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Category",
                classification["category"]
            )

            col2.metric(
                "Sentiment",
                classification["sentiment"]
            )

            col3.metric(
                "Priority",
                classification["priority"]
            )

            st.write(
                "**Summary:**",
                classification["summary"]
            )

            st.write(
                "**Follow-up Required:**",
                classification["requires_followup"]
            )

            st.divider()

            # Display suggested response

            if (
                st.session_state.get("analysis_id") == enquiry_id
                and "response" in st.session_state
            ):

                st.subheader("✉️ Suggested Response")

                st.text_area(
                    "Suggested Response",
                    st.session_state["response"],
                    height=180
                )

                st.warning(
                    "This is an AI-generated draft. "
                    "Clinic staff must review and approve it before sending. "
                    "No patient message is sent automatically."
                )
                    # Display suggested response
                if st.session_state.get("analysis_id") == enquiry_id:
        
                        st.subheader("✉️ AI Generated Response")
        
                        st.text_area(
    "Suggested Response",
    st.session_state["response"],
    height=180,
    key="ai_suggested_response"
)
             
        
                        st.warning(
                            "This is an AI-generated draft. "
                            "Clinic staff must review and approve it before sending. "
                            "No patient message is sent automatically."
                        )