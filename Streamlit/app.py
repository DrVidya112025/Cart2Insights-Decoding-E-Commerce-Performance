import streamlit as st
import plotly.express as px
from database import run_query, get_connection
import queries
import pandas as pd
import os
from utils import format_currency, format_number
from weekly_reports import generate_weekly_report


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Cart2Insights - E-Commerce Performance",
    page_icon="🛒",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0F172A;
        color: white;
    }

    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #FFD700;
        text-align: center;
        margin-bottom: 5px;
    }

    .sub-title {
        font-size: 18px;
        text-align: center;
        color: #CBD5E1;
        margin-bottom: 30px;
    }

    h1, h2, h3 {
        color: #FFD700 !important;
    }

    .kpi-card {
        background-color: #1E40AF;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
        min-height: 120px;
    }

    .kpi-title {
        font-size: 15px;
        color: #DBEAFE;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: bold;
        color: white;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">🛒 Cart2Insights</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Decoding E-Commerce Performance</div>',
    unsafe_allow_html=True
)


# ============================================================
# DATABASE CONNECTION TEST
# ============================================================

try:

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT DATABASE()")
    db_name = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

except Exception as e:

    st.error(
        f"Database connection error: {e}"
    )

    st.stop()


# ============================================================
# OPTIONAL CSV DATA
# ============================================================
#
# The dashboard uses MySQL.
#
# We do NOT assume any specific CSV filenames.
# Any CSV files that actually exist in the folder
# are loaded automatically.
#
# Missing CSV files will NOT generate warnings.
# ============================================================

DATA_PATH = r"D:\HCL_PROJECTS\Cart2 Insight\Data\cleaned"

data = {}

if os.path.exists(DATA_PATH):

    try:

        for filename in os.listdir(DATA_PATH):

            if filename.lower().endswith(".csv"):

                file_path = os.path.join(
                    DATA_PATH,
                    filename
                )

                try:

                    df = pd.read_csv(
                        file_path,
                        low_memory=False
                    )

                    file_key = os.path.splitext(
                        filename
                    )[0]

                    data[file_key] = df

                except Exception:
                    pass

    except Exception:
        pass


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_value(df, column, default=0):

    try:

        if (
            df is not None
            and not df.empty
            and column in df.columns
        ):

            value = df.iloc[0][column]

            if pd.isna(value):
                return default

            return value

    except Exception:
        pass

    return default


# ============================================================
# BUSINESS OVERVIEW - DIRECT MYSQL KPI QUERIES
# ============================================================

st.header("📊 Business Overview")


# ------------------------------------------------------------
# TOTAL REVENUE
# ------------------------------------------------------------

try:

    revenue_query = """
    SELECT
        ROUND(
            SUM(oi.price + oi.freight_value),
            2
        ) AS total_revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    """

    revenue_df = run_query(revenue_query)

    total_revenue_value = get_value(
        revenue_df,
        "total_revenue",
        0
    )

except Exception as e:

    st.error(f"Revenue KPI error: {e}")
    total_revenue_value = 0


# ------------------------------------------------------------
# TOTAL ORDERS
# ------------------------------------------------------------

try:

    orders_query = """
    SELECT
        COUNT(DISTINCT order_id) AS total_orders
    FROM orders
    """

    orders_df = run_query(orders_query)

    total_orders_value = get_value(
        orders_df,
        "total_orders",
        0
    )

except Exception as e:

    st.error(f"Orders KPI error: {e}")
    total_orders_value = 0


# ------------------------------------------------------------
# TOTAL CUSTOMERS
# ------------------------------------------------------------

try:

    customers_query = """
    SELECT
        COUNT(DISTINCT customer_unique_id)
        AS total_customers
    FROM customers
    """

    customers_df = run_query(customers_query)

    total_customers_value = get_value(
        customers_df,
        "total_customers",
        0
    )

except Exception as e:

    st.error(f"Customers KPI error: {e}")
    total_customers_value = 0


# ------------------------------------------------------------
# TOTAL SELLERS
# ------------------------------------------------------------

try:

    sellers_query = """
    SELECT
        COUNT(DISTINCT seller_id)
        AS total_sellers
    FROM sellers
    """

    sellers_df = run_query(sellers_query)

    total_sellers_value = get_value(
        sellers_df,
        "total_sellers",
        0
    )

except Exception as e:

    st.error(f"Sellers KPI error: {e}")
    total_sellers_value = 0


# ------------------------------------------------------------
# AVERAGE ORDER VALUE
# ------------------------------------------------------------

try:

    aov_query = """
    SELECT
        ROUND(
            SUM(
                oi.price + oi.freight_value
            )
            /
            COUNT(DISTINCT o.order_id),
            2
        ) AS average_order_value
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    """

    aov_df = run_query(aov_query)

    aov_value = get_value(
        aov_df,
        "average_order_value",
        0
    )

except Exception as e:

    st.error(f"AOV KPI error: {e}")
    aov_value = 0


# ------------------------------------------------------------
# AVERAGE REVIEW SCORE
# ------------------------------------------------------------

try:

    review_query = """
    SELECT
        ROUND(
            AVG(review_score),
            2
        ) AS average_review_score
    FROM order_reviews
    """

    review_df = run_query(review_query)

    review_value = get_value(
        review_df,
        "average_review_score",
        0
    )

except Exception as e:

    st.error(f"Review KPI error: {e}")
    review_value = 0


# ------------------------------------------------------------
# CUSTOMER LIFETIME VALUE
# ------------------------------------------------------------

try:

    clv_query = """
    SELECT
        ROUND(
            SUM(
                oi.price + oi.freight_value
            )
            /
            COUNT(
                DISTINCT c.customer_unique_id
            ),
            2
        ) AS customer_lifetime_value

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id
    """

    clv_df = run_query(clv_query)

    clv_value = get_value(
        clv_df,
        "customer_lifetime_value",
        0
    )

except Exception as e:

    st.error(f"CLV KPI error: {e}")
    clv_value = 0


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">
                Total Revenue
            </div>
            <div class="kpi-value">
                {format_currency(total_revenue_value)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">
                Total Orders
            </div>
            <div class="kpi-value">
                {format_number(total_orders_value)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">
                Total Customers
            </div>
            <div class="kpi-value">
                {format_number(total_customers_value)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">
                Total Sellers
            </div>
            <div class="kpi-value">
                {format_number(total_sellers_value)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


col5, col6, col7 = st.columns(3)


with col5:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">
                Average Order Value
            </div>
            <div class="kpi-value">
                {format_currency(aov_value)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col6:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">
                Average Review Score
            </div>
            <div class="kpi-value">
                {review_value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col7:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">
                Customer Lifetime Value
            </div>
            <div class="kpi-value">
                {format_currency(clv_value)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# INTERACTIVE FILTERS
# ============================================================

st.header("🔎 Interactive Filters")

filter1, filter2, filter3, filter4 = st.columns(4)


# ------------------------------------------------------------
# DATE FILTER
# ------------------------------------------------------------

with filter1:

    start_date = st.date_input(
        "Start Date",
        value=pd.to_datetime(
            "2017-01-01"
        ).date(),
        key="main_start_date"
    )


with filter2:

    end_date = st.date_input(
        "End Date",
        value=pd.to_datetime(
            "2018-08-31"
        ).date(),
        key="main_end_date"
    )


# ------------------------------------------------------------
# CATEGORY FILTER
# ------------------------------------------------------------

try:

    category_query = """
    SELECT DISTINCT
        product_category_name_english AS category
    FROM products
    WHERE product_category_name_english IS NOT NULL
    ORDER BY product_category_name_english
    """

    category_data = run_query(
        category_query
    )

except Exception as e:

    st.error(
        f"Category filter error: {e}"
    )

    category_data = pd.DataFrame()


categories = [
    "All Categories"
]

if (
    category_data is not None
    and not category_data.empty
    and "category" in category_data.columns
):

    categories += (
        category_data["category"]
        .dropna()
        .astype(str)
        .tolist()
    )


with filter3:

    selected_category = st.selectbox(
        "Category",
        categories,
        key="main_category_filter"
    )


# ------------------------------------------------------------
# REGION FILTER
# ------------------------------------------------------------

try:

    region_query = """
    SELECT DISTINCT
        customer_state AS region
    FROM customers
    WHERE customer_state IS NOT NULL
    ORDER BY customer_state
    """

    region_data = run_query(
        region_query
    )

except Exception as e:

    st.error(
        f"Region filter error: {e}"
    )

    region_data = pd.DataFrame()


regions = [
    "All Regions"
]

if (
    region_data is not None
    and not region_data.empty
    and "region" in region_data.columns
):

    regions += (
        region_data["region"]
        .dropna()
        .astype(str)
        .tolist()
    )


with filter4:

    selected_region = st.selectbox(
        "Region",
        regions,
        key="main_region_filter"
    )


# ============================================================
# DATE VALIDATION
# ============================================================

if start_date > end_date:

    st.error(
        "Start Date cannot be after End Date."
    )

    st.stop()


# ============================================================
# COMMON SQL FILTER CONDITIONS
# ============================================================

category_condition = ""

region_condition = ""


if selected_category != "All Categories":

    category_condition = f"""
    AND p.product_category_name_english =
        '{selected_category}'
    """


if selected_region != "All Regions":

    region_condition = f"""
    AND c.customer_state =
        '{selected_region}'
    """


# ============================================================
# MONTHLY REVENUE QUERY
# ============================================================

filtered_sales_query = f"""

SELECT

    DATE_FORMAT(
        o.order_purchase_timestamp,
        '%Y-%m'
    ) AS month,

    ROUND(
        SUM(
            oi.price + oi.freight_value
        ),
        2
    ) AS revenue

FROM orders o

JOIN order_items oi
    ON o.order_id = oi.order_id

JOIN products p
    ON oi.product_id = p.product_id

JOIN customers c
    ON o.customer_id = c.customer_id

WHERE
    o.order_purchase_timestamp >= '{start_date}'

AND
    o.order_purchase_timestamp <
        DATE_ADD(
            '{end_date}',
            INTERVAL 1 DAY
        )

{category_condition}

{region_condition}

GROUP BY
    DATE_FORMAT(
        o.order_purchase_timestamp,
        '%Y-%m'
    )

ORDER BY
    month

"""

try:

    filtered_sales = run_query(
        filtered_sales_query
    )

except Exception as e:

    st.error(
        f"Monthly revenue query error: {e}"
    )

    filtered_sales = pd.DataFrame()


# ============================================================
# REVENUE BY CATEGORY QUERY
# ============================================================

filtered_category_query = f"""

SELECT

    p.product_category_name_english
        AS category,

    ROUND(
        SUM(
            oi.price + oi.freight_value
        ),
        2
    ) AS revenue

FROM orders o

JOIN order_items oi
    ON o.order_id = oi.order_id

JOIN products p
    ON oi.product_id = p.product_id

JOIN customers c
    ON o.customer_id = c.customer_id

WHERE
    o.order_purchase_timestamp >= '{start_date}'

AND
    o.order_purchase_timestamp <
        DATE_ADD(
            '{end_date}',
            INTERVAL 1 DAY
        )

{category_condition}

{region_condition}

GROUP BY
    p.product_category_name_english

ORDER BY
    revenue DESC

"""

try:

    category_revenue = run_query(
        filtered_category_query
    )

except Exception as e:

    st.error(
        f"Category revenue query error: {e}"
    )

    category_revenue = pd.DataFrame()


# ============================================================
# TABS
# ============================================================

tabs = st.tabs(
    [
        "📈 Sales Analysis",
        "👥 Customer Analysis",
        "🏪 Seller & Product",
        "🚚 Delivery Analysis",
        "⭐ Customer Experience",
        "📋 Data Tables",
        "📥 CSV Reports",
        "📅 Weekly SQL Report"
    ]
)


# ============================================================
# TAB 1
# SALES ANALYSIS
# ============================================================

with tabs[0]:

    st.header("📈 Sales Analysis")


    # ========================================================
    # 1. MONTHLY REVENUE TREND
    # ========================================================

    st.subheader(
        "📈 Monthly Revenue Trend"
    )

    if (
        filtered_sales is not None
        and not filtered_sales.empty
    ):

        fig_monthly = px.line(
            filtered_sales,
            x="month",
            y="revenue",
            markers=True,
            title="Monthly Revenue"
        )

        fig_monthly.update_layout(
            template="plotly_dark",
            xaxis_title="Month",
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig_monthly,
            use_container_width=True
        )

    else:

        st.info(
            "No monthly revenue data found "
            "for the selected filters."
        )


    # ========================================================
    # 2. REVENUE BY CATEGORY
    # ========================================================

    st.subheader(
        "📊 Revenue by Product Category"
    )

    if (
        category_revenue is not None
        and not category_revenue.empty
    ):

        top_categories = (
            category_revenue
            .head(10)
            .copy()
        )

        fig_category = px.bar(
            top_categories,
            x="revenue",
            y="category",
            orientation="h",
            title="Top 10 Categories by Revenue"
        )

        fig_category.update_layout(
            template="plotly_dark",
            xaxis_title="Revenue",
            yaxis_title="Category",
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

        st.dataframe(
            top_categories,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No category revenue data found."
        )


    # ========================================================
    # 3. TOP-SELLING PRODUCTS
    # ========================================================

    st.subheader(
        "🏆 Top-Selling Products"
    )

    top_products_sales_query = f"""

    SELECT

        oi.product_id,

        p.product_category_name_english
            AS category,

        COUNT(*) AS units_sold,

        ROUND(
            SUM(
                oi.price + oi.freight_value
            ),
            2
        ) AS revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    WHERE
        o.order_purchase_timestamp >= '{start_date}'

    AND
        o.order_purchase_timestamp <
            DATE_ADD(
                '{end_date}',
                INTERVAL 1 DAY
            )

    {category_condition}

    {region_condition}

    GROUP BY
        oi.product_id,
        p.product_category_name_english

    ORDER BY
        units_sold DESC

    LIMIT 10

    """

    try:

        top_products_sales = run_query(
            top_products_sales_query
        )

    except Exception as e:

        st.error(
            f"Top products query error: {e}"
        )

        top_products_sales = pd.DataFrame()


    if (
        top_products_sales is not None
        and not top_products_sales.empty
    ):

        fig_products = px.bar(
            top_products_sales,
            x="units_sold",
            y="product_id",
            orientation="h",
            hover_data=[
                "category",
                "revenue"
            ],
            title="Top 10 Products by Units Sold"
        )

        fig_products.update_layout(
            template="plotly_dark",
            xaxis_title="Units Sold",
            yaxis_title="Product ID",
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig_products,
            use_container_width=True
        )

        st.dataframe(
            top_products_sales,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No product sales data found."
        )


    # ========================================================
    # 4. SALES BY LOCATION
    # ========================================================

    st.subheader(
        "📍 Sales by Location"
    )

    sales_location_query = f"""

    SELECT

        c.customer_state AS state,

        COUNT(
            DISTINCT o.order_id
        ) AS total_orders,

        ROUND(
            SUM(
                oi.price + oi.freight_value
            ),
            2
        ) AS revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    WHERE
        o.order_purchase_timestamp >= '{start_date}'

    AND
        o.order_purchase_timestamp <
            DATE_ADD(
                '{end_date}',
                INTERVAL 1 DAY
            )

    {category_condition}

    {region_condition}

    GROUP BY
        c.customer_state

    ORDER BY
        revenue DESC

    """

    try:

        sales_location = run_query(
            sales_location_query
        )

    except Exception as e:

        st.error(
            f"Sales location query error: {e}"
        )

        sales_location = pd.DataFrame()


    if (
        sales_location is not None
        and not sales_location.empty
    ):

        fig_location = px.bar(
            sales_location,
            x="revenue",
            y="state",
            orientation="h",
            hover_data=[
                "total_orders"
            ],
            title="Revenue by State"
        )

        fig_location.update_layout(
            template="plotly_dark",
            xaxis_title="Revenue",
            yaxis_title="State",
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig_location,
            use_container_width=True
        )

        st.dataframe(
            sales_location,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No location sales data found."
        )


    # ========================================================
    # APPLIED FILTERS
    # ========================================================

    st.subheader(
        "🔎 Applied Filters"
    )

    st.write(
        f"**Date Range:** "
        f"{start_date} to {end_date}"
    )

    st.write(
        f"**Category:** "
        f"{selected_category}"
    )

    st.write(
        f"**Region:** "
        f"{selected_region}"
    )


# ============================================================
# TAB 2
# CUSTOMER ANALYSIS
# ============================================================

with tabs[1]:

    st.header(
        "👥 Customer Analysis"
    )


    # ========================================================
    # CUSTOMER DISTRIBUTION
    # ========================================================

    customer_distribution_query = f"""

    SELECT

        c.customer_state AS state,

        COUNT(
            DISTINCT c.customer_unique_id
        ) AS customers

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    WHERE
        o.order_purchase_timestamp >= '{start_date}'

    AND
        o.order_purchase_timestamp <
            DATE_ADD(
                '{end_date}',
                INTERVAL 1 DAY
            )

    {region_condition}

    GROUP BY
        c.customer_state

    ORDER BY
        customers DESC

    """

    try:

        customer_distribution = run_query(
            customer_distribution_query
        )

    except Exception as e:

        st.error(
            f"Customer distribution error: {e}"
        )

        customer_distribution = pd.DataFrame()


    if (
        customer_distribution is not None
        and not customer_distribution.empty
    ):

        fig_customer_state = px.bar(
            customer_distribution.head(10),
            x="customers",
            y="state",
            orientation="h",
            title="Top 10 States by Customer Count"
        )

        fig_customer_state.update_layout(
            template="plotly_dark",
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig_customer_state,
            use_container_width=True
        )


    # ========================================================
    # REPEAT CUSTOMERS
    # ========================================================

    repeat_customer_query = f"""

    SELECT

        CASE

            WHEN order_count > 1
                THEN 'Repeat Customer'

            ELSE 'One-Time Customer'

        END AS customer_type,

        COUNT(*) AS customers

    FROM (

        SELECT

            c.customer_unique_id,

            COUNT(
                DISTINCT o.order_id
            ) AS order_count

        FROM customers c

        JOIN orders o
            ON c.customer_id = o.customer_id

        WHERE
            o.order_purchase_timestamp >= '{start_date}'

        AND
            o.order_purchase_timestamp <
                DATE_ADD(
                    '{end_date}',
                    INTERVAL 1 DAY
                )

        GROUP BY
            c.customer_unique_id

    ) customer_orders

    GROUP BY
        customer_type

    """

    try:

        repeat_customers = run_query(
            repeat_customer_query
        )

    except Exception as e:

        st.error(
            f"Repeat customer query error: {e}"
        )

        repeat_customers = pd.DataFrame()


    if (
        repeat_customers is not None
        and not repeat_customers.empty
    ):

        fig_repeat = px.pie(
            repeat_customers,
            names="customer_type",
            values="customers",
            title="Customer Type Distribution"
        )

        fig_repeat.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig_repeat,
            use_container_width=True
        )


    # ========================================================
    # TOP CUSTOMERS
    # ========================================================

    top_customer_query = f"""

    SELECT

        c.customer_unique_id,

        COUNT(
            DISTINCT o.order_id
        ) AS total_orders,

        ROUND(
            SUM(
                oi.price + oi.freight_value
            ),
            2
        ) AS total_revenue

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE
        o.order_purchase_timestamp >= '{start_date}'

    AND
        o.order_purchase_timestamp <
            DATE_ADD(
                '{end_date}',
                INTERVAL 1 DAY
            )

    GROUP BY
        c.customer_unique_id

    ORDER BY
        total_revenue DESC

    LIMIT 10

    """

    try:

        top_customers = run_query(
            top_customer_query
        )

    except Exception as e:

        st.error(
            f"Top customers query error: {e}"
        )

        top_customers = pd.DataFrame()


    if (
        top_customers is not None
        and not top_customers.empty
    ):

        fig_top_customers = px.bar(
            top_customers,
            x="total_revenue",
            y="customer_unique_id",
            orientation="h",
            title="Top Customers by Revenue"
        )

        fig_top_customers.update_layout(
            template="plotly_dark",
            yaxis=dict(
                categoryorder="total ascending"
            )
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
# ========================================================
# NEW VS REPEAT CUSTOMERS
# ========================================================

st.subheader(
    "👥 New vs Repeat Customers"
)

new_repeat_customer_query = f"""

SELECT

    customer_type,

    COUNT(*) AS customer_count

FROM (

    SELECT

        c.customer_unique_id,

        CASE

            WHEN COUNT(DISTINCT o.order_id) = 1
                THEN 'New Customer'

            ELSE 'Repeat Customer'

        END AS customer_type

    FROM orders o

    JOIN customers c
        ON o.customer_id = c.customer_id

    WHERE
        o.order_purchase_timestamp >= '{start_date}'

    AND
        o.order_purchase_timestamp <
            DATE_ADD(
                '{end_date}',
                INTERVAL 1 DAY
            )

    {region_condition}

    GROUP BY
        c.customer_unique_id

) customer_segments

GROUP BY
    customer_type

ORDER BY
    customer_count DESC

"""

try:

    new_repeat_customers = run_query(
        new_repeat_customer_query
    )

except Exception as e:

    st.error(
        f"New vs repeat customer query error: {e}"
    )

    new_repeat_customers = pd.DataFrame()


if (
    new_repeat_customers is not None
    and not new_repeat_customers.empty
):

    fig_new_repeat = px.bar(
        new_repeat_customers,
        x="customer_type",
        y="customer_count",
        text="customer_count",
        title="New vs Repeat Customers"
    )

    fig_new_repeat.update_layout(
        template="plotly_dark",
        xaxis_title="Customer Type",
        yaxis_title="Number of Customers"
    )

    st.plotly_chart(
        fig_new_repeat,
        use_container_width=True
    )

    st.dataframe(
        new_repeat_customers,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No new or repeat customer data available."
    )

# ============================================================
# TAB 3
# SELLER & PRODUCT ANALYSIS
# ============================================================

with tabs[2]:

    st.header(
        "🏪 Seller & Product Analysis"
    )


    # ========================================================
    # 1. TOP SELLERS
    # ========================================================

    st.subheader(
        "🏆 Top Sellers"
    )

    top_sellers_query = f"""

    SELECT

        oi.seller_id,

        COUNT(
            DISTINCT o.order_id
        ) AS total_orders,

        COUNT(*) AS products_sold,

        ROUND(
            SUM(
                oi.price + oi.freight_value
            ),
            2
        ) AS seller_revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    JOIN products p
        ON oi.product_id = p.product_id

    WHERE
        o.order_purchase_timestamp >= '{start_date}'

    AND
        o.order_purchase_timestamp <
            DATE_ADD(
                '{end_date}',
                INTERVAL 1 DAY
            )

    {category_condition}

    {region_condition}

    GROUP BY
        oi.seller_id

    ORDER BY
        products_sold DESC

    LIMIT 10

    """

    try:

        top_sellers = run_query(
            top_sellers_query
        )

    except Exception as e:

        st.error(
            f"Top sellers query error: {e}"
        )

        top_sellers = pd.DataFrame()


    if (
        top_sellers is not None
        and not top_sellers.empty
    ):

        fig_top_sellers = px.bar(
            top_sellers,
            x="products_sold",
            y="seller_id",
            orientation="h",
            hover_data=[
                "total_orders",
                "seller_revenue"
            ],
            title="Top 10 Sellers by Products Sold"
        )

        fig_top_sellers.update_layout(
            template="plotly_dark",
            xaxis_title="Products Sold",
            yaxis_title="Seller ID",
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig_top_sellers,
            use_container_width=True
        )

        st.dataframe(
            top_sellers,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No seller data available."
        )


    # ========================================================
    # 2. SELLER REVENUE
    # ========================================================

    st.subheader(
        "💰 Seller Revenue"
    )

    seller_revenue_query = f"""

    SELECT

        oi.seller_id,

        ROUND(
            SUM(oi.price),
            2
        ) AS product_revenue,

        ROUND(
            SUM(oi.freight_value),
            2
        ) AS freight_revenue,

        ROUND(
            SUM(
                oi.price + oi.freight_value
            ),
            2
        ) AS total_revenue,

        COUNT(
            DISTINCT o.order_id
        ) AS total_orders

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    JOIN products p
        ON oi.product_id = p.product_id

    WHERE
        o.order_purchase_timestamp >= '{start_date}'

    AND
        o.order_purchase_timestamp <
            DATE_ADD(
                '{end_date}',
                INTERVAL 1 DAY
            )

    {category_condition}

    {region_condition}

    GROUP BY
        oi.seller_id

    ORDER BY
        total_revenue DESC

    LIMIT 10

    """

    try:

        seller_revenue = run_query(
            seller_revenue_query
        )

    except Exception as e:

        st.error(
            f"Seller revenue query error: {e}"
        )

        seller_revenue = pd.DataFrame()


    if (
        seller_revenue is not None
        and not seller_revenue.empty
    ):

        fig_seller_revenue = px.bar(
            seller_revenue,
            x="total_revenue",
            y="seller_id",
            orientation="h",
            hover_data=[
                "product_revenue",
                "freight_revenue",
                "total_orders"
            ],
            title="Top 10 Sellers by Revenue"
        )

        fig_seller_revenue.update_layout(
            template="plotly_dark",
            xaxis_title="Revenue",
            yaxis_title="Seller ID",
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig_seller_revenue,
            use_container_width=True
        )

        st.dataframe(
            seller_revenue,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No seller revenue data available."
        )


    # ========================================================
    # 3. PRODUCT / CATEGORY PERFORMANCE
    # ========================================================

    st.subheader(
        "📦 Product / Category Performance"
    )

    product_category_query = f"""

    SELECT

        p.product_category_name_english
            AS category,

        COUNT(
            DISTINCT oi.product_id
        ) AS unique_products,

        COUNT(*) AS units_sold,

        COUNT(
            DISTINCT o.order_id
        ) AS total_orders,

        ROUND(
            SUM(
                oi.price + oi.freight_value
            ),
            2
        ) AS revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    WHERE
        o.order_purchase_timestamp >= '{start_date}'

    AND
        o.order_purchase_timestamp <
            DATE_ADD(
                '{end_date}',
                INTERVAL 1 DAY
            )

    {category_condition}

    {region_condition}

    GROUP BY
        p.product_category_name_english

    ORDER BY
        revenue DESC

    LIMIT 15

    """

    try:

        product_category = run_query(
            product_category_query
        )

    except Exception as e:

        st.error(
            f"Product/category query error: {e}"
        )

        product_category = pd.DataFrame()


    if (
        product_category is not None
        and not product_category.empty
    ):

        fig_category_performance = px.bar(
            product_category,
            x="revenue",
            y="category",
            orientation="h",
            hover_data=[
                "unique_products",
                "units_sold",
                "total_orders"
            ],
            title="Top Product Categories by Revenue"
        )

        fig_category_performance.update_layout(
            template="plotly_dark",
            xaxis_title="Revenue",
            yaxis_title="Category",
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig_category_performance,
            use_container_width=True
        )

        st.dataframe(
            product_category,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No product/category performance data available."
        )


    # ========================================================
    # 4. TOP PRODUCTS BY REVENUE
    # ========================================================

    st.subheader(
        "🏅 Top Products by Revenue"
    )

    top_product_revenue_query = f"""

    SELECT

        oi.product_id,

        p.product_category_name_english
            AS category,

        COUNT(*) AS units_sold,

        ROUND(
            SUM(
                oi.price + oi.freight_value
            ),
            2
        ) AS revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    WHERE
        o.order_purchase_timestamp >= '{start_date}'

    AND
        o.order_purchase_timestamp <
            DATE_ADD(
                '{end_date}',
                INTERVAL 1 DAY
            )

    {category_condition}

    {region_condition}

    GROUP BY
        oi.product_id,
        p.product_category_name_english

    ORDER BY
        revenue DESC

    LIMIT 10

    """

    try:

        top_product_revenue = run_query(
            top_product_revenue_query
        )

    except Exception as e:

        st.error(
            f"Top product revenue query error: {e}"
        )

        top_product_revenue = pd.DataFrame()


    if (
        top_product_revenue is not None
        and not top_product_revenue.empty
    ):

        fig_top_product_revenue = px.bar(
            top_product_revenue,
            x="revenue",
            y="product_id",
            orientation="h",
            hover_data=[
                "category",
                "units_sold"
            ],
            title="Top 10 Products by Revenue"
        )

        fig_top_product_revenue.update_layout(
            template="plotly_dark",
            xaxis_title="Revenue",
            yaxis_title="Product ID",
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig_top_product_revenue,
            use_container_width=True
        )

        st.dataframe(
            top_product_revenue,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No product revenue data available."
        )


    # ========================================================
    # 5. SELLER RATINGS
    # ========================================================

    st.subheader(
        "⭐ Seller Ratings"
    )

    seller_rating_query = f"""

    SELECT

        seller_id,

        COUNT(*) AS total_reviews,

        ROUND(
            AVG(review_score),
            2
        ) AS average_rating,

        SUM(
            review_score = 5
        ) AS five_star_reviews,

        SUM(
            review_score <= 2
        ) AS low_rating_reviews

    FROM (

        SELECT DISTINCT

            oi.seller_id,

            r.review_id,

            r.review_score

        FROM orders o

        JOIN order_items oi
            ON o.order_id = oi.order_id

        JOIN order_reviews r
            ON o.order_id = r.order_id

        JOIN customers c
            ON o.customer_id = c.customer_id

        JOIN products p
            ON oi.product_id = p.product_id

        WHERE
            o.order_purchase_timestamp >= '{start_date}'

        AND
            o.order_purchase_timestamp <
                DATE_ADD(
                    '{end_date}',
                    INTERVAL 1 DAY
                )

        {category_condition}

        {region_condition}

    ) seller_reviews

    GROUP BY
        seller_id

    HAVING
        COUNT(*) >= 10

    ORDER BY
        average_rating DESC,
        total_reviews DESC

    LIMIT 15

    """

    try:

        seller_ratings = run_query(
            seller_rating_query
        )

    except Exception as e:

        st.error(
            f"Seller ratings query error: {e}"
        )

        seller_ratings = pd.DataFrame()


    if (
        seller_ratings is not None
        and not seller_ratings.empty
    ):

        fig_seller_ratings = px.bar(
            seller_ratings,
            x="average_rating",
            y="seller_id",
            orientation="h",
            hover_data=[
                "total_reviews",
                "five_star_reviews",
                "low_rating_reviews"
            ],
            title="Top Rated Sellers (Minimum 10 Reviews)"
        )

        fig_seller_ratings.update_layout(
            template="plotly_dark",
            xaxis_title="Average Rating",
            yaxis_title="Seller ID",
            xaxis=dict(
                range=[0, 5]
            ),
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig_seller_ratings,
            use_container_width=True
        )

        st.dataframe(
            seller_ratings,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No seller rating data available."
        )


    # ========================================================
    # 6. BUSINESS INSIGHTS
    # ========================================================

    st.subheader(
        "💡 Seller & Product Insights"
    )


    # Highest Revenue Seller
    if (
        seller_revenue is not None
        and not seller_revenue.empty
    ):

        top_revenue_seller = (
            seller_revenue.iloc[0]
        )

        st.write(
            f"• **Highest Revenue Seller:** "
            f"{top_revenue_seller['seller_id']}"
        )

        st.write(
            f"• **Seller Revenue:** "
            f"{format_currency(top_revenue_seller['total_revenue'])}"
        )


    # Top Revenue Category
    if (
        product_category is not None
        and not product_category.empty
    ):

        top_category = (
            product_category.iloc[0]
        )

        st.write(
            f"• **Top Revenue Category:** "
            f"{top_category['category']}"
        )

        st.write(
            f"• **Category Revenue:** "
            f"{format_currency(top_category['revenue'])}"
        )


    # Highest Rated Seller
    if (
        seller_ratings is not None
        and not seller_ratings.empty
    ):

        top_rated_seller = (
            seller_ratings.iloc[0]
        )

        st.write(
            f"• **Highest Rated Seller "
            f"(minimum 10 reviews):** "
            f"{top_rated_seller['seller_id']}"
        )

        st.write(
            f"• **Average Rating:** "
            f"{top_rated_seller['average_rating']:.2f} / 5"
        )

        st.write(
            f"• **Reviews Considered:** "
            f"{top_rated_seller['total_reviews']}"
        )

    else:

        st.write(
            "• **Highest Rated Seller:** "
            "No seller with at least 10 reviews."
        )


# ============================================================
# TAB 4
# DELIVERY ANALYSIS
# ============================================================


# ============================================================
# TAB 4
# DELIVERY ANALYSIS
# ============================================================

with tabs[3]:

    st.header(
        "🚚 Delivery Analysis"
    )


    # ========================================================
    # DELIVERY STATUS
    # ========================================================

    delivery_status_query = f"""

    SELECT

        CASE

            WHEN
                o.order_delivered_customer_date IS NULL

                THEN 'Not Delivered'

            WHEN
                o.order_delivered_customer_date
                <= o.order_estimated_delivery_date

                THEN 'Early / On Time'

            ELSE 'Delayed'

        END AS delivery_status,

        COUNT(*) AS total_orders

    FROM orders o

    WHERE
        o.order_purchase_timestamp >= '{start_date}'

    AND
        o.order_purchase_timestamp <
            DATE_ADD(
                '{end_date}',
                INTERVAL 1 DAY
            )

    GROUP BY
        delivery_status

    """

    try:

        delivery_status = run_query(
            delivery_status_query
        )

    except Exception as e:

        st.error(
            f"Delivery status error: {e}"
        )

        delivery_status = pd.DataFrame()


    if (
        delivery_status is not None
        and not delivery_status.empty
    ):

        fig_delivery = px.pie(
            delivery_status,
            names="delivery_status",
            values="total_orders",
            title="Delivery Performance"
        )

        fig_delivery.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig_delivery,
            use_container_width=True
        )


    # ========================================================
    # AVERAGE DELIVERY DAYS BY STATE
    # ========================================================

    avg_delivery_query = f"""

    SELECT

        c.customer_state AS state,

        ROUND(
            AVG(
                DATEDIFF(
                    o.order_delivered_customer_date,
                    o.order_purchase_timestamp
                )
            ),
            2
        ) AS avg_delivery_days

    FROM orders o

    JOIN customers c
        ON o.customer_id = c.customer_id

    WHERE
        o.order_purchase_timestamp >= '{start_date}'

    AND
        o.order_purchase_timestamp <
            DATE_ADD(
                '{end_date}',
                INTERVAL 1 DAY
            )

    AND
        o.order_delivered_customer_date IS NOT NULL

    GROUP BY
        c.customer_state

    ORDER BY
        avg_delivery_days DESC

    """

    try:

        avg_delivery = run_query(
            avg_delivery_query
        )

    except Exception as e:

        st.error(
            f"Average delivery query error: {e}"
        )

        avg_delivery = pd.DataFrame()


    if (
        avg_delivery is not None
        and not avg_delivery.empty
    ):

        fig_delivery_state = px.bar(
            avg_delivery.head(10),
            x="avg_delivery_days",
            y="state",
            orientation="h",
            title="Average Delivery Days by State"
        )

        fig_delivery_state.update_layout(
            template="plotly_dark",
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig_delivery_state,
            use_container_width=True
        )

        st.dataframe(
            avg_delivery,
            use_container_width=True,
            hide_index=True
        )


    # ========================================================
    # DELIVERY VS REVIEW SCORE
    # ========================================================

    delivery_review_query = f"""

    SELECT

        r.review_score,

        COUNT(*) AS total_reviews

    FROM orders o

    JOIN order_reviews r
        ON o.order_id = r.order_id

    WHERE
        o.order_purchase_timestamp >= '{start_date}'

    AND
        o.order_purchase_timestamp <
            DATE_ADD(
                '{end_date}',
                INTERVAL 1 DAY
            )

    GROUP BY
        r.review_score

    ORDER BY
        r.review_score

    """

    try:

        delivery_review = run_query(
            delivery_review_query
        )

    except Exception as e:

        st.error(
            f"Delivery review query error: {e}"
        )

        delivery_review = pd.DataFrame()


    if (
        delivery_review is not None
        and not delivery_review.empty
    ):

        fig_delivery_review = px.bar(
            delivery_review,
            x="review_score",
            y="total_reviews",
            title="Reviews by Score"
        )

        fig_delivery_review.update_layout(
            template="plotly_dark",
            xaxis_title="Review Score",
            yaxis_title="Reviews"
        )

        st.plotly_chart(
            fig_delivery_review,
            use_container_width=True
        )


# ============================================================
# TAB 5
# CUSTOMER EXPERIENCE
# ============================================================

with tabs[4]:

    st.header(
        "⭐ Customer Experience"
    )


    # ========================================================
    # REVIEW SCORE DISTRIBUTION
    # ========================================================

    review_distribution_query = f"""

    SELECT

        r.review_score,

        COUNT(*) AS total_reviews

    FROM order_reviews r

    JOIN orders o
        ON r.order_id = o.order_id

    WHERE
        o.order_purchase_timestamp >= '{start_date}'

    AND
        o.order_purchase_timestamp <
            DATE_ADD(
                '{end_date}',
                INTERVAL 1 DAY
            )

    GROUP BY
        r.review_score

    ORDER BY
        r.review_score

    """

    try:

        review_distribution = run_query(
            review_distribution_query
        )

    except Exception as e:

        st.error(
            f"Review distribution error: {e}"
        )

        review_distribution = pd.DataFrame()


    if (
        review_distribution is not None
        and not review_distribution.empty
    ):

        fig_reviews = px.bar(
            review_distribution,
            x="review_score",
            y="total_reviews",
            title="Review Score Distribution"
        )

        fig_reviews.update_layout(
            template="plotly_dark",
            xaxis_title="Review Score",
            yaxis_title="Number of Reviews"
        )

        st.plotly_chart(
            fig_reviews,
            use_container_width=True
        )


    # ========================================================
    # REVIEWS BY CATEGORY
    # ========================================================

    reviews_category_query = f"""

    SELECT

        p.product_category_name_english
            AS category,

        ROUND(
            AVG(r.review_score),
            2
        ) AS avg_review_score

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    JOIN order_reviews r
        ON o.order_id = r.order_id

    WHERE
        o.order_purchase_timestamp >= '{start_date}'

    AND
        o.order_purchase_timestamp <
            DATE_ADD(
                '{end_date}',
                INTERVAL 1 DAY
            )

    {category_condition}

    {region_condition}

    GROUP BY
        p.product_category_name_english

    ORDER BY
        avg_review_score DESC

    LIMIT 15

    """

    try:

        reviews_category = run_query(
            reviews_category_query
        )

    except Exception as e:

        st.error(
            f"Reviews by category error: {e}"
        )

        reviews_category = pd.DataFrame()


    if (
        reviews_category is not None
        and not reviews_category.empty
    ):

        fig_review_category = px.bar(
            reviews_category,
            x="avg_review_score",
            y="category",
            orientation="h",
            title="Average Review Score by Category"
        )

        fig_review_category.update_layout(
            template="plotly_dark",
            xaxis_title="Average Review Score",
            yaxis_title="Category",
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig_review_category,
            use_container_width=True
        )

        st.dataframe(
            reviews_category,
            use_container_width=True,
            hide_index=True
        )
# ========================================================
# RATING VS DELIVERY PERFORMANCE
# ========================================================

st.subheader(
    "⭐ Rating vs Delivery Performance"
)

rating_delivery_query = f"""

SELECT

    delivery_performance,

    COUNT(DISTINCT order_id) AS total_orders,

    COUNT(review_id) AS total_reviews,

    ROUND(
        AVG(review_score),
        2
    ) AS average_rating

FROM (

    SELECT

        o.order_id,

        r.review_id,

        r.review_score,

        CASE

            WHEN o.order_delivered_customer_date IS NULL
                THEN 'Not Delivered'

            WHEN o.order_delivered_customer_date
                 <= o.order_estimated_delivery_date
                THEN 'On Time'

            ELSE 'Delayed'

        END AS delivery_performance

    FROM orders o

    LEFT JOIN order_reviews r
        ON o.order_id = r.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    WHERE
        o.order_purchase_timestamp >= '{start_date}'

    AND
        o.order_purchase_timestamp <
            DATE_ADD(
                '{end_date}',
                INTERVAL 1 DAY
            )

    {region_condition}

) delivery_rating

GROUP BY
    delivery_performance

ORDER BY
    average_rating DESC

"""

try:

    rating_delivery = run_query(
        rating_delivery_query
    )

except Exception as e:

    st.error(
        f"Rating vs delivery query error: {e}"
    )

    rating_delivery = pd.DataFrame()


if (
    rating_delivery is not None
    and not rating_delivery.empty
):

    fig_rating_delivery = px.bar(
        rating_delivery,
        x="delivery_performance",
        y="average_rating",
        text="average_rating",
        hover_data=[
            "total_orders",
            "total_reviews"
        ],
        title="Average Customer Rating by Delivery Performance"
    )

    fig_rating_delivery.update_layout(
        template="plotly_dark",
        xaxis_title="Delivery Performance",
        yaxis_title="Average Rating",
        yaxis=dict(
            range=[0, 5]
        )
    )

    st.plotly_chart(
        fig_rating_delivery,
        use_container_width=True
    )

    st.dataframe(
        rating_delivery,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No rating and delivery performance data available."
    )
# ============================================================
# TAB 6
# DATA TABLES
# ============================================================

with tabs[5]:

    st.header(
        "📋 Data Tables"
    )

    if not data:

        st.info(
            "No CSV files were found in the cleaned "
            "data folder. Dashboard analysis is being "
            "performed directly from MySQL."
        )

    else:

        for name, df in data.items():

            st.subheader(
                name.replace(
                    "_",
                    " "
                ).title()
            )

            st.write(
                f"Rows: {len(df):,} | "
                f"Columns: {len(df.columns):,}"
            )

            st.dataframe(
                df.head(100),
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# TAB 7
# CSV REPORTS
# ============================================================

with tabs[6]:

    st.header(
        "📥 CSV Reports"
    )

    if not data:

        st.info(
            "No CSV files are currently available "
            "in the cleaned folder."
        )

    else:

        for name, df in data.items():

            st.subheader(
                name.replace(
                    "_",
                    " "
                ).title()
            )

            st.write(
                f"Rows: {len(df):,} | "
                f"Columns: {len(df.columns):,}"
            )

            csv_data = df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label=f"Download {name}.csv",
                data=csv_data,
                file_name=f"{name}.csv",
                mime="text/csv",
                key=f"download_{name}"
            )


# ============================================================
# TAB 8
# WEEKLY SQL REPORT
# ============================================================

with tabs[7]:

    st.header(
        "📅 Weekly SQL Report"
    )

    st.write(
        "Automated weekly business performance "
        "report generated from MySQL."
    )


    # ========================================================
    # GENERATE WEEKLY REPORT
    # ========================================================

    try:

        weekly_report = generate_weekly_report()

    except Exception as e:

        weekly_report = None

        st.error(
            f"Error generating weekly report: {e}"
        )


    # ========================================================
    # DISPLAY WEEKLY REPORT
    # ========================================================

    if weekly_report is None:

        st.info(
            "No weekly report data available."
        )

    elif isinstance(
        weekly_report,
        dict
    ):

        for report_name, report_df in weekly_report.items():

            st.subheader(
                report_name.replace(
                    "_",
                    " "
                ).title()
            )

            if (
                isinstance(
                    report_df,
                    pd.DataFrame
                )
                and not report_df.empty
            ):

                st.dataframe(
                    report_df,
                    use_container_width=True,
                    hide_index=True
                )


                # ------------------------------------------------
                # WEEKLY REVENUE
                # ------------------------------------------------

                if (
                    "week_start"
                    in report_df.columns
                    and "revenue"
                    in report_df.columns
                ):

                    fig_weekly_revenue = px.line(
                        report_df,
                        x="week_start",
                        y="revenue",
                        markers=True,
                        title="Weekly Revenue"
                    )

                    fig_weekly_revenue.update_layout(
                        template="plotly_dark"
                    )

                    st.plotly_chart(
                        fig_weekly_revenue,
                        use_container_width=True
                    )


                # ------------------------------------------------
                # WEEKLY ORDERS
                # ------------------------------------------------

                if (
                    "week_start"
                    in report_df.columns
                    and "orders"
                    in report_df.columns
                ):

                    fig_weekly_orders = px.bar(
                        report_df,
                        x="week_start",
                        y="orders",
                        title="Weekly Orders"
                    )

                    fig_weekly_orders.update_layout(
                        template="plotly_dark"
                    )

                    st.plotly_chart(
                        fig_weekly_orders,
                        use_container_width=True
                    )


                # ------------------------------------------------
                # WEEKLY AOV
                # ------------------------------------------------

                if (
                    "week_start"
                    in report_df.columns
                    and "aov"
                    in report_df.columns
                ):

                    fig_weekly_aov = px.line(
                        report_df,
                        x="week_start",
                        y="aov",
                        markers=True,
                        title="Weekly Average Order Value"
                    )

                    fig_weekly_aov.update_layout(
                        template="plotly_dark"
                    )

                    st.plotly_chart(
                        fig_weekly_aov,
                        use_container_width=True
                    )

    elif isinstance(
        weekly_report,
        pd.DataFrame
    ):

        if not weekly_report.empty:

            st.dataframe(
                weekly_report,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No weekly report data available."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#94A3B8;
        padding:10px;
    ">
        Cart2Insights — Decoding E-Commerce Performance
        <br>
        E-Commerce Analytics Dashboard
    </div>
    """,
    unsafe_allow_html=True
)