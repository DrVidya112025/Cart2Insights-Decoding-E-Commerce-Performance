
from database import run_query


def generate_weekly_report():

    # ========================================================
    # TEST 1 - Check database and order dates
    # ========================================================

    test_query = """
    SELECT
        DATABASE() AS database_name,
        MIN(order_purchase_timestamp) AS first_order,
        MAX(order_purchase_timestamp) AS last_order,
        COUNT(*) AS total_orders
    FROM orders;
    """

    test_result = run_query(test_query)

    print("\n========================================")
    print("WEEKLY REPORT DATABASE TEST")
    print(test_result)
    print("========================================\n")


    # ========================================================
    # TEST 2 - Weekly revenue
    # ========================================================

    revenue_query = """
    SELECT
        DATE_SUB(
            DATE(o.order_purchase_timestamp),
            INTERVAL WEEKDAY(o.order_purchase_timestamp) DAY
        ) AS week_start,

        ROUND(
            SUM(oi.price + oi.freight_value),
            2
        ) AS revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.order_purchase_timestamp >= (
        SELECT DATE_SUB(
            MAX(order_purchase_timestamp),
            INTERVAL 12 WEEK
        )
        FROM orders
    )

    GROUP BY week_start

    ORDER BY week_start;
    """

    weekly_revenue = run_query(revenue_query)

    print("\n========================================")
    print("WEEKLY REVENUE RESULT")
    print(weekly_revenue)
    print("ROWS:", len(weekly_revenue))
    print("========================================\n")


    # ========================================================
    # TEST 3 - Weekly orders
    # ========================================================

    orders_query = """
    SELECT
        DATE_SUB(
            DATE(order_purchase_timestamp),
            INTERVAL WEEKDAY(order_purchase_timestamp) DAY
        ) AS week_start,

        COUNT(DISTINCT order_id) AS total_orders

    FROM orders

    WHERE order_purchase_timestamp >= (
        SELECT DATE_SUB(
            MAX(order_purchase_timestamp),
            INTERVAL 12 WEEK
        )
        FROM orders
    )

    GROUP BY week_start

    ORDER BY week_start;
    """

    weekly_orders = run_query(orders_query)

    print("\n========================================")
    print("WEEKLY ORDERS RESULT")
    print(weekly_orders)
    print("ROWS:", len(weekly_orders))
    print("========================================\n")


    # ========================================================
    # TEST 4 - Weekly AOV
    # ========================================================

    aov_query = """
    SELECT
        DATE_SUB(
            DATE(o.order_purchase_timestamp),
            INTERVAL WEEKDAY(o.order_purchase_timestamp) DAY
        ) AS week_start,

        ROUND(
            SUM(oi.price + oi.freight_value)
            / COUNT(DISTINCT o.order_id),
            2
        ) AS average_order_value

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.order_purchase_timestamp >= (
        SELECT DATE_SUB(
            MAX(order_purchase_timestamp),
            INTERVAL 12 WEEK
        )
        FROM orders
    )

    GROUP BY week_start

    ORDER BY week_start;
    """

    weekly_aov = run_query(aov_query)

    print("\n========================================")
    print("WEEKLY AOV RESULT")
    print(weekly_aov)
    print("ROWS:", len(weekly_aov))
    print("========================================\n")


    # ========================================================
    # TEST 5 - Weekly Reviews
    # ========================================================

    reviews_query = """
    SELECT
        DATE_SUB(
            DATE(o.order_purchase_timestamp),
            INTERVAL WEEKDAY(o.order_purchase_timestamp) DAY
        ) AS week_start,

        ROUND(
            AVG(r.review_score),
            2
        ) AS average_review_score

    FROM orders o

    JOIN order_reviews r
        ON o.order_id = r.order_id

    WHERE o.order_purchase_timestamp >= (
        SELECT DATE_SUB(
            MAX(order_purchase_timestamp),
            INTERVAL 12 WEEK
        )
        FROM orders
    )

    GROUP BY week_start

    ORDER BY week_start;
    """

    weekly_reviews = run_query(reviews_query)

    print("\n========================================")
    print("WEEKLY REVIEWS RESULT")
    print(weekly_reviews)
    print("ROWS:", len(weekly_reviews))
    print("========================================\n")


    # ========================================================
    # TEST 6 - Weekly Delivery
    # ========================================================

    delivery_query = """
    SELECT
        DATE_SUB(
            DATE(order_purchase_timestamp),
            INTERVAL WEEKDAY(order_purchase_timestamp) DAY
        ) AS week_start,

        COUNT(DISTINCT order_id) AS total_orders,

        SUM(
            CASE
                WHEN order_delivered_customer_date IS NOT NULL
                THEN 1
                ELSE 0
            END
        ) AS delivered_orders,

        SUM(
            CASE
                WHEN order_delivered_customer_date IS NOT NULL
                AND order_estimated_delivery_date IS NOT NULL
                AND order_delivered_customer_date >
                    order_estimated_delivery_date
                THEN 1
                ELSE 0
            END
        ) AS delayed_orders

    FROM orders

    WHERE order_purchase_timestamp >= (
        SELECT DATE_SUB(
            MAX(order_purchase_timestamp),
            INTERVAL 12 WEEK
        )
        FROM orders
    )

    GROUP BY week_start

    ORDER BY week_start;
    """

    weekly_delivery = run_query(delivery_query)

    print("\n========================================")
    print("WEEKLY DELIVERY RESULT")
    print(weekly_delivery)
    print("ROWS:", len(weekly_delivery))
    print("========================================\n")


    # ========================================================
    # RETURN RESULTS TO STREAMLIT
    # ========================================================

    return {
        "Weekly Revenue": weekly_revenue,
        "Weekly Orders": weekly_orders,
        "Weekly AOV": weekly_aov,
        "Weekly Reviews": weekly_reviews,
        "Weekly Delivery": weekly_delivery
    }

