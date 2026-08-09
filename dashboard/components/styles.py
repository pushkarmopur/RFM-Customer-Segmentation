import streamlit as st


SEGMENT_COLORS = {
    "Dormant Occasional Customers": "#64748B",
    "Active Regular Customers": "#2563EB",
    "High-Value Loyal Customers": "#059669",
    "Low-Value Infrequent Customers": "#D97706",
    "High-Value Large-Order Buyers": "#7C3AED",
}


GMM_SEGMENT_COLORS = {
    "Dormant Occasional Customers": "#64748B",
    "Active Regular Customers": "#2563EB",
    "High-Value Loyal Customers": "#059669",
    "Low-Value Infrequent Customers": "#D97706",
    "Elite High-Value Customers": "#9333EA",
}


PRIORITY_COLORS = {
    "Low": "#DCFCE7",
    "Medium": "#FEF3C7",
    "High": "#FFEDD5",
    "Very High": "#FEE2E2",
    "Critical": "#FECACA",
}


def apply_global_styles():

    st.markdown(
        """
        <style>

        /* Main page */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            max-width: 1500px;
        }

        /* Main heading */
        h1 {
            font-weight: 750;
            letter-spacing: -0.03em;
        }

        /* Section headings */
        h2, h3 {
            font-weight: 650;
        }

        /* Metric cards */
        [data-testid="stMetric"] {
            background: white;
            border: 1px solid #E5E7EB;
            padding: 1rem;
            border-radius: 14px;
            box-shadow:
                0 1px 2px rgba(0, 0, 0, 0.04);
        }

        [data-testid="stMetricLabel"] {
            font-weight: 600;
        }

        /* Dataframes */
        [data-testid="stDataFrame"] {
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            overflow: hidden;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            border-right: 1px solid #E5E7EB;
        }

        /* Captions */
        .small-note {
            color: #64748B;
            font-size: 0.86rem;
            line-height: 1.45;
        }

        /* Information panels */
        .info-panel {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 1.1rem 1.2rem;
            margin-bottom: 1rem;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(
    title: str,
    subtitle: str
):

    st.title(title)

    st.markdown(
        f"""
        <div class="small-note">
            {subtitle}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")