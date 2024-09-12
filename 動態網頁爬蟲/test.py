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

# 等待页面加载
driver.implicitly_wait(10)

# 找到特定的 div 元素
terms_of_use = driver.find_element(By.ID, "terms_of_use")

# 滚动该元素到最下
driver.execute_script("arguments[0].scrollIntoView(true);", terms_of_use)

# 点击勾选同意
checkbox = driver.find_element(By.ID, "CbOk")
checkbox.click()

# 点击利用开始
button = driver.find_element(By.ID, "BTN_LOGIN")
button.click()

# 进入后等待页面加载
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "DdlFacilityKind")))

# 找到下拉元素(施設区分)
dropdown = Select(driver.find_element(By.ID, "DdlFacilityKind"))

# 选择道路桥
dropdown.select_by_value("BR0")

# 将高速道路公司取消勾选
checkbox_road_mngr1 = driver.find_element(By.ID, "CbRoadMngr1")
if checkbox_road_mngr1.is_selected():
    checkbox_road_mngr1.click()

# 将国土交通省取消勾选
checkbox_road_mngr2 = driver.find_element(By.ID, "CbRoadMngr2")
if checkbox_road_mngr2.is_selected():
    checkbox_road_mngr2.click()

# 点击一览画面
button_list = driver.find_element(By.ID, "Btn_List")
button_list.click()

# 等待页面加载
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "contentArea")))


# 提取 __VIEWSTATE 和 __VIEWSTATEGENERATOR 的值
viewstate = driver.find_element(By.ID, '__VIEWSTATE').get_attribute('value')
viewstate_generator = driver.find_element(By.ID, '__VIEWSTATEGENERATOR').get_attribute('value')
# 使用 Selenium 执行 JavaScript 发出 AJAX 请求并获取数据
ajax_script = f"""
    var APP_ROOT = '/';
    return $.ajax({{
        type: "POST",
        async: false,
        url: APP_ROOT + "Ajax/GetFacilityDetailData.aspx",
        dataType: "json",
        data: {{
            "ID": "23.80693,125.22155",
            "KIND": "BR0"
        }},
        traditional: true
    }}).responseJSON;
"""
data = driver.execute_script(ajax_script)
print(data)

# if data and "datalist" in data:
#     df = pd.DataFrame(data["datalist"])
#     print("前 100 条记录:")
#     print(df.head(100))  # 打印前 100 条记录
# else:
#     print("ERROR")


# # 处理数据并保存到 Excel
# if data and "datalist" in data:
#     df = pd.DataFrame(data["datalist"])
#     df.to_excel('output.xlsx', index=False)
#     print("数据已保存到 output.xlsx")
# else:
#     print("未能获取数据")


# 关闭浏览器
driver.quit()
