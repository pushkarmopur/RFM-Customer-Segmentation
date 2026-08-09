import pandas as pd
import streamlit as st

from components.data_loader import (
    load_dashboard_data,
)

from components.metrics import (
    total_customers,
    total_monetary,
    high_value_customer_percentage,
    high_value_monetary_percentage,
    average_monetary_per_customer,
    median_customer_monetary,
    compact_currency,
    currency,
    percentage,
)

from components.charts import (
    SEGMENT_ORDER,
    build_segment_summary,
    monetary_contribution_chart,
    customer_vs_monetary_share_chart,
    frequency_monetary_scatter,
    aov_basket_scatter,
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
    segment_summary_file,
    strategy_mapping,
) = load_dashboard_data()


# ---------------------------------------------------------
# Page heading
# ---------------------------------------------------------

page_header(
    "Customer Value & Revenue",
    (
        "Explore commercial contribution, revenue "
        "concentration and customer purchasing value "
        "across the final K-Means segments."
    ),
)


# ---------------------------------------------------------
# Overall portfolio results
# ---------------------------------------------------------

portfolio_monetary = (
    total_monetary(
        customers
    )
)


high_value_customer_pct = (
    high_value_customer_percentage(
        customers
    )
)


high_value_revenue_pct = (
    high_value_monetary_percentage(
        customers
    )
)


# ---------------------------------------------------------
# Portfolio headline KPIs
# ---------------------------------------------------------

st.markdown(
    "### Commercial Overview"
)


kpi1, kpi2, kpi3 = st.columns(
    3,
    gap="medium",
)


with kpi1:

    st.metric(
        label="Total Monetary Value",
        value=compact_currency(
            portfolio_monetary
        ),
        border=True,
        help=(
            "Total observed Monetary value "
            "across all final customer records."
        ),
    )


with kpi2:

    st.metric(
        label="High-Value Customers",
        value=percentage(
            high_value_customer_pct
        ),
        border=True,
        help=(
            "Combined customer share of "
            "High-Value Loyal Customers and "
            "High-Value Large-Order Buyers."
        ),
    )


with kpi3:

    st.metric(
        label="High-Value Monetary Contribution",
        value=percentage(
            high_value_revenue_pct
        ),
        border=True,
        help=(
            "Combined Monetary contribution "
            "of the two high-value segments."
        ),
    )


# ---------------------------------------------------------
# Main commercial insight
# ---------------------------------------------------------

st.write("")


with st.container(
    border=True
):

    st.markdown(
        ":green-badge[COMMERCIAL CONCENTRATION]"
    )

    st.markdown(
        f"""
        ### {high_value_customer_pct:.2f}% of customers
        generate {high_value_revenue_pct:.2f}% of
        total observed Monetary value
        """
    )

    st.caption(
        "High-Value Loyal Customers + "
        "High-Value Large-Order Buyers"
    )


# ---------------------------------------------------------
# Segment filters
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Explore Customer Value"
)


filter_container = st.container(
    border=True
)


with filter_container:

    filter1, filter2 = st.columns(
        [2, 1],
        gap="large",
    )


    with filter1:

        available_segments = [
            segment
            for segment in SEGMENT_ORDER
            if segment
            in customers[
                "Segment_Name"
            ].unique()
        ]


        selected_segments = st.multiselect(
            "Customer segments",
            options=available_segments,
            default=available_segments,
            key="value_segment_filter",
            help=(
                "Choose the K-Means customer "
                "segments included in the detailed "
                "commercial analysis below."
            ),
        )


    with filter2:

        use_log_scale = st.checkbox(
            "Use logarithmic scatter axes",
            value=True,
            key="value_log_scales",
            help=(
                "Logarithmic axes make the strongly "
                "right-skewed customer-value "
                "distributions easier to inspect."
            ),
        )


# ---------------------------------------------------------
# Apply customer filter
# ---------------------------------------------------------

filtered_customers = customers[
    customers[
        "Segment_Name"
    ].isin(
        selected_segments
    )
].copy()


if filtered_customers.empty:

    st.warning(
        "Select at least one customer segment "
        "to continue the value analysis."
    )

    st.stop()


# ---------------------------------------------------------
# Selected portfolio KPIs
# ---------------------------------------------------------

selected_count = total_customers(
    filtered_customers
)


selected_average_value = (
    average_monetary_per_customer(
        filtered_customers
    )
)


selected_median_value = (
    median_customer_monetary(
        filtered_customers
    )
)


selected_total_value = (
    total_monetary(
        filtered_customers
    )
)


st.write("")

st.markdown(
    "### Current Selection"
)


selection1, selection2, selection3, selection4 = (
    st.columns(
        4,
        gap="medium",
    )
)


with selection1:

    st.metric(
        label="Customers in Selection",
        value=f"{selected_count:,}",
        border=True,
    )


with selection2:

    st.metric(
        label="Monetary Value in Selection",
        value=compact_currency(
            selected_total_value
        ),
        border=True,
    )


with selection3:

    st.metric(
        label="Average Monetary per Customer",
        value=currency(
            selected_average_value
        ),
        border=True,
        help=(
            "Mean customer Monetary value. "
            "This can be influenced by extreme "
            "high-value customers."
        ),
    )


with selection4:

    st.metric(
        label="Median Customer Monetary",
        value=currency(
            selected_median_value
        ),
        border=True,
        help=(
            "Median Monetary value provides a "
            "more typical customer value when "
            "extreme customers are retained."
        ),
    )


# ---------------------------------------------------------
# Build portfolio-level segment summary
# ---------------------------------------------------------

full_summary = build_segment_summary(
    customers
)


visible_summary = full_summary[
    full_summary[
        "Segment_Name"
    ].isin(
        selected_segments
    )
].copy()


# ---------------------------------------------------------
# Segment-level value charts
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Segment Commercial Contribution"
)


chart1, chart2 = st.columns(
    2,
    gap="large",
)


with chart1:

    st.markdown(
        "#### Monetary Contribution by Segment"
    )

    st.caption(
        "Contribution to total portfolio "
        "Monetary value."
    )

    fig_revenue = (
        monetary_contribution_chart(
            visible_summary
        )
    )

    st.plotly_chart(
        fig_revenue,
        width="stretch",
        key="value_revenue_segment_chart",
        config={
            "displayModeBar": False
        },
    )


with chart2:

    st.markdown(
        "#### Customer Share versus Monetary Share"
    )

    st.caption(
        "Compares each segment's population "
        "share with its commercial contribution."
    )

    fig_share = (
        customer_vs_monetary_share_chart(
            visible_summary
        )
    )

    st.plotly_chart(
        fig_share,
        width="stretch",
        key="value_share_comparison",
        config={
            "displayModeBar": False
        },
    )


# ---------------------------------------------------------
# Customer purchasing behaviour
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Customer-Level Purchasing Behaviour"
)


st.caption(
    (
        "Each point represents one customer. "
        "Hover over a point to inspect the "
        "customer ID, segment and behavioural "
        "measures."
    )
)


scatter1, scatter2 = st.columns(
    2,
    gap="large",
)


with scatter1:

    st.markdown(
        "#### Purchase Frequency versus Monetary Value"
    )

    st.caption(
        (
            "Shows how repeated purchasing relates "
            "to total observed customer value."
        )
    )

    frequency_fig = (
        frequency_monetary_scatter(
            filtered_customers,
            log_axes=use_log_scale,
        )
    )

    st.plotly_chart(
        frequency_fig,
        width="stretch",
        key="frequency_monetary_scatter",
        config={
            "displayModeBar": False
        },
    )


with scatter2:

    st.markdown(
        "#### Average Order Value versus Basket Size"
    )

    st.caption(
        (
            "Bubble size represents total customer "
            "Monetary value and helps distinguish "
            "large-order behaviour."
        )
    )

    basket_fig = (
        aov_basket_scatter(
            filtered_customers,
            log_axes=use_log_scale,
        )
    )

    st.plotly_chart(
        basket_fig,
        width="stretch",
        key="aov_basket_scatter",
        config={
            "displayModeBar": False
        },
    )


# ---------------------------------------------------------
# Interpretation note
# ---------------------------------------------------------

st.info(
    (
        "High-Value Loyal Customers are expected "
        "to combine high purchase frequency with "
        "high total Monetary value. High-Value "
        "Large-Order Buyers are differentiated "
        "more strongly by Average Order Value and "
        "Basket Size than by purchase frequency."
    )
)


# ---------------------------------------------------------
# Customer ranking
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Highest-Value Customers"
)


st.caption(
    (
        "Rank customers by observed Monetary value "
        "within the currently selected segment set."
    )
)


ranking_controls1, ranking_controls2 = (
    st.columns(
        [1, 2],
        gap="large",
    )
)


with ranking_controls1:

    top_n = st.selectbox(
        "Number of customers",
        options=[
            10,
            20,
            50,
            100,
        ],
        index=1,
        key="value_top_n",
    )


with ranking_controls2:

    customer_search = st.text_input(
        "Optional Customer ID search",
        value="",
        placeholder=(
            "Enter part or all of a Customer ID"
        ),
        key="value_customer_search",
    )


# ---------------------------------------------------------
# Prepare ranking table
# ---------------------------------------------------------

ranking_data = (
    filtered_customers
    .sort_values(
        "Monetary",
        ascending=False,
    )
    .copy()
)


if customer_search.strip():

    ranking_data = ranking_data[
        ranking_data[
            "CustomerID"
        ]
        .astype(str)
        .str.contains(
            customer_search.strip(),
            case=False,
            na=False,
        )
    ]


ranking_data = ranking_data.head(
    top_n
)


ranking_table = ranking_data[
    [
        "CustomerID",
        "Segment_Name",
        "Monetary",
        "Frequency",
        "Recency",
        "AverageOrderValue",
        "BasketSize",
        "ProductDiversity",
        "TotalQuantity",
    ]
].copy()


ranking_table = ranking_table.rename(
    columns={
        "CustomerID":
            "Customer ID",

        "Segment_Name":
            "Customer Segment",

        "Monetary":
            "Monetary Value",

        "Frequency":
            "Frequency",

        "Recency":
            "Recency",

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


# ---------------------------------------------------------
# Format ranking values
# ---------------------------------------------------------

ranking_display = (
    ranking_table.copy()
)


ranking_display[
    "Monetary Value"
] = ranking_display[
    "Monetary Value"
].map(
    lambda value:
        f"£{value:,.2f}"
)


ranking_display[
    "Avg. Order Value"
] = ranking_display[
    "Avg. Order Value"
].map(
    lambda value:
        f"£{value:,.2f}"
)


ranking_display[
    "Basket Size"
] = ranking_display[
    "Basket Size"
].map(
    lambda value:
        f"{value:,.1f}"
)


ranking_display[
    "Total Quantity"
] = ranking_display[
    "Total Quantity"
].map(
    lambda value:
        f"{value:,.1f}"
)


st.dataframe(
    ranking_display,
    hide_index=True,
    width="stretch",
)


# ---------------------------------------------------------
# Selected portfolio concentration table
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Segment Value Concentration"
)


st.caption(
    (
        "A value-concentration ratio above 1 "
        "means the segment contributes more "
        "Monetary value than would be expected "
        "from its customer share alone."
    )
)


concentration_table = (
    visible_summary[
        [
            "Segment_Name",
            "Customer_Count",
            "Customer_Share",
            "Monetary_Share",
        ]
    ]
    .copy()
)


concentration_table[
    "Value_Concentration"
] = (
    concentration_table[
        "Monetary_Share"
    ]
    /
    concentration_table[
        "Customer_Share"
    ]
)


concentration_table = (
    concentration_table
    .sort_values(
        "Value_Concentration",
        ascending=False,
    )
)


concentration_table = (
    concentration_table.rename(
        columns={
            "Segment_Name":
                "Customer Segment",

            "Customer_Count":
                "Customers",

            "Customer_Share":
                "Customer Share",

            "Monetary_Share":
                "Monetary Share",

            "Value_Concentration":
                "Value Concentration Index",
        }
    )
)


concentration_display = (
    concentration_table.copy()
)


concentration_display[
    "Customer Share"
] = concentration_display[
    "Customer Share"
].map(
    lambda value:
        f"{value:.2f}%"
)


concentration_display[
    "Monetary Share"
] = concentration_display[
    "Monetary Share"
].map(
    lambda value:
        f"{value:.2f}%"
)


concentration_display[
    "Value Concentration Index"
] = concentration_display[
    "Value Concentration Index"
].map(
    lambda value:
        f"{value:.2f}"
)


st.dataframe(
    concentration_display,
    hide_index=True,
    width="stretch",
)


# ---------------------------------------------------------
# Download filtered customer population
# ---------------------------------------------------------

st.write("")

st.markdown(
    "### Export Commercial Analysis Data"
)


st.caption(
    (
        "Download the customer records currently "
        "included in the commercial analysis."
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
]


download_csv = (
    filtered_customers[
        download_columns
    ]
    .sort_values(
        "Monetary",
        ascending=False,
    )
    .to_csv(
        index=False
    )
)


st.download_button(
    label="Download Commercial Customer Data",
    data=download_csv,
    file_name=(
        "customer_value_revenue_analysis.csv"
    ),
    mime="text/csv",
    key="download_commercial_data",
)