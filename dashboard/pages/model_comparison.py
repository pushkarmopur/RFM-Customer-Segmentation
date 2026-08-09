import pandas as pd
import streamlit as st

from sklearn.metrics import (
    adjusted_rand_score,
    normalized_mutual_info_score,
)

from components.data_loader import (
    load_dashboard_data,
)

from components.metrics import (
    agreement_percentage,
    percentage,
)

from components.charts import (
    model_stability_chart,
    model_alignment_heatmap,
    agreement_by_segment_chart,
    uncertainty_overlap_chart,
)

from components.styles import (
    page_header,
)


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
    "Model Comparison",
    (
        "Compare the final K-Means K=5 operational "
        "segmentation with the GMM C5 Spherical "
        "probabilistic supporting model."
    ),
)


# ---------------------------------------------------------
# Helper: extract final common model metric
# ---------------------------------------------------------

def metric_value(
    metric_name: str,
    model_column: str,
) -> float:

    rows = model_metrics[
        model_metrics[
            "Metric"
        ]
        == metric_name
    ]

    if rows.empty:
        return float("nan")

    return float(
        rows.iloc[0][
            model_column
        ]
    )


# ---------------------------------------------------------
# Common internal validation results
# ---------------------------------------------------------

kmeans_silhouette = metric_value(
    "Silhouette Score",
    "KMeans_K5",
)

gmm_silhouette = metric_value(
    "Silhouette Score",
    "GMM_C5_Spherical",
)

kmeans_dbi = metric_value(
    "Davies-Bouldin Index",
    "KMeans_K5",
)

gmm_dbi = metric_value(
    "Davies-Bouldin Index",
    "GMM_C5_Spherical",
)

kmeans_ch = metric_value(
    "Calinski-Harabasz Index",
    "KMeans_K5",
)

gmm_ch = metric_value(
    "Calinski-Harabasz Index",
    "GMM_C5_Spherical",
)


# ---------------------------------------------------------
# Cross-model assignment similarity
# ---------------------------------------------------------

cross_model_ari = (
    adjusted_rand_score(
        customers[
            "Cluster"
        ].astype(int),
        customers[
            "GMM_Component"
        ].astype(int),
    )
)


cross_model_nmi = (
    normalized_mutual_info_score(
        customers[
            "Cluster"
        ].astype(int),
        customers[
            "GMM_Component"
        ].astype(int),
    )
)


aligned_agreement = (
    agreement_percentage(
        customers
    )
)


# ---------------------------------------------------------
# Model overview
# ---------------------------------------------------------

st.markdown(
    "### Final Models"
)


model_col1, model_col2 = st.columns(
    2,
    gap="large",
)


with model_col1:

    with st.container(
        border=True
    ):

        st.markdown(
            "#### Primary Operational Model"
        )

        st.markdown(
            "## K-Means K=5"
        )

        st.write(
            (
                "Used for final customer segmentation, "
                "business profiling and operational "
                "strategy mapping."
            )
        )


with model_col2:

    with st.container(
        border=True
    ):

        st.markdown(
            "#### Supporting Analytical Model"
        )

        st.markdown(
            "## GMM C5 Spherical"
        )

        st.write(
            (
                "Used to provide probabilistic "
                "membership evidence, alternative "
                "components and uncertainty analysis."
            )
        )


# ---------------------------------------------------------
# Common validation KPI cards
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Common Internal Validation"
)


st.caption(
    (
        "These metrics can be applied to both final "
        "five-group partitions. Higher Silhouette and "
        "Calinski-Harabasz are preferred; lower "
        "Davies-Bouldin is preferred."
    )
)


validation1, validation2 = st.columns(
    2,
    gap="medium",
)


with validation1:

    st.metric(
        "K-Means Silhouette",
        f"{kmeans_silhouette:.4f}",
        border=True,
    )


with validation2:

    st.metric(
        "GMM Silhouette",
        f"{gmm_silhouette:.4f}",
        border=True,
    )


validation3, validation4 = st.columns(
    2,
    gap="medium",
)


with validation3:

    st.metric(
        "K-Means Davies-Bouldin",
        f"{kmeans_dbi:.4f}",
        border=True,
    )


with validation4:

    st.metric(
        "GMM Davies-Bouldin",
        f"{gmm_dbi:.4f}",
        border=True,
    )


validation5, validation6 = st.columns(
    2,
    gap="medium",
)


with validation5:

    st.metric(
        "K-Means Calinski-Harabasz",
        f"{kmeans_ch:,.2f}",
        border=True,
    )


with validation6:

    st.metric(
        "GMM Calinski-Harabasz",
        f"{gmm_ch:,.2f}",
        border=True,
    )


# ---------------------------------------------------------
# Cross-model KPI cards
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Cross-Model Assignment Similarity"
)


cross1, cross2, cross3 = st.columns(
    3,
    gap="medium",
)


with cross1:

    st.metric(
        "Adjusted Rand Index",
        f"{cross_model_ari:.4f}",
        border=True,
        help=(
            "Measures similarity between the two "
            "complete customer partitions while "
            "remaining invariant to cluster labels."
        ),
    )


with cross2:

    st.metric(
        "Normalised Mutual Information",
        f"{cross_model_nmi:.4f}",
        border=True,
        help=(
            "Measures shared assignment information "
            "between the K-Means and GMM partitions."
        ),
    )


with cross3:

    st.metric(
        "Aligned Customer Agreement",
        percentage(
            aligned_agreement
        ),
        border=True,
        help=(
            "Percentage of customers in corresponding "
            "groups after aligning GMM components "
            "with K-Means segments."
        ),
    )


st.info(
    (
        "ARI, NMI and aligned agreement measure "
        "similarity between two unsupervised "
        "partitions. They are not classification "
        "accuracy measures."
    )
)


# ---------------------------------------------------------
# Complete common technical comparison
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Complete Technical Comparison"
)


st.caption(
    (
        "The table compares only measures that have "
        "a meaningful interpretation for both final "
        "models."
    )
)


technical_table = model_metrics[
    [
        "Metric",
        "Definition",
        "Preferred_Direction",
        "KMeans_K5",
        "GMM_C5_Spherical",
        "Metric_Preference",
    ]
].copy()


technical_table = technical_table.rename(
    columns={
        "Metric":
            "Evaluation Metric",

        "Definition":
            "Definition",

        "Preferred_Direction":
            "Preferred Direction",

        "KMeans_K5":
            "K-Means K=5",

        "GMM_C5_Spherical":
            "GMM C5 Spherical",

        "Metric_Preference":
            "Stronger Evidence",
    }
)


st.dataframe(
    technical_table,
    hide_index=True,
    width="stretch",
)


# ---------------------------------------------------------
# Metric compatibility warning
# ---------------------------------------------------------

st.warning(
    (
        "WCSS is a K-Means-specific objective, while "
        "AIC and BIC evaluate likelihood-based GMM "
        "models. They are therefore not displayed as "
        "if they were directly comparable performance "
        "scores."
    )
)


# ---------------------------------------------------------
# Stability analysis
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Random-Seed and Subsampling Stability"
)


st.caption(
    (
        "Adjusted Rand Index is used to compare "
        "assignment consistency across repeated "
        "initialisations and repeated 80% customer "
        "subsamples."
    )
)


stability_fig = (
    model_stability_chart(
        model_metrics
    )
)


st.plotly_chart(
    stability_fig,
    width="stretch",
    key="model_stability_comparison",
    config={
        "displayModeBar": False
    },
)


st.markdown(
    """
    **Interpretation**

    - Both final models show very high random-seed stability.
    - GMM C5 Spherical has a slightly higher mean subsampling ARI.
    - K-Means K=5 has the stronger minimum subsampling result.
    - Stability evidence therefore supports both models rather than
      indicating that either model is unstable.
    """
)


# ---------------------------------------------------------
# Assignment alignment matrix
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### K-Means versus Aligned GMM Customer Matrix"
)


st.caption(
    (
        "Cells show the number of customers shared "
        "between each K-Means business segment and "
        "each aligned GMM business segment. This is "
        "an overlap matrix, not a confusion matrix "
        "against known customer labels."
    )
)


alignment_fig = (
    model_alignment_heatmap(
        customers
    )
)


st.plotly_chart(
    alignment_fig,
    width="stretch",
    key="model_alignment_matrix",
    config={
        "displayModeBar": False
    },
)


# ---------------------------------------------------------
# Agreement by segment + uncertainty overlap
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Assignment Agreement and Uncertainty"
)


agreement_col, uncertainty_col = (
    st.columns(
        2,
        gap="large",
    )
)


with agreement_col:

    st.markdown(
        "#### Agreement by K-Means Segment"
    )

    st.caption(
        (
            "Shows where corresponding K-Means "
            "and GMM group assignments are most "
            "and least consistent."
        )
    )

    agreement_fig = (
        agreement_by_segment_chart(
            customers
        )
    )

    st.plotly_chart(
        agreement_fig,
        width="stretch",
        key="agreement_by_segment",
        config={
            "displayModeBar": False
        },
    )


with uncertainty_col:

    st.markdown(
        "#### Uncertain-Customer Overlap"
    )

    st.caption(
        (
            "Compares customers flagged by the "
            "K-Means boundary criteria with those "
            "flagged by the GMM ambiguity criteria."
        )
    )

    overlap_fig = (
        uncertainty_overlap_chart(
            customers
        )
    )

    st.plotly_chart(
        overlap_fig,
        width="stretch",
        key="uncertainty_overlap",
        config={
            "displayModeBar": False
        },
    )


# ---------------------------------------------------------
# Agreement table by segment
# ---------------------------------------------------------

agreement_table = (
    customers.groupby(
        "Segment_Name",
        as_index=False,
        observed=True,
    )
    .agg(
        Customers=(
            "CustomerID",
            "nunique"
        ),
        Agreeing_Customers=(
            "Models_Agree_After_Alignment",
            "sum"
        ),
        Agreement=(
            "Models_Agree_After_Alignment",
            "mean"
        ),
    )
)


agreement_table[
    "Agreement"
] = (
    agreement_table[
        "Agreement"
    ]
    * 100
)


agreement_table = (
    agreement_table
    .sort_values(
        "Agreement",
        ascending=False,
    )
)


agreement_table = agreement_table.rename(
    columns={
        "Segment_Name":
            "K-Means Segment",

        "Agreeing_Customers":
            "Aligned Customers",

        "Agreement":
            "Agreement Percentage",
    }
)


agreement_display = (
    agreement_table.copy()
)


agreement_display[
    "Agreement Percentage"
] = agreement_display[
    "Agreement Percentage"
].map(
    lambda value:
        f"{value:.2f}%"
)


st.dataframe(
    agreement_display,
    hide_index=True,
    width="stretch",
)


# ---------------------------------------------------------
# Final model decision
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Final Model Decision"
)


decision1, decision2 = st.columns(
    2,
    gap="large",
)


with decision1:

    with st.container(
        border=True
    ):

        st.markdown(
            ":blue-badge[PRIMARY OPERATIONAL MODEL]"
        )

        st.markdown(
            "## K-Means K=5"
        )

        st.markdown(
            """
            **Why it remains primary**

            - stronger common internal validation;
            - near-perfect random-seed stability;
            - strong subsampling stability;
            - clear hard customer assignments;
            - five commercially interpretable profiles;
            - direct connection to the final business
              strategy mapping.
            """
        )


with decision2:

    with st.container(
        border=True
    ):

        st.markdown(
            ":violet-badge[SUPPORTING ANALYTICAL MODEL]"
        )

        st.markdown(
            "## GMM C5 Spherical"
        )

        st.markdown(
            """
            **Why it is retained**

            - very strong repeated-run stability;
            - membership probabilities;
            - second-most likely component;
            - probability margin;
            - entropy-based uncertainty evidence;
            - independent comparison with the
              K-Means segmentation.
            """
        )


# ---------------------------------------------------------
# Final conclusion
# ---------------------------------------------------------

st.success(
    (
        "K-Means K=5 is retained as the primary "
        "operational segmentation. GMM C5 Spherical "
        "is retained as a supporting probabilistic "
        "evidence layer rather than as a replacement "
        "for the operational K-Means model."
    )
)