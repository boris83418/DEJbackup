import pandas as pd
import pyodbc

# 資料庫連線設定
server = 'jpdejitdev01'
database = 'ITQAS2'         
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes"
)
cursor = conn.cursor()

# 定義檔案路徑與對應的資料庫表格名稱
excel_file_path = r'D:\\DeltaBox\\OneDrive - Delta Electronics, Inc\\deltaproject\\DEJbackup\\SoftbankExcel\\表單\\SoftBankData_DBusing.xlsx'
table_mapping = {
    'Customer Code': 'dbo.SoftBank_Data_CustomerCode',
    'FactoryShipment': 'dbo.SoftBank_Data_FactoryShipment',
    'Orderinfo': 'dbo.SoftBank_Data_Orderinfo',
    'Productinfo':'dbo.SoftBank_Data_Productinfo'
}

# 定義欄位映射，增加資料型別  # (欄位名稱, 資料型別)
column_mappings = {
    'Customer Code': {
        'ASP施工店': ('ASP', 'NVARCHAR(255)'), 
        'Customer code': ('Customer_code', 'NVARCHAR(255)')
    },
    'FactoryShipment': {
        'PartNo_ETA_FLTC': ('PartNo_ETA_FLTC', 'NVARCHAR(255)'),  # 創建key
        'PO_Date': ('PO_Date', 'DATE'),  # 日期欄位
        'Item': ('Item', 'NVARCHAR(255)'),
        'PO_NO': ('PO_NO', 'NVARCHAR(255)'),
        'Part_No': ('Part_No', 'NVARCHAR(255)'),
        'Qty': ('Qty', 'INT'),
        'Actual_Ex_fac_date': ('Actual_Ex_fac_date', 'DATE'),  # 日期欄位
        'ETD_SH': ('ETD_SH', 'DATE'),  # 日期欄位
        'ETA_FLTC': ('ETA_FLTC', 'DATE'),
        'Original_ETA': ('Original_ETA', 'DATE'),  # 日期欄位
        'ship_method': ('ship_method', 'NVARCHAR(255)'),
        'ETA_Year': ('ETA_Year', 'INT'),
        'Status': ('Status', 'NVARCHAR(255)')
    },
    'Orderinfo': {
        'DEJ見積り番号': ('DEJ_Estimate_Number', 'NVARCHAR(255)'),
        '注文日': ('Order_Date', 'DATE'),  # 日期欄位
        '實際出荷日': ('Actual_Shipment_Date', 'DATE'),  # 日期欄位
        '預計出荷日': ('Estimated_Shipment_Date', 'DATE'),  # 日期欄位
        '納品日': ('Delivery_Date', 'DATE'),  # 日期欄位
        '希望納期': ('Desired_Delivery_Date', 'DATE'),  # 日期欄位
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
    }
    ,
    'Productinfo': {
        'Delta_PartNO': ('Delta_PartNO', 'NVARCHAR(255)'),
        'Category': ('Category', 'NVARCHAR(255)'),
        'Customer_Model_Name': ('Customer_Model_Name', 'NVARCHAR(255)'),
        'Model': ('Model', 'NVARCHAR(255)'),
        '税抜単価': ('UnitPrice', 'INT'),
        '標準納期': ('Standard_Delivery_Time', 'INT')
    }
}


# 處理每個工作表
for sheet_name, table_name in table_mapping.items():
    # 讀取工作表資料
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    
    # 去除欄位名稱的空白
    df.columns = df.columns.str.strip()
    # print(df.columns)
    
    if sheet_name == 'FactoryShipment':
        df['PartNo_ETA_FLTC'] = df['Part_No'].astype(str) + df['ETA_FLTC'].astype(str)
        # 處理重複的 PartNo_ETA_FLTC，將 Qty 進行合併
        df = df.groupby('PartNo_ETA_FLTC', as_index=False).agg({
            'PO_Date': 'first',  # 假設選擇第一筆資料的日期
            'Item': 'first',  # 假設選擇第一筆資料的 Item
            'PO_NO': 'first',  # 假設選擇第一筆資料的 PO_NO
            'Part_No': 'first',
            'Qty': 'sum',  # 合併相同 PartNo_ETA_FLTC 的 Qty
            'Actual_Ex_fac_date': 'first',  # 假設選擇第一筆資料的 Actual_Ex_fac_date
            'ETD_SH': 'first',  # 假設選擇第一筆資料的 ETD_SH
            'ETA_FLTC': 'first',  # 假設選擇第一筆資料的 ETA_FLTC
            'Original_ETA': 'first',  # 假設選擇第一筆資料的 Original_ETA
            'ship_method': 'first',  # 假設選擇第一筆資料的 ship_method
            'ETA_Year': 'first',  # 假設選擇第一筆資料的 ETA_Year
            'Status': 'first'  # 假設選擇第一筆資料的 Status
        })
    

    # 若資料庫表格存在則刪除並重新創建
    drop_and_create_table_sql = f"""
    IF OBJECT_ID(N'{table_name}', N'U') IS NOT NULL
        DROP TABLE {table_name};

    CREATE TABLE {table_name} (
    """
    

    # 根據 column_mappings 來動態生成欄位和資料型別
    if sheet_name in column_mappings:
        for excel_col, (db_col, db_type) in column_mappings[sheet_name].items():
            # 特別處理 'Customer Code' 和 'FactoryShipment' 表格中的主鍵欄位
            if sheet_name == 'Customer Code' and excel_col == 'ASP施工店':
                drop_and_create_table_sql += f"[{db_col}] {db_type} PRIMARY KEY,\n"
            elif sheet_name == 'FactoryShipment' and excel_col == 'PartNo_ETA_FLTC':
                drop_and_create_table_sql += f"[{db_col}] {db_type} PRIMARY KEY,\n"
            elif sheet_name == 'Productinfo' and excel_col == 'Delta_PartNO':
                drop_and_create_table_sql += f"[{db_col}] {db_type} PRIMARY KEY,\n" 
            else:
                drop_and_create_table_sql += f"[{db_col}] {db_type},\n"  # 使用對應資料型別


        # 移除最後一個多餘的逗號
        drop_and_create_table_sql = drop_and_create_table_sql.rstrip(',\n')

    # 完成 SQL 語句
    drop_and_create_table_sql += "\n);"
    
    # 執行創建表格的 SQL 語句
    print(f"Executing SQL: {drop_and_create_table_sql}")
    cursor.execute(drop_and_create_table_sql)
    conn.commit()

    print(f"{sheet_name} 表的Title建立")
    

    # 構建 INSERT INTO 
    columns = []
    for col in df.columns:
        if col in column_mappings[sheet_name]:
            db_col = column_mappings[sheet_name][col][0]  # 取得對應的資料庫欄位名稱
            columns.append(f"[{db_col}]")
        else:
            print(f"Column '{col}' not found in column_mappings. Skipping.")
    placeholders = ", ".join(["?"] * len(columns))
    insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    # 逐列插入資料
    for row in df.itertuples(index=False, name=None):
        try:
            cursor.execute(insert_sql, row)
        except pyodbc.IntegrityError:
            print(f"跳過重複主鍵值: {row[0]}")  # 如果遇到重複主鍵，則跳過

    print(f"{sheet_name} 資料已成功寫入 {table_name}")

# 提交變更並關閉連線
conn.commit()
cursor.close()
conn.close()

print("所有資料已成功寫入資料庫")

