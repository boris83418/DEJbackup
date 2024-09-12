import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# 设置 WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 打开目标网站
driver.get('https://road-structures-map.mlit.go.jp/FacilityList.aspx')

# 等待页面加载完成
driver.implicitly_wait(10)

# 找到特定的 div 元素
terms_of_use = driver.find_element(By.ID, "terms_of_use")

# 滚动到该元素
driver.execute_script("arguments[0].scrollIntoView(true);", terms_of_use)

# 可以在滚动后进行其他操作，如点击或勾选
checkbox = driver.find_element(By.ID, "CbOk")
checkbox.click()

# 如果需要，可以点击 "利用開始" 按钮
button = driver.find_element(By.ID, "BTN_LOGIN")
button.click()

# 等待页面加载完成
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "DdlFacilityKind")))

# 找到下拉菜单元素
dropdown = Select(driver.find_element(By.ID, "DdlFacilityKind"))

# 选择「道路橋」
dropdown.select_by_value("BR0")  # 根据 value 属性选择

# 定位「高速道路公司」复选框并取消选择
checkbox_road_mngr1 = driver.find_element(By.ID, "CbRoadMngr1")
if checkbox_road_mngr1.is_selected():
    checkbox_road_mngr1.click()

# 定位「国土交通省」复选框并取消选择
checkbox_road_mngr2 = driver.find_element(By.ID, "CbRoadMngr2")
if checkbox_road_mngr2.is_selected():
    checkbox_road_mngr2.click()

# 定位「一覧画面」按钮并点击
button_list = driver.find_element(By.ID, "Btn_List")
button_list.click()

# 等待页面加载完成
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "contentArea")))

# 函数：抓取表格数据
def scrape_table():
    rows = driver.find_elements(By.CSS_SELECTOR, "#contentArea tr.clusterize-no-data")
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        data.append([col.text for col in cols])
    return data

# 存储所有抓取的数据
all_data = []

# 设置滚动区域
scroll_container = driver.find_element(By.ID, "listpanel_content")

# 设置初始滚动高度
last_height = driver.execute_script("return arguments[0].scrollHeight;", scroll_container)

while True:
    # 抓取当前页面的数据
    all_data.extend(scrape_table())

    # 慢慢滚动到底部
    while True:
        driver.execute_script("arguments[0].scrollTop += arguments[0].clientHeight;", scroll_container)
        time.sleep(1)  # 每次滚动后等待1秒以确保数据加载
        new_height = driver.execute_script("return arguments[0].scrollHeight;", scroll_container)
        if new_height == last_height:
            break
        last_height = new_height

    # 确保所有数据都被抓取
    time.sleep(2)  # 等待额外的时间以确保页面完全加载

    # 检查是否有新的数据可抓取
    if len(driver.find_elements(By.CSS_SELECTOR, "#contentArea tr.clusterize-no-data")) == 0:
        break

# 将数据写入 Excel 文件
df = pd.DataFrame(all_data)
df.to_excel('output.xlsx', index=False, header=False)

print("数据已保存到 output.xlsx")

# 关闭浏览器
driver.quit()
