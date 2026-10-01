import streamlit as st
import plotly.express as px
from database import run_query
import queries
import pandas as pd
import os
from utils import format_currency, format_number, show_kpi
from weekly_reports import generate_weekly_report
from database import get_connection

try:
    test_conn = get_connection()
    test_cursor = test_conn.cursor()

    test_cursor.execute("SELECT DATABASE()")
    current_db = test_cursor.fetchone()

    test_cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = test_cursor.fetchone()

    print("====================================")
    print("CURRENT DATABASE:", current_db)
    print("ORDERS COUNT:", order_count)
    print("====================================")

    test_cursor.close()
    test_conn.close()

except Exception as e:
    print("DATABASE TEST ERROR:", e)

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Cart2 Insight",
    page_icon="🛒",
    layout="wide"
)
# ============================================================
# LOAD ALL CLEANED CSV FILES
# ============================================================

import os
import pandas as pd

CLEANED_PATH = r"D:\HCL_PROJECTS\Cart2 Insight\Data\cleaned"

data = {}

if not os.path.exists(CLEANED_PATH):

    st.error(f"❌ Folder not found:\n{CLEANED_PATH}")

else:

    csv_files = [
        file
        for file in os.listdir(CLEANED_PATH)
        if file.lower().endswith(".csv")
    ]

    if len(csv_files) == 0:

        st.error(
            f"❌ No CSV files found in:\n{CLEANED_PATH}"
        )

    else:

        st.success(
            f"✅ Found {len(csv_files)} CSV file(s)"
        )

        for filename in csv_files:

            file_path = os.path.join(
                CLEANED_PATH,
                filename
            )

            try:

                df = pd.read_csv(file_path)

                data[filename] = df

            except Exception as e:

                st.error(
                    f"❌ Error loading {filename}: {e}"
                )
# ============================================================
# DASHBOARD THEME
# ============================================================

st.markdown("""
<style>

/* ============================================================
   MAIN BACKGROUND
   ============================================================ */

.stApp {
    background-color: #0F172A !important;
    color: #F8FAFC !important;
}


/* ============================================================
   MAIN HEADINGS
   ============================================================ */

h1 {
    color: #FFD700 !important;
    font-size: 42px !important;
    font-weight: 800 !important;
}

h2,
h3 {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}


/* ============================================================
   TAB HEADINGS
   ============================================================ */

/* Space between tabs */
[data-baseweb="tab-list"] {
    gap: 12px !important;
}

/* Tab button */
[data-baseweb="tab"] {
    min-height: 85px !important;
    padding: 18px 24px !important;
}

/* Tab text */
[data-baseweb="tab"] [data-testid="stMarkdownContainer"] p {
    color: #FFFFFF !important;
    font-size: 30px !important;
    font-weight: 900 !important;
    line-height: 1.2 !important;
    margin: 0 !important;
}

/* Force icon + text inside tabs to white */
[data-baseweb="tab"] * {
    color: #FFFFFF !important;
}

/* Selected tab */
[data-baseweb="tab"][aria-selected="true"] {
    color: #FFFFFF !important;
}

[data-baseweb="tab"][aria-selected="true"] * {
    color: #FFFFFF !important;
}

[data-baseweb="tab"][aria-selected="true"]
[data-testid="stMarkdownContainer"] p {
    color: #FFFFFF !important;
    font-size: 32px !important;
    font-weight: 900 !important;
}


/* ============================================================
   KPI CARDS
   ============================================================ */

[data-testid="stMetric"] {
    background-color: #1E40AF !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    padding: 15px !important;
}

/* KPI labels */
[data-testid="stMetricLabel"] {
    color: #FFFFFF !important;
    font-size: 16px !important;
    font-weight: 700 !important;
}

/* KPI values */
[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 28px !important;
    font-weight: 800 !important;
}


/* ============================================================
   SUCCESS MESSAGE
   ============================================================ */

div[data-testid="stAlert"] {
    background-color: #065F46 !important;
    border-radius: 8px !important;
}

div[data-testid="stAlert"] p {
    color: #FFFFFF !important;
    font-size: 20px !important;
    font-weight: 700 !important;
}


/* ============================================================
   DATA TABLE
   ============================================================ */

[data-testid="stDataFrame"] {
    font-size: 16px !important;
}


/* ============================================================
   DIVIDER
   ============================================================ */

hr {
    border-color: #475569 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TITLE
# ============================================================

st.title("🛒 Cart2 Insight")
st.subheader("E-Commerce Analytics Dashboard")

st.markdown(
    """
    This dashboard analyzes e-commerce sales, customers,
    sellers, products, delivery performance, and customer
    experience using MySQL and Streamlit.
    """
)
st.markdown("""
    <style>
        /* Tab section headings */
        h2 {
            font-family: 'Poppins', sans-serif;
            font-size: 36px !important;        /* Larger font size */
            font-weight: 800;
            color: #FFD700 !important;         /* Bright gold color */
            text-shadow: 0 0 12px #FFD700, 0 0 24px #FF6B35;  /* Strong glow */
            margin-top: 25px;
            margin-bottom: 15px;
        }

        /* Icons before headings */
        h2::before {
            font-size: 44px;                   /* Bigger icon size */
            margin-right: 10px;
        }

        /* Optional divider for clarity */
        hr {
            border: 1px solid #FFD700;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)


# ============================================================
# TEST DATABASE CONNECTION
# ============================================================

try:
    revenue_df = run_query(queries.TOTAL_REVENUE)
    orders_df = run_query(queries.TOTAL_ORDERS)
    customers_df = run_query(queries.TOTAL_CUSTOMERS)
    sellers_df = run_query(queries.TOTAL_SELLERS)
    aov_df = run_query(queries.AVERAGE_ORDER_VALUE)
    review_df = run_query(queries.AVERAGE_REVIEW_SCORE)
    clv_df = run_query(queries.CUSTOMER_LIFETIME_VALUE)
    st.success("✅ Connected to MySQL database: cart2")

except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()


# ============================================================
# BUSINESS OVERVIEW
# ============================================================

st.header("📊 Business Overview")

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

total_revenue = revenue_df.iloc[0]["total_revenue"]
total_orders = orders_df.iloc[0]["total_orders"]
total_customers = customers_df.iloc[0]["total_customers"]
total_sellers = sellers_df.iloc[0]["total_sellers"]
average_order_value = aov_df.iloc[0]["average_order_value"]
average_review_score = review_df.iloc[0]["average_review_score"]
clv = clv_df.iloc[0]["clv"]


with col1:
    show_kpi(
        "Total Revenue",
        format_currency(total_revenue)
    )

with col2:
    show_kpi(
        "Total Orders",
        format_number(total_orders)
    )

with col3:
    show_kpi(
        "Total Customers",
        format_number(total_customers)
    )

with col4:
    show_kpi(
        "Total Sellers",
        format_number(total_sellers)
    )

with col5:
    show_kpi(
        "Average Order Value",
        format_currency(average_order_value)
    )

with col6:
    show_kpi(
        "Average Review",
        f"{average_review_score:.2f} / 5"
    )

with col7:
    show_kpi("Customer Lifetime Value", format_currency(clv))

st.divider()
# ============================================================
# INTERACTIVE FILTERS
# ============================================================

st.header("🔎 Interactive Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    start_date = st.date_input(
        "Start Date",
        value=pd.to_datetime("2017-01-01").date(),
        key="main_start_date"
    )

with filter_col2:
    end_date = st.date_input(
        "End Date",
        value=pd.to_datetime("2018-08-31").date(),
        key="main_end_date"
    )

with filter_col3:
    category_query = """
    SELECT DISTINCT
        product_category_name_english AS category
    FROM products
    WHERE product_category_name_english IS NOT NULL
    ORDER BY product_category_name_english
    """

    category_df = run_query(category_query)

    categories = ["All Categories"]

    if not category_df.empty:
        categories += (
            category_df["category"]
            .dropna()
            .tolist()
        )

    selected_category = st.selectbox(
        "Product Category",
        categories,
        key="main_category"
    )


region_query = """
SELECT DISTINCT
    customer_state AS region
FROM customers
WHERE customer_state IS NOT NULL
ORDER BY customer_state
"""

region_df = run_query(region_query)

regions = ["All Regions"]

if not region_df.empty:
    regions += (
        region_df["region"]
        .dropna()
        .tolist()
    )

selected_region = st.selectbox(
    "Region",
    regions,
    key="main_region"
)

st.divider()
# ============================================================
# FILTERED SALES QUERY
# ============================================================

filtered_sales_query = f"""
SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.order_purchase_timestamp >= '{start_date}'
AND o.order_purchase_timestamp < DATE_ADD('{end_date}', INTERVAL 1 DAY)
"""

if selected_category != "All Categories":

    filtered_sales_query += f"""
    AND p.product_category_name_english = '{selected_category}'
    """

if selected_region != "All Regions":

    filtered_sales_query += f"""
    AND c.customer_state = '{selected_region}'
    """

filtered_sales_query += """
GROUP BY DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')
ORDER BY month
"""

filtered_sales = run_query(filtered_sales_query)
# ============================================================
# FILTERED CATEGORY REVENUE
# ============================================================

filtered_category_query = f"""
SELECT
    p.product_category_name_english AS category,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.order_purchase_timestamp >= '{start_date}'
AND o.order_purchase_timestamp < DATE_ADD('{end_date}', INTERVAL 1 DAY)
"""

if selected_category != "All Categories":

    filtered_category_query += f"""
    AND p.product_category_name_english = '{selected_category}'
    """

if selected_region != "All Regions":

    filtered_category_query += f"""
    AND c.customer_state = '{selected_region}'
    """

filtered_category_query += """
GROUP BY p.product_category_name_english
ORDER BY revenue DESC
"""

category_revenue = run_query(filtered_category_query)

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    [
        "📈 Sales Analysis",
        "👥 Customer Analysis",
        "🏪 Seller & Product",
        "🚚 Delivery Analysis",
        "⭐ Customer Experience",
        "📋 Data Tables",
        "📂 CSV Reports",
        "📊 Weekly SQL Report"
    ]
)

# ============================================================
# DASHBOARD SECTIONS
# ============================================================# Make tab headings larger and bold
st.markdown("""
<style>

[data-baseweb="tab-list"] {
    gap: 8px !important;
}

[data-baseweb="tab"] {
    min-height: 70px !important;
    padding: 15px 25px !important;
}

[data-baseweb="tab"] p {
    font-size: 26px !important;
    font-weight: 900 !important;
}

[data-baseweb="tab"] div {
    font-size: 26px !important;
    font-weight: 900 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TAB 1 - SALES ANALYSIS
# ============================================================

with tab1:

    st.header("📈 Sales Analysis")

    # --------------------------------------------------------
    # Monthly Revenue - Uses Interactive Filters
    # --------------------------------------------------------

    st.subheader("Monthly Revenue")

    if filtered_sales.empty:

        st.warning("⚠️ No sales data found for the selected filters.")

    else:

        st.line_chart(
            filtered_sales
            .set_index("month")["revenue"]
        )

    # --------------------------------------------------------
    # Revenue by Product Category - Uses Interactive Filters
    # --------------------------------------------------------

    st.subheader("Revenue by Product Category")

    if category_revenue.empty:

        st.warning(
            "⚠️ No category revenue data found for the selected filters."
        )

    else:

        st.bar_chart(
            category_revenue
            .head(10)
            .set_index("category")["revenue"]
        )

    # --------------------------------------------------------
    # Filter Summary
    # --------------------------------------------------------

    st.subheader("🔎 Applied Filters")

    filter_summary_col1, filter_summary_col2, filter_summary_col3 = st.columns(3)

    with filter_summary_col1:
        st.write(f"**Start Date:** {start_date}")

    with filter_summary_col2:
        st.write(f"**End Date:** {end_date}")

    with filter_summary_col3:
        st.write(f"**Category:** {selected_category}")

    st.write(f"**Region:** {selected_region}")
# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

with tab2:

    st.header("👥 Customer Analysis")

    customer_distribution = run_query(
        queries.CUSTOMER_DISTRIBUTION
    )

    repeat_customers = run_query(
        queries.REPEAT_CUSTOMERS
    )

    top_customers = run_query(
        queries.TOP_CUSTOMERS
    )

    st.subheader("Customers by State")

    st.bar_chart(
        customer_distribution.set_index(
            "state"
        )["customer_count"]
    )

    st.subheader("New vs Repeat Customers")

    st.dataframe(
        repeat_customers,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Top 10 Customers by Total Spending")

    top_customers_chart = top_customers.sort_values(
    "total_spending",
    ascending=True
    ).copy()

    top_customers_chart["customer_rank"] = [
    f"Customer {i}"
    for i in range(1, len(top_customers_chart) + 1)
    ]

    fig_top_customers = px.bar(
    top_customers_chart,
    x="total_spending",
    y="customer_rank",
    orientation="h",
    text="total_spending",
    title="Top 10 Customers by Total Spending"
    )

    fig_top_customers.update_layout(
    xaxis_title="Total Spending (₹)",
    yaxis_title="Customer"
    )

    fig_top_customers.update_traces(
    texttemplate="₹%{x:,.0f}",
    textposition="outside"
    )

    st.plotly_chart(
    fig_top_customers,
    use_container_width=True
    )

    st.dataframe(
    top_customers,
    use_container_width=True,
    hide_index=True
    )
# ============================================================
# SELLER & PRODUCT ANALYSIS
# ============================================================

with tab3:

    st.header("🏪 Seller & Product Analysis")

    top_sellers = run_query(
        queries.TOP_SELLERS
    )

    
    top_products = run_query(
        queries.TOP_PRODUCTS
    )

    st.write("TOP PRODUCTS COLUMNS:", top_products.columns.tolist())

    # -------------------------
    # TOP SELLERS
    # -------------------------

    st.subheader("Top 10 Sellers by Revenue")

    top_sellers_chart = top_sellers.sort_values(
    "seller_revenue",
    ascending=True
    ).copy()

    top_sellers_chart["seller_rank"] = [
    f"Seller {i}"
    for i in range(1, len(top_sellers_chart) + 1)
    ]

    fig_sellers = px.bar(
    top_sellers_chart,
    x="seller_revenue",
    y="seller_rank",
    orientation="h",
    text="seller_revenue",
    title="Top 10 Sellers by Revenue"
    )

    fig_sellers.update_layout(
    xaxis_title="Revenue (₹)",
    yaxis_title="Seller"
    )

    fig_sellers.update_traces(
    texttemplate="₹%{x:,.0f}",
    textposition="outside"
    )

    st.plotly_chart(
    fig_sellers,
    use_container_width=True
    )

    st.dataframe(
    top_sellers,
    use_container_width=True,
    hide_index=True
    )

    # -------------------------
    # TOP PRODUCTS
    # -------------------------

    st.subheader("Top 10 Products by Units Sold")

    top_products_chart = top_products.sort_values(
    "units_sold",
    ascending=True
    ).copy()

    top_products_chart["product_rank"] = [
    f"Product {i}"
    for i in range(1, len(top_products_chart) + 1)
    ]

    fig_products = px.bar(
    top_products_chart,
    x="units_sold",
    y="product_rank",
    orientation="h",
    text="units_sold",
    title="Top 10 Products by Units Sold"
    )

    fig_products.update_layout(
    xaxis_title="Units Sold",
    yaxis_title="Product"
    )

    fig_products.update_traces(
    texttemplate="%{x:,}",
    textposition="outside"
    )

    st.plotly_chart(
    fig_products,
    use_container_width=True
    )

    st.dataframe(
    top_products,
    use_container_width=True,
    hide_index=True
    )


# ============================================================
# DELIVERY ANALYSIS
# ============================================================

with tab4:

    st.header("🚚 Delivery Analysis")

    delivery_status = run_query(
        queries.DELIVERY_STATUS
    )

    # -------------------------
    # DELIVERY STATUS
    # -------------------------

    st.subheader("Delivery Status")

    fig_delivery_status = px.bar(
    delivery_status,
    x="delivery_status",
    y="order_count",
    text="order_count",
    title="Orders by Delivery Status"
    )

    fig_delivery_status.update_layout(
    xaxis_title="Delivery Status",
    yaxis_title="Number of Orders"
    )

    fig_delivery_status.update_traces(
    texttemplate="%{y:,}",
    textposition="outside"
    )

    st.plotly_chart(
    fig_delivery_status,
    use_container_width=True
    )
    
    delivery_by_state = run_query(
        queries.DELIVERY_BY_STATE
    )

    delivery_review = run_query(
        queries.DELIVERY_VS_REVIEW
    )

    st.subheader("Delivery Status")

    st.bar_chart(
        delivery_status.set_index(
            "delivery_status"
        )["order_count"]
    )

    # -------------------------
    # AVERAGE DELIVERY DAYS BY STATE
    # -------------------------

    st.subheader("Average Delivery Days by State")

    delivery_state_chart = delivery_by_state.sort_values(
    "average_delivery_days",
    ascending=True
    ).copy()

    fig_delivery_state = px.bar(
    delivery_state_chart,
    x="average_delivery_days",
    y="state",
    orientation="h",
    text="average_delivery_days",
    title="Average Delivery Days by State"
    )

    fig_delivery_state.update_layout(
    xaxis_title="Average Delivery Days",
    yaxis_title="State"
    )

    fig_delivery_state.update_traces(
    texttemplate="%{x:.1f} days",
    textposition="outside"
    )

    st.plotly_chart(
    fig_delivery_state,
    use_container_width=True
    )

# -------------------------
# DELIVERY STATUS VS REVIEW SCORE
# -------------------------

    delivery_review = run_query(
    queries.DELIVERY_VS_REVIEW
    )

    st.subheader("Delivery Status vs Review Score")

    fig_delivery_review = px.bar(
    delivery_review,
    x="delivery_status",
    y="average_review_score",
    text="average_review_score",
    title="Average Review Score by Delivery Status"
    )

    fig_delivery_review.update_layout(
    xaxis_title="Delivery Status",
    yaxis_title="Average Review Score",
    yaxis_range=[0, 5]
    )

    fig_delivery_review.update_traces(
    texttemplate="%{y:.2f}",
    textposition="outside"
    )

    st.plotly_chart(
    fig_delivery_review,
    use_container_width=True
    )
# ============================================================
# CUSTOMER EXPERIENCE
# ============================================================

with tab5:

    st.header("⭐ Customer Experience")

    review_distribution = run_query(
        queries.REVIEW_DISTRIBUTION
    )

    reviews_category = run_query(
        queries.REVIEWS_BY_CATEGORY
    )

    st.subheader("Review Score Distribution")

# -------------------------
# REVIEW SCORE DISTRIBUTION
# -------------------------

    st.subheader("Review Score Distribution")

    fig_review_distribution = px.bar(
    review_distribution,
    x="review_score",
    y="review_count",
    text="review_count",
    title="Review Score Distribution"
    )

    fig_review_distribution.update_layout(
    xaxis_title="Review Score",
    yaxis_title="Number of Reviews",
    xaxis=dict(
        dtick=1
    )
    )

    fig_review_distribution.update_traces(
    texttemplate="%{y:,}",
    textposition="outside"
    )

    st.plotly_chart(
    fig_review_distribution,
    use_container_width=True
    )

    st.subheader("Reviews by Product Category")

# -------------------------
# REVIEWS BY PRODUCT CATEGORY
# -------------------------

    st.subheader("Reviews by Product Category")

    reviews_category_chart = reviews_category.sort_values(
    "average_rating",
    ascending=True
    ).copy()

    fig_reviews_category = px.bar(
    reviews_category_chart,
    x="average_rating",
    y="category",
    orientation="h",
    text="average_rating",
    title="Average Review Rating by Product Category"
    )

    fig_reviews_category.update_layout(
    xaxis_title="Average Review Rating",
    yaxis_title="Product Category",
    xaxis_range=[0, 5]
    )

    fig_reviews_category.update_traces(
    texttemplate="%{x:.2f}",
    textposition="outside"
    )

    st.plotly_chart(
    fig_reviews_category,
    use_container_width=True
    )

    st.dataframe(
    reviews_category,
    use_container_width=True,
    hide_index=True
    )

# ============================================================
# DATA TABLES
# ============================================================

with tab6:

    st.header("📋 Data Tables")

    # -------------------------
    # CATEGORY REVENUE
    # -------------------------

    st.subheader("Category Revenue")

    st.dataframe(
        category_revenue,
        use_container_width=True,
        hide_index=True
    )

    # -------------------------
    # TOP SELLERS
    # -------------------------

    st.subheader("Top Sellers")

    st.dataframe(
        top_sellers,
        use_container_width=True,
        hide_index=True
    )

    # -------------------------
    # TOP PRODUCTS
    # -------------------------

    st.subheader("Top Products")

    st.dataframe(
        top_products,
        use_container_width=True,
        hide_index=True
    )

    # -------------------------
    # CUSTOMER SPENDING
    # -------------------------

    st.subheader("Customer Spending")

    customer_spending = run_query(
        queries.CUSTOMER_SPENDING
    )

    st.dataframe(
        customer_spending,
        use_container_width=True,
        hide_index=True
    )

    # -------------------------
    # DELIVERY BY STATE
    # -------------------------

    st.subheader("Delivery by State")

    st.dataframe(
        delivery_by_state,
        use_container_width=True,
        hide_index=True
    )

    # -------------------------
    # REVIEW BY CATEGORY
    # -------------------------

    st.subheader("Reviews by Product Category")

    st.dataframe(
        reviews_category,
        use_container_width=True,
        hide_index=True
    )
# ============================================================
# CSV REPORTS - ALL 9 DATASETS
# ============================================================

with tab7:

    st.header("📂 Cleaned CSV Reports")

    if len(data) == 0:

        st.warning("⚠️ No CSV files available.")

    else:

        st.write(
            f"**{len(data)} CSV files loaded successfully.**"
        )

        for filename, df in data.items():

            st.subheader(f"📄 {filename}")

            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(
                    f"Rows: **{df.shape[0]:,}** | "
                    f"Columns: **{df.shape[1]}**"
                )

            with col2:

                csv_data = df.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    "⬇️ Download CSV",
                    csv_data,
                    filename,
                    "text/csv",
                    key=f"download_{filename}"
                )

            with st.expander(f"👁️ Preview {filename}"):

                st.dataframe(
                    df.head(10),
                    use_container_width=True
                )

            st.divider()

# ============================================================
# TAB 8 - AUTOMATED WEEKLY SQL REPORT
# ============================================================

with tab8:

    st.header("📊 Automated SQL Weekly Report")

    st.write(
        "This report retrieves the latest 12 weeks of "
        "performance data directly from MySQL."
    )

    if st.button(
        "🔄 Generate Weekly Report",
        key="generate_weekly_report"
    ):

        with st.spinner("Generating weekly SQL report..."):

            try:

                weekly_report = generate_weekly_report()

                st.success(
                    "✅ Weekly SQL report generated successfully!"
                )

                # ====================================================
                # DEBUG OUTPUT
                # ====================================================

                st.subheader("DEBUG - Weekly Revenue")
                st.write(
                    weekly_report["Weekly Revenue"]
                )

                st.subheader("DEBUG - Weekly Orders")
                st.write(
                    weekly_report["Weekly Orders"]
                )

                st.subheader("DEBUG - Weekly AOV")
                st.write(
                    weekly_report["Weekly AOV"]
                )

                st.subheader("DEBUG - Weekly Reviews")
                st.write(
                    weekly_report["Weekly Reviews"]
                )

                st.subheader("DEBUG - Weekly Delivery")
                st.write(
                    weekly_report["Weekly Delivery"]
                )

                # ====================================================
                # WEEKLY REVENUE
                # ====================================================

                st.subheader("💰 Weekly Revenue")

                revenue_report = weekly_report[
                    "Weekly Revenue"
                ]

                if revenue_report.empty:

                    st.warning(
                        "No weekly revenue data found."
                    )

                else:

                    st.line_chart(
                        revenue_report.set_index(
                            "week_start"
                        )["revenue"]
                    )

                    st.dataframe(
                        revenue_report,
                        use_container_width=True,
                        hide_index=True
                    )

                    revenue_csv = (
                        revenue_report
                        .to_csv(index=False)
                        .encode("utf-8")
                    )

                    st.download_button(
                        "⬇️ Download Weekly Revenue",
                        revenue_csv,
                        "weekly_revenue.csv",
                        "text/csv",
                        key="download_weekly_revenue"
                    )

                # ====================================================
                # WEEKLY ORDERS
                # ====================================================

                st.subheader("📦 Weekly Orders")

                orders_report = weekly_report[
                    "Weekly Orders"
                ]

                if orders_report.empty:

                    st.warning(
                        "No weekly order data found."
                    )

                else:

                    st.line_chart(
                        orders_report.set_index(
                            "week_start"
                        )["total_orders"]
                    )

                    st.dataframe(
                        orders_report,
                        use_container_width=True,
                        hide_index=True
                    )

                    orders_csv = (
                        orders_report
                        .to_csv(index=False)
                        .encode("utf-8")
                    )

                    st.download_button(
                        "⬇️ Download Weekly Orders",
                        orders_csv,
                        "weekly_orders.csv",
                        "text/csv",
                        key="download_weekly_orders"
                    )

                # ====================================================
                # WEEKLY AOV
                # ====================================================

                st.subheader(
                    "💵 Weekly Average Order Value"
                )

                aov_report = weekly_report[
                    "Weekly AOV"
                ]

                if aov_report.empty:

                    st.warning(
                        "No weekly AOV data found."
                    )

                else:

                    st.line_chart(
                        aov_report.set_index(
                            "week_start"
                        )["average_order_value"]
                    )

                    st.dataframe(
                        aov_report,
                        use_container_width=True,
                        hide_index=True
                    )

                    aov_csv = (
                        aov_report
                        .to_csv(index=False)
                        .encode("utf-8")
                    )

                    st.download_button(
                        "⬇️ Download Weekly AOV",
                        aov_csv,
                        "weekly_aov.csv",
                        "text/csv",
                        key="download_weekly_aov"
                    )

                # ====================================================
                # WEEKLY REVIEWS
                # ====================================================

                st.subheader(
                    "⭐ Weekly Review Score"
                )

                reviews_report = weekly_report[
                    "Weekly Reviews"
                ]

                if reviews_report.empty:

                    st.warning(
                        "No weekly review data found."
                    )

                else:

                    st.line_chart(
                        reviews_report.set_index(
                            "week_start"
                        )["average_review_score"]
                    )

                    st.dataframe(
                        reviews_report,
                        use_container_width=True,
                        hide_index=True
                    )

                    reviews_csv = (
                        reviews_report
                        .to_csv(index=False)
                        .encode("utf-8")
                    )

                    st.download_button(
                        "⬇️ Download Weekly Reviews",
                        reviews_csv,
                        "weekly_reviews.csv",
                        "text/csv",
                        key="download_weekly_reviews"
                    )

                # ====================================================
                # WEEKLY DELIVERY
                # ====================================================

                st.subheader(
                    "🚚 Weekly Delivery Performance"
                )

                delivery_report = weekly_report[
                    "Weekly Delivery"
                ]

                if delivery_report.empty:

                    st.warning(
                        "No weekly delivery data found."
                    )

                else:

                    st.line_chart(
                        delivery_report.set_index(
                            "week_start"
                        )[
                            [
                                "delivered_orders",
                                "delayed_orders"
                            ]
                        ]
                    )

                    st.dataframe(
                        delivery_report,
                        use_container_width=True,
                        hide_index=True
                    )

                    delivery_csv = (
                        delivery_report
                        .to_csv(index=False)
                        .encode("utf-8")
                    )

                    st.download_button(
                        "⬇️ Download Weekly Delivery",
                        delivery_csv,
                        "weekly_delivery.csv",
                        "text/csv",
                        key="download_weekly_delivery"
                    )

            except Exception as e:

                st.error(
                    f"❌ Weekly report generation failed: {e}"
                )