# Cart2Insights-Decoding-E-Commerce-Performance

In today’s digital marketplace, e‑commerce platforms generate vast amounts of data from customer orders, products, sellers, payments, deliveries, and reviews. However, this data often
resides in multiple disconnected datasets, making it difficult to derive a unified view of business performance and customer behavior.

Cart2Insights bridges that gap by transforming raw transactional data into actionable business intelligence. The project focuses on analyzing multi‑dimensional e‑commerce data to uncover insights 
that drive strategic decisions across sales, operations, and customer experience.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# STEP 1: Understanding the Business Problem

## 1. Problem Statement
** Modern e-commerce platforms generate substantial volumes of data across multiple operational domains, including customer orders, product catalogs, seller activity, payment transactions, 
delivery logistics, and customer reviews. 
** However, this data remains fragmented across disparate systems, making it difficult to establish a unified, holistic view of business performance and customer behavior. 
** The core challenge, therefore, lies in converting this raw, distributed data into actionable insights capable of informing strategic decision-making. 
** In the absence of effective data integration and analysis, organizations face significant obstacles in monitoring overall performance, understanding customer segmentation, optimizing sales 
and revenue streams, assessing product and seller effectiveness, streamlining delivery operations, and enhancing customer satisfaction.

## 2. Business Use Cases:
●	E-Commerce Performance Monitoring
●	Customer Behavior & Segmentation
●	Sales & Revenue Optimization
●	Product & Seller Performance Analysis
●	Delivery & Operational Optimization
●	Customer Experience Improvement
●	Data-Driven Business Decision Making

## 3.Detailed Description of Business Use Cases

1. E-Commerce Performance Monitoring
Enable real-time and historical tracking of key business metrics—such as order volume, revenue trends, conversion rates, and platform-wide KPIs—to provide stakeholders with a comprehensive,
up-to-date view
of overall business health.
3. Customer Behavior & Segmentation
Analyze purchasing patterns, browsing behavior, and demographic data to segment customers into meaningful groups (e.g., high-value customers, frequent buyers, churn-risk segments), enabling
targeted marketing and personalized engagement strategies.
5. Sales & Revenue Optimization
Identify revenue trends, high-performing product categories, seasonal demand patterns, and pricing effectiveness to uncover opportunities for maximizing sales and improving profit margins.
6. Product & Seller Performance Analysis
Evaluate product-level metrics (sales volume, return rates, ratings) and seller performance (fulfillment reliability, quality scores, customer feedback) to identify top performers, underperforming
listings,and areas requiring intervention.
8. Delivery & Operational Optimization
Assess logistics data—including delivery times, shipment delays, and regional fulfillment performance—to streamline operations, reduce delivery bottlenecks, and improve supply chain efficiency.
9. Customer Experience Improvement
Leverage customer reviews, ratings, and satisfaction metrics to identify pain points in the customer journey and drive improvements in service quality, product offerings, and support processes.
10. Data-Driven Business Decision Making
Consolidate insights from all the above areas into unified dashboards and reports, empowering leadership and cross-functional teams to make informed, strategic decisions backed by data rather than intuition.

## 4. Understand the business context:
An e-commerce platform facilitates the online sale of products.
So, generates substantial volumes of data across several interconnected areas:

 Customers and their order history
 Products and sellers
 Payments and revenue
 Deliveries and shipping logistics
 Customer reviews and satisfaction ratings.
    
This data resides across multiple related datasets.When analyzed collectively rather than in isolation, 
it enables a comprehensive understanding of business performance and highlights areas with the greatest potential for improvement.

## 5. Identify the key business objectives

Monitor performance —                
Track revenue, order volume, customer growth, seller activity, average order value, and review scores over time to maintain visibility into overall business health.
Understand customers —               
Identify who is purchasing, how much they spend, and distinguish between repeat and one-time buyers to inform retention strategy.
Optimize sales —                     
Determine which product categories, individual products, and geographic regions contribute most significantly to revenue generation.
Evaluate sellers and products —     
Assess performance across revenue, order volume, and customer ratings to identify top performers as well as underperforming sellers or listings.
Improve delivery operations —        
Measure delivery times and delay patterns to pinpoint where fulfilment processes break down and impact customer experience.
Enhance customer experience —        Determine the underlying drivers of review scores and customer satisfaction.
Enable data-driven decision-making — 
Deliver consolidated insights through a centralized SQL data warehouse supported by a live, interactive dashboard.
Support risk management —            
Proactively flag underperforming sellers, delivery regions, or product categories before they materially affect revenue or brand reputation.
Benchmark growth over time —        
Establish baseline metrics and trend lines that allow performance to be tracked against historical periods and business targets.

## 6. Define the questions the analysis should answer

Theme	                             Key Business Questions

Business Overview                    What is the platform's total revenue and order volume to date?
                                     How many unique customers and sellers are active on the platform?
                                     What is the average order value, and what is the average customer review score?
                                         
Sales & revenue	                     How does monthly revenue trend, and how has it evolved over time? 
                                     Which categories, products, and locations contribute most to overall revenue? 
                                     What is the average order value, and how does it vary across segments? 
                        
Customers	                         What proportion of customers are repeat buyers versus one-time purchasers? 
                                     How is customer spend distributed across the base? 
                                     Who are the top customers by value, and what characterizes them?


Products & sellers	                 Which products generate the highest sales volume and revenue? 
                                     Which sellers drive the most revenue, orders, and customer satisfaction? 
                                     How do ratings vary across sellers and product categories?


Payments	                         Which payment methods and installment patterns are most commonly used? 
                                     Is there a relationship between payment method and order completion or cancellation status?


Delivery	                         What is the average delivery time across orders? 
                                     What proportion of deliveries are late, and by how much? 
                                     Which regions experience the slowest fulfilment?


Satisfaction	                     What does the distribution of review scores look like? 
                                     Does late delivery correlate with lower ratings? 
                                     Which product categories receive the most negative reviews, and why?


Business growth	                     What specific actions can improve revenue performance and customer experience? 
                                     Which underperforming areas present the greatest opportunity for improvement?
                                                                                                  
## 7. Statistically Tested Business Questions (Hypothesis-Driven)

These three statistical questions are being acted on:

### 	Business Question using Statistical Test
>> 1	Do delayed orders receive significantly lower review scores than on-time orders?=Independent two-sample t-test

>> 2	Does average order value differ significantly across product categories?=One-way ANOVA

>> 3	Is there a significant association between payment method and order status?=Chi-square test of independence   

******************************************************************************************************************************************************************
******************************************************************************************************************************************************************
# STEP 2: Understand the Dataset and ER Diagram

## 2.1 Overview of the Dataset

The Cart2 Insight project uses an e-commerce dataset containing 9 related tables. 
These tables capture information about customers, orders, products, sellers, payments, reviews, product categories, and geographical locations.

The main purpose of understanding the dataset and Entity-Relationship (ER) structure is to identify how the tables are connected and 
determine the correct keys and relationships before performing data cleaning, SQL loading, analysis, and feature engineering.

The nine tables are:

1. Customers
2. Geolocation
3. Orders
4. Order Items
5. Order Payments
6. Order Reviews
7. Products
8. Sellers
9. Product Category Translation

## 2.2.Understanding the 9 Tables

## 2.2.1. Customers

The `customers` table contains information about customers who placed orders.

**Important columns:**

| Column                   | Data Type | Description                                           | Key         |
| ------------------------ | --------- | ----------------------------------------------------- | ----------- |
| customer_id              | VARCHAR   | Unique identifier for the customer/order record       | Primary Key |
| customer_unique_id       | VARCHAR   | Identifier associated with the customer across orders | —           |
| customer_zip_code_prefix | INT       | Customer ZIP-code prefix                              | Foreign Key           |
| customer_city            | VARCHAR   | Customer city                                         | —           |
| customer_state           | VARCHAR   | Customer state                                        | —           |

**Rows:** 99,441
**Primary Key:** `customer_id`

---

## 2.2.2 Geolocation

The `geolocation` table contains geographical information associated with Brazilian ZIP-code prefixes.

| Column                      | Data Type | Description     | Key |
| --------------------------- | --------- | --------------- | -------------|
| geolocation_zip_code_prefix | INT       | ZIP-code prefix | Primary Key  |
| geolocation_lat             | DECIMAL   | Latitude        | —            |
| geolocation_lng             | DECIMAL   | Longitude       | —            |
| geolocation_city            | VARCHAR   | City            | —            |
| geolocation_state           | VARCHAR   | State           | —            |

**Rows:** 738,327

The ZIP-code prefix is **not unique**, so it was not used as a primary key.
Check	Result
Total rows	1,000,163
Unique zip_code_prefix values	19,015
Prefixes appearing more than once	17,972
Prefixes appearing exactly once	1,043

Only about 5% of ZIP prefixes are unique in this table. The rest repeat dozens or even hundreds of times — 
for example, ZIP prefix 24220 appears 1,146 times, and 24230 appears 1,102 times, each with different latitude/longitude values.

---

## 2.2.3. Orders

The `orders` table contains the main order-level information and connects customers with the order lifecycle.

| Column                        | Data Type | Description                                      | Key         |
| ----------------------------- | --------- | ------------------------------------------------ | ----------- |
| order_id                      | VARCHAR   | Unique order identifier                          | Primary Key |
| customer_id                   | VARCHAR   | Customer associated with the order               | Foreign Key |
| order_status                  | VARCHAR   | Current order status                             | —           |
| order_purchase_timestamp      | DATETIME  | Date and time when order was placed              | —           |
| order_approved_at             | DATETIME  | Payment approval timestamp                       | —           |
| order_delivered_carrier_date  | DATETIME  | Date order was handed to carrier                 | —           |
| order_delivered_customer_date | DATETIME  | Date order reached customer                      | —           |
| order_estimated_delivery_date | DATETIME  | Estimated delivery date                          | —           |


**Rows:** 99,441
**Primary Key:** `order_id`
**Foreign Key:** `customer_id → customers.customer_id`

---

## 2.2.4. Order Items

The `order_items` table contains individual products included in each order.

| Column              | Data Type | Description                   | Key                 |
| ------------------- | --------- | ----------------------------- | ------------------- |
| order_id            | VARCHAR   | Order identifier              | Foreign Key         |
| order_item_id       | INT       | Item sequence within an order | Primary Key         |
| product_id          | VARCHAR   | Product identifier            | Foreign Key         |
| seller_id           | VARCHAR   | Seller identifier             | Foreign Key         |
| shipping_limit_date | DATETIME  | Seller shipping deadline      | —                   |
| price               | DECIMAL   | Product price                 | —                   |
| freight_value       | DECIMAL   | Freight/shipping cost         | —                   |

**Rows:** 112,650
**Primary Key:** `(order_id, order_item_id)`
**Foreign Keys:**
* `order_id → orders.order_id`
* `product_id → products.product_id`
* `seller_id → sellers.seller_id`

---

## 2.2.5. Order Payments

The `order_payments` table contains payment information for orders.

| Column               | Data Type | Description                | Key                 |
| -------------------- | --------- | -------------------------- | ------------------- |
| order_id             | VARCHAR   | Order identifier           | Foreign Key         |
| payment_sequential   | INT       | Sequence number of payment | Primary Key         |
| payment_type         | VARCHAR   | Payment method             | —                   |
| payment_installments | INT       | Number of installments     | —                   |
| payment_value        | DECIMAL   | Payment amount             | —                   |

**Rows:** 103,886
**Primary Key:** `(order_id, payment_sequential)`
**Foreign Key:** `order_id → orders.order_id`

---

## 2.2.6. Order Reviews

The `order_reviews` table contains customer review information.

| Column                  | Data Type    | Description                                         | Key         |
| ----------------------- | ------------ | --------------------------------------------------- | ----------- |
| review_id               | VARCHAR      | Review identifier                                   | Primary Key |          |
| order_id                | VARCHAR      | Associated order                                    | Foreign Key |
| review_score            | INT          | Customer rating from 1 to 5                         | —           |
| review_comment_title    | VARCHAR/TEXT | Review title                                        | —           |
| review_comment_message  | TEXT         | Review message                                      | —           |
| review_creation_date    | DATETIME     | Review creation date                                | —           |
| review_answer_timestamp | DATETIME     | Review response timestamp                           | —           |

---
## 2.2.7. Products

The `products` table contains information about products sold on the platform.

| Column                        | Data Type | Description                   | Key         |
| ----------------------------- | --------- | ----------------------------- | ----------- |
| product_id                    | VARCHAR   | Unique product identifier     | Primary Key |
| product_category_name         | VARCHAR   | Original product category     | Foreign Key |
| product_name_length           | INT       | Length of product name        | —           |
| product_description_length    | INT       | Length of product description | —           |
| product_photos_qty            | INT       | Number of product photographs | —           |
| product_weight_g              | DECIMAL   | Product weight in grams       | —           |
| product_length_cm             | DECIMAL   | Product length                | —           |
| product_height_cm             | DECIMAL   | Product height                | —           |
| product_width_cm              | DECIMAL   | Product width                 | —           |


**Rows:** 32,951
**Primary Key:** product_id
**Foreign Key:** product_category_name 
product_category_name → product_category_translation.product_category_name

---

## 2.2.8. Sellers

The `sellers` table contains information about sellers.

| Column                 | Data Type | Description              | Key         |
| ---------------------- | --------- | ------------------------ | ----------- |
| seller_id              | VARCHAR   | Unique seller identifier | Primary Key |
| seller_zip_code_prefix | INT       | Seller ZIP-code prefix   | Foreign Key |
| seller_city            | VARCHAR   | Seller city              | —           |
| seller_state           | VARCHAR   | Seller state             | —           |

**Rows:** 3,095

**Primary Key:** seller_id
**Foreign Key:** seller_zip_code_prefix
---

## 2.2.9. Product Category Translation

The `product_category_translation` table maps the original Portuguese product category names to English category names.

| Column                        | Data Type | Description            | Key         |
| ----------------------------- | --------- | ---------------------- | ----------- |
| product_category_name         | VARCHAR   | Original category name | Primary Key |
| product_category_name_english | VARCHAR   | English category name  | —           |

**Rows:** 73
**Primary Key:** `product_category_name`

Two categories referenced by products were added during SQL preparation because they were missing 
from the original cleaned category file. This allowed the product-category foreign-key relationship to be maintained.

## 2.3. Identify Primary Keys 

Primary keys uniquely identify records within each table.

| Table                        | Primary Key                      |
| ---------------------------- | -------------------------------- |
| customers                    |  customer_id                     |
| geolocation                  |  geolocation_zip_code_prefix     |
| orders                       |  order_id                        |
| order_items                  |  order_item_id                   |
| order_payments               |  payment_sequential              |
| order_reviews                |  review_id                       |
| products                     |  product_id                      |
| sellers                      |  seller_id                       |
| product_category_translation |  product_category_name           |

## 2.4 Identify Foreign Keys

The major foreign-key relationships in the database are:

| Child Table    | Foreign Key                | Parent Table                 | Parent Key              |
| -------------- | -----------------------    | ---------------------------- | ----------------------- |
| orders         | customer_zip_code_prefix   | customers                    | customer_id             |
| order_items    | order_id                   | orders                       | order_id                |
| order_items    | product_id                 | products                     | product_id              |
| order_items    | seller_id                  | sellers                      | seller_id               |
| order_payments | order_id                   | orders                       | order_id                |
| order_reviews  | order_id                   | orders                       | order_id                | 
| products       | product_category_name      | category_translation         | product_category_name   |
| sellers        | seller_zip_code_prefix     | geolocation                  | geolocation_zip_code_prefix|
| customers      | customer_zip_code_prefix   | geolocation                  | geolocation_zip_code_prefix|
    

All relationship in the table above is a valid, enforceable foreign key, since each parent key listed is a true primary key.

## 2.5.  Understanding the Relationships between table
Understanding how these tables relate to one another is essential before any cleaning, warehousing, or analysis can begin.

The nine tables in this dataset are not independent — together, they form a single, connected structure that traces 
the complete lifecycle of an order, from the moment a customer places it to the moment they leave a review.


1. Customers Dataset - olist_customers_dataset.csv
   Key Field: customer_id
   Links to:  Orders Dataset via customer_id → identifies which orders belong to which customer.
   Insight:  Helps track churn, repeat purchases, and customer segmentation.

2. Orders Dataset - olist_orders_dataset.csv
   Key Field:   order_id
   Links to:   
                Customers Dataset (customer_id)
                Order Items Dataset (order_id)
                Order Payments Dataset (order_id)
                Order Reviews Dataset (order_id)
   Insight:     Central hub table — connects customers, items, payments, and reviews.

3. Order Items Dataset - olist_order_items_dataset.csv
   Key Fields:  order_id, product_id, seller_id
   Links to:
                Orders Dataset (order_id)
                Products Dataset (product_id)
                Sellers Dataset (seller_id)

    Insight:    Defines what products were bought, from which seller, in each order.

4. Products Dataset - olist_products_dataset.csv
   Key Field:   product_id
   Links to:
                Order Items Dataset (product_id)
                Product Category Translation Dataset (product_category_name)
   Insight:     Provides product details and category mapping for analysis.

5. Product Category Translation - product_category_name_translation.csv
   Key Field:   product_category_name
   Links to:
                Products Dataset (product_category_name)
   Insight:     Translates Portuguese product categories into English for easier reporting.

6. Order Payments Dataset - olist_order_payments_dataset.csv)\
   Key Field:   order_id
   Links to:
                Orders Dataset (order_id)
   Insight:     Tracks payment methods, installments, and amounts.

7. Order Reviews Dataset -olist_order_reviews_dataset.csv
   Key Field:   order_id
   Links to:
                Orders Dataset (order_id)
   Insight:     Captures customer feedback, ratings, and review timestamps.

8. Sellers Dataset - olist_sellers_dataset.csv
   Key Field:   seller_id
   Links to:
   Order Items Dataset (seller_id)
   Insight:    Provides seller location and identity, useful for seller performance analysis.

9. Geolocation Dataset - olist_geolocation_dataset.csv
   Key Fields: geolocation_zip_code_prefix
   Links to:
               Customers Dataset (customer_zip_code_prefix)
               Sellers Dataset (seller_zip_code_prefix)
   Insight:    Enables mapping of customer and seller locations based on ZIP-code prefixes for delivery optimization.

## 2.6.ER Diagram
[ER Diagram](https://shadiyapp.github.io/Decoding-E-Commerce-Performance/)
## 2.7.Prepare a Data Dictionary

A data dictionary provides a structured description of the fields used in the project.

| Table                        | Column                        | Data Type    | Description                                      |
| ---------------------------- | ----------------------------- | ------------ | ------------------------------------------------ |
| customers                    | customer_id                   | VARCHAR      | Unique customer/order record identifier          |
| customers                    | customer_unique_id            | VARCHAR      | Customer-level identifier                        |
| customers                    | customer_zip_code_prefix      | INT          | Customer ZIP-code prefix                         |
| customers                    | customer_city                 | VARCHAR      | Customer city                                    |
| customers                    | customer_state                | VARCHAR      | Customer state                                   |
| geolocation                  | geolocation_zip_code_prefix   | INT          | ZIP-code prefix                                  |
| geolocation                  | geolocation_lat               | DECIMAL      | Geographic latitude                              |
| geolocation                  | geolocation_lng               | DECIMAL      | Geographic longitude                             |
| geolocation                  | geolocation_city              | VARCHAR      | Geographic city                                  |
| geolocation                  | geolocation_state             | VARCHAR      | Geographic state                                 |
| orders                       | order_id                      | VARCHAR      | Unique order identifier                          |
| orders                       | customer_id                   | VARCHAR      | Customer associated with order                   |
| orders                       | order_status                  | VARCHAR      | Current order status                             |
| orders                       | order_purchase_timestamp      | DATETIME     | Order purchase date and time                     |
| orders                       | order_approved_at             | DATETIME     | Payment approval date and time                   |
| orders                       | order_delivered_carrier_date  | DATETIME     | Date handed to carrier                           |
| orders                       | order_delivered_customer_date | DATETIME     | Date delivered to customer                       |
| orders                       | order_estimated_delivery_date | DATETIME     | Estimated delivery date                          |
| orders                       | actual_delivery_days          | INT          | Actual delivery duration                         |
| orders                       | estimated_delivery_days       | INT          | Estimated delivery duration                      |
| orders                       | delivery_delay_days           | INT          | Difference between actual and estimated delivery |
| order_items                  | order_id                      | VARCHAR      | Associated order                                 |
| order_items                  | order_item_id                 | INT          | Item sequence within order                       |
| order_items                  | product_id                    | VARCHAR      | Associated product                               |
| order_items                  | seller_id                     | VARCHAR      | Associated seller                                |
| order_items                  | shipping_limit_date           | DATETIME     | Shipping deadline                                |
| order_items                  | price                         | DECIMAL      | Product price                                    |
| order_items                  | freight_value                 | DECIMAL      | Shipping/freight cost                            |
| order_payments               | order_id                      | VARCHAR      | Associated order                                 |
| order_payments               | payment_sequential            | INT          | Payment sequence                                 |
| order_payments               | payment_type                  | VARCHAR      | Payment method                                   |
| order_payments               | payment_installments          | INT          | Number of installments                           |
| order_payments               | payment_value                 | DECIMAL      | Payment amount                                   |
| order_reviews                | review_pk                     | INT          | Unique review record identifier                  |
| order_reviews                | review_id                     | VARCHAR      | Review identifier                                |
| order_reviews                | order_id                      | VARCHAR      | Associated order                                 |
| order_reviews                | review_score                  | INT          | Customer rating from 1 to 5                      |
| order_reviews                | review_comment_title          | VARCHAR/TEXT | Review title                                     |
| order_reviews                | review_comment_message        | TEXT         | Review message                                   |
| order_reviews                | review_creation_date          | DATETIME     | Review creation date                             |
| order_reviews                | review_answer_timestamp       | DATETIME     | Review response date                             |
| products                     | product_id                    | VARCHAR      | Unique product identifier                        |
| products                     | product_category_name         | VARCHAR      | Original product category                        |
| products                     | product_category_name_english | VARCHAR      | English product category                         |
| products                     | product_name_length           | INT          | Product-name length                              |
| products                     | product_description_length    | INT          | Product-description length                       |
| products                     | product_photos_qty            | INT          | Number of product photos                         |
| products                     | product_weight_g              | DECIMAL      | Product weight                                   |
| products                     | product_length_cm             | DECIMAL      | Product length                                   |
| products                     | product_height_cm             | DECIMAL      | Product height                                   |
| products                     | product_width_cm              | DECIMAL      | Product width                                    |
| sellers                      | seller_id                     | VARCHAR      | Unique seller identifier                         |
| sellers                      | seller_zip_code_prefix        | INT          | Seller ZIP-code prefix                           |
| sellers                      | seller_city                   | VARCHAR      | Seller city                                      |
| sellers                      | seller_state                  | VARCHAR      | Seller state                                     |
| product_category_translation | product_category_name         | VARCHAR      | Original category name                           |
| product_category_translation | product_category_name_english | VARCHAR      | English category name                            |

## 2.8. Understand columns and data types

Dataset 1
customer_id : str
customer_unique_id : str
customer_zip_code_prefix : int64
customer_city : str
customer_state : str

Dataset 2
geolocation_zip_code_prefix : int64
geolocation_lat : float64
geolocation_lng : float64
geolocation_city : str
geolocation_state : str

Dataset 3
order_id : str
order_item_id : int64
product_id : str
seller_id : str
shipping_limit_date : str
price : float64
freight_value : float64

Dataset 4
order_id : str
payment_sequential : int64
payment_type : str
payment_installments : int64
payment_value : float64

Dataset 5
review_id : str
order_id : str
review_score : int64
review_comment_title : str
review_comment_message : str
review_creation_date : str
review_answer_timestamp : str

Dataset 6
order_id : str
customer_id : str
order_status : str
order_purchase_timestamp : str
order_approved_at : str
order_delivered_carrier_date : str
order_delivered_customer_date : str
order_estimated_delivery_date : str

Dataset 7
product_id : str
product_category_name : str
product_name_lenght : float64
product_description_lenght : float64
product_photos_qty : float64
product_weight_g : float64
product_length_cm : float64
product_height_cm : float64
product_width_cm : float64

Dataset 8
seller_id : str
seller_zip_code_prefix : int64
seller_city : str
seller_state : str

Dataset 9
product_category_name : str
product_category_name_english : str

******************************************************************************************************************************************************************
******************************************************************************************************************************************************************
# Step 3:Raw Data
## 3.1 Load the Raw Data
The objective of this step is to load all raw CSV files into Python using Pandas and understand the initial structure of the dataset before performing data cleaning and preprocessing.
To ensure that the dataset working with is accurate, consistent, and ready for meaningful analysis or modeling.In other words, it transforms raw, messy data into a reliable form that can
produce trustworthy insights

For each dataset, the following checks were performed:

Number of rows and columns
Column names
Data types
Basic structure of the data
Identification of potential data-quality issues

The raw datasets were loaded using the Pandas library
## 3.2 Check shape, columns, and data types
Loop through each DataFrame to check shape, columns, and data types

## 3.3 Understand the structure of each table
 This check gives overview of each raw dataset before cleaning. 
 Helps to find how many rows/columns exist, what fields are available, and whether you need to handle missing values or type conversions.

******************************************************************************************************************************************************************
******************************************************************************************************************************************************************
# STEP: 4  Data Quality Analysis
The objective is to systematically assess the quality of the raw e-commerce datasets before performing data cleaning and transformation.

## 4.1 To investigate:

1.Missing values
2.Exact duplicates
3.Primary-key uniqueness
4.Foreign-key validity
5.Incorrect Data types
6.Categorical consistency
7.Numerical validity
8.Date validity
9.Potential outliers

******************************************************************************************************************************************************************
******************************************************************************************************************************************************************
# STEP: 5 Data Cleaning & Preprocessing
Data Cleaning & Preprocessing is the essential step that transforms raw, messy datasets into reliable, analysis‑ready information. 
It invovles
1. Load the Data  
2. CHECK THE DATA  
3. Create cleaned copies and Remove exact duplicate rows  
4. VERIFY DUPLICATES  
5. HANDLE INCORRECT DATA TYPES  
6. IDENTIFY INVALID / INCONSISTENT VALUES  
7. ORDER DATE CONSISTENCY  
8. CATEGORICAL VALUE CHECK  
9. INSPECT SUSPICIOUS PAYMENT VALUES  
10. INSPECT DATE INCONSISTENCIES  
11. PAYMENT DATA QUALITY FLAGS  
12. DATE CONSISTENCY CHECK  
13. STANDARDIZE CATEGORICAL VALUES  
14. HANDLE INVALID RECORDS  
15. FLAG INVALID PAYMENT RECORDS  
16. RENAME COLUMNS WHERE REQUIRED  
17. UPDATE CLEAN DATASET DICTIONARY  
18. FINAL SAVE VERIFICATION  
19. OUTLIER DETECTION USING IQR  
20. PRIMARY KEY / UNIQUENESS CHECK  
21. DUPLICATE REVIEW ID INVESTIGATION  
22. REVIEW COMPOSITE KEY CHECK  
23. MISSING VALUE SUMMARY  
24. HANDLE MISSING REVIEW TEXT  
25. HANDLE MISSING PRODUCT CATEGORY  
26. PRODUCT MEASUREMENT MISSING FLAG  
27. FINAL MISSING VALUE VERIFICATION  
28. PRODUCT METADATA MISSING FLAG  


Save all the cleaned datasets.

******************************************************************************************************************************************************************
******************************************************************************************************************************************************************
# Step 6 Store Cleaned Data in MySQL

>CREATE DATABASE cart2;

Create tables based on the ER diagram

1. customers
2. orders
3. order_items
4. order_payments
5. order_reviews
6. products
7. sellers
8. geolocation
9.category_translation
-------------------------------------------
##  Define Primary Keys

1.customers.customer_id
2.orders.order_id
3.products.product_id
4.sellers.seller_id

---------------------------------------------
## Define Foreign Keys

1. orders.customer_id → customers.customer_id
2. order_items.order_id → orders.order_id
3. order_items.product_id → products.product_id
4. order_items.seller_id → sellers.seller_id
5. order_payments.order_id → orders.order_id
6. order_reviews.order_id → orders.order_id
----------------------------------------------------
| Business question    | Main SQL concepts     |
| -------------------- | --------------------- |
| Total Revenue        | `SUM()`               |
| Total Orders         | `COUNT()`             |
| Total Customers      | `COUNT()`             |
| Total Sellers        | `COUNT()`             |
| Average Order Value  | `AVG()` / aggregation |
| Average Review Score | `AVG()`               |

>>Load the cleaned CSV files
>>Verify row counts
>>primary-key uniqueness
>>foreign-key integrity
>>NULL values
******************************************************************************************************************************************************************************************************************
******************************************************************************************************************************************************************************************************************
# STEP: 7 FEATURE ENGINEERING


## Feature Meaning
1. total_order_value :     	Total payment value for an order

2. delivery_days:            Actual number of days taken to deliver
. 
3.delivery_delay:            Days delayed compared with estimated delivery

4.customer_order_count:      Number of orders placed by the customer

5.customer_total_spending:   Total amount spent by the customer

6.average_order_value:       Customer's average spending per order

7.seller_revenue:            Total revenue generated by the seller

8.seller_order_count:        Number of orders handled by the seller

9.repeat_customer:           1 if customer has more than one order, otherwise 0

## Feature	Definition

1	Total Order Value:Sum of price + freight_value for all items in an order

2	Actual Delivery Days	:Delivered customer date − order purchase date

3	Delivery Delay Days	: Actual delivery date − estimated delivery date

4	Customer Order Count	:Number of unique orders placed by the customer

5	Customer Total Spending	 : Sum of price + freight_value across all customer orders

6	Average Spending per Order	 : Customer total spending ÷ customer order count

7	Seller Revenue	 : Sum of price for products sold by the seller

8	Seller Order Count	: Number of unique orders handled by the seller

9	Repeat Customer	  :if customer has more than one order, otherwise 0

Feature Engineering: 
Created meaningful business features including order value, delivery performance, customer purchasing behavior, repeat-customer indicators, 
and seller performance metrics using SQL aggregations, CTEs, joins, and conditional logic.

******************************************************************************************************************************************************************
******************************************************************************************************************************************************************
# Step 8 Exploratory Data Analysis

1.Bring data from SQL into Python
2. Load EDA data
3.Numerical summary
4.Univariate Analysis.
5.Bivariate Analysis
  5.1Correlation Heatmap
6.Multivariate Analysis
7.Order Value Distribution
8.Boxplot Analysis
9.Actual Delivery Days Distribution
10.Delivery Delay Distribution
11.Review Score Distribution
12.Trend analysis

******************************************************************************************************************************************************************
******************************************************************************************************************************************************************
# Step 9: Statistical Analysis

1.T-Test — Delivery & Customer Satisfaction
2.Connect the SQL Database
3.Create the two T-test groups
4.Perform the T-Test
5.Check the T-test assumptions
6.Statistical Summary
7.Business Insight
8.ANOVA — Product Category & Spending
9.Chi-Square Test — Payment Method & Order Status

******************************************************************************************************************************************************************
******************************************************************************************************************************************************************
# Step 10 SQL Analysis & Streamlit Dashboard
SQL is used to query and aggregate the cleaned e‑commerce datasets stored in a relational database.
>>Connect MySQL to Streamlut Dashboard

Create Dashboards with:
## Create dashboard tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "📈 Sales Analysis",
        ●	Monthly revenue trend
        ●	Revenue by category
        ●	Top-selling products
        ●	Sales by location

        "👥 Customer Analysis",
        ●	Customer distribution
        ●	Customer spending
        ●	Repeat vs new customers
        ●	Top customers

        "🏪 Seller & Product",
        ●	Top sellers
        ●	Seller revenue
        ●	Product/category performance
        ●	Seller ratings

        "🚚 Delivery Analysis",
        ●	Average delivery time
        ●	On-time vs delayed orders
        ●	Delivery performance by location
        ●	Delivery delay vs review score

        "⭐ Customer Experience",
        ●	Review score distribution
        ●	Reviews by category
        ●	Rating vs delivery performance
        
        "📋 Data Tables"
        "📋 Weekly Reports"
        
        
**********************************************************************************************************************************************************************************************************************
**********************************************************************************************************************************************************************************************************************
# Step 11: Generate Business Insights

## Project Findings Summary

This project has produced the following major findings:
Revenue

Total revenue: ₹15,843,553.24
Total orders: 99,441
Average order value: ₹160.58

Sales Trend
Revenue generally increased throughout 2017 and into 2018. November 2017 recorded the highest monthly revenue, at approximately ₹11.79 lakh. 
September 2018 appears to represent an incomplete reporting period.

## Product Categories

Health & Beauty, Watches & Gifts, Bed, Bath & Table, Sports & Leisure, and Computers & Accessories were among the highest-revenue categories.
ANOVA testing confirmed statistically significant differences in category-level spending (F = 153.796, p < 0.001).

## Delivery

The average delivery time was 12.50 days. Of all orders, 89,941 were delivered on time or early, while 6,535 were delayed. 
Delayed orders recorded an average review score of 2.27, compared with 4.29 for on-time or early deliveries — a difference confirmed by a t-test (p < 0.001).

## Customer Experience

The overall average review score was 4.09 out of 5, with 5-star reviews forming the largest group. 
Delivery delays showed a strong negative relationship with review scores.

## Customer Behavior

The dataset classifies all customers as new customers. This reflects an important limitation of the Olist dataset: the customer_id field 
is effectively order-specific, meaning repeat-customer behavior cannot be reliably inferred from this field alone.

## Payment & Order Status

A Chi-Square test indicated a statistically significant association between payment method and order status (χ² = 677.083, p < 0.001). 
However, since 45% of expected cell counts were below 5, this result should be interpreted with caution.

## Translating Findings into Recommendations

The following recommendations connect each finding directly to a corresponding business action:

## Finding	                                                    Business Recommendation
    
Delayed orders have much lower ratings	                       Improve delivery monitoring and identify delayed shipments early
Some states have substantially longer delivery times	       Investigate logistics performance and carrier coverage by region
Spending varies significantly by category	                   Apply category-specific pricing, promotions, and inventory strategies
Revenue shows strong seasonal variation	                       Plan inventory and marketing efforts around high-revenue periods
High-revenue categories contribute substantially to sales	   Maintain availability and closely monitor stock levels in these categories
Overall review score is 4.09/5	                               Maintain current service quality while focusing improvement efforts on low-rated orders
Customer repeat behavior cannot be reliably measured	       Adopt a stable customer identifier to enable future retention analysis
Payment/order-status Chi-Square result has sparse cells	       Monitor payment-status patterns, but avoid drawing strong conclusions from this 
                                                               test without further analysis
        
******************************************************************************************************************************************************************
# Project Directory Structure
```text
 Cart2Insights/
├── data/
│   ├── raw/                                  # Raw data of the project
│   │   ├── olist_customers_dataset.csv
│   │   ├── olist_geolocation_dataset.csv
│   │   ├── olist_order_items_dataset.csv
│   │   ├── olist_order_payments_dataset.csv
│   │   ├── olist_order_reviews_dataset.csv
│   │   ├── olist_orders_dataset.csv
│   │   ├── olist_products_dataset.csv
│   │   ├── olist_sellers_dataset.csv
│   │   └── product_category_name_translation.csv
│
│   └── cleaned/                              # Cleaned, standardized, and enriched analytical datasets
│       ├── customers_cleaned.csv
│       ├── products_cleaned.csv
│       ├── sellers_cleaned.csv
│       ├── geolocation_cleaned.csv
│       ├── order_items_cleaned.csv
│       ├── order_payments_cleaned.csv
│       ├── order_reviews_cleaned.csv
│       ├── category_translation_cleaned.csv
│       └── orders_cleaned.csv
│
├── notebooks/                               # Jupyter notebooks for EDA and statistical modeling
│   ├── Step 1 Understanding the Business Problem.ipynb
│   ├── Step 2 Understand the Dataset & ER Diagram.ipynb
│   ├── Step 3 Load the Raw Data.ipynb
│   ├── Step 4 Data Quality Analysis.ipynb
│   ├── Step 5 Data Cleaning & Preprocessing.ipynb
│   ├── Step 6 Store Clean Data in SQL.ipynb
│   ├── Step 7 Feature Engineering.ipynb
│   ├── Step 8 Exploratory Data Analysis.ipynb
│   ├── Step 9 Statistical Analysis.ipynb
│   ├── Step 10 SQL Analysis & Streamlit Dashboard.ipynb
│   └── Step 11 Business Insight.ipynb
│
├── Database/
│   └── Cart2.sql                            # MySQL DDL schemas, indexing scripts, and analytical queries
│
├── streamlit/
│   ├── app.py                               # Main entry point of the Streamlit dashboard
│   ├── database.py                          # Handles database connections and configurations
│   ├── queries.py                           # Stores SQL queries or ORM functions for retrieving data
│   ├── utils.py                             # Utility/helper functions used across the project
│   └── weekly_reports.py                    # Generates weekly performance reports from the data
│
└── README.md
*************************************************

