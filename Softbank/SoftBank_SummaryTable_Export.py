import pandas as pd
import logging
import pyodbc

# 設定日誌紀錄
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logfile.log", encoding='utf-8'),
        logging.StreamHandler()
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

def export_summarytable_to_excel(conn, table_name, output_file):
    try:
        # 用 SQL 查詢資料
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)
        
        # 確保日期列格式正確
        date_columns = ['order_date', 'actual_shipment_date', 'estimated_shipment_date', 
                        'delivery_date', 'Desired_delivery_Date', 'standard_delivery_time']
        
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')  # 確保是 datetime 格式

        # 匯出到 Excel
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name=table_name, index=False)
            workbook = writer.book
            worksheet = writer.sheets[table_name]
            
            # 設定格式：粗框與粗體
            bold_format = workbook.add_format({'bold': True, 'border': 2})  # 粗體 + 粗框
            border_format = workbook.add_format({'border': 2})  # 只有粗框
            date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'border': 2})  # 日期格式
            
            # 套用格式到表頭
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, bold_format)
            
            # 套用格式到資料列
            for row_num in range(1, len(df) + 1):  # 從第 1 列開始（跳過表頭）
                for col_num in range(len(df.columns)):
                    cell_value = df.iloc[row_num - 1, col_num]
                    # 檢查是否是日期欄位，如果是則使用日期格式
                    if isinstance(cell_value, pd.Timestamp):  # 檢查是否為日期類型
                        worksheet.write(row_num, col_num, cell_value, date_format)
                    else:
                        worksheet.write(row_num, col_num, cell_value, border_format)

        logging.info(f"表格 {table_name} 匯出成功至 {output_file}")
    except Exception as e:
        logging.error(f"匯出表格 {table_name} 時發生錯誤: {e}")
        raise

# 用法範例
if __name__ == "__main__":
    try:
        # 連接到資料庫
        conn = connect_to_database('jpdejitdev01', 'ITQAS2')

        # 匯出表格到 Excel
        output_excel_path = r"D:\\DeltaBox\\OneDrive - Delta Electronics, Inc\\deltaproject\\DEJbackup\\SoftbankExcel\\表單\\SoftBankSummaryTable.xlsx"
        table_name = "dbo.SoftBankSummaryView"  # 要匯出的View
        export_summarytable_to_excel(conn, table_name, output_excel_path)

    except Exception as e:
        logging.error(f"整體程式執行失敗: {e}")
    finally:
        if conn:
            conn.close()