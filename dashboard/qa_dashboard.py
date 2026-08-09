from pathlib import Path
import sys

import pandas as pd
from sklearn.metrics import (
    adjusted_rand_score,
    normalized_mutual_info_score,
)


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


from components.data_loader import (
    load_customer_data,
    load_model_metrics,
    load_segment_summary,
    load_strategy_mapping,
)


# ---------------------------------------------------------
# Expected final results
# ---------------------------------------------------------

EXPECTED = {
    "customers": 4338,
    "segments": 5,
    "high_value_customers": 1703,
    "kmeans_review_customers": 541,
    "gmm_ambiguous_customers": 259,
    "models_agree_customers": 3531,
}


HIGH_VALUE_SEGMENTS = [
    "High-Value Loyal Customers",
    "High-Value Large-Order Buyers",
]


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def check(name, actual, expected):
    status = "PASS" if actual == expected else "FAIL"

    print(
        f"{status:<5} | "
        f"{name:<35} | "
        f"Actual: {actual} | "
        f"Expected: {expected}"
    )

    return status == "PASS"


# ---------------------------------------------------------
# Load final data
# ---------------------------------------------------------

customers = load_customer_data()
model_metrics = load_model_metrics()
segment_summary = load_segment_summary()
strategy_mapping = load_strategy_mapping()


print("=" * 100)
print("RFM CUSTOMER SEGMENTATION DASHBOARD - FINAL QA")
print("=" * 100)


results = []


# ---------------------------------------------------------
# Main dataset tests
# ---------------------------------------------------------

results.append(
    check(
        "Customer count",
        customers["CustomerID"].nunique(),
        EXPECTED["customers"],
    )
)


results.append(
    check(
        "Duplicate Customer IDs",
        int(
            customers[
                "CustomerID"
            ].duplicated().sum()
        ),
        0,
    )
)


results.append(
    check(
        "Missing Customer IDs",
        int(
            customers[
                "CustomerID"
            ].isna().sum()
        ),
        0,
    )
)


results.append(
    check(
        "K-Means segment count",
        customers[
            "Segment_Name"
        ].nunique(),
        EXPECTED["segments"],
    )
)


# ---------------------------------------------------------
# High-value result
# ---------------------------------------------------------

high_value_mask = customers[
    "Segment_Name"
].isin(
    HIGH_VALUE_SEGMENTS
)


high_value_customers = customers.loc[
    high_value_mask,
    "CustomerID",
].nunique()


results.append(
    check(
        "High-value customers",
        high_value_customers,
        EXPECTED["high_value_customers"],
    )
)


high_value_customer_share = (
    high_value_customers
    / customers["CustomerID"].nunique()
    * 100
)


high_value_monetary_share = (
    customers.loc[
        high_value_mask,
        "Monetary",
    ].sum()
    / customers["Monetary"].sum()
    * 100
)


print(
    f"INFO  | High-value customer share        | "
    f"{high_value_customer_share:.2f}%"
)

print(
    f"INFO  | High-value Monetary share        | "
    f"{high_value_monetary_share:.2f}%"
)


# ---------------------------------------------------------
# Confidence results
# ---------------------------------------------------------

kmeans_review = int(
    customers[
        "Combined_Boundary_Flag"
    ].sum()
)


gmm_ambiguous = int(
    customers[
        "Combined_Ambiguous_Flag"
    ].sum()
)


models_agree = int(
    customers[
        "Models_Agree_After_Alignment"
    ].sum()
)


results.append(
    check(
        "K-Means review customers",
        kmeans_review,
        EXPECTED[
            "kmeans_review_customers"
        ],
    )
)


results.append(
    check(
        "GMM ambiguous customers",
        gmm_ambiguous,
        EXPECTED[
            "gmm_ambiguous_customers"
        ],
    )
)


results.append(
    check(
        "Aligned agreeing customers",
        models_agree,
        EXPECTED[
            "models_agree_customers"
        ],
    )
)


# ---------------------------------------------------------
# Cross-model metrics
# ---------------------------------------------------------

ari = adjusted_rand_score(
    customers[
        "Cluster"
    ].astype(int),
    customers[
        "GMM_Component"
    ].astype(int),
)


nmi = normalized_mutual_info_score(
    customers[
        "Cluster"
    ].astype(int),
    customers[
        "GMM_Component"
    ].astype(int),
)


agreement_pct = (
    models_agree
    / len(customers)
    * 100
)


print(
    f"INFO  | Cross-model ARI                  | "
    f"{ari:.4f}"
)

print(
    f"INFO  | Cross-model NMI                  | "
    f"{nmi:.4f}"
)

print(
    f"INFO  | Aligned agreement                | "
    f"{agreement_pct:.2f}%"
)


# ---------------------------------------------------------
# Supporting-table tests
# ---------------------------------------------------------

results.append(
    check(
        "Model metrics rows",
        len(model_metrics),
        8,
    )
)


results.append(
    check(
        "Segment summary rows",
        len(segment_summary),
        10,
    )
)


kmeans_strategy_rows = strategy_mapping[
    strategy_mapping[
        "Model"
    ] == "K-Means K=5"
]


results.append(
    check(
        "K-Means strategy rows",
        len(kmeans_strategy_rows),
        5,
    )
)


# ---------------------------------------------------------
# Final outcome
# ---------------------------------------------------------

print("=" * 100)


if all(results):

    print(
        "FINAL RESULT: PASS - "
        "Dashboard data and core analytical "
        "outputs passed all QA checks."
    )

else:

    print(
        "FINAL RESULT: FAIL - "
        "One or more dashboard checks failed."
    )

    raise SystemExit(1)


print("=" * 100)