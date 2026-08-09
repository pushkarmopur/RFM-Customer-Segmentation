import pandas as pd
import streamlit as st

from components.data_loader import (
    load_dashboard_data,
)

from components.metrics import (
    total_customers,
    total_monetary,
    segment_customer_share,
    segment_monetary_share,
    value_concentration_index,
    agreement_percentage,
    kmeans_review_percentage,
    gmm_ambiguous_percentage,
    percentage,
    compact_currency,
)

from components.charts import (
    SEGMENT_ORDER,
    build_segment_summary,
    segment_profile_index_chart,
    segment_value_scale_matrix,
)

from components.styles import (
    page_header,
)


# ---------------------------------------------------------
# Segment interpretation
# ---------------------------------------------------------

SEGMENT_DESCRIPTIONS = {

    "Dormant Occasional Customers":
        (
            "Customers with a long period since their "
            "most recent purchase, low repeat purchasing "
            "and limited overall monetary contribution."
        ),

    "Active Regular Customers":
        (
            "Recently active customers who purchase "
            "regularly and represent the largest "
            "customer group, but whose commercial "
            "contribution remains below their population "
            "share."
        ),

    "High-Value Loyal Customers":
        (
            "Recent, frequent and high-value customers "
            "with broad product engagement and the "
            "largest contribution to total observed "
            "Monetary value."
        ),

    "Low-Value Infrequent Customers":
        (
            "Customers with low purchase frequency, "
            "low spending, smaller baskets and limited "
            "product engagement."
        ),

    "High-Value Large-Order Buyers":
        (
            "Customers who purchase less frequently "
            "than loyal customers but place large, "
            "high-value orders with substantial basket "
            "quantities."
        ),
}


# ---------------------------------------------------------
# Why each strategy is appropriate
# ---------------------------------------------------------

STRATEGY_RATIONALE = {

    "Dormant Occasional Customers":
        (
            "The segment has experienced a long period "
            "of inactivity and contributes a relatively "
            "small share of Monetary value. A controlled "
            "win-back approach therefore provides a more "
            "appropriate use of marketing resources than "
            "high-cost retention activity."
        ),

    "Active Regular Customers":
        (
            "This is the largest customer group and its "
            "members remain relatively active. However, "
            "their Monetary contribution is substantially "
            "lower than their share of customers. "
            "Cross-selling and loyalty activity therefore "
            "focus on developing value from an already "
            "engaged population."
        ),

    "High-Value Loyal Customers":
        (
            "This segment combines recent purchasing, "
            "high purchase frequency, strong product "
            "engagement and the largest Monetary "
            "contribution. Retention should therefore "
            "receive very high priority because losing "
            "customers from this group could have a "
            "substantial commercial effect."
        ),

    "Low-Value Infrequent Customers":
        (
            "The segment combines low purchasing "
            "frequency with low spending and limited "
            "product engagement. Low-cost automated "
            "nurturing therefore provides a more "
            "proportionate strategy than intensive "
            "manual intervention."
        ),

    "High-Value Large-Order Buyers":
        (
            "These customers are differentiated by "
            "large baskets and high order values rather "
            "than very high purchase frequency. The "
            "business should protect order value and "
            "encourage repeat large purchases without "
            "assuming that these customers represent "
            "verified wholesale or B2B buyers."
        ),
}


# ---------------------------------------------------------
# Load final data
# ---------------------------------------------------------

(
    customers,
    model_metrics,
    segment_summary_file,
    strategy_mapping,
) = load_dashboard_data()


# ---------------------------------------------------------
# Page header
# ---------------------------------------------------------

page_header(
    "Strategy & Decision Support",
    (
        "Translate customer segmentation evidence "
        "into prioritised business objectives, "
        "recommended actions and measurable KPIs."
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
    key="strategy_segment_selector",
    help=(
        "Select one final K-Means customer segment "
        "to view its commercial profile and "
        "recommended management action."
    ),
)


# ---------------------------------------------------------
# Selected customer data
# ---------------------------------------------------------

selected_customers = customers[
    customers["Segment_Name"]
    == selected_segment
].copy()


# ---------------------------------------------------------
# Strategy mapping
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

    strategy = strategy_rows.iloc[0]

    objective = str(
        strategy[
            "Primary_Objective"
        ]
    )

    recommended_action = str(
        strategy[
            "Recommended_Action"
        ]
    )

    target_kpi = str(
        strategy[
            "Primary_KPI"
        ]
    )

    priority = str(
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


selected_monetary = (
    total_monetary(
        selected_customers
    )
)


value_index = (
    value_concentration_index(
        customer_share,
        monetary_share,
    )
)


segment_agreement = (
    agreement_percentage(
        selected_customers
    )
)


segment_kmeans_review = (
    kmeans_review_percentage(
        selected_customers
    )
)


segment_gmm_ambiguous = (
    gmm_ambiguous_percentage(
        selected_customers
    )
)


# ---------------------------------------------------------
# Build complete portfolio summary
# ---------------------------------------------------------

portfolio_summary = (
    build_segment_summary(
        customers
    )
)


portfolio_summary[
    "Revenue_Rank"
] = (
    portfolio_summary[
        "Total_Monetary"
    ]
    .rank(
        method="dense",
        ascending=False,
    )
    .astype(int)
)


selected_summary = (
    portfolio_summary[
        portfolio_summary[
            "Segment_Name"
        ]
        == selected_segment
    ]
    .iloc[0]
)


revenue_rank = int(
    selected_summary[
        "Revenue_Rank"
    ]
)


# ---------------------------------------------------------
# Selected segment hero section
# ---------------------------------------------------------

st.write("")

with st.container(
    border=True
):

    st.markdown(
        "### Selected Customer Segment"
    )

    st.markdown(
        f"# {selected_segment}"
    )

    st.write(
        SEGMENT_DESCRIPTIONS[
            selected_segment
        ]
    )

    if priority == "Very High":

        st.markdown(
            ":red-badge[VERY HIGH PRIORITY]"
        )

    elif priority == "High":

        st.markdown(
            ":orange-badge[HIGH PRIORITY]"
        )

    elif priority == "Medium":

        st.markdown(
            ":blue-badge[MEDIUM PRIORITY]"
        )

    elif priority == "Low":

        st.markdown(
            ":green-badge[LOW PRIORITY]"
        )


# ---------------------------------------------------------
# Strategic direction
# ---------------------------------------------------------

st.write("")

strategy1, strategy2 = st.columns(
    2,
    gap="large",
)


with strategy1:

    with st.container(
        border=True
    ):

        st.caption(
            "PRIMARY OBJECTIVE"
        )

        st.markdown(
            f"### {objective}"
        )


with strategy2:

    with st.container(
        border=True
    ):

        st.caption(
            "TARGET KPI"
        )

        st.markdown(
            f"### {target_kpi}"
        )


# ---------------------------------------------------------
# Commercial KPI row
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Commercial Importance"
)


commercial1, commercial2, commercial3, commercial4 = (
    st.columns(
        4,
        gap="medium",
    )
)


with commercial1:

    st.metric(
        "Customers",
        f"{selected_customer_count:,}",
        border=True,
    )


with commercial2:

    st.metric(
        "Customer Share",
        percentage(
            customer_share
        ),
        border=True,
    )


with commercial3:

    st.metric(
        "Monetary Contribution",
        percentage(
            monetary_share
        ),
        border=True,
    )


with commercial4:

    st.metric(
        "Value Concentration Index",
        f"{value_index:.2f}",
        border=True,
        help=(
            "Monetary share divided by customer "
            "share. Values above 1 indicate "
            "disproportionately high Monetary "
            "contribution."
        ),
    )


# ---------------------------------------------------------
# Secondary decision KPIs
# ---------------------------------------------------------

st.write("")


decision_kpi1, decision_kpi2, decision_kpi3, decision_kpi4 = (
    st.columns(
        4,
        gap="medium",
    )
)


with decision_kpi1:

    st.metric(
        "Observed Monetary Value",
        compact_currency(
            selected_monetary
        ),
        border=True,
    )


with decision_kpi2:

    st.metric(
        "Monetary Rank",
        f"#{revenue_rank} of 5",
        border=True,
    )


with decision_kpi3:

    st.metric(
        "Aligned Model Agreement",
        percentage(
            segment_agreement
        ),
        border=True,
    )


with decision_kpi4:

    st.metric(
        "K-Means Review Group",
        percentage(
            segment_kmeans_review
        ),
        border=True,
    )


# ---------------------------------------------------------
# Main management recommendation
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Management Recommendation"
)


with st.container(
    border=True
):

    st.markdown(
        ":green-badge[RECOMMENDED ACTION]"
    )

    st.markdown(
        f"## {recommended_action}"
    )

    st.divider()

    st.markdown(
        "#### Why this action?"
    )

    st.write(
        STRATEGY_RATIONALE[
            selected_segment
        ]
    )

    st.divider()

    st.markdown(
        f"""
        **Management focus:** {objective}

        **Target KPI:** {target_kpi}

        **Operational priority:** {priority}
        """
    )


# ---------------------------------------------------------
# Decision summary
# ---------------------------------------------------------

st.write("")

with st.container(
    border=True
):

    st.markdown(
        "#### Decision Summary"
    )

    st.write(
        (
            f"{selected_segment} contains "
            f"{selected_customer_count:,} customers, "
            f"representing {customer_share:.2f}% "
            f"of the customer base and "
            f"{monetary_share:.2f}% of total observed "
            f"Monetary value. The segment ranks "
            f"#{revenue_rank} of five by Monetary "
            f"contribution. The primary management "
            f"objective is {objective.lower()}, with "
            f"{target_kpi.lower()} used as the target "
            f"KPI."
        )
    )


# ---------------------------------------------------------
# Behaviour + decision confidence
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Behavioural and Confidence Evidence"
)


profile_col, confidence_col = st.columns(
    [1.6, 1],
    gap="large",
)


with profile_col:

    st.markdown(
        "#### Selected Segment versus Overall Median"
    )

    st.caption(
        (
            "100 represents the overall customer "
            "median for each behavioural feature."
        )
    )

    profile_fig = (
        segment_profile_index_chart(
            customers,
            selected_segment,
        )
    )

    st.plotly_chart(
        profile_fig,
        width="stretch",
        key="strategy_profile_chart",
        config={
            "displayModeBar": False
        },
    )

    st.info(
        (
            "Recency requires reverse interpretation: "
            "lower values indicate more recent "
            "purchasing activity."
        )
    )


with confidence_col:

    with st.container(
        border=True
    ):

        st.markdown(
            "#### Decision Confidence Context"
        )

        st.metric(
            "Cross-Model Agreement",
            percentage(
                segment_agreement
            ),
            border=True,
        )

        st.metric(
            "K-Means Review Group",
            percentage(
                segment_kmeans_review
            ),
            border=True,
        )

        st.metric(
            "GMM Ambiguous Membership",
            percentage(
                segment_gmm_ambiguous
            ),
            border=True,
        )

        st.caption(
            (
                "These values describe assignment "
                "confidence within the selected "
                "segment. They are not accuracy "
                "or misclassification rates."
            )
        )


# ---------------------------------------------------------
# Value-scale portfolio matrix
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Segment Value–Scale Matrix"
)


st.caption(
    (
        "The matrix positions every K-Means segment "
        "using customer share and Monetary "
        "contribution. Bubble size represents the "
        "number of customers. The selected segment "
        "is outlined."
    )
)


value_scale_fig = (
    segment_value_scale_matrix(
        portfolio_summary,
        selected_segment,
    )
)


st.plotly_chart(
    value_scale_fig,
    width="stretch",
    key="strategy_value_scale_matrix",
    config={
        "displayModeBar": False
    },
)


# ---------------------------------------------------------
# Matrix interpretation
# ---------------------------------------------------------

matrix1, matrix2, matrix3, matrix4 = (
    st.columns(
        4,
        gap="medium",
    )
)


with matrix1:

    with st.container(
        border=True
    ):

        st.markdown(
            "**High Value + Large Population**"
        )

        st.caption(
            "Protect and develop strategically "
            "important customer groups."
        )


with matrix2:

    with st.container(
        border=True
    ):

        st.markdown(
            "**High Value + Smaller Population**"
        )

        st.caption(
            "Prioritise retention and protect "
            "commercial concentration."
        )


with matrix3:

    with st.container(
        border=True
    ):

        st.markdown(
            "**Lower Value + Large Population**"
        )

        st.caption(
            "Develop value efficiently through "
            "cross-selling or loyalty activity."
        )


with matrix4:

    with st.container(
        border=True
    ):

        st.markdown(
            "**Lower Value + Smaller Population**"
        )

        st.caption(
            "Use efficient nurture or controlled "
            "reactivation approaches."
        )


# ---------------------------------------------------------
# Complete action plan
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Complete Customer Segment Action Plan"
)


st.caption(
    (
        "The selected segment is highlighted while "
        "the full portfolio remains visible for "
        "management comparison."
    )
)


action_summary = portfolio_summary.merge(
    strategy_mapping[
        strategy_mapping[
            "Model"
        ]
        == "K-Means K=5"
    ][
        [
            "Business_Segment",
            "Primary_Objective",
            "Recommended_Action",
            "Primary_KPI",
            "Operational_Priority",
        ]
    ],
    left_on="Segment_Name",
    right_on="Business_Segment",
    how="left",
)


action_summary = action_summary[
    [
        "Segment_Name",
        "Customer_Count",
        "Customer_Share",
        "Monetary_Share",
        "Primary_Objective",
        "Primary_KPI",
        "Operational_Priority",
    ]
].copy()


action_summary = action_summary.rename(
    columns={
        "Segment_Name":
            "Segment",

        "Customer_Count":
            "Customers",

        "Customer_Share":
            "Customer Share",

        "Monetary_Share":
            "Monetary Share",

        "Primary_Objective":
            "Objective",

        "Primary_KPI":
            "Target KPI",

        "Operational_Priority":
            "Priority",
    }
)


priority_order = {
    "Very High": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4,
}


action_summary[
    "_Priority_Order"
] = action_summary[
    "Priority"
].map(
    priority_order
)


action_summary = (
    action_summary
    .sort_values(
        [
            "_Priority_Order",
            "Monetary Share",
        ],
        ascending=[
            True,
            False,
        ],
    )
    .drop(
        columns=[
            "_Priority_Order"
        ]
    )
)


# ---------------------------------------------------------
# Highlight selected segment
# ---------------------------------------------------------

def highlight_selected_segment(
    row
):

    if row["Segment"] == selected_segment:

        return [
            (
                "background-color: #DBEAFE; "
                "font-weight: 600;"
            )
        ] * len(row)

    return [
        ""
    ] * len(row)


styled_action_summary = (
    action_summary.style.apply(
        highlight_selected_segment,
        axis=1,
    )
)


st.dataframe(
    styled_action_summary,
    hide_index=True,
    width="stretch",
    column_config={

        "Customer Share":
            st.column_config.NumberColumn(
                "Customer Share",
                format="%.2f%%",
            ),

        "Monetary Share":
            st.column_config.NumberColumn(
                "Monetary Share",
                format="%.2f%%",
            ),

        "Segment":
            st.column_config.Column(
                "Segment",
                width="large",
            ),
    },
)


# ---------------------------------------------------------
# Selected segment customer export
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Export Selected Strategy Population"
)


st.caption(
    (
        "Download the customers associated with "
        "the selected management strategy."
    )
)


export_columns = [
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
    "Primary_Objective",
    "Recommended_Action",
    "Primary_KPI",
    "Operational_Priority",
]


selected_export = (
    selected_customers[
        export_columns
    ]
    .sort_values(
        "Monetary",
        ascending=False,
    )
    .to_csv(
        index=False
    )
)


safe_name = (
    selected_segment
    .lower()
    .replace(" ", "_")
    .replace("-", "_")
)


st.download_button(
    label="Download Selected Strategy Customers",
    data=selected_export,
    file_name=(
        f"{safe_name}_strategy_customers.csv"
    ),
    mime="text/csv",
    key="download_strategy_population",
)


# ---------------------------------------------------------
# Final methodological note
# ---------------------------------------------------------

st.write("")

st.info(
    (
        "Business recommendations are linked to "
        "the behavioural profiles produced by the "
        "primary K-Means K=5 segmentation. "
        "GMM confidence evidence is presented as "
        "supporting analytical context and does not "
        "replace the operational K-Means segment."
    )
)