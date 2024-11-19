import pandas as pd
import pyodbc
import logging

# 設定日誌紀錄
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logfile.log", encoding='utf-8'),  # 支援 utf-8 編碼
        logging.StreamHandler()  # 顯示到終端機的輸出
    ]
)

# 資料庫連線函數
def connect_to_database(server, database):
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes"
        )
        logging.info(f"成功連線到資料庫: {server}/{database}")
        return conn
    except Exception as e:
        logging.error(f"資料庫連線失敗: {e}")
        raise

# 創建資料庫表格
def create_table(cursor, table_name, column_mappings, sheet_name):
    try:
        drop_and_create_table_sql = f"""
        IF OBJECT_ID(N'{table_name}', N'U') IS NOT NULL
            DROP TABLE {table_name};

        CREATE TABLE {table_name} (
        """
        for excel_col, (db_col, db_type) in column_mappings[sheet_name].items():
            # 判斷主鍵
            if (sheet_name == 'Customer Code' and excel_col == 'ASP施工店') or \
               (sheet_name == 'FactoryShipment' and excel_col == 'PartNo_ETA_FLTC') or \
               (sheet_name == 'Productinfo' and excel_col == 'Delta_PartNO'):
                drop_and_create_table_sql += f"[{db_col}] {db_type} PRIMARY KEY,\n"
            else:
                drop_and_create_table_sql += f"[{db_col}] {db_type},\n"
        drop_and_create_table_sql = drop_and_create_table_sql.rstrip(',\n') + "\n);"
        
        logging.info(f"執行 SQL: {drop_and_create_table_sql}")
        cursor.execute(drop_and_create_table_sql)
        logging.info(f"{sheet_name} 表格建立完成")
    except Exception as e:
        logging.error(f"創建表格 {table_name} 失敗: {e}")
        raise # 重新引發異常

# 動態生成 INSERT INTO 語句
def generate_insert_sql(table_name, df, column_mappings, sheet_name):
    columns = []
    for col in df.columns:
        if col in column_mappings[sheet_name]:
            db_col = column_mappings[sheet_name][col][0]
            columns.append(f"[{db_col}]")
        else:
            logging.warning(f"Column '{col}' not found in column_mappings. Skipping.")
    placeholders = ", ".join(["?"] * len(columns))
    return f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

# 插入資料
def insert_data(cursor, table_name, df, insert_sql):
    for index, row in df.iterrows():
        try:
            # 將 row 轉換為 tuple 或 list 以匹配 SQL 佔位符
            cursor.execute(insert_sql, tuple(row))
        except pyodbc.IntegrityError as e:
            # 捕獲 IntegrityError，並記錄警告
            logging.warning(f"跳過重複主鍵值: {row[0]}")
            continue  # 跳過此筆資料，繼續處理下一筆
        except Exception as e:
            # 捕獲其他非預期的錯誤
            logging.error(f"插入資料時出錯: {e}")
            continue


# 主處理函數
def process_excel_to_sql(excel_file_path, table_mapping, column_mappings):
    try:
        conn = connect_to_database('jpdejitdev01', 'ITQAS2')
        cursor = conn.cursor()

        for sheet_name, table_name in table_mapping.items():
            logging.info(f"處理工作表: {sheet_name}")

            # 讀取資料並處理資料型別
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
            df.columns = df.columns.str.strip()

            # 優化資料型別：檢查並轉換資料型別
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = pd.to_datetime(df[col], errors='coerce') if 'Date' in col else df[col]
                    df[col] = df[col].astype(str) if df[col].dtype == 'datetime64[ns]' else df[col]

            # 特殊處理 FactoryShipment 表格
            if sheet_name == 'FactoryShipment':
                df['PartNo_ETA_FLTC'] = df['Part_No'].astype(str) + df['ETA_FLTC'].astype(str)
                df = df.groupby('PartNo_ETA_FLTC', as_index=False).agg({
                    'PO_Date': 'first',
                    'Item': 'first',
                    'Qty': 'sum',
                    'PO_NO': 'first',
                    'Part_No': 'first',
                    'Actual_Ex_fac_date': 'first',
                    'ETD_SH': 'first',
                    'ETA_FLTC': 'first',
                    'Original_ETA': 'first',
                    'ship_method': 'first',
                    'ETA_Year': 'first',
                    'Status': 'first'
                })

            # 建表與插入資料
            create_table(cursor, table_name, column_mappings, sheet_name)
            insert_sql = generate_insert_sql(table_name, df, column_mappings, sheet_name)
            insert_data(cursor, table_name, df, insert_sql)

        conn.commit()
        logging.info("所有資料已成功寫入資料庫")
    except Exception as e:
        logging.error(f"處理過程中出現錯誤: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

# 主程式
if __name__ == "__main__":
    # Excel 檔案路徑
    excel_file_path = r'D:\\DeltaBox\\OneDrive - Delta Electronics, Inc\\deltaproject\\DEJbackup\\SoftbankExcel\\表單\\SoftBankData_DBusing.xlsx'

    # 表格對應
    table_mapping = {
        'Customer Code': 'dbo.SoftBank_Data_CustomerCode',
        'FactoryShipment': 'dbo.SoftBank_Data_FactoryShipment',
        'Orderinfo': 'dbo.SoftBank_Data_Orderinfo',
        'Productinfo': 'dbo.SoftBank_Data_Productinfo'
    }

    # 欄位映射
    column_mappings = {
        'Customer Code': {
            'ASP施工店': ('ASP', 'NVARCHAR(255)'), 
            'Customer code': ('Customer_code', 'NVARCHAR(255)')
        },
        'FactoryShipment': {
            'PartNo_ETA_FLTC': ('PartNo_ETA_FLTC', 'NVARCHAR(255)'),
            'PO_Date': ('PO_Date', 'DATE'),
            'Item': ('Item', 'NVARCHAR(255)'),
            'PO_NO': ('PO_NO', 'NVARCHAR(255)'),
            'Part_No': ('Part_No', 'NVARCHAR(255)'),
            'Qty': ('Qty', 'INT'),
            'Actual_Ex_fac_date': ('Actual_Ex_fac_date', 'DATE'),
            'ETD_SH': ('ETD_SH', 'DATE'),
            'ETA_FLTC': ('ETA_FLTC', 'DATE'),
            'Original_ETA': ('Original_ETA', 'DATE'),
            'ship_method': ('ship_method', 'NVARCHAR(255)'),
            'ETA_Year': ('ETA_Year', 'INT'),
            'Status': ('Status', 'NVARCHAR(255)')
        },
        'Orderinfo': {
            'DEJ見積り番号': ('DEJ_Estimate_Number', 'NVARCHAR(255)'),
            '注文日': ('Order_Date', 'DATE'),
            '實際出荷日': ('Actual_Shipment_Date', 'DATE'),
            '預計出荷日': ('Estimated_Shipment_Date', 'DATE'),
            '納品日': ('Delivery_Date', 'DATE'),
            '希望納期': ('Desired_Delivery_Date', 'DATE'),
            '標準納期': ('Standard_Delivery_Time', 'INT'),
            '工事名/局名': ('Station_Name', 'NVARCHAR(255)'),
            '品名・規格': ('Product_Name', 'NVARCHAR(255)'),
            '台数': ('Quantity', 'INT'),
            '発注先': ('OrdererLocation', 'NVARCHAR(255)'),
            '担当者': ('Person_in_Charge', 'NVARCHAR(255)'),
            '送り先': ('Recipient', 'NVARCHAR(255)'),
            '部署名': ('Contact_Department_Name', 'NVARCHAR(255)'),
            '連絡人': ('Contact_Person', 'NVARCHAR(255)'),
            '住所': ('Contact_Address', 'NVARCHAR(255)'),
            '電話': ('ContactPhone', 'NVARCHAR(255)'),
            '註': ('ContactNotes', 'NVARCHAR(255)'),
            'SO＃': ('SO_NO', 'NVARCHAR(255)'),
            'DN＃': ('DN_NO', 'NVARCHAR(255)'),
            '送り状番号': ('Invoice_Number', 'NVARCHAR(255)')
        },
        'Productinfo': {
            'Delta_PartNO': ('Delta_PartNO', 'NVARCHAR(255)'),
            'Category': ('Category', 'NVARCHAR(255)'),
            'Customer_Model_Name': ('Customer_Model_Name', 'NVARCHAR(255)'),
            'Model': ('Model', 'NVARCHAR(255)'),
            '税抜単価': ('UnitPrice', 'INT'),
            '標準納期': ('Standard_Delivery_Time', 'INT')
        }
    }

    process_excel_to_sql(excel_file_path, table_mapping, column_mappings)
