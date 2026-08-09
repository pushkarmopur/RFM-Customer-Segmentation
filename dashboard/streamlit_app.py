from pathlib import Path
import sys

import streamlit as st


# ---------------------------------------------------------
# Make dashboard modules importable
# ---------------------------------------------------------

APP_DIR = Path(__file__).resolve().parent

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


from components.data_loader import load_dashboard_data
from components.styles import apply_global_styles


# ---------------------------------------------------------
# Streamlit page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="RFM Customer Segmentation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


apply_global_styles()


# ---------------------------------------------------------
# Validate/load shared data once
# ---------------------------------------------------------

try:

    (
        customers,
        model_metrics,
        segment_summary,
        strategy_mapping,
    ) = load_dashboard_data()

except Exception as error:

    st.error(
        "The dashboard data could not be loaded."
    )

    st.exception(error)

    st.stop()


# ---------------------------------------------------------
# Navigation
# ---------------------------------------------------------

pages = {

    "Overview": [

        st.Page(
            APP_DIR
            / "pages"
            / "executive_overview.py",
            title="Executive Overview",
            icon="🏠",
            default=True,
        ),

    ],

    "Customer Analysis": [

        st.Page(
            APP_DIR
            / "pages"
            / "segment_profiles.py",
            title="Customer Segment Profiles",
            icon="👥",
        ),

        st.Page(
            APP_DIR
            / "pages"
            / "customer_value.py",
            title="Customer Value & Revenue",
            icon="💷",
        ),

        st.Page(
            APP_DIR
            / "pages"
            / "confidence_explorer.py",
            title="Customer Confidence & Explorer",
            icon="🔎",
        ),

    ],

    "Model Evaluation": [

        st.Page(
            APP_DIR
            / "pages"
            / "model_comparison.py",
            title="Model Comparison",
            icon="📈",
        ),

    ],

    "Decision Support": [

        st.Page(
            APP_DIR
            / "pages"
            / "strategy_decision_support.py",
            title="Strategy & Decision Support",
            icon="🎯",
        ),

    ],

}


# ---------------------------------------------------------
# Sidebar project information
# ---------------------------------------------------------

with st.sidebar:

    st.markdown(
        "## RFM Customer Segmentation"
    )

    st.caption(
        "MSc dissertation decision-support artefact"
    )

    st.divider()

    st.markdown(
        """
        **Dataset**  
        UCI Online Retail

        **Customers**  
        4,338

        **Clustering features**  
        7

        **Primary operational model**  
        K-Means K=5

        **Supporting analytical model**  
        GMM C5 Spherical
        """
    )

    st.divider()

    st.caption(
        "Pushkar Mopur · Atlantic Technological "
        "University · 2026"
    )


# ---------------------------------------------------------
# Run selected page
# ---------------------------------------------------------

navigation = st.navigation(
    pages,
    position="sidebar",
)

navigation.run()