import plotly.express as px
import pandas as pd

# 設定任務數據
data = {
    "Task": ["Plan and discuss", "Redesign excel format", "DB insert and Coding", "UAT", "Go live"],
    "Start": ["2024-11-01", "2024-12-01", "2025-01-01", "2025-02-15", "2025-03-01"],
    "Finish": ["2024-11-30", "2024-12-31", "2025-02-15", "2025-02-28", "2025-03-02"]
}

# 建立 DataFrame
df = pd.DataFrame(data)

# 繪製甘特圖
fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", title="Development of Gantt Chart")
fig.update_yaxes(
    categoryorder="array", 
    categoryarray=["Go live", "UAT", "DB insert and Coding", "Redesign excel format", "Plan and discuss"],
    tickfont=dict(size=18)  # 調整 Y 軸標籤字體大小
)
fig.update_xaxes(
    tickfont=dict(size=18)  # 調整 X 軸標籤字體大小
)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Tasks",
    title_font=dict(size=24)  # 設定圖表標題字體大小
)

fig.show()