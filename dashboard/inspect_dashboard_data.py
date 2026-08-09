from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# Locate project folders
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "Data" / "dashboard data"


FILES = {
    "Customer Segmentation Data":
        DATA_DIR / "final_customer_segmentation_dashboard_data.csv",

    "Model Metrics":
        DATA_DIR / "final_dashboard_model_metrics.csv",

    "Segment Summary":
        DATA_DIR / "final_dashboard_segment_summary.csv",

    "Strategy Mapping":
        DATA_DIR / "final_dashboard_strategy_mapping.csv",
}


print("=" * 90)
print("RFM CUSTOMER SEGMENTATION - DASHBOARD DATA CHECK")
print("=" * 90)

print(f"\nProject root:\n{PROJECT_ROOT}")
print(f"\nDashboard data folder:\n{DATA_DIR}")


# ---------------------------------------------------------
# Check that every required file exists
# ---------------------------------------------------------

print("\n" + "=" * 90)
print("1. FILE CHECK")
print("=" * 90)

all_files_exist = True

for name, path in FILES.items():

    exists = path.exists()

    print(f"{name}: {'FOUND' if exists else 'MISSING'}")
    print(f"  {path}")

    if not exists:
        all_files_exist = False


if not all_files_exist:
    raise FileNotFoundError(
        "One or more dashboard files are missing. "
        "Fix the file paths before continuing."
    )


# ---------------------------------------------------------
# Load main customer dataset
# ---------------------------------------------------------

customer_file = FILES["Customer Segmentation Data"]

customers = pd.read_csv(
    customer_file,
    dtype={"CustomerID": "string"}
)


print("\n" + "=" * 90)
print("2. MAIN CUSTOMER DATASET")
print("=" * 90)

print(f"Rows: {customers.shape[0]:,}")
print(f"Columns: {customers.shape[1]:,}")

print("\nCOLUMN NAMES:")
for number, column in enumerate(customers.columns, start=1):
    print(f"{number:02d}. {column}")


# ---------------------------------------------------------
# Basic validation
# ---------------------------------------------------------

print("\n" + "=" * 90)
print("3. CUSTOMER DATA VALIDATION")
print("=" * 90)

print(
    "Unique Customer IDs:",
    f"{customers['CustomerID'].nunique():,}"
)

print(
    "Duplicate Customer IDs:",
    f"{customers['CustomerID'].duplicated().sum():,}"
)

print(
    "Missing Customer IDs:",
    f"{customers['CustomerID'].isna().sum():,}"
)


if "Segment_Name" in customers.columns:

    print("\nK-MEANS SEGMENTS:")

    segment_counts = (
        customers["Segment_Name"]
        .value_counts()
    )

    print(segment_counts.to_string())


if "Monetary" in customers.columns:

    total_monetary = customers["Monetary"].sum()

    print(
        "\nTotal Monetary Value:",
        f"£{total_monetary:,.2f}"
    )


# ---------------------------------------------------------
# Validate high-value business result
# ---------------------------------------------------------

high_value_segments = [
    "High-Value Loyal Customers",
    "High-Value Large-Order Buyers",
]


if {
    "Segment_Name",
    "Monetary",
    "CustomerID"
}.issubset(customers.columns):

    high_value_mask = customers["Segment_Name"].isin(
        high_value_segments
    )

    high_value_customers = (
        customers.loc[high_value_mask, "CustomerID"]
        .nunique()
    )

    high_value_customer_pct = (
        high_value_customers
        / customers["CustomerID"].nunique()
        * 100
    )

    high_value_monetary = (
        customers.loc[high_value_mask, "Monetary"]
        .sum()
    )

    high_value_monetary_pct = (
        high_value_monetary
        / customers["Monetary"].sum()
        * 100
    )

    print("\nHIGH-VALUE RESULT")

    print(
        "High-value customers:",
        f"{high_value_customers:,}"
    )

    print(
        "High-value customer share:",
        f"{high_value_customer_pct:.2f}%"
    )

    print(
        "High-value Monetary value:",
        f"£{high_value_monetary:,.2f}"
    )

    print(
        "High-value Monetary contribution:",
        f"{high_value_monetary_pct:.2f}%"
    )


# ---------------------------------------------------------
# Helper for boolean-like columns
# ---------------------------------------------------------

def to_boolean(series):

    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "yes"])
    )


# ---------------------------------------------------------
# K-Means boundary result
# ---------------------------------------------------------

if "Combined_Boundary_Flag" in customers.columns:

    boundary = to_boolean(
        customers["Combined_Boundary_Flag"]
    )

    print(
        "\nK-Means Review Group:",
        f"{boundary.sum():,} customers "
        f"({boundary.mean() * 100:.2f}%)"
    )


# ---------------------------------------------------------
# GMM ambiguity result
# ---------------------------------------------------------

if "Combined_Ambiguous_Flag" in customers.columns:

    ambiguous = to_boolean(
        customers["Combined_Ambiguous_Flag"]
    )

    print(
        "GMM Ambiguous Membership:",
        f"{ambiguous.sum():,} customers "
        f"({ambiguous.mean() * 100:.2f}%)"
    )


# ---------------------------------------------------------
# Cross-model agreement
# ---------------------------------------------------------

if "Models_Agree_After_Alignment" in customers.columns:

    agreement = to_boolean(
        customers["Models_Agree_After_Alignment"]
    )

    print(
        "Aligned K-Means/GMM Agreement:",
        f"{agreement.sum():,} customers "
        f"({agreement.mean() * 100:.2f}%)"
    )


# ---------------------------------------------------------
# Inspect supporting CSV files
# ---------------------------------------------------------

print("\n" + "=" * 90)
print("4. SUPPORTING DATASETS")
print("=" * 90)


for name in [
    "Model Metrics",
    "Segment Summary",
    "Strategy Mapping",
]:

    path = FILES[name]

    df = pd.read_csv(path)

    print("\n" + "-" * 90)
    print(name.upper())
    print("-" * 90)

    print(
        f"Shape: {df.shape[0]} rows × "
        f"{df.shape[1]} columns"
    )

    print("\nColumns:")

    for number, column in enumerate(
        df.columns,
        start=1
    ):
        print(f"{number:02d}. {column}")

    print("\nContents:")
    print(df.to_string(index=False))


print("\n" + "=" * 90)
print("DATA CHECK COMPLETE")
print("=" * 90)