from pathlib import Path

import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "Data" / "dashboard data"


CUSTOMER_DATA_FILE = (
    DATA_DIR / "final_customer_segmentation_dashboard_data.csv"
)

MODEL_METRICS_FILE = (
    DATA_DIR / "final_dashboard_model_metrics.csv"
)

SEGMENT_SUMMARY_FILE = (
    DATA_DIR / "final_dashboard_segment_summary.csv"
)

STRATEGY_MAPPING_FILE = (
    DATA_DIR / "final_dashboard_strategy_mapping.csv"
)


# ---------------------------------------------------------
# Required customer-level columns
# ---------------------------------------------------------

REQUIRED_CUSTOMER_COLUMNS = [
    "CustomerID",
    "Recency",
    "Frequency",
    "Monetary",
    "AverageOrderValue",
    "BasketSize",
    "ProductDiversity",
    "TotalQuantity",
    "Cluster",
    "Segment_Name",
    "Alternative_Cluster",
    "Alternative_Segment",
    "Silhouette_Value_KMeans",
    "Relative_Centroid_Margin",
    "Combined_Boundary_Flag",
    "Assignment_Confidence_Category",
    "GMM_Component",
    "Alternative_GMM_Component",
    "Maximum_Probability",
    "Second_Probability",
    "Probability_Margin",
    "Normalised_Entropy",
    "Silhouette_Value_GMM",
    "Combined_Ambiguous_Flag",
    "Membership_Confidence_Category",
    "Aligned_GMM_Cluster",
    "Models_Agree_After_Alignment",
    "Cross_Model_Uncertainty_Group",
    "GMM_Segment_Name",
    "GMM_Segment_Description",
    "Primary_Objective",
    "Recommended_Action",
    "Primary_KPI",
    "Operational_Priority",
    "Primary_Operational_Model",
    "Supporting_Analytical_Model",
]


# ---------------------------------------------------------
# Boolean conversion
# ---------------------------------------------------------

def convert_to_boolean(series: pd.Series) -> pd.Series:
    """
    Convert boolean-like text or numeric values into True/False.
    """

    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "yes"])
    )


# ---------------------------------------------------------
# Main customer-level dataset
# ---------------------------------------------------------

@st.cache_data(show_spinner=False)
def load_customer_data() -> pd.DataFrame:

    if not CUSTOMER_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Customer dashboard file not found: "
            f"{CUSTOMER_DATA_FILE}"
        )

    df = pd.read_csv(
        CUSTOMER_DATA_FILE,
        dtype={"CustomerID": "string"}
    )

    missing_columns = [
        column
        for column in REQUIRED_CUSTOMER_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "The customer dashboard dataset is missing "
            f"required columns: {missing_columns}"
        )

    # Keep customer identifier as text.
    df["CustomerID"] = (
        df["CustomerID"]
        .astype("string")
        .str.strip()
    )

    # Convert final analytical flags into true booleans.
    boolean_columns = [
        "Combined_Boundary_Flag",
        "Combined_Ambiguous_Flag",
        "Models_Agree_After_Alignment",
    ]

    for column in boolean_columns:
        df[column] = convert_to_boolean(df[column])

    # Explicitly mark cluster/component identifiers as integers.
    integer_columns = [
        "Cluster",
        "Alternative_Cluster",
        "GMM_Component",
        "Alternative_GMM_Component",
        "Aligned_GMM_Cluster",
    ]

    for column in integer_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).astype("Int64")

    return df


# ---------------------------------------------------------
# Model metrics
# ---------------------------------------------------------

@st.cache_data(show_spinner=False)
def load_model_metrics() -> pd.DataFrame:

    if not MODEL_METRICS_FILE.exists():
        raise FileNotFoundError(
            f"Model metrics file not found: "
            f"{MODEL_METRICS_FILE}"
        )

    return pd.read_csv(MODEL_METRICS_FILE)


# ---------------------------------------------------------
# Segment summary
# ---------------------------------------------------------

@st.cache_data(show_spinner=False)
def load_segment_summary() -> pd.DataFrame:

    if not SEGMENT_SUMMARY_FILE.exists():
        raise FileNotFoundError(
            f"Segment summary file not found: "
            f"{SEGMENT_SUMMARY_FILE}"
        )

    return pd.read_csv(SEGMENT_SUMMARY_FILE)


# ---------------------------------------------------------
# Strategy mapping
# ---------------------------------------------------------

@st.cache_data(show_spinner=False)
def load_strategy_mapping() -> pd.DataFrame:

    if not STRATEGY_MAPPING_FILE.exists():
        raise FileNotFoundError(
            f"Strategy mapping file not found: "
            f"{STRATEGY_MAPPING_FILE}"
        )

    return pd.read_csv(STRATEGY_MAPPING_FILE)


# ---------------------------------------------------------
# Load everything
# ---------------------------------------------------------

@st.cache_data(show_spinner=False)
def load_dashboard_data():

    customers = load_customer_data()
    model_metrics = load_model_metrics()
    segment_summary = load_segment_summary()
    strategy_mapping = load_strategy_mapping()

    return (
        customers,
        model_metrics,
        segment_summary,
        strategy_mapping,
    )