from flask import Flask, render_template, request, redirect, url_for, session
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

    total_price = sum(item['UnitPrice'] for item in session['added_data'])  # 計算已添加產品的總價
    return render_template('index.html', query_result=query_result, added_data=session['added_data'], total_price=total_price, error=error)

@app.route('/add', methods=['POST'])
def add():
    product_name = request.form.get('ProductName')
    unit_price = request.form.get('UnitPrice')
    if product_name and unit_price:
        new_data = {'ProductName': product_name, 'UnitPrice': float(unit_price)}  # 新增產品資料
        session['added_data'].append(new_data)  # 將新資料添加到會話中
        session.modified = True  # 標記會話已修改
    return redirect(url_for('index'))  # 重定向到首頁

@app.route('/delete', methods=['POST'])
def delete():
    product_name = request.form.get('ProductName')
    if product_name:
        session['added_data'] = [data for data in session['added_data'] if data['ProductName'] != product_name]  # 刪除指定產品
        session.modified = True  # 標記會話已修改
    return redirect(url_for('index'))  # 重定向到首頁

if __name__ == '__main__':
    app.run(debug=True)

