import pymssql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# 連結數據庫
server = 'jpdejitdev01'
database = 'ITQAS'

# 使用 Windows Authentication
conn = pymssql.connect(server=server, database=database)

# 讀表放入DataFrame
#SUM複習
# query = """SELECT sum(QtybyAccount) as totalQty
# FROM IT_ComputerList
# WHERE created > '2024-06-18 00:00:00';"""
# df = pd.read_sql(query, conn)

query = """SELECT *
FROM CCC_Revenue;"""
df = pd.read_sql(query, conn)

# 顯示前幾行數據
print(df.head())

#幾筆符合
print(f"幾筆符合:{df.shape[0]}")
#幾個欄位
print(f"幾個欄位:{df.shape[1]}")

#關閉連結
conn.close()

#繪圖
# 配置图形样式
# sns.set(style="whitegrid")
# # 确保列名匹配
# # 将 'yearMonth' 列转换为字符串格式以确保排序正确
# df['yearMonth'] = df['yearMonth'].astype(str)

# # 绘制图表
# plt.figure(figsize=(12, 6))

# # 根据 Profit Center 进行分组，绘制 Amount 和 lastYearAvg 的折线图
# sns.lineplot(data=df, x='yearMonth', y='Amount', hue='Profit Center', marker='o')
# sns.lineplot(data=df, x='yearMonth', y='lastYearAvg', hue='Profit Center', marker='o', linestyle='--')

# # 添加标题和标签
# plt.title('Amount vs Last Year Avg by YearMonth')
# plt.xlabel('Year-Month')
# plt.ylabel('Value')
# plt.legend(title='Legend')
# plt.grid(True)

# # 显示图表
plt.show()
