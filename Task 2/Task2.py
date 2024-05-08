import os
import pandas as pd
import sqlite3

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
    """Generates a list of the unique characters from the sales database table. 

    Returns:
        `list`: Unique sales customers
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
        lifespan = (customer_data['ORDERDATE'].max() - customer_data['ORDERDATE'].min()).days
        total_profit = (customer_data['SALES'] - (customer_data['MSRP'] * customer_data['QUANTITYORDERED'])).sum()
        
        if orderAmount > 0:
            customer_data['MARGIN'] = (customer_data['SALES'] - (customer_data['MSRP'] * customer_data['QUANTITYORDERED'])) / customer_data['SALES']
            profitMargin = customer_data['MARGIN'].mean()
        else:
            profitMargin = 0  
        
        results[eachCustomer] = {'orderAmount': orderAmount, 'lifespan': lifespan, 'totalProfit': total_profit, 'profitMargin': profitMargin}

    mean_metrics = {
        'meanOrderAmount': sum(item['orderAmount'] for item in results.values()) / len(results),
        'meanLifespan': sum(item['lifespan'] for item in results.values()) / len(results),
        'meanTotalProfit': sum(item['totalProfit'] for item in results.values()) / len(results),
        'meanProfitMargin': sum(item['profitMargin'] for item in results.values()) / len(results)
    }

    return mean_metrics  

def getCLV_Iterative():
    

    return


def getCLV_Recursive():

    return


def getCLV_SQL():

    return