import pandas as pd
import streamlit as st

from components.data_loader import (
    load_dashboard_data,
)

from components.metrics import (
    total_customers,
    segment_customer_share,
    segment_monetary_share,
    value_concentration_index,
    percentage,
    currency,
)

from components.charts import (
    SEGMENT_ORDER,
    PROFILE_FEATURES,
    segment_profile_index_chart,
    segment_median_heatmap,
)

from components.styles import (
    page_header,
)


# ---------------------------------------------------------
# Segment descriptions
# ---------------------------------------------------------

SEGMENT_DESCRIPTIONS = {

    "Dormant Occasional Customers":
        (
            "Customers with a long period since "
            "their most recent purchase, low repeat "
            "purchasing and limited total monetary "
            "contribution."
        ),

    "Active Regular Customers":
        (
            "Recently active customers who purchase "
            "regularly and form the largest customer "
            "group, but whose monetary contribution "
            "is lower than the high-value segments."
        ),

    "High-Value Loyal Customers":
        (
            "Recent, frequent and high-value customers "
            "with broad product engagement. This group "
            "makes the largest contribution to total "
            "observed Monetary value."
        ),

    "Low-Value Infrequent Customers":
        (
            "Customers with low purchase frequency, "
            "low spending, smaller baskets and limited "
            "product diversity."
        ),

    "High-Value Large-Order Buyers":
        (
            "Customers who purchase less frequently "
            "than the loyal group but place large, "
            "high-value orders with substantial "
            "basket quantities."
        ),
}


# ---------------------------------------------------------
# Load dashboard data
# ---------------------------------------------------------

(
    customers,
    model_metrics,
    segment_summary,
    strategy_mapping,
) = load_dashboard_data()


# ---------------------------------------------------------
# Page heading
# ---------------------------------------------------------

page_header(
    "Customer Segment Profiles",
    (
        "Explore the behavioural characteristics, "
        "commercial contribution and business role "
        "of each operational K-Means customer segment."
    ),
)


# ---------------------------------------------------------
# Segment selector
# ---------------------------------------------------------

st.markdown(
    "### Select a Customer Segment"
)


available_segments = [
    segment
    for segment in SEGMENT_ORDER
    if segment
    in customers[
        "Segment_Name"
    ].unique()
]


default_segment = (
    "High-Value Loyal Customers"
)


if default_segment in available_segments:

    default_index = (
        available_segments.index(
            default_segment
        )
    )

else:

    default_index = 0


selected_segment = st.selectbox(
    "Customer segment",
    options=available_segments,
    index=default_index,
    key="profile_segment_selector",
    help=(
        "Choose one operational K-Means segment "
        "to update the complete profile page."
    ),
)


# ---------------------------------------------------------
# Selected customer records
# ---------------------------------------------------------

selected_customers = customers[
    customers["Segment_Name"]
    == selected_segment
].copy()


# ---------------------------------------------------------
# Strategy record for selected K-Means segment
# ---------------------------------------------------------

strategy_rows = strategy_mapping[
    (
        strategy_mapping["Model"]
        == "K-Means K=5"
    )
    &
    (
        strategy_mapping[
            "Business_Segment"
        ]
        == selected_segment
    )
]


if not strategy_rows.empty:

    strategy = (
        strategy_rows.iloc[0]
    )

    objective = (
        strategy[
            "Primary_Objective"
        ]
    )

    recommended_action = (
        strategy[
            "Recommended_Action"
        ]
    )

    target_kpi = (
        strategy[
            "Primary_KPI"
        ]
    )

    priority = (
        strategy[
            "Operational_Priority"
        ]
    )

else:

    objective = "-"
    recommended_action = "-"
    target_kpi = "-"
    priority = "-"


# ---------------------------------------------------------
# Selected segment calculations
# ---------------------------------------------------------

selected_customer_count = (
    total_customers(
        selected_customers
    )
)


customer_share = (
    segment_customer_share(
        customers,
        selected_customers,
    )
)


monetary_share = (
    segment_monetary_share(
        customers,
        selected_customers,
    )
)


value_index = (
    value_concentration_index(
        customer_share,
        monetary_share,
    )
)


# ---------------------------------------------------------
# Selected segment overview
# ---------------------------------------------------------

st.write("")

st.markdown(
    f"## {selected_segment}"
)


st.caption(
    SEGMENT_DESCRIPTIONS[
        selected_segment
    ]
)


st.write("")


overview1, overview2, overview3, overview4 = (
    st.columns(
        4,
        gap="medium",
    )
)


with overview1:

    st.metric(
        label="Customers",
        value=f"{selected_customer_count:,}",
        border=True,
        help=(
            "Number of customers assigned "
            "to the selected K-Means segment."
        ),
    )


with overview2:

    st.metric(
        label="Customer Share",
        value=percentage(
            customer_share
        ),
        border=True,
        help=(
            "Selected segment as a percentage "
            "of all 4,338 customers."
        ),
    )


with overview3:

    st.metric(
        label="Monetary Contribution",
        value=percentage(
            monetary_share
        ),
        border=True,
        help=(
            "Selected segment's contribution "
            "to total observed Monetary value."
        ),
    )


with overview4:

    st.metric(
        label="Operational Priority",
        value=str(priority),
        border=True,
        help=(
            "Business priority assigned during "
            "the final segment interpretation."
        ),
    )


# ---------------------------------------------------------
# Median behavioural profile
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Median Behavioural Profile"
)


st.caption(
    "Medians describe the typical customer within "
    "the selected segment and reduce the influence "
    "of genuine extreme-value customers."
)


median_recency = float(
    selected_customers[
        "Recency"
    ].median()
)

median_frequency = float(
    selected_customers[
        "Frequency"
    ].median()
)

median_monetary = float(
    selected_customers[
        "Monetary"
    ].median()
)

median_aov = float(
    selected_customers[
        "AverageOrderValue"
    ].median()
)

median_basket = float(
    selected_customers[
        "BasketSize"
    ].median()
)

median_diversity = float(
    selected_customers[
        "ProductDiversity"
    ].median()
)

median_quantity = float(
    selected_customers[
        "TotalQuantity"
    ].median()
)


median1, median2, median3, median4 = (
    st.columns(
        4,
        gap="medium",
    )
)


with median1:

    st.metric(
        "Median Recency",
        f"{median_recency:,.0f} days",
        border=True,
        help=(
            "Days since the latest purchase. "
            "Lower Recency means more recent activity."
        ),
    )


with median2:

    st.metric(
        "Median Frequency",
        f"{median_frequency:,.0f}",
        border=True,
        help=(
            "Median number of unique completed "
            "purchase invoices."
        ),
    )


with median3:

    st.metric(
        "Median Monetary",
        currency(
            median_monetary
        ),
        border=True,
        help=(
            "Median total observed customer "
            "Monetary value."
        ),
    )


with median4:

    st.metric(
        "Median Average Order Value",
        currency(
            median_aov
        ),
        border=True,
        help=(
            "Median financial value per "
            "purchase occasion."
        ),
    )


st.write("")


median5, median6, median7 = (
    st.columns(
        3,
        gap="medium",
    )
)


with median5:

    st.metric(
        "Median Basket Size",
        f"{median_basket:,.1f} units",
        border=True,
        help=(
            "Typical physical quantity "
            "per purchase occasion."
        ),
    )


with median6:

    st.metric(
        "Median Product Diversity",
        f"{median_diversity:,.0f} products",
        border=True,
        help=(
            "Median number of unique products "
            "purchased by the segment."
        ),
    )


with median7:

    st.metric(
        "Median Total Quantity",
        f"{median_quantity:,.1f} units",
        border=True,
        help=(
            "Median total purchasing volume "
            "across the analysis period."
        ),
    )


# ---------------------------------------------------------
# Profile chart + business interpretation
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Behavioural Interpretation"
)


profile_col, decision_col = (
    st.columns(
        [1.6, 1],
        gap="large",
    )
)


with profile_col:

    st.markdown(
        "#### Selected Segment versus Overall Customer Median"
    )

    st.caption(
        "An index of 100 represents the median "
        "of the complete customer population."
    )

    profile_chart = (
        segment_profile_index_chart(
            customers,
            selected_segment,
        )
    )

    st.plotly_chart(
        profile_chart,
        width="stretch",
        key="segment_profile_index",
        config={
            "displayModeBar": False
        },
    )

    st.info(
        (
            "Recency requires reverse interpretation: "
            "a value below 100 indicates more recent "
            "purchasing activity, while a value above "
            "100 indicates greater inactivity."
        )
    )


with decision_col:

    with st.container(
        border=True
    ):

        st.markdown(
            "#### Business Interpretation"
        )

        st.markdown(
            "**Observed behaviour**"
        )

        st.write(
            SEGMENT_DESCRIPTIONS[
                selected_segment
            ]
        )

        st.divider()

        st.markdown(
            "**Primary objective**"
        )

        st.write(
            objective
        )

        st.markdown(
            "**Recommended action**"
        )

        st.write(
            recommended_action
        )

        st.markdown(
            "**Target KPI**"
        )

        st.write(
            target_kpi
        )

        st.markdown(
            "**Operational priority**"
        )

        st.write(
            priority
        )

        st.divider()

        st.markdown(
            "**Value Concentration Index**"
        )

        st.metric(
            label=(
                "Monetary share ÷ "
                "Customer share"
            ),
            value=f"{value_index:.2f}",
            border=True,
        )

        if value_index > 1:

            st.caption(
                (
                    "This segment contributes a "
                    "larger share of Monetary value "
                    "than its share of customers."
                )
            )

        elif value_index < 1:

            st.caption(
                (
                    "This segment contributes a "
                    "smaller share of Monetary value "
                    "than its share of customers."
                )
            )

        else:

            st.caption(
                (
                    "The segment's Monetary share "
                    "is approximately proportional "
                    "to its customer share."
                )
            )


# ---------------------------------------------------------
# All-segment heatmap
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### All-Segment Median Behavioural Heatmap"
)


st.caption(
    (
        "Each cell displays the original-scale median. "
        "Colour intensity ranks the relative magnitude "
        "of that feature across the five K-Means "
        "segments. Darker does not automatically mean "
        "better. In particular, higher Recency means "
        "longer inactivity."
    )
)


heatmap = (
    segment_median_heatmap(
        customers
    )
)


st.plotly_chart(
    heatmap,
    width="stretch",
    key="segment_profile_heatmap",
    config={
        "displayModeBar": False
    },
)


# ---------------------------------------------------------
# Median profile comparison table
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Median Profile Comparison"
)


comparison_table = (
    customers.groupby(
        "Segment_Name",
        observed=True,
    )[PROFILE_FEATURES]
    .median()
    .reindex(
        [
            segment
            for segment in SEGMENT_ORDER
            if segment
            in customers[
                "Segment_Name"
            ].unique()
        ]
    )
    .reset_index()
)


comparison_table = (
    comparison_table.rename(
        columns={
            "Segment_Name":
                "Customer Segment",

            "Recency":
                "Recency",

            "Frequency":
                "Frequency",

            "Monetary":
                "Monetary",

            "AverageOrderValue":
                "Avg. Order Value",

            "BasketSize":
                "Basket Size",

            "ProductDiversity":
                "Product Diversity",

            "TotalQuantity":
                "Total Quantity",
        }
    )
)


comparison_display = (
    comparison_table.copy()
)


comparison_display[
    "Recency"
] = comparison_display[
    "Recency"
].map(
    lambda value:
        f"{value:,.0f}"
)


comparison_display[
    "Frequency"
] = comparison_display[
    "Frequency"
].map(
    lambda value:
        f"{value:,.0f}"
)


comparison_display[
    "Monetary"
] = comparison_display[
    "Monetary"
].map(
    lambda value:
        f"£{value:,.2f}"
)


comparison_display[
    "Avg. Order Value"
] = comparison_display[
    "Avg. Order Value"
].map(
    lambda value:
        f"£{value:,.2f}"
)


comparison_display[
    "Basket Size"
] = comparison_display[
    "Basket Size"
].map(
    lambda value:
        f"{value:,.1f}"
)


comparison_display[
    "Product Diversity"
] = comparison_display[
    "Product Diversity"
].map(
    lambda value:
        f"{value:,.0f}"
)


comparison_display[
    "Total Quantity"
] = comparison_display[
    "Total Quantity"
].map(
    lambda value:
        f"{value:,.1f}"
)


st.dataframe(
    comparison_display,
    hide_index=True,
    width="stretch",
)


# ---------------------------------------------------------
# Download selected segment customers
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Export Selected Segment"
)


st.caption(
    (
        "Download the customer-level records for "
        "the currently selected segment for further "
        "review or operational analysis."
    )
)


download_columns = [
    "CustomerID",
    "Segment_Name",
    "Recency",
    "Frequency",
    "Monetary",
    "AverageOrderValue",
    "BasketSize",
    "ProductDiversity",
    "TotalQuantity",
    "Assignment_Confidence_Category",
    "GMM_Segment_Name",
    "Membership_Confidence_Category",
    "Models_Agree_After_Alignment",
]


download_data = (
    selected_customers[
        download_columns
    ]
    .to_csv(
        index=False
    )
)


safe_segment_name = (
    selected_segment
    .lower()
    .replace(" ", "_")
    .replace("-", "_")
)


st.download_button(
    label="Download Selected Customers as CSV",
    data=download_data,
    file_name=(
        f"{safe_segment_name}.csv"
    ),
    mime="text/csv",
    key="download_selected_segment",
)