-- Business Question 1
-- Berapa total revenue?

SELECT
     sum(Revenue) AS total_revenue
FROM coffee_shop_sales;

-- ===========================================
-- Business Question 2
-- Outlet mana yang memiliki revenue tertinggi?

SELECT
    store_location,
	sum(Revenue) AS total_revenue
From coffee_shop_sales
GROUP BY store_location
ORDER BY total_revenue DESC;

-- ===========================================
-- Business Question 3
-- Produk apa yang paling banyak terjual?

SELECT 
    product_detail,
	SUM (transaction_qty) AS total_quantity
FROM coffee_shop_sales
GROUP BY product_detail
ORDER BY total_quantity DESC
limit 5;

-- ===========================================
-- Business Question 4
-- Kategori produk dengan revenue terbesar

SELECT
    product_category,
	sum (Revenue) AS total_revenue
FROM coffee_shop_sales
GROUP BY product_category
ORDER BY total_revenue DESC;

-- ===========================================
-- Business Question 5
-- Revenue berdasarkan bulan

SELECT
    Month,
	sum(Revenue) AS total_revenue
FROM coffee_shop_sales
GROUP BY Month;

-- ===========================================
-- Business Question 6
-- Jumlah revenue tiap outlet

SELECT
    store_location,
	SUM (Revenue) AS total_revenue
FROM coffee_shop_sales
GROUP BY store_location
ORDER BY total_revenue DESC;
