import os
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime

def initializeDatabaseInstance():
    '''
    Initializes sqlite database instance in repository
    '''
    script_dir = os.path.dirname(__file__)
    salesCSV = os.path.join(script_dir, 'sales_data_sampleUTF8.csv')
    data = pd.read_csv(salesCSV, encoding='ISO-8859-1')

    db_path = os.path.join(script_dir,'sales_db.sqlite')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    columns = ', '.join([f"{col} TEXT" for col in data.columns])  
    table_name = 'sales_data'  
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
    conn.commit()
    data.to_sql(table_name, conn, if_exists='replace', index=False)  

    print('Database initialized. Displaying first 5 records of `sales_data` table:')
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")  
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    conn.close()


def initializeDatabaseConnection():
    """Initializes sqlite connection and cursor to sales database. Make sure to close the database connection after with `conn.close()`

    Returns:
        `conn`: connection to db
        `cursor`: cursor to db
    """
    script_dir = os.path.dirname(__file__)
    db_path = os.path.join(script_dir,'sales_db.sqlite')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor
    

def getUniqueCustomers():
    """Generates a list of the unique customers from the sales database table.

    Returns:
        `list`: List of the unique customers from the sales database table.
    """
    conn, cursor = initializeDatabaseConnection()
    data = pd.read_sql_query('SELECT * FROM sales_data', con=conn)
    conn.close()
    return data['CUSTOMERNAME'].unique().tolist()

def getMetricsIterative():
    """Calculates the following sales metrics: average quantities of orders, average life span, average total profit, average profit margin 

    Returns:
        `dict`: Dictionary which contains meanOrderAmount, meanLifespan, meanTotalProfit, and meanProfitMargin
    """
    customerList = getUniqueCustomers()
    conn, cursor = initializeDatabaseConnection()
    data = pd.read_sql_query('SELECT * FROM sales_data', con=conn)
    data['ORDERDATE'] = pd.to_datetime(data['ORDERDATE'])
    conn.close()

    results = {}
    for eachCustomer in customerList:
        customer_data = data[data['CUSTOMERNAME'] == eachCustomer].copy()
        orderAmount = customer_data.shape[0]
        lifespan_days = (customer_data['ORDERDATE'].max() - customer_data['ORDERDATE'].min()).days
        total_profit = (customer_data['SALES'] - (customer_data['MSRP'] * customer_data['QUANTITYORDERED'])).sum()
        
        if orderAmount > 0:
            profit_per_order = total_profit / orderAmount
            customer_data['MARGIN'] = (customer_data['SALES'] - (customer_data['MSRP'] * customer_data['QUANTITYORDERED'])) / customer_data['SALES']
            profitMargin = customer_data['MARGIN'].mean()
        else:
            profit_per_order = 0
            profitMargin = 0  
        
        results[eachCustomer] = {
            'orderAmount': orderAmount,
            'lifespanDays': lifespan_days,
            'totalProfit': total_profit,
            'profitMargin': profitMargin,
            'profitPerOrder': profit_per_order
        }

    mean_metrics = {
        'meanOrderAmount': np.mean([item['orderAmount'] for item in results.values()]),
        'meanLifespanDays': np.mean([item['lifespanDays'] for item in results.values()]),
        'meanTotalProfit': np.mean([item['totalProfit'] for item in results.values()]),
        'meanProfitMargin': np.mean([item['profitMargin'] for item in results.values()]),
        'meanProfitPerOrder': np.mean([item['profitPerOrder'] for item in results.values()])
    }
    return mean_metrics

def getCLV_Iterative():
    """Calculates customer lifetime value using average metrics from the entire sales table.

    Returns:
        `float`: Customer lifetime value.
    """
    metrics = getMetricsIterative()
    avg_profit_per_order = metrics['meanProfitPerOrder']
    avg_order_frequency = metrics['meanOrderAmount'] / (metrics['meanLifespanDays'] / 365)  # convert lifespan to years
    avg_lifespan_years = metrics['meanLifespanDays'] / 365

    clv = avg_profit_per_order * avg_order_frequency * avg_lifespan_years
    return clv



def getMetricsRecursive(data, customerList, index=0, results=None):
    """Using recursive methods, calculates the following sales metrics: average quantities of orders, average life span, average total profit, average profit margin.

    Args:
        data (`DataFrame`): The customer sales data table, in the d type of `DataFrame`
        customerList (`list`): The unique list of customers. This list will be filled with the `getUniqueCustomer()` function.
        index (int, optional): Tracks if the function has iterated through the customer list. Should not be changed. Defaults to 0.
        results (`dict`, optional): Stores results. Should not be changed. Defaults to None.

    Returns:
        `dict`: Dictionary which contains meanOrderAmount, meanLifespan, meanTotalProfit, and meanProfitMargin
    """
    if results is None:
        results = {}
    if index >= len(customerList): # checks if the recursion has processed all customers. If index is equal to or greater than the length of customerList, it computes the average (mean) of all metrics collected in the results dictionary and returns them.
        mean_metrics = {
            'meanOrderAmount': np.mean([item['orderAmount'] for item in results.values()]),
            'meanLifespanDays': np.mean([item['lifespanDays'] for item in results.values()]),
            'meanTotalProfit': np.mean([item['totalProfit'] for item in results.values()]),
            'meanProfitMargin': np.mean([item['profitMargin'] for item in results.values()]),
            'meanProfitPerOrder': np.mean([item['profitPerOrder'] for item in results.values()])
        }
        return mean_metrics
    else:
        customer_data = data[data['CUSTOMERNAME'] == customerList[index]].copy()
        orderAmount = customer_data.shape[0]
        lifespan_days = (customer_data['ORDERDATE'].max() - customer_data['ORDERDATE'].min()).days
        total_profit = (customer_data['SALES'] - (customer_data['MSRP'] * customer_data['QUANTITYORDERED'])).sum()

        if orderAmount > 0:
            profit_per_order = total_profit / orderAmount
            customer_data['MARGIN'] = (customer_data['SALES'] - (customer_data['MSRP'] * customer_data['QUANTITYORDERED'])) / customer_data['SALES']
            profitMargin = customer_data['MARGIN'].mean()
        else:
            profit_per_order = 0
            profitMargin = 0

        results[customerList[index]] = {
            'orderAmount': orderAmount,
            'lifespanDays': lifespan_days,
            'totalProfit': total_profit,
            'profitMargin': profitMargin,
            'profitPerOrder': profit_per_order
        }

        return getMetricsRecursive(data, customerList, index + 1, results)

def getCLV_Recursive(metrics):
    avg_profit_per_order = metrics['meanProfitPerOrder']
    avg_order_frequency = metrics['meanOrderAmount'] / (metrics['meanLifespanDays'] / 365)
    avg_lifespan_years = metrics['meanLifespanDays'] / 365

    return avg_profit_per_order * avg_order_frequency * avg_lifespan_years

def mainRecursive():
    customerList = getUniqueCustomers()
    conn, cursor = initializeDatabaseConnection()
    data = pd.read_sql_query('SELECT * FROM sales_data', con=conn)
    data['ORDERDATE'] = pd.to_datetime(data['ORDERDATE'])
    conn.close()

    metrics = getMetricsRecursive(data, customerList)
    clv =  getCLV_Recursive(metrics)
    return clv

# Call mainRecursive function to get the CLV
clv = mainRecursive()
print(f"Recursive CLV Calculation: {clv}")


def getUniqueCustomersSQL():
    """Generates a list of the unique customers from the sales database table."""
    conn, cursor = initializeDatabaseConnection()
    query = 'SELECT DISTINCT CUSTOMERNAME FROM sales_data'
    customer_data = pd.read_sql_query(query, con=conn)
    conn.close()
    return customer_data['CUSTOMERNAME'].tolist()

def getMetricsIterativeSQL():
    """Calculates sales metrics using SQL aggregation functions directly."""
    conn, cursor = initializeDatabaseConnection()
    
    # Query to calculate metrics for each customer directly in SQL
    query = '''
    SELECT CUSTOMERNAME, COUNT(*) AS orderAmount, 
        DATEDIFF(MAX(ORDERDATE), MIN(ORDERDATE)) AS lifespanDays,
        SUM(SALES - MSRP * QUANTITYORDERED) AS totalProfit,
        AVG((SALES - MSRP * QUANTITYORDERED) / SALES) AS profitMargin
    FROM sales_data
    GROUP BY CUSTOMERNAME
    '''
    
    results = pd.read_sql_query(query, con=conn)
    conn.close()

    # Calculating mean of the metrics from the results
    mean_metrics = {
        'meanOrderAmount': results['orderAmount'].mean(),
        'meanLifespanDays': results['lifespanDays'].mean(),
        'meanTotalProfit': results['totalProfit'].mean(),
        'meanProfitMargin': results['profitMargin'].mean()
    }
    
    return mean_metrics

def getCLV_IterativeSQL():
    """Calculates customer lifetime value using average metrics from the entire sales table."""
    metrics = getMetricsIterative()
    avg_profit_per_order = metrics['meanTotalProfit'] / metrics['meanOrderAmount']
    avg_order_frequency = metrics['meanOrderAmount'] / (metrics['meanLifespanDays'] / 365)
    avg_lifespan_years = metrics['meanLifespanDays'] / 365

    clv = avg_profit_per_order * avg_order_frequency * avg_lifespan_years
    return clv
