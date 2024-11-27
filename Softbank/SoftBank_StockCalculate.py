import pandas as pd
from datetime import datetime, timedelta
import pyodbc

# 連接資料庫
def connect_to_db():
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=jpdejitdev01;"
        "Database=ITQAS2;"
        "Trusted_Connection=yes;"
    )
    return conn

# 提取數據
def fetch_data():
    connection = connect_to_db()

    # 進貨數據
    factory_query = """
    SELECT Part_No, eta_FLTC, Qty, Status
    FROM SoftBank_Data_FactoryShipment
    """
    factory_data = pd.read_sql_query(factory_query, connection)

    # 出貨數據
    order_query = """
    SELECT Product_Name, 
           COALESCE(Actual_shipment_Date, Estimated_Shipment_Date) AS Shipment_Date, 
           Quantity
    FROM SoftBank_Data_Orderinfo
    """
    order_data = pd.read_sql_query(order_query, connection)

    connection.close()
    return factory_data, order_data

# 計算每日庫存
def calculate_inventory(factory_data, order_data):
    # 清理數據
    factory_data['eta_FLTC'] = pd.to_datetime(factory_data['eta_FLTC']).dt.date  # 只取日期
    order_data['Shipment_Date'] = pd.to_datetime(order_data['Shipment_Date']).dt.date  # 只取日期

    # 生成日期範圍
    start_date = datetime.today().date()
    end_date = start_date + timedelta(days=90)
    date_range = pd.date_range(start=start_date, end=end_date).date  # 只取日期

    # 初始化庫存表，以產品為索引，日期為列
    products = factory_data['Part_No'].unique()
    inventory = pd.DataFrame(index=products, columns=date_range, data=0)

    # 處理進貨數據
    for _, row in factory_data.iterrows():
        inventory.loc[row['Part_No'], row['eta_FLTC']:] += row['Qty']

    # 處理出貨數據
    for _, row in order_data.iterrows():
        inventory.loc[row['Product_Name'], row['Shipment_Date']:] -= row['Quantity']

    # 重設索引，將產品名稱作為一列
    inventory.reset_index(inplace=True)
    inventory.rename(columns={'index': 'Product'}, inplace=True)

    return inventory

# 將結果輸出到 Excel
def export_to_excel(inventory):
    # 生成檔案名稱，包含日期和時間
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    file_name = f"daily_inventory_simulate_{timestamp}.xlsx"
    
    # 輸出 Excel
    inventory.to_excel(file_name, index=False)
    print(f"每日庫存表已匯出至 {file_name}")

# 主函數
if __name__ == "__main__":
    # 提取數據
    factory_data, order_data = fetch_data()

    # 計算每日庫存
    inventory = calculate_inventory(factory_data, order_data)

    # 匯出到 Excel
    export_to_excel(inventory)
