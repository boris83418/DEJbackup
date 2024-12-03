import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import sys
# 連接資料庫
def connect_to_db():
    # 使用 SQLAlchemy 創建引擎
    connection_string = (
        "mssql+pyodbc:///?odbc_connect="
        "Driver={SQL Server};"
        "Server=jpdejitdev01;"
        "Database=ITQAS2;"
        "Trusted_Connection=yes;"
    )
    engine = create_engine(connection_string)
    return engine

# 提取數據
def fetch_data():
    engine = connect_to_db()

    # 進貨數據
    factory_query = """
    SELECT Part_No, eta_FLTC, Qty, Status
    FROM SoftBank_Data_FactoryShipment
    """
    factory_data = pd.read_sql_query(factory_query, engine)

    # 出貨數據
    order_query = """
    SELECT Product_Name, 
           COALESCE(Actual_shipment_Date, Estimated_Shipment_Date) AS Shipment_Date, 
           Quantity,
           Quotation_status
    FROM SoftBank_Data_Orderinfo
    """
    order_data = pd.read_sql_query(order_query, engine)

    # 初始庫存數據
    product_query = """
    SELECT Delta_PartNO AS Part_No, [Month-End_SAP_Inventory]
    FROM SoftBank_Data_Productinfo
    """
    product_data = pd.read_sql_query(product_query, engine)

    return factory_data, order_data, product_data

# 計算每日庫存
def calculate_inventory(factory_data, order_data, product_data):
    # 清理數據
    factory_data['eta_FLTC'] = pd.to_datetime(factory_data['eta_FLTC']).dt.date
    order_data['Shipment_Date'] = pd.to_datetime(order_data['Shipment_Date']).dt.date

    # 獲取當月的第一天
    start_date = datetime.today().replace(day=1).date()
    end_date = start_date + timedelta(days=180)
    date_range = pd.date_range(start=start_date, end=end_date).date

    # 過濾當月及以後的進貨數據
    factory_data = factory_data[factory_data['eta_FLTC'] >= start_date]

    # 過濾當月及以後的出貨數據，並排除 Quotation_status 為 "quotation" 或 "cancel" 的記錄
    order_data = order_data[
        (order_data['Shipment_Date'] >= start_date) &
        (~order_data['Quotation_status'].isin(['quotation', 'cancel']))
    ]

    # 初始化庫存表，以日期為索引，產品為列
    products = factory_data['Part_No'].unique()
    inventory = pd.DataFrame(index=date_range, columns=products, data=0)

    # 加入初始庫存
    inventory.loc[start_date, :] = product_data.set_index('Part_No')['Month-End_SAP_Inventory']

    # 聚合進貨數據
    factory_agg = factory_data.groupby(['eta_FLTC', 'Part_No'])['Qty'].sum().unstack(fill_value=0)
    factory_agg = factory_agg.reindex(columns=products, index=date_range, fill_value=0).cumsum(axis=0)

    # 聚合出貨數據
    order_agg = order_data.groupby(['Shipment_Date', 'Product_Name'])['Quantity'].sum().unstack(fill_value=0)
    order_agg = order_agg.reindex(columns=products, index=date_range, fill_value=0).cumsum(axis=0)

    # 計算最終庫存
    inventory += factory_agg - order_agg

    return inventory



# 將結果輸出到 Excel
def export_to_excel(inventory):
    # 轉置庫存數據框，使日期在上面，產品在左邊
    inventory_transposed = inventory.T
    
    # 生成檔案名稱，包含日期和時間
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    file_name = f"daily_inventory_simulate_{timestamp}.xlsx"
    
    # 輸出 Excel
    inventory_transposed.to_excel(file_name, index=True)
    
    # 確保控制台支持 Unicode
    sys.stdout.reconfigure(encoding='utf-8')
    
    print(f"每日庫存表已匯出至 {file_name}")

# 主函數
if __name__ == "__main__":
    # 提取數據
    factory_data, order_data, product_data = fetch_data()

    # 計算每日庫存
    inventory = calculate_inventory(factory_data, order_data, product_data)

    # 匯出到 Excel
    export_to_excel(inventory)
