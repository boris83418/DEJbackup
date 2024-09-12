import json
from datetime import datetime
import requests
import os
from dateutil import parser


# 時間格式轉換
def format_datetime(iso_string):
    try:
        dt = parser.isoparse(iso_string)
        return dt.strftime('%Y-%m-%d %I:%M %p')
    except ValueError:
        return iso_string

# 呼叫API
def API_info(departportforinput,arriveportforinput,departDateforinput,returnDateforinput):
        # 根據上面Input去API查詢
    url = "https://sky-scanner3.p.rapidapi.com/flights/search-roundtrip"
        
    querystring = {
        "fromEntityId": departportforinput,
        "toEntityId": arriveportforinput,
        "departDate": departDateforinput,
        "returnDate": returnDateforinput,
        "market": "US",
        "locale": "en-US",
        "currency": "TWD",
        "stops": "direct",
        "adults": "1",
        "infants": "0",
        "cabinClass": "economy"
    }

    headers = {
	"x-rapidapi-key": "130dbd3002mshb0a1497759e83bep1b6bf3jsn46a0cd257b33",
	"x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
    }
    
    # 發起請求
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # 檢查請求狀況   
    except requests.exceptions.RequestException as e:
        print(f"網路請求發生錯誤: {e}")
        return
    
    data=response.json()
    #檢查error
    if not data.get("status",True):
        errors=data.get("errors",{})
        errorsmsg=[f"{key}:{value}" for key, value in errors.items() ]
        print("API 回傳錯誤消息")
        for msg in errorsmsg:
            print(msg)
        return None
    
    # 確保文件夾存在
    if not os.path.exists('RapidAPI_Jsonfile'):
        os.makedirs('RapidAPI_Jsonfile')

    file_path = os.path.join('RapidAPI_Jsonfile', 'flight_data.json')

    # JSON 寫入
    try:
        with open(file_path, 'w') as file:
            json.dump(response.json(), file, indent=4)
    except Exception as e:
        print(f"寫入 JSON 文件失敗: {e}")
        return

    # 讀取 JSON 文件
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data





def main():
    print("請輸入參數查詢航班資訊")
    departportforinput = input("出發地(機場代號 ex:TPE): ")
    arriveportforinput = input("抵達地(機場代號 ex:HND): ")
    departDateforinput = input("出發時間 (YYYY-MM-DD): ")
    returnDateforinput = input("回程時間 (YYYY-MM-DD): ")

    data=API_info(departportforinput,arriveportforinput,departDateforinput,returnDateforinput)

    if data is None:
        print("獲取數據失敗，請檢察輸入參數或網絡連接")
        return
    

    # 另一個 list 用於後續排序
    list_forinfo = []
    
    # 航空公司名字置換
    replace_dict = {
        "Tigerair Taiwan": "虎航",
        "Peach": "樂桃",
        "Juneyao Airlines": "吉祥航空",
        "Scoot":"酷航",
        "JetStar":"捷星"
    }
    


    for i in range(len(data.get('data', {}).get('itineraries', []))):
        dic = {}
        try:
            dic['go_departport'] = data['data']['itineraries'][i]['legs'][0]['origin']['displayCode']
            dic['go_departtime'] = format_datetime(data['data']['itineraries'][i]['legs'][0]['departure'])
            dic['go_arriveport'] = data['data']['itineraries'][i]['legs'][0]['destination']['displayCode']
            dic['go_arrivetime'] = format_datetime(data['data']['itineraries'][i]['legs'][0]['arrival'])
            dic['go_carrier'] = data['data']['itineraries'][i]['legs'][0]['carriers']['marketing'][0]['name']

            dic['back_departport'] = data['data']['itineraries'][i]['legs'][1]['origin']['displayCode']
            dic['back_departtime'] = format_datetime(data['data']['itineraries'][i]['legs'][1]['departure'])
            dic['back_arriveport'] = data['data']['itineraries'][i]['legs'][1]['destination']['displayCode']
            dic['back_arrivetime'] = format_datetime(data['data']['itineraries'][i]['legs'][1]['arrival'])
            dic['back_carrier'] = data['data']['itineraries'][i]['legs'][1]['carriers']['marketing'][0]['name']
            dic['formateprice'] = data['data']['itineraries'][i]['price']['formatted']
            dic['rawprice'] = data['data']['itineraries'][i]['price']['raw']
            list_forinfo.append(dic)
        except (KeyError, IndexError) as e:
            print(f"處理數據時發生錯誤: {e}")

    # 用 raw price 進行排序
    list_sort = sorted(list_forinfo, key=lambda x: x['rawprice'])

    for i in list_sort:
        # 用 dict 來 get value 值找不到的話返回原始值
        go_carrier = replace_dict.get(i['go_carrier'], i['go_carrier'])
        back_carrier = replace_dict.get(i['back_carrier'], i['back_carrier'])
        print('----------------------------------------------------------------')
        print('去程班機:', go_carrier)
        print(i['go_departport'] + "->" + i['go_arriveport'])
        print(i['go_departtime'] + "->" + i['go_arrivetime'])
        print('回程班機:', back_carrier)
        print(i['back_departport'] + "->" + i['back_arriveport'])
        print(i['back_departtime'] + "->" + i['back_arrivetime'])
        print(i['formateprice'])
        print('----------------------------------------------------------------')



if __name__ == "__main__":
    main()
    input("Press Enter to exit...")
