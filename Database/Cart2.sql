CREATE DATABASE cart2;
USE cart2;
###########
CREATE TABLE geolocation (
    geolocation_zip_code_prefix VARCHAR(10),
    geolocation_lat FLOAT,
    geolocation_lng FLOAT,
    geolocation_city VARCHAR(50),
    geolocation_state VARCHAR(10),
    geolocation_country VARCHAR(20)
);
##########
CREATE TABLE customers (
    customer_id VARCHAR(32) PRIMARY KEY,
    customer_unique_id VARCHAR(32),
    customer_zip_code_prefix VARCHAR(10),
    customer_city VARCHAR(50),
    customer_state VARCHAR(10)
);
###########
CREATE TABLE sellers (
    seller_id VARCHAR(32) PRIMARY KEY,
    seller_zip_code_prefix VARCHAR(10),
    seller_city VARCHAR(50),
    seller_state VARCHAR(10)
);
##################
CREATE TABLE product_category_translation (
    product_category_name VARCHAR(100) PRIMARY KEY,
    product_category_name_english VARCHAR(100)
);
###############
CREATE TABLE products (
    product_id VARCHAR(32) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_length INT,
    product_description_length INT,
    product_photos_qty INT,
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT,
    zero_weight_flag INT,
    product_category_name_english VARCHAR(100),
    CONSTRAINT fk_products_category
        FOREIGN KEY (product_category_name)
        REFERENCES product_category_translation(product_category_name)
);
################
CREATE TABLE orders (
    order_id VARCHAR(32) PRIMARY KEY,
    customer_id VARCHAR(32),
    order_status VARCHAR(20),
    order_purchase_timestamp DATETIME,
    order_approved_at DATETIME,
    order_delivered_carrier_date DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME,
    carrier_date_issue VARCHAR(20),
    delivery_date_issue VARCHAR(20),
    delivery_performance VARCHAR(30),
    actual_delivery_days INT,
    estimated_delivery_days INT,
    delivery_delay_days INT
);
############
CREATE TABLE order_items (
    order_id VARCHAR(32),
    order_item_id INT,
    product_id VARCHAR(32),
    seller_id VARCHAR(32),
    shipping_limit_date DATETIME,
    price FLOAT,
    freight_value FLOAT,
    PRIMARY KEY (order_id, order_item_id),
    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),
    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),
    CONSTRAINT fk_order_items_seller
        FOREIGN KEY (seller_id)
        REFERENCES sellers(seller_id)
);
#############
CREATE TABLE order_payments (
    order_id VARCHAR(32),
    payment_sequential INT,
    payment_type VARCHAR(20),
    payment_installments INT,
    payment_value FLOAT,
    PRIMARY KEY (order_id, payment_sequential),
    CONSTRAINT fk_order_payments_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);
############
CREATE TABLE order_reviews (
    review_pk INT AUTO_INCREMENT PRIMARY KEY,
    review_id VARCHAR(32),
    order_id VARCHAR(32),
    review_score INT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date DATETIME,
    review_answer_timestamp DATETIME,
    CONSTRAINT fk_order_reviews_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);
############
SHOW TABLES;
#########
SELECT DATABASE();
USE cart2;
SELECT
    MIN(order_purchase_timestamp) AS first_order,
    MAX(order_purchase_timestamp) AS last_order,
    COUNT(*) AS total_orders
FROM orders;

SELECT
    MAX(order_purchase_timestamp) AS max_date,
    DATE_SUB(
        MAX(order_purchase_timestamp),
        INTERVAL 12 WEEK
    ) AS start_date
FROM orders;

SELECT
    COUNT(*) AS orders_in_period
FROM orders
WHERE order_purchase_timestamp >= (
    SELECT DATE_SUB(
        MAX(order_purchase_timestamp),
        INTERVAL 12 WEEK
    )
    FROM orders
);

SELECT
    YEARWEEK(o.order_purchase_timestamp, 1) AS week,
    MIN(DATE(o.order_purchase_timestamp)) AS week_start,
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
GROUP BY YEARWEEK(o.order_purchase_timestamp, 1)
ORDER BY week;

SELECT DATABASE();

SELECT COUNT(*) AS order_count
FROM orders;