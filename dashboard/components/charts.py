from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components.styles import SEGMENT_COLORS


# ---------------------------------------------------------
# Consistent K-Means segment ordering
# ---------------------------------------------------------

SEGMENT_ORDER = [
    "Dormant Occasional Customers",
    "Active Regular Customers",
    "High-Value Loyal Customers",
    "Low-Value Infrequent Customers",
    "High-Value Large-Order Buyers",
]


# ---------------------------------------------------------
# Shared chart layout
# ---------------------------------------------------------

def apply_chart_layout(
    fig: go.Figure,
    title: str | None = None,
    height: int = 430,
):

    fig.update_layout(
        title=dict(
            text=title if title else ""
        ),
        height=height,
        margin=dict(
            l=20,
            r=20,
            t=50 if title else 25,
            b=20,
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial",
            size=13,
            color="#1F2937",
        ),
        legend_title_text="",
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
        ),
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#F1F5F9",
        zeroline=False,
        automargin=True,
    )

    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        automargin=True,
    )

    return fig


# ---------------------------------------------------------
# Build segment-level portfolio summary directly
# from the customer-level dashboard dataset
# ---------------------------------------------------------

def build_segment_summary(
    df: pd.DataFrame
) -> pd.DataFrame:

    summary = (
        df.groupby(
            "Segment_Name",
            as_index=False,
            observed=True,
        )
        .agg(
            Customer_Count=(
                "CustomerID",
                "nunique"
            ),
            Total_Monetary=(
                "Monetary",
                "sum"
            ),
        )
    )

    total_customers = (
        summary["Customer_Count"].sum()
    )

    total_monetary = (
        summary["Total_Monetary"].sum()
    )

    summary["Customer_Share"] = (
        summary["Customer_Count"]
        / total_customers
        * 100
    )

    summary["Monetary_Share"] = (
        summary["Total_Monetary"]
        / total_monetary
        * 100
    )

    return summary


# ---------------------------------------------------------
# Customers by segment
# ---------------------------------------------------------

def customers_by_segment_chart(
    summary: pd.DataFrame
) -> go.Figure:

    plot_df = summary.sort_values(
        "Customer_Count",
        ascending=True,
    )

    fig = px.bar(
        plot_df,
        x="Customer_Count",
        y="Segment_Name",
        orientation="h",
        color="Segment_Name",
        color_discrete_map=SEGMENT_COLORS,
        text="Customer_Count",
        custom_data=[
            "Customer_Share",
            "Monetary_Share",
        ],
    )

    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Customers: %{x:,}<br>"
            "Customer share: "
            "%{customdata[0]:.2f}%<br>"
            "Monetary contribution: "
            "%{customdata[1]:.2f}%"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Customers",
        yaxis_title="",
    )

    return apply_chart_layout(
        fig,
        height=430,
    )


# ---------------------------------------------------------
# Monetary contribution by segment
# ---------------------------------------------------------

def monetary_contribution_chart(
    summary: pd.DataFrame
) -> go.Figure:

    plot_df = summary.sort_values(
        "Monetary_Share",
        ascending=True,
    )

    fig = px.bar(
        plot_df,
        x="Monetary_Share",
        y="Segment_Name",
        orientation="h",
        color="Segment_Name",
        color_discrete_map=SEGMENT_COLORS,
        text="Monetary_Share",
        custom_data=[
            "Total_Monetary",
            "Customer_Share",
        ],
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Monetary contribution: "
            "%{x:.2f}%<br>"
            "Monetary value: "
            "£%{customdata[0]:,.2f}<br>"
            "Customer share: "
            "%{customdata[1]:.2f}%"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Share of total Monetary value (%)",
        yaxis_title="",
    )

    return apply_chart_layout(
        fig,
        height=430,
    )


# ---------------------------------------------------------
# Customer share vs Monetary share
# ---------------------------------------------------------

def customer_vs_monetary_share_chart(
    summary: pd.DataFrame
) -> go.Figure:

    plot_df = summary.copy()

    category_order = [
        segment
        for segment in SEGMENT_ORDER
        if segment in plot_df["Segment_Name"].tolist()
    ]

    plot_df["Segment_Name"] = pd.Categorical(
        plot_df["Segment_Name"],
        categories=category_order,
        ordered=True,
    )

    plot_df = plot_df.sort_values(
        "Segment_Name"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Customer Share",
            x=plot_df["Segment_Name"],
            y=plot_df["Customer_Share"],
            marker_color="#2563EB",
            text=plot_df["Customer_Share"],
            texttemplate="%{text:.2f}%",
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Customer share: %{y:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Bar(
            name="Monetary Contribution",
            x=plot_df["Segment_Name"],
            y=plot_df["Monetary_Share"],
            marker_color="#059669",
            text=plot_df["Monetary_Share"],
            texttemplate="%{text:.2f}%",
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Monetary contribution: "
                "%{y:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        barmode="group",
        xaxis_title="",
        yaxis_title="Share of portfolio (%)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="left",
            x=0,
        ),
    )

    fig.update_xaxes(
        tickangle=-20,
    )

    return apply_chart_layout(
        fig,
        height=500,
    )



# =========================================================
# PAGE 2 - CUSTOMER SEGMENT PROFILE VISUALS
# =========================================================


PROFILE_FEATURES = [
    "Recency",
    "Frequency",
    "Monetary",
    "AverageOrderValue",
    "BasketSize",
    "ProductDiversity",
    "TotalQuantity",
]


PROFILE_LABELS = {
    "Recency": "Recency",
    "Frequency": "Frequency",
    "Monetary": "Monetary",
    "AverageOrderValue": "Avg. Order Value",
    "BasketSize": "Basket Size",
    "ProductDiversity": "Product Diversity",
    "TotalQuantity": "Total Quantity",
}


# ---------------------------------------------------------
# Format original-scale profile values
# ---------------------------------------------------------

def format_profile_value(
    feature: str,
    value: float,
) -> str:

    if feature in [
        "Monetary",
        "AverageOrderValue",
    ]:
        return f"£{value:,.2f}"

    if feature in [
        "BasketSize",
        "TotalQuantity",
    ]:
        return f"{value:,.1f}"

    return f"{value:,.0f}"


# ---------------------------------------------------------
# Selected segment vs overall median
# ---------------------------------------------------------

def segment_profile_index_chart(
    df: pd.DataFrame,
    selected_segment: str,
) -> go.Figure:

    selected_df = df[
        df["Segment_Name"]
        == selected_segment
    ]

    rows = []

    for feature in PROFILE_FEATURES:

        selected_median = float(
            selected_df[feature].median()
        )

        overall_median = float(
            df[feature].median()
        )

        if overall_median == 0:
            profile_index = 0.0
        else:
            profile_index = (
                selected_median
                / overall_median
                * 100
            )

        rows.append(
            {
                "Feature":
                    PROFILE_LABELS[feature],

                "Feature_Name":
                    feature,

                "Profile_Index":
                    profile_index,

                "Selected_Median":
                    selected_median,

                "Overall_Median":
                    overall_median,

                "Selected_Display":
                    format_profile_value(
                        feature,
                        selected_median,
                    ),

                "Overall_Display":
                    format_profile_value(
                        feature,
                        overall_median,
                    ),
            }
        )

    plot_df = pd.DataFrame(rows)

    segment_colour = SEGMENT_COLORS.get(
        selected_segment,
        "#2563EB",
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=plot_df["Profile_Index"],
            y=plot_df["Feature"],
            orientation="h",
            marker_color=segment_colour,
            text=plot_df["Profile_Index"],
            texttemplate="%{text:.0f}",
            textposition="outside",
            cliponaxis=False,
            customdata=plot_df[
                [
                    "Selected_Display",
                    "Overall_Display",
                ]
            ].to_numpy(),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Profile index: %{x:.1f}<br>"
                "Selected segment median: "
                "%{customdata[0]}<br>"
                "Overall customer median: "
                "%{customdata[1]}"
                "<extra></extra>"
            ),
        )
    )

    fig.add_vline(
        x=100,
        line_width=2,
        line_dash="dash",
        line_color="#94A3B8",
        annotation_text="Overall median",
        annotation_position="top",
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title=(
            "Profile index "
            "(overall customer median = 100)"
        ),
        yaxis_title="",
    )

    fig.update_yaxes(
        autorange="reversed"
    )

    fig.update_xaxes(
        rangemode="tozero"
    )

    return apply_chart_layout(
        fig,
        height=500,
    )


# ---------------------------------------------------------
# All-segment median heatmap
# ---------------------------------------------------------

def segment_median_heatmap(
    df: pd.DataFrame,
) -> go.Figure:

    medians = (
        df.groupby(
            "Segment_Name",
            observed=True,
        )[PROFILE_FEATURES]
        .median()
    )

    available_segments = [
        segment
        for segment in SEGMENT_ORDER
        if segment in medians.index
    ]

    medians = medians.reindex(
        available_segments
    )

    # Rank each feature separately.
    # Colour means relative magnitude,
    # not whether the value is good/bad.
    relative_rank = (
        medians.rank(
            pct=True,
            axis=0,
        )
        * 100
    )

    display_text = []

    for segment in medians.index:

        row = []

        for feature in PROFILE_FEATURES:

            value = float(
                medians.loc[
                    segment,
                    feature
                ]
            )

            row.append(
                format_profile_value(
                    feature,
                    value,
                )
            )

        display_text.append(row)

    feature_labels = [
        PROFILE_LABELS[feature]
        for feature in PROFILE_FEATURES
    ]

    fig = go.Figure(
        data=go.Heatmap(
            z=relative_rank.values,
            x=feature_labels,
            y=medians.index.tolist(),
            text=display_text,
            texttemplate="%{text}",
            colorscale=[
                [0.00, "#EFF6FF"],
                [0.25, "#DBEAFE"],
                [0.50, "#93C5FD"],
                [0.75, "#3B82F6"],
                [1.00, "#1D4ED8"],
            ],
            zmin=20,
            zmax=100,
            colorbar=dict(
                title="Relative<br>level",
                tickvals=[
                    20,
                    40,
                    60,
                    80,
                    100,
                ],
            ),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "%{x}<br>"
                "Median: %{text}"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
    )

    fig.update_xaxes(
        tickangle=-20,
        showgrid=False,
    )

    fig.update_yaxes(
        showgrid=False,
        autorange="reversed",
    )

    return apply_chart_layout(
        fig,
        height=450,
    )



# =========================================================
# PAGE 3 - CUSTOMER VALUE & REVENUE VISUALS
# =========================================================


# ---------------------------------------------------------
# Frequency versus Monetary
# ---------------------------------------------------------

def frequency_monetary_scatter(
    df: pd.DataFrame,
    log_axes: bool = True,
) -> go.Figure:

    plot_df = df.copy()

    fig = px.scatter(
        plot_df,
        x="Frequency",
        y="Monetary",
        color="Segment_Name",
        color_discrete_map=SEGMENT_COLORS,
        hover_name="CustomerID",
        hover_data={
            "Segment_Name": False,
            "Recency": True,
            "Frequency": True,
            "Monetary": ":,.2f",
            "AverageOrderValue": ":,.2f",
            "BasketSize": ":,.1f",
            "ProductDiversity": True,
            "TotalQuantity": ":,.1f",
        },
        opacity=0.65,
        log_x=log_axes,
        log_y=log_axes,
        render_mode="webgl",
    )

    fig.update_traces(
        marker=dict(
            size=8,
            line=dict(
                width=0.3,
                color="white",
            ),
        )
    )

    fig.update_layout(
        xaxis_title=(
            "Purchase Frequency"
            + (
                " — logarithmic scale"
                if log_axes
                else ""
            )
        ),
        yaxis_title=(
            "Customer Monetary Value (£)"
            + (
                " — logarithmic scale"
                if log_axes
                else ""
            )
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
    )

    return apply_chart_layout(
        fig,
        height=570,
    )


# ---------------------------------------------------------
# Average Order Value versus Basket Size
# ---------------------------------------------------------

def aov_basket_scatter(
    df: pd.DataFrame,
    log_axes: bool = True,
) -> go.Figure:

    plot_df = df.copy()

    fig = px.scatter(
        plot_df,
        x="AverageOrderValue",
        y="BasketSize",
        color="Segment_Name",
        size="Monetary",
        color_discrete_map=SEGMENT_COLORS,
        hover_name="CustomerID",
        hover_data={
            "Segment_Name": False,
            "Monetary": ":,.2f",
            "Frequency": True,
            "Recency": True,
            "AverageOrderValue": ":,.2f",
            "BasketSize": ":,.1f",
            "ProductDiversity": True,
            "TotalQuantity": ":,.1f",
        },
        opacity=0.60,
        size_max=30,
        log_x=log_axes,
        log_y=log_axes,
        render_mode="webgl",
    )

    fig.update_layout(
        xaxis_title=(
            "Average Order Value (£)"
            + (
                " — logarithmic scale"
                if log_axes
                else ""
            )
        ),
        yaxis_title=(
            "Average Basket Size (units)"
            + (
                " — logarithmic scale"
                if log_axes
                else ""
            )
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
    )

    return apply_chart_layout(
        fig,
        height=570,
    )


# =========================================================
# PAGE 4 - CUSTOMER CONFIDENCE VISUALS
# =========================================================


# ---------------------------------------------------------
# Confidence category colour helper
# ---------------------------------------------------------

def confidence_colour_map(
    categories
):

    colour_map = {}

    for category in categories:

        category_text = str(
            category
        ).lower()

        if (
            "strong" in category_text
            or "high" in category_text
        ):
            colour = "#059669"

        elif (
            "moderate" in category_text
            or "medium" in category_text
        ):
            colour = "#D97706"

        elif (
            "boundary" in category_text
            or "ambiguous" in category_text
            or "low" in category_text
            or "review" in category_text
        ):
            colour = "#DC2626"

        else:
            colour = "#64748B"

        colour_map[
            category
        ] = colour

    return colour_map


# ---------------------------------------------------------
# Confidence category distribution
# ---------------------------------------------------------

def confidence_distribution_chart(
    df: pd.DataFrame,
    category_column: str,
) -> go.Figure:

    counts = (
        df[
            category_column
        ]
        .value_counts(
            dropna=False
        )
        .rename_axis(
            "Confidence"
        )
        .reset_index(
            name="Customers"
        )
    )

    counts[
        "Percentage"
    ] = (
        counts["Customers"]
        / counts["Customers"].sum()
        * 100
    )

    colour_map = (
        confidence_colour_map(
            counts[
                "Confidence"
            ].tolist()
        )
    )

    fig = px.bar(
        counts,
        x="Customers",
        y="Confidence",
        orientation="h",
        color="Confidence",
        color_discrete_map=colour_map,
        text="Percentage",
        custom_data=[
            "Customers"
        ],
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Customers: %{customdata[0]:,}<br>"
            "Share: %{text:.2f}%"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Customers",
        yaxis_title="",
    )

    return apply_chart_layout(
        fig,
        height=350,
    )


# ---------------------------------------------------------
# K-Means confidence scatter
# ---------------------------------------------------------

def kmeans_confidence_scatter(
    df: pd.DataFrame,
) -> go.Figure:

    categories = (
        df[
            "Assignment_Confidence_Category"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    colour_map = (
        confidence_colour_map(
            categories
        )
    )

    fig = px.scatter(
        df,
        x="Relative_Centroid_Margin",
        y="Silhouette_Value_KMeans",
        color="Assignment_Confidence_Category",
        color_discrete_map=colour_map,
        hover_name="CustomerID",
        hover_data={
            "Segment_Name": True,
            "Alternative_Segment": True,
            "Relative_Centroid_Margin": ":.4f",
            "Silhouette_Value_KMeans": ":.4f",
            "Monetary": ":,.2f",
            "Frequency": True,
            "Recency": True,
        },
        opacity=0.65,
        render_mode="webgl",
    )

    fig.add_vline(
        x=0.10,
        line_dash="dash",
        line_color="#DC2626",
        annotation_text="Margin = 0.10",
        annotation_position="top",
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="#7C3AED",
        annotation_text="Silhouette = 0",
        annotation_position="top left",
    )

    fig.update_layout(
        xaxis_title=(
            "Relative Centroid Margin"
        ),
        yaxis_title=(
            "Individual K-Means Silhouette"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
    )

    return apply_chart_layout(
        fig,
        height=560,
    )


# ---------------------------------------------------------
# GMM confidence scatter
# ---------------------------------------------------------

def gmm_confidence_scatter(
    df: pd.DataFrame,
) -> go.Figure:

    categories = (
        df[
            "Membership_Confidence_Category"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    colour_map = (
        confidence_colour_map(
            categories
        )
    )

    fig = px.scatter(
        df,
        x="Probability_Margin",
        y="Maximum_Probability",
        color="Membership_Confidence_Category",
        size="Second_Probability",
        color_discrete_map=colour_map,
        hover_name="CustomerID",
        hover_data={
            "GMM_Segment_Name": True,
            "Maximum_Probability": ":.2%",
            "Second_Probability": ":.2%",
            "Probability_Margin": ":.2%",
            "Normalised_Entropy": ":.4f",
            "GMM_Component": True,
            "Alternative_GMM_Component": True,
        },
        opacity=0.65,
        size_max=24,
        render_mode="webgl",
    )

    fig.add_vline(
        x=0.20,
        line_dash="dash",
        line_color="#DC2626",
        annotation_text="Margin = 0.20",
        annotation_position="top",
    )

    fig.add_hline(
        y=0.60,
        line_dash="dash",
        line_color="#7C3AED",
        annotation_text="Max probability = 0.60",
        annotation_position="bottom right",
    )

    fig.update_layout(
        xaxis_title=(
            "Probability Margin"
        ),
        yaxis_title=(
            "Maximum Membership Probability"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
    )

    fig.update_xaxes(
        tickformat=".0%"
    )

    fig.update_yaxes(
        tickformat=".0%"
    )

    return apply_chart_layout(
        fig,
        height=560,
    )



# =========================================================
# PAGE 5 - MODEL COMPARISON VISUALS
# =========================================================


GMM_SEGMENT_ORDER = [
    "Dormant Occasional Customers",
    "Active Regular Customers",
    "High-Value Loyal Customers",
    "Low-Value Infrequent Customers",
    "Elite High-Value Customers",
]


# ---------------------------------------------------------
# Stability comparison
# ---------------------------------------------------------

def model_stability_chart(
    model_metrics: pd.DataFrame,
) -> go.Figure:

    stability_metrics = [
        "Mean Random-Seed ARI",
        "Minimum Random-Seed ARI",
        "Mean 80% Subsampling ARI",
        "Minimum 80% Subsampling ARI",
    ]

    plot_df = model_metrics[
        model_metrics[
            "Metric"
        ].isin(
            stability_metrics
        )
    ].copy()

    long_df = plot_df.melt(
        id_vars=["Metric"],
        value_vars=[
            "KMeans_K5",
            "GMM_C5_Spherical",
        ],
        var_name="Model",
        value_name="ARI",
    )

    long_df["Model"] = (
        long_df["Model"]
        .replace(
            {
                "KMeans_K5":
                    "K-Means K=5",

                "GMM_C5_Spherical":
                    "GMM C5 Spherical",
            }
        )
    )

    long_df["Metric"] = pd.Categorical(
        long_df["Metric"],
        categories=stability_metrics,
        ordered=True,
    )

    long_df = long_df.sort_values(
        "Metric"
    )

    fig = px.bar(
        long_df,
        x="Metric",
        y="ARI",
        color="Model",
        barmode="group",
        text="ARI",
        color_discrete_map={
            "K-Means K=5": "#2563EB",
            "GMM C5 Spherical": "#7C3AED",
        },
    )

    fig.update_traces(
        texttemplate="%{text:.4f}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "%{fullData.name}: %{y:.4f}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="Adjusted Rand Index",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="left",
            x=0,
        ),
    )

    fig.update_yaxes(
        range=[0, 1.05]
    )

    fig.update_xaxes(
        tickangle=-15
    )

    return apply_chart_layout(
        fig,
        height=500,
    )


# ---------------------------------------------------------
# K-Means versus aligned GMM overlap matrix
# ---------------------------------------------------------

def model_alignment_heatmap(
    df: pd.DataFrame,
) -> go.Figure:

    matrix = pd.crosstab(
        df["Segment_Name"],
        df["GMM_Segment_Name"],
    )

    row_order = [
        segment
        for segment in SEGMENT_ORDER
        if segment in matrix.index
    ]

    column_order = [
        segment
        for segment in GMM_SEGMENT_ORDER
        if segment in matrix.columns
    ]

    matrix = matrix.reindex(
        index=row_order,
        columns=column_order,
        fill_value=0,
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=matrix.values,
            x=matrix.columns.tolist(),
            y=matrix.index.tolist(),
            text=matrix.values,
            texttemplate="%{text:,}",
            colorscale=[
                [0.00, "#F8FAFC"],
                [0.20, "#DBEAFE"],
                [0.45, "#93C5FD"],
                [0.70, "#3B82F6"],
                [1.00, "#1D4ED8"],
            ],
            colorbar=dict(
                title="Customers"
            ),
            hovertemplate=(
                "<b>K-Means:</b> %{y}<br>"
                "<b>GMM:</b> %{x}<br>"
                "Customers: %{z:,}"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        xaxis_title="GMM C5 Spherical Segment",
        yaxis_title="K-Means K=5 Segment",
    )

    fig.update_xaxes(
        tickangle=-25,
        showgrid=False,
    )

    fig.update_yaxes(
        showgrid=False,
        autorange="reversed",
    )

    return apply_chart_layout(
        fig,
        height=580,
    )


# ---------------------------------------------------------
# Agreement by K-Means segment
# ---------------------------------------------------------

def agreement_by_segment_chart(
    df: pd.DataFrame,
) -> go.Figure:

    agreement = (
        df.groupby(
            "Segment_Name",
            as_index=False,
            observed=True,
        )
        .agg(
            Customers=(
                "CustomerID",
                "nunique"
            ),
            Agreement=(
                "Models_Agree_After_Alignment",
                "mean"
            ),
        )
    )

    agreement[
        "Agreement_Percentage"
    ] = (
        agreement["Agreement"]
        * 100
    )

    agreement = agreement.sort_values(
        "Agreement_Percentage",
        ascending=True,
    )

    fig = px.bar(
        agreement,
        x="Agreement_Percentage",
        y="Segment_Name",
        orientation="h",
        color="Segment_Name",
        color_discrete_map=SEGMENT_COLORS,
        text="Agreement_Percentage",
        custom_data=["Customers"],
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Aligned agreement: %{x:.2f}%<br>"
            "Customers: %{customdata[0]:,}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Aligned Customer Agreement (%)",
        yaxis_title="",
    )

    fig.update_xaxes(
        range=[0, 105]
    )

    return apply_chart_layout(
        fig,
        height=430,
    )


# ---------------------------------------------------------
# Cross-model uncertainty overlap
# ---------------------------------------------------------

def uncertainty_overlap_chart(
    df: pd.DataFrame,
) -> go.Figure:

    kmeans_flag = (
        df[
            "Combined_Boundary_Flag"
        ]
    )

    gmm_flag = (
        df[
            "Combined_Ambiguous_Flag"
        ]
    )

    categories = pd.Series(
        "Flagged by neither model",
        index=df.index,
    )

    categories.loc[
        kmeans_flag
        &
        ~gmm_flag
    ] = "K-Means review only"

    categories.loc[
        ~kmeans_flag
        &
        gmm_flag
    ] = "GMM ambiguous only"

    categories.loc[
        kmeans_flag
        &
        gmm_flag
    ] = "Flagged by both models"

    counts = (
        categories
        .value_counts()
        .rename_axis(
            "Review_Group"
        )
        .reset_index(
            name="Customers"
        )
    )

    desired_order = [
        "Flagged by neither model",
        "K-Means review only",
        "GMM ambiguous only",
        "Flagged by both models",
    ]

    counts[
        "Review_Group"
    ] = pd.Categorical(
        counts[
            "Review_Group"
        ],
        categories=desired_order,
        ordered=True,
    )

    counts = counts.sort_values(
        "Review_Group"
    )

    counts[
        "Percentage"
    ] = (
        counts["Customers"]
        / len(df)
        * 100
    )

    colour_map = {
        "Flagged by neither model":
            "#059669",

        "K-Means review only":
            "#2563EB",

        "GMM ambiguous only":
            "#D97706",

        "Flagged by both models":
            "#DC2626",
    }

    fig = px.bar(
        counts,
        x="Customers",
        y="Review_Group",
        orientation="h",
        color="Review_Group",
        color_discrete_map=colour_map,
        text="Customers",
        custom_data=[
            "Percentage"
        ],
    )

    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Customers: %{x:,}<br>"
            "Share: %{customdata[0]:.2f}%"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Customers",
        yaxis_title="",
    )

    return apply_chart_layout(
        fig,
        height=400,
    )



# =========================================================
# PAGE 6 - STRATEGY & DECISION SUPPORT VISUALS
# =========================================================


# ---------------------------------------------------------
# Segment value-scale matrix
# ---------------------------------------------------------

def segment_value_scale_matrix(
    summary: pd.DataFrame,
    selected_segment: str | None = None,
) -> go.Figure:

    plot_df = summary.copy()

    short_labels = {
        "Dormant Occasional Customers":
            "Dormant",

        "Active Regular Customers":
            "Active Regular",

        "High-Value Loyal Customers":
            "High-Value Loyal",

        "Low-Value Infrequent Customers":
            "Low-Value",

        "High-Value Large-Order Buyers":
            "Large-Order",
    }

    plot_df["Short_Label"] = (
        plot_df["Segment_Name"]
        .map(short_labels)
    )

    fig = px.scatter(
        plot_df,
        x="Customer_Share",
        y="Monetary_Share",
        size="Customer_Count",
        color="Segment_Name",
        text="Short_Label",
        color_discrete_map=SEGMENT_COLORS,
        size_max=55,
        custom_data=[
            "Customer_Count",
            "Total_Monetary",
        ],
    )

    fig.update_traces(
        textposition="top center",
        marker=dict(
            line=dict(
                width=1,
                color="white",
            )
        ),
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"
            "Customers: %{customdata[0]:,}<br>"
            "Customer share: %{x:.2f}%<br>"
            "Monetary contribution: %{y:.2f}%<br>"
            "Monetary value: £%{customdata[1]:,.2f}"
            "<extra></extra>"
        ),
    )

    # Equal-share reference because five segments
    fig.add_vline(
        x=20,
        line_dash="dash",
        line_color="#94A3B8",
        annotation_text="20% customer-share reference",
        annotation_position="top",
    )

    fig.add_hline(
        y=20,
        line_dash="dash",
        line_color="#94A3B8",
        annotation_text="20% monetary-share reference",
        annotation_position="top left",
    )

    # Highlight selected segment
    if selected_segment is not None:

        selected = plot_df[
            plot_df["Segment_Name"]
            == selected_segment
        ]

        if not selected.empty:

            fig.add_trace(
                go.Scatter(
                    x=selected[
                        "Customer_Share"
                    ],
                    y=selected[
                        "Monetary_Share"
                    ],
                    mode="markers",
                    marker=dict(
                        size=66,
                        color="rgba(0,0,0,0)",
                        line=dict(
                            width=4,
                            color="#111827",
                        ),
                    ),
                    hoverinfo="skip",
                    showlegend=False,
                )
            )

    fig.update_layout(
        xaxis_title="Customer Share (%)",
        yaxis_title="Monetary Contribution (%)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="left",
            x=0,
        ),
    )

    fig.update_xaxes(
        range=[0, 40]
    )

    fig.update_yaxes(
        range=[0, 75]
    )

    return apply_chart_layout(
        fig,
        height=600,
    )