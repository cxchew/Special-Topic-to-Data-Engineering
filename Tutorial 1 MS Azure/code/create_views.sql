-- Azure Synapse Analytics Serverless SQL Script
-- Description: Creates external views over Gold Delta tables for Power BI consumption.

CREATE DATABASE gold_db;
GO

USE gold_db;
GO

-- 1. Create View for Customer Dimensions
CREATE OR ALTER VIEW dbo.dim_customer AS
SELECT *
FROM OPENROWSET(
    BULK 'https://yourstorageaccount.dfs.core.windows.net/gold/dim_customer/',
    FORMAT = 'DELTA'
) AS [result];
GO

-- 2. Create View for Fact Sales Transactions
CREATE OR ALTER VIEW dbo.fact_sales AS
SELECT *
FROM OPENROWSET(
    BULK 'https://yourstorageaccount.dfs.core.windows.net/gold/fact_sales/',
    FORMAT = 'DELTA'
) AS [result];
GO

-- Verification Check Query
SELECT TOP 10 * FROM dbo.dim_customer;
GO
