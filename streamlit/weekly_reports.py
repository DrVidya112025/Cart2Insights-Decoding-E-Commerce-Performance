from database import run_query


# ============================================================
# 1. WEEKLY REVENUE
# ============================================================

WEEKLY_REVENUE = """
SELECT
    YEARWEEK(o.order_purchase_timestamp, 1) AS week,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.order_purchase_timestamp >= DATE_SUB(CURDATE(), INTERVAL 12 WEEK)
GROUP BY YEARWEEK(o.order_purchase_timestamp, 1)
ORDER BY week;
"""


# ============================================================
# 2. WEEKLY ORDERS
# ============================================================

WEEKLY_ORDERS = """
SELECT
    YEARWEEK(order_purchase_timestamp, 1) AS week,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
WHERE order_purchase_timestamp >= DATE_SUB(CURDATE(), INTERVAL 12 WEEK)
GROUP BY YEARWEEK(order_purchase_timestamp, 1)
ORDER BY week;
"""


# ============================================================
# 3. WEEKLY AVERAGE ORDER VALUE
# ============================================================

WEEKLY_AOV = """
SELECT
    YEARWEEK(o.order_purchase_timestamp, 1) AS week,

    ROUND(
        SUM(oi.price + oi.freight_value)
        / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value

FROM orders o

JOIN order_items oi
    ON o.order_id = oi.order_id

WHERE o.order_purchase_timestamp >=
      DATE_SUB(CURDATE(), INTERVAL 12 WEEK)

GROUP BY YEARWEEK(o.order_purchase_timestamp, 1)

ORDER BY week;
"""


# ============================================================
# 4. WEEKLY REVIEW SCORE
# ============================================================

WEEKLY_REVIEWS = """
SELECT
    YEARWEEK(o.order_purchase_timestamp, 1) AS week,

    ROUND(
        AVG(r.review_score),
        2
    ) AS average_review_score

FROM orders o

JOIN order_reviews r
    ON o.order_id = r.order_id

WHERE o.order_purchase_timestamp >=
      DATE_SUB(CURDATE(), INTERVAL 12 WEEK)

GROUP BY YEARWEEK(o.order_purchase_timestamp, 1)

ORDER BY week;
"""


# ============================================================
# 5. WEEKLY DELIVERY PERFORMANCE
# ============================================================

WEEKLY_DELIVERY = """
SELECT
    YEARWEEK(order_purchase_timestamp, 1) AS week,

    COUNT(*) AS total_orders,

    SUM(
        CASE
            WHEN order_delivered_customer_date IS NOT NULL
            THEN 1
            ELSE 0
        END
    ) AS delivered_orders,

    SUM(
        CASE
            WHEN order_delivered_customer_date >
                 order_estimated_delivery_date
            THEN 1
            ELSE 0
        END
    ) AS delayed_orders

FROM orders

WHERE order_purchase_timestamp >=
      DATE_SUB(CURDATE(), INTERVAL 12 WEEK)

GROUP BY YEARWEEK(order_purchase_timestamp, 1)

ORDER BY week;
"""


# ============================================================
# FUNCTION TO GENERATE WEEKLY REPORT
# ============================================================

def generate_weekly_report():

    report = {}

    report["Weekly Revenue"] = run_query(
        WEEKLY_REVENUE
    )

    report["Weekly Orders"] = run_query(
        WEEKLY_ORDERS
    )

    report["Weekly AOV"] = run_query(
        WEEKLY_AOV
    )

    report["Weekly Reviews"] = run_query(
        WEEKLY_REVIEWS
    )

    report["Weekly Delivery"] = run_query(
        WEEKLY_DELIVERY
    )

    return report
