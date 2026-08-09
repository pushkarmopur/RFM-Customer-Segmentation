import pandas as pd
import streamlit as st

from components.data_loader import (
    load_dashboard_data,
)

from components.metrics import (
    total_customers,
    kmeans_review_percentage,
    gmm_ambiguous_percentage,
    both_models_flagged_percentage,
    agreement_percentage,
    mean_gmm_max_probability,
    percentage,
)

from components.charts import (
    SEGMENT_ORDER,
    confidence_distribution_chart,
    kmeans_confidence_scatter,
    gmm_confidence_scatter,
)

from components.styles import (
    page_header,
)


# ---------------------------------------------------------
# Load final dashboard data
# ---------------------------------------------------------

(
    customers,
    model_metrics,
    segment_summary,
    strategy_mapping,
) = load_dashboard_data()


# ---------------------------------------------------------
# Alternative GMM business-name mapping
# ---------------------------------------------------------

GMM_COMPONENT_TO_SEGMENT = {

    0:
        "Active Regular Customers",

    1:
        "Elite High-Value Customers",

    2:
        "High-Value Loyal Customers",

    3:
        "Dormant Occasional Customers",

    4:
        "Low-Value Infrequent Customers",
}


customers = customers.copy()


customers[
    "Alternative_GMM_Segment"
] = customers[
    "Alternative_GMM_Component"
].map(
    GMM_COMPONENT_TO_SEGMENT
)


customers[
    "Model_Agreement_Status"
] = customers[
    "Models_Agree_After_Alignment"
].map(
    {
        True: "Agree",
        False: "Different",
    }
)


# ---------------------------------------------------------
# Page heading
# ---------------------------------------------------------

page_header(
    "Customer Confidence & Explorer",
    (
        "Review customer-level K-Means boundary "
        "evidence, GMM probabilistic membership "
        "and cross-model assignment agreement."
    ),
)


# ---------------------------------------------------------
# Filters
# ---------------------------------------------------------

st.markdown(
    "### Explore Assignment Confidence"
)


filter_box = st.container(
    border=True
)


with filter_box:

    search_col, segment_col = (
        st.columns(
            2,
            gap="large",
        )
    )


    with search_col:

        customer_search = st.text_input(
            "Customer ID search",
            value="",
            placeholder=(
                "Enter part or all of a Customer ID"
            ),
            key="confidence_customer_search",
        )


    with segment_col:

        available_segments = [
            segment
            for segment in SEGMENT_ORDER
            if segment
            in customers[
                "Segment_Name"
            ].unique()
        ]

        selected_segments = st.multiselect(
            "K-Means segments",
            options=available_segments,
            default=available_segments,
            key="confidence_segment_filter",
        )


    confidence_col1, confidence_col2 = (
        st.columns(
            2,
            gap="large",
        )
    )


    with confidence_col1:

        kmeans_categories = sorted(
            customers[
                "Assignment_Confidence_Category"
            ]
            .dropna()
            .unique()
            .tolist()
        )

        selected_kmeans_confidence = (
            st.multiselect(
                "K-Means confidence",
                options=kmeans_categories,
                default=kmeans_categories,
                key="kmeans_confidence_filter",
            )
        )


    with confidence_col2:

        gmm_categories = sorted(
            customers[
                "Membership_Confidence_Category"
            ]
            .dropna()
            .unique()
            .tolist()
        )

        selected_gmm_confidence = (
            st.multiselect(
                "GMM membership confidence",
                options=gmm_categories,
                default=gmm_categories,
                key="gmm_confidence_filter",
            )
        )


    agreement_option = st.selectbox(
        "Cross-model agreement",
        options=[
            "All customers",
            "Models agree",
            "Models differ",
        ],
        index=0,
        key="confidence_agreement_filter",
    )


# ---------------------------------------------------------
# Apply filters
# ---------------------------------------------------------

filtered = customers[
    (
        customers[
            "Segment_Name"
        ].isin(
            selected_segments
        )
    )
    &
    (
        customers[
            "Assignment_Confidence_Category"
        ].isin(
            selected_kmeans_confidence
        )
    )
    &
    (
        customers[
            "Membership_Confidence_Category"
        ].isin(
            selected_gmm_confidence
        )
    )
].copy()


if agreement_option == "Models agree":

    filtered = filtered[
        filtered[
            "Models_Agree_After_Alignment"
        ]
    ]


elif agreement_option == "Models differ":

    filtered = filtered[
        ~filtered[
            "Models_Agree_After_Alignment"
        ]
    ]


if customer_search.strip():

    filtered = filtered[
        filtered[
            "CustomerID"
        ]
        .astype(str)
        .str.contains(
            customer_search.strip(),
            case=False,
            na=False,
        )
    ]


if filtered.empty:

    st.warning(
        "No customers match the current "
        "confidence filters."
    )

    st.stop()


# ---------------------------------------------------------
# KPI section
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Confidence Overview"
)


kpi1, kpi2, kpi3 = (
    st.columns(
        3,
        gap="medium",
    )
)


with kpi1:

    st.metric(
        "Customers in Selection",
        f"{total_customers(filtered):,}",
        border=True,
    )


with kpi2:

    st.metric(
        "K-Means Review Group",
        percentage(
            kmeans_review_percentage(
                filtered
            )
        ),
        border=True,
        help=(
            "Customers satisfying the broader "
            "K-Means boundary/review criteria "
            "within the current selection."
        ),
    )


with kpi3:

    st.metric(
        "GMM Ambiguous Membership",
        percentage(
            gmm_ambiguous_percentage(
                filtered
            )
        ),
        border=True,
    )


st.write("")


kpi4, kpi5, kpi6 = (
    st.columns(
        3,
        gap="medium",
    )
)


with kpi4:

    st.metric(
        "Flagged by Both Models",
        percentage(
            both_models_flagged_percentage(
                filtered
            )
        ),
        border=True,
    )


with kpi5:

    st.metric(
        "Aligned Model Agreement",
        percentage(
            agreement_percentage(
                filtered
            )
        ),
        border=True,
    )


with kpi6:

    st.metric(
        "Average GMM Max Probability",
        percentage(
            mean_gmm_max_probability(
                filtered
            )
            * 100
        ),
        border=True,
    )


# ---------------------------------------------------------
# Methodological clarification
# ---------------------------------------------------------

st.info(
    (
        "These indicators describe assignment "
        "confidence and boundary behaviour. "
        "They are not classification accuracy "
        "or misclassification rates because the "
        "customer segments have no ground-truth labels."
    )
)


# ---------------------------------------------------------
# Confidence distributions
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Confidence Category Distribution"
)


dist1, dist2 = st.columns(
    2,
    gap="large",
)


with dist1:

    st.markdown(
        "#### K-Means Assignment Confidence"
    )

    kmeans_distribution = (
        confidence_distribution_chart(
            filtered,
            "Assignment_Confidence_Category",
        )
    )

    st.plotly_chart(
        kmeans_distribution,
        width="stretch",
        key="kmeans_confidence_distribution",
        config={
            "displayModeBar": False
        },
    )


with dist2:

    st.markdown(
        "#### GMM Membership Confidence"
    )

    gmm_distribution = (
        confidence_distribution_chart(
            filtered,
            "Membership_Confidence_Category",
        )
    )

    st.plotly_chart(
        gmm_distribution,
        width="stretch",
        key="gmm_confidence_distribution",
        config={
            "displayModeBar": False
        },
    )


# ---------------------------------------------------------
# K-Means customer confidence
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### K-Means Customer Boundary Analysis"
)


st.caption(
    (
        "The plot combines individual Silhouette "
        "with the customer's relative distance "
        "margin between the assigned and next-nearest "
        "centroids."
    )
)


kmeans_chart = (
    kmeans_confidence_scatter(
        filtered
    )
)


st.plotly_chart(
    kmeans_chart,
    width="stretch",
    key="kmeans_confidence_scatter",
    config={
        "displayModeBar": False
    },
)


st.caption(
    (
        "Review evidence is strongest toward the "
        "lower-left area: negative Silhouette values "
        "or small centroid margins indicate a less "
        "clear hard-cluster assignment."
    )
)


# ---------------------------------------------------------
# GMM customer confidence
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### GMM Membership Probability Analysis"
)


st.caption(
    (
        "Maximum probability shows support for the "
        "assigned GMM component. Probability margin "
        "compares the first and second most likely "
        "components. Bubble size represents the "
        "second-highest probability."
    )
)


gmm_chart = (
    gmm_confidence_scatter(
        filtered
    )
)


st.plotly_chart(
    gmm_chart,
    width="stretch",
    key="gmm_confidence_scatter",
    config={
        "displayModeBar": False
    },
)


st.caption(
    (
        "Lower maximum probability, a small "
        "probability margin or higher entropy "
        "indicates less concentrated GMM membership."
    )
)


# ---------------------------------------------------------
# Single customer inspector
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Individual Customer Inspector"
)


filtered_ids = (
    filtered[
        "CustomerID"
    ]
    .astype(str)
    .sort_values()
    .tolist()
)


selected_customer_id = st.selectbox(
    "Select a customer",
    options=filtered_ids,
    key="confidence_customer_inspector",
)


customer_row = (
    filtered[
        filtered[
            "CustomerID"
        ].astype(str)
        == str(
            selected_customer_id
        )
    ]
    .iloc[0]
)


st.write("")


customer1, customer2, customer3 = (
    st.columns(
        3,
        gap="medium",
    )
)


with customer1:

    st.metric(
        "Customer ID",
        str(
            customer_row[
                "CustomerID"
            ]
        ),
        border=True,
    )


with customer2:

    st.metric(
        "K-Means Segment",
        str(
            customer_row[
                "Segment_Name"
            ]
        ),
        border=True,
    )


with customer3:

    st.metric(
        "GMM Segment",
        str(
            customer_row[
                "GMM_Segment_Name"
            ]
        ),
        border=True,
    )


# ---------------------------------------------------------
# K-Means detail panel
# ---------------------------------------------------------

detail1, detail2 = st.columns(
    2,
    gap="large",
)


with detail1:

    with st.container(
        border=True
    ):

        st.markdown(
            "#### K-Means Assignment Evidence"
        )

        st.markdown(
            "**Confidence category**"
        )

        st.write(
            customer_row[
                "Assignment_Confidence_Category"
            ]
        )

        st.markdown(
            "**Individual Silhouette**"
        )

        st.write(
            f"{customer_row['Silhouette_Value_KMeans']:.4f}"
        )

        st.markdown(
            "**Relative centroid margin**"
        )

        st.write(
            f"{customer_row['Relative_Centroid_Margin']:.4f}"
        )

        st.markdown(
            "**Alternative K-Means segment**"
        )

        st.write(
            customer_row[
                "Alternative_Segment"
            ]
        )


# ---------------------------------------------------------
# GMM detail panel
# ---------------------------------------------------------

with detail2:

    with st.container(
        border=True
    ):

        st.markdown(
            "#### GMM Membership Evidence"
        )

        st.markdown(
            "**Membership category**"
        )

        st.write(
            customer_row[
                "Membership_Confidence_Category"
            ]
        )

        st.markdown(
            "**Maximum probability**"
        )

        st.write(
            f"{customer_row['Maximum_Probability']:.2%}"
        )

        st.markdown(
            "**Second probability**"
        )

        st.write(
            f"{customer_row['Second_Probability']:.2%}"
        )

        st.markdown(
            "**Probability margin**"
        )

        st.write(
            f"{customer_row['Probability_Margin']:.2%}"
        )

        st.markdown(
            "**Normalised entropy**"
        )

        st.write(
            f"{customer_row['Normalised_Entropy']:.4f}"
        )

        st.markdown(
            "**Alternative GMM segment**"
        )

        st.write(
            customer_row[
                "Alternative_GMM_Segment"
            ]
        )


# ---------------------------------------------------------
# Cross-model result
# ---------------------------------------------------------

st.write("")


agreement_status = (
    "Agree"
    if customer_row[
        "Models_Agree_After_Alignment"
    ]
    else "Different"
)


if agreement_status == "Agree":

    st.success(
        (
            "The aligned K-Means and GMM "
            "assignments correspond for this customer."
        )
    )

else:

    st.warning(
        (
            "K-Means and aligned GMM place this "
            "customer in different corresponding "
            "groups. This represents cross-model "
            "assignment disagreement, not an error."
        )
    )


# ---------------------------------------------------------
# Customer confidence explorer table
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Customer Confidence Explorer"
)


st.caption(
    (
        "Use the filters above to focus on boundary, "
        "ambiguous or cross-model disagreement cases."
    )
)


explorer = filtered[
    [
        "CustomerID",
        "Segment_Name",
        "Assignment_Confidence_Category",
        "Silhouette_Value_KMeans",
        "Relative_Centroid_Margin",
        "Alternative_Segment",
        "GMM_Segment_Name",
        "Membership_Confidence_Category",
        "Maximum_Probability",
        "Second_Probability",
        "Probability_Margin",
        "Normalised_Entropy",
        "Alternative_GMM_Segment",
        "Model_Agreement_Status",
        "Cross_Model_Uncertainty_Group",
    ]
].copy()


explorer = explorer.rename(
    columns={
        "CustomerID":
            "Customer ID",

        "Segment_Name":
            "K-Means Segment",

        "Assignment_Confidence_Category":
            "K-Means Confidence",

        "Silhouette_Value_KMeans":
            "Silhouette",

        "Relative_Centroid_Margin":
            "Centroid Margin",

        "Alternative_Segment":
            "Alternative K-Means Segment",

        "GMM_Segment_Name":
            "GMM Segment",

        "Membership_Confidence_Category":
            "GMM Confidence",

        "Maximum_Probability":
            "Max Probability",

        "Second_Probability":
            "Second Probability",

        "Probability_Margin":
            "Probability Margin",

        "Normalised_Entropy":
            "Entropy",

        "Alternative_GMM_Segment":
            "Alternative GMM Segment",

        "Model_Agreement_Status":
            "Models Agree?",

        "Cross_Model_Uncertainty_Group":
            "Review Status",
    }
)


# ---------------------------------------------------------
# Format table values
# ---------------------------------------------------------

for column in [
    "Max Probability",
    "Second Probability",
    "Probability Margin",
]:

    explorer[
        column
    ] = explorer[
        column
    ].map(
        lambda value:
            f"{value:.2%}"
    )


for column in [
    "Silhouette",
    "Centroid Margin",
    "Entropy",
]:

    explorer[
        column
    ] = explorer[
        column
    ].map(
        lambda value:
            f"{value:.4f}"
    )


# ---------------------------------------------------------
# Highlight uncertainty
# ---------------------------------------------------------

def highlight_confidence(
    value
):

    text = str(
        value
    ).lower()

    if (
        "boundary" in text
        or "ambiguous" in text
        or "different" in text
        or "review" in text
        or "low" in text
    ):

        return (
            "background-color: #FEE2E2; "
            "color: #991B1B;"
        )

    if (
        "moderate" in text
        or "medium" in text
    ):

        return (
            "background-color: #FEF3C7; "
            "color: #92400E;"
        )

    if (
        "strong" in text
        or "agree" == text
    ):

        return (
            "background-color: #DCFCE7; "
            "color: #166534;"
        )

    return ""


styled_explorer = (
    explorer.style.map(
        highlight_confidence,
        subset=[
            "K-Means Confidence",
            "GMM Confidence",
            "Models Agree?",
            "Review Status",
        ],
    )
)


st.dataframe(
    styled_explorer,
    hide_index=True,
    width="stretch",
    height=500,
)


# ---------------------------------------------------------
# Review-only download
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Export Confidence Review Data"
)


st.caption(
    (
        "Download customers identified by either "
        "the K-Means review criteria, the GMM "
        "ambiguity criteria or both."
    )
)


review_population = filtered[
    (
        filtered[
            "Combined_Boundary_Flag"
        ]
    )
    |
    (
        filtered[
            "Combined_Ambiguous_Flag"
        ]
    )
].copy()


review_csv = (
    review_population
    .to_csv(
        index=False
    )
)


st.download_button(
    label=(
        "Download Customers Requiring Review"
    ),
    data=review_csv,
    file_name=(
        "customer_assignment_review.csv"
    ),
    mime="text/csv",
    key="download_confidence_review",
)