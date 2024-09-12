import uuid  # 添加这一行
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pyodbc   

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'added_data' not in session:
        session['added_data'] = []  # 初始化会话中的 'added_data' 为空列表

    query_result = []
    error = None

    if request.method == 'POST':
        product_id = request.form.get('ProductID')  # 获取表单中的 'ProductID' 字段
        if product_id:
            query = "SELECT ProductName, UnitPrice FROM dbo.Quotation WHERE ProductID = ?"
            try:
                conn = pyodbc.connect('DRIVER={SQL Server};SERVER=jpdejitdev01;DATABASE=ITQAS2; Trusted_Connection=yes;')
                cursor = conn.cursor()
                cursor.execute(query, product_id)
                results = cursor.fetchall()
                conn.close()
                
                # 打印查詢結果以調試
                print(f"Query Results: {results}")
                
                if results:
                    query_result = [{'ProductName': row.ProductName, 'UnitPrice': row.UnitPrice} for row in results]
                else:
                    error = "No results found."  # 查詢無結果
            except Exception as e:
                error = f"Error: {str(e)}. Query: {query}"  # 查詢出錯
        else:
            error = "No ProductID provided."  # 未提供 ProductID

    total_price = sum(item['UnitTotalPrice'] for item in session['added_data'])  # 計算已添加產品的總價
    return render_template('index.html', query_result=query_result, added_data=session['added_data'], total_price=total_price, error=error)

@app.route('/add', methods=['POST'])
def add():
    product_name = request.form.get('ProductName')
    unit_price = request.form.get('UnitPrice')
    if product_name and unit_price:
        unit_price = float(unit_price)
        unit_quantity = 1  # 如果数量为空，默认为1
        unit_total_price = unit_price * unit_quantity
        new_data = {
            'id': str(uuid.uuid4()),  # 为每个产品实例生成唯一ID
            'ProductName': product_name,
            'UnitPrice': unit_price,
            'UnitQuantity': unit_quantity,
            'UnitTotalPrice': unit_total_price
        }
        session['added_data'].append(new_data)  # 将新数据添加到会话中
        session.modified = True  # 标记会话已修改
    return redirect(url_for('index'))  # 重定向到首页

@app.route('/delete', methods=['POST'])
def delete():
    product_id = request.form.get('ProductID')
    if product_id:
        session['added_data'] = [data for data in session['added_data'] if data['id'] != product_id]  # 刪除指定產品
        session.modified = True  # 標記會話已修改
    return redirect(url_for('index'))  # 重定向到首頁

@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    data = request.get_json()
    product_id = data.get('productId')
    unit_quantity = data.get('unitQuantity')
    unit_total_price = data.get('unitTotalPrice')

    for item in session['added_data']:
        if item['id'] == product_id:
            item['UnitQuantity'] = unit_quantity
            item['UnitTotalPrice'] = unit_total_price
            break

    session.modified = True
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)

