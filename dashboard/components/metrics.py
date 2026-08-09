import pandas as pd


HIGH_VALUE_SEGMENTS = [
    "High-Value Loyal Customers",
    "High-Value Large-Order Buyers",
]


def total_customers(df: pd.DataFrame) -> int:
    return int(df["CustomerID"].nunique())


def total_monetary(df: pd.DataFrame) -> float:
    return float(df["Monetary"].sum())


def total_segments(df: pd.DataFrame) -> int:
    return int(df["Segment_Name"].nunique())


def average_monetary_per_customer(
    df: pd.DataFrame
) -> float:

    customers = total_customers(df)

    if customers == 0:
        return 0.0

    return total_monetary(df) / customers


def median_customer_monetary(
    df: pd.DataFrame
) -> float:

    if df.empty:
        return 0.0

    return float(df["Monetary"].median())


def high_value_customers(
    df: pd.DataFrame
) -> int:

    mask = df["Segment_Name"].isin(
        HIGH_VALUE_SEGMENTS
    )

    return int(
        df.loc[mask, "CustomerID"].nunique()
    )


def high_value_customer_percentage(
    df: pd.DataFrame
) -> float:

    customers = total_customers(df)

    if customers == 0:
        return 0.0

    return (
        high_value_customers(df)
        / customers
        * 100
    )


def high_value_monetary(
    df: pd.DataFrame
) -> float:

    mask = df["Segment_Name"].isin(
        HIGH_VALUE_SEGMENTS
    )

    return float(
        df.loc[mask, "Monetary"].sum()
    )


def high_value_monetary_percentage(
    df: pd.DataFrame
) -> float:

    monetary = total_monetary(df)

    if monetary == 0:
        return 0.0

    return (
        high_value_monetary(df)
        / monetary
        * 100
    )


def kmeans_review_customers(
    df: pd.DataFrame
) -> int:

    return int(
        df["Combined_Boundary_Flag"].sum()
    )


def kmeans_review_percentage(
    df: pd.DataFrame
) -> float:

    customers = total_customers(df)

    if customers == 0:
        return 0.0

    return (
        kmeans_review_customers(df)
        / customers
        * 100
    )


def gmm_ambiguous_customers(
    df: pd.DataFrame
) -> int:

    return int(
        df["Combined_Ambiguous_Flag"].sum()
    )


def gmm_ambiguous_percentage(
    df: pd.DataFrame
) -> float:

    customers = total_customers(df)

    if customers == 0:
        return 0.0

    return (
        gmm_ambiguous_customers(df)
        / customers
        * 100
    )


def agreement_customers(
    df: pd.DataFrame
) -> int:

    return int(
        df["Models_Agree_After_Alignment"].sum()
    )


def agreement_percentage(
    df: pd.DataFrame
) -> float:

    customers = total_customers(df)

    if customers == 0:
        return 0.0

    return (
        agreement_customers(df)
        / customers
        * 100
    )


def both_models_flagged_customers(
    df: pd.DataFrame
) -> int:

    mask = (
        df["Combined_Boundary_Flag"]
        &
        df["Combined_Ambiguous_Flag"]
    )

    return int(mask.sum())


def both_models_flagged_percentage(
    df: pd.DataFrame
) -> float:

    customers = total_customers(df)

    if customers == 0:
        return 0.0

    return (
        both_models_flagged_customers(df)
        / customers
        * 100
    )


def mean_gmm_max_probability(
    df: pd.DataFrame
) -> float:

    if df.empty:
        return 0.0

    return float(
        df["Maximum_Probability"].mean()
    )


def segment_customer_share(
    full_df: pd.DataFrame,
    selected_df: pd.DataFrame
) -> float:

    full_count = total_customers(full_df)

    if full_count == 0:
        return 0.0

    return (
        total_customers(selected_df)
        / full_count
        * 100
    )


def segment_monetary_share(
    full_df: pd.DataFrame,
    selected_df: pd.DataFrame
) -> float:

    full_value = total_monetary(full_df)

    if full_value == 0:
        return 0.0

    return (
        total_monetary(selected_df)
        / full_value
        * 100
    )


def value_concentration_index(
    customer_share: float,
    monetary_share: float
) -> float:

    if customer_share == 0:
        return 0.0

    return monetary_share / customer_share


def currency(value: float) -> str:
    return f"£{value:,.2f}"


def compact_currency(value: float) -> str:

    absolute = abs(value)

    if absolute >= 1_000_000:
        return f"£{value / 1_000_000:.2f}M"

    if absolute >= 1_000:
        return f"£{value / 1_000:.1f}K"

    return f"£{value:,.2f}"


def percentage(value: float) -> str:
    return f"{value:.2f}%"