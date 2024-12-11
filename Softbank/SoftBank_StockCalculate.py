import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import sys
import os

# 連接資料庫
def connect_to_db():
    # 使用 SQLAlchemy 創建引擎
    try:
        connection_string = (
            "mssql+pyodbc:///?odbc_connect="
            "Driver={SQL Server};"
            "Server=jpdejitdev01;"
            "Database=ITQAS2;"
            "Trusted_Connection=yes;"
        )
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        print(f"❌ 資料庫連接失敗: {e}")
        sys.exit(1)  # 如果無法連接，則結束程式

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


def calculate_inventory(factory_data, order_data, product_data):
    # 清理數據
    factory_data['eta_FLTC'] = pd.to_datetime(factory_data['eta_FLTC']).dt.date
    order_data['Shipment_Date'] = pd.to_datetime(order_data['Shipment_Date']).dt.date
    
    # 獲取當月的第一天
    start_date = datetime.today().replace(day=1).date()
    end_date = start_date + timedelta(days=180)
    date_range = pd.date_range(start=start_date, end=end_date).date

    # 過濾當月及以後的出貨數據，並排除 Quotation_status 為 "quotation" 或 "cancel" 的記錄
    order_data = order_data[
        (order_data['Shipment_Date'] >= start_date) & 
        (~order_data['Quotation_status'].isin(['quotation', 'cancel']))
    ]

    # 使用 product_data['Delta_PartNO'] 來生成產品列表，這樣可以包括所有產品
    products = product_data['Part_No'].unique()

    # 初始化庫存表，以日期為索引，產品為列
    inventory = pd.DataFrame(index=date_range, columns=products, data=0)
    
    # 只考慮 product_data 中存在於 order_data 中的產品，並加入初始庫存
    initial_inventory = product_data[product_data['Part_No'].isin(products)]
    inventory.loc[start_date] = initial_inventory.set_index('Part_No')['Month-End_SAP_Inventory']

    # 進貨數據處理：只考慮與 order_data 產品名匹配的進貨數據
    valid_factory_data = factory_data[factory_data['Part_No'].isin(products)]
    if not valid_factory_data.empty:
        factory_agg = valid_factory_data.groupby(['eta_FLTC', 'Part_No'])['Qty'].sum().unstack(fill_value=0)
        factory_agg = factory_agg.reindex(columns=products, index=date_range, fill_value=0)
    else:
        factory_agg = pd.DataFrame(0, index=date_range, columns=products)
    
    # 出貨數據處理：使用 order_data 的 Product_Name 作為列名
    if not order_data.empty:
        order_agg = order_data.groupby(['Shipment_Date', 'Product_Name'])['Quantity'].sum().unstack(fill_value=0)
        order_agg = order_agg.reindex(columns=products, index=date_range, fill_value=0)
    else:
        order_agg = pd.DataFrame(0, index=date_range, columns=products)

    # **手動更新第一天的庫存** (期初庫存 + 當天進貨 - 當天出貨)
    inventory.loc[start_date] = initial_inventory.set_index('Part_No')['Month-End_SAP_Inventory'] + \
                                factory_agg.loc[start_date] - order_agg.loc[start_date]

    # **從第二天開始的逐天計算**
    for i in range(1, len(date_range)):
        prev_date = date_range[i - 1]
        curr_date = date_range[i]
        inventory.loc[curr_date] = inventory.loc[prev_date] + factory_agg.loc[curr_date] - order_agg.loc[curr_date]

    return inventory






# 將結果輸出到 Excel
import os  # 新增 os 模組以處理路徑

def export_to_excel(inventory):
    """ 
    將計算後的庫存導出到 Excel，並在導出前合併等同的 Part_No
    """
    # **等同的 Part_No 替換對應表**
    part_no_mapping = {
        '3798D000000278-S(free)': '3798D000000278-S',
        '3798D000000225-S(free)': '3798D000000225-S',
        '3798D000000228-S(free)': '3798D000000228-S',
    }

    # **合併等同的 Part_No**
    for free_part_no, main_part_no in part_no_mapping.items():
        if free_part_no in inventory.columns and main_part_no in inventory.columns:
            # 將 'free' Part_No 的庫存加到主 Part_No 上
            inventory[main_part_no] += inventory[free_part_no]
            inventory.drop(columns=[free_part_no], inplace=True)
        elif free_part_no in inventory.columns:
            # 如果只有 'free' Part_No，將其重命名為主 Part_No
            inventory.rename(columns={free_part_no: main_part_no}, inplace=True)

    # **轉置庫存數據框，使日期在上面，產品在左邊**
    inventory_transposed = inventory.T
    
    # **生成檔案名稱，包含日期和時間**
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    file_name = f"Daily_Inventory_Simulate_{timestamp}.xlsx"
    
    # **指定存儲的網路目錄**
    save_path = r"\\jpdejstcfs01\\STC_share\\JP IT\\STC SBK 仕分けリスト\\IT system\\Report"
    full_path = os.path.join(save_path, file_name)
    
    # **輸出 Excel**
    inventory_transposed.to_excel(full_path, index=True)
    
    # **確保控制台支持 Unicode**
    sys.stdout.reconfigure(encoding='utf-8')
    
    print(f"每日庫存表已匯出至 {full_path}")

    
# 主函數
if __name__ == "__main__":
    # 提取數據
    factory_data, order_data, product_data = fetch_data()

    # 計算每日庫存
    inventory = calculate_inventory(factory_data, order_data, product_data)

    # 匯出到 Excel
    export_to_excel(inventory)
