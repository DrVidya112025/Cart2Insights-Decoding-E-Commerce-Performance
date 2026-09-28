# ============================================================
# CART2 INSIGHT - SQL QUERIES
# ============================================================


# -------------------------
# BUSINESS OVERVIEW
# -------------------------

TOTAL_REVENUE = """
SELECT ROUND(SUM(price + freight_value), 2) AS total_revenue
FROM order_items;
"""


TOTAL_ORDERS = """
SELECT COUNT(*) AS total_orders
FROM orders;
"""


TOTAL_CUSTOMERS = """
SELECT COUNT(*) AS total_customers
FROM customers;
"""


TOTAL_SELLERS = """
SELECT COUNT(*) AS total_sellers
FROM sellers;
"""


AVERAGE_ORDER_VALUE = """
SELECT ROUND(AVG(order_value), 2) AS average_order_value
FROM (
    SELECT
        order_id,
        SUM(price + freight_value) AS order_value
    FROM order_items
    GROUP BY order_id
) AS order_totals;
"""


AVERAGE_REVIEW_SCORE = """
SELECT ROUND(AVG(review_score), 2) AS average_review_score
FROM order_reviews;
"""


# -------------------------
# SALES ANALYSIS
# -------------------------

MONTHLY_REVENUE = """
SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')
ORDER BY month;
"""


REVENUE_BY_CATEGORY = """
SELECT
    COALESCE(
        p.product_category_name_english,
        'Unknown'
    ) AS category,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY COALESCE(
    p.product_category_name_english,
    'Unknown'
)
ORDER BY revenue DESC;
"""


TOP_PRODUCTS = """
SELECT
    oi.product_id,
    COALESCE(
        p.product_category_name_english,
        'Unknown'
    ) AS category,
    COUNT(*) AS units_sold,
    ROUND(
        SUM(oi.price + oi.freight_value),
        2
    ) AS revenue
FROM order_items oi
LEFT JOIN products p
    ON oi.product_id = p.product_id
GROUP BY
    oi.product_id,
    p.product_category_name_english
ORDER BY units_sold DESC
LIMIT 10;
"""


SALES_BY_STATE = """
SELECT
    c.customer_state AS state,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(
        SUM(oi.price + oi.freight_value),
        2
    ) AS revenue
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_state
ORDER BY revenue DESC;
"""


# -------------------------
# CUSTOMER ANALYSIS
# -------------------------

CUSTOMER_DISTRIBUTION = """
SELECT
    customer_state AS state,
    COUNT(*) AS customer_count
FROM customers
GROUP BY customer_state
ORDER BY customer_count DESC;
"""


CUSTOMER_SPENDING = """
SELECT
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(
        SUM(oi.price + oi.freight_value),
        2
    ) AS total_spending
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_unique_id
ORDER BY total_spending DESC;
"""


REPEAT_CUSTOMERS = """
WITH customer_orders AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
)
SELECT
    CASE
        WHEN order_count > 1 THEN 'Repeat Customer'
        ELSE 'New Customer'
    END AS customer_type,
    COUNT(*) AS customer_count
FROM customer_orders
GROUP BY
    CASE
        WHEN order_count > 1 THEN 'Repeat Customer'
        ELSE 'New Customer'
    END;
"""


# -------------------------
# SELLER & PRODUCT ANALYSIS
# -------------------------

TOP_SELLERS = """
SELECT
    s.seller_id,
    COUNT(DISTINCT oi.order_id) AS order_count,
    COUNT(*) AS items_sold,
    ROUND(SUM(oi.price), 2) AS seller_revenue
FROM sellers s
JOIN order_items oi
    ON s.seller_id = oi.seller_id
GROUP BY s.seller_id
ORDER BY seller_revenue DESC
LIMIT 10;
"""


SELLER_RATINGS = """
SELECT
    oi.seller_id,
    COUNT(DISTINCT oi.order_id) AS order_count,
    ROUND(AVG(r.review_score), 2) AS average_rating
FROM order_items oi
JOIN order_reviews r
    ON oi.order_id = r.order_id
GROUP BY oi.seller_id
HAVING COUNT(DISTINCT oi.order_id) >= 10
ORDER BY average_rating DESC;
"""


# -------------------------
# DELIVERY ANALYSIS
# -------------------------

AVERAGE_DELIVERY_DAYS = """
SELECT
    ROUND(AVG(actual_delivery_days), 2)
    AS average_delivery_days
FROM orders
WHERE actual_delivery_days IS NOT NULL;
"""


DELIVERY_STATUS = """
SELECT
    CASE
        WHEN delivery_delay_days > 0 THEN 'Delayed'
        ELSE 'On Time / Early'
    END AS delivery_status,
    COUNT(*) AS order_count
FROM orders
WHERE delivery_delay_days IS NOT NULL
GROUP BY
    CASE
        WHEN delivery_delay_days > 0 THEN 'Delayed'
        ELSE 'On Time / Early'
    END;
"""


DELIVERY_BY_STATE = """
SELECT
    c.customer_state AS state,
    ROUND(
        AVG(o.actual_delivery_days),
        2
    ) AS average_delivery_days,
    COUNT(*) AS order_count,
    SUM(
        CASE
            WHEN o.delivery_delay_days > 0
            THEN 1
            ELSE 0
        END
    ) AS delayed_orders
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.actual_delivery_days IS NOT NULL
GROUP BY c.customer_state
ORDER BY average_delivery_days DESC;
"""


DELIVERY_VS_REVIEW = """
SELECT
    CASE
        WHEN o.delivery_delay_days > 0
        THEN 'Delayed'
        ELSE 'On Time / Early'
    END AS delivery_status,
    ROUND(
        AVG(r.review_score),
        2
    ) AS average_review_score
FROM orders o
JOIN order_reviews r
    ON o.order_id = r.order_id
WHERE o.delivery_delay_days IS NOT NULL
GROUP BY
    CASE
        WHEN o.delivery_delay_days > 0
        THEN 'Delayed'
        ELSE 'On Time / Early'
    END;
"""


# -------------------------
# CUSTOMER EXPERIENCE
# -------------------------

REVIEW_DISTRIBUTION = """
SELECT
    review_score,
    COUNT(*) AS review_count
FROM order_reviews
GROUP BY review_score
ORDER BY review_score;
"""


REVIEWS_BY_CATEGORY = """
SELECT
    COALESCE(
        p.product_category_name_english,
        'Unknown'
    ) AS category,
    COUNT(*) AS review_count,
    ROUND(
        AVG(r.review_score),
        2
    ) AS average_rating
FROM order_reviews r
JOIN order_items oi
    ON r.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY COALESCE(
    p.product_category_name_english,
    'Unknown'
)
ORDER BY average_rating DESC;
"""
# -------------------------
# TOP CUSTOMERS
# -------------------------

TOP_CUSTOMERS = """
SELECT
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(
        SUM(oi.price + oi.freight_value),
        2
    ) AS total_spending
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_unique_id
ORDER BY total_spending DESC
LIMIT 10;
"""
# ============================================================
# CUSTOMER LIFETIME VALUE
# ============================================================

CUSTOMER_LIFETIME_VALUE = """
SELECT
    SUM(oi.price + oi.freight_value) /
    COUNT(DISTINCT c.customer_unique_id) AS clv
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered';
"""
# ============================================================
# KPI SUMMARY
# ============================================================

KPI_SUMMARY = """
SELECT
    SUM(oi.price + oi.freight_value) AS revenue,

    COUNT(DISTINCT o.order_id) AS orders,

    SUM(oi.price + oi.freight_value)
        / COUNT(DISTINCT o.order_id) AS aov,

    SUM(oi.price + oi.freight_value)
        / COUNT(DISTINCT o.customer_id) AS clv

FROM orders o

JOIN order_items oi
    ON o.order_id = oi.order_id

WHERE o.order_status = 'delivered';
"""