import requests
from bs4 import BeautifulSoup
from collections import Counter

def get_ptt_comments(url):
    try:
        # 创建一个会话对象
        session = requests.Session()
        
        # 设置请求头，模拟浏览器访问
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 访问年龄验证页面
        age_check_url = "https://www.ptt.cc/ask/over18"
        data = {
            'from': url,
            'yes': 'yes'
        }
        session.post(age_check_url, headers=headers, data=data)
        
        # 发送请求获取目标网页内容
        response = session.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容长度: {len(response.text)}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 检查页面标题
        title = soup.title.string if soup.title else "无标题"
        print(f"页面标题: {title}")

        # 找到所有的留言
        comments = soup.find_all('div', class_='push')
        print(f"找到 {len(comments)} 条留言")

        if len(comments) == 0:
            # 如果没有找到留言，打印页面结构
            print("页面结构:")
            print(soup.prettify()[:1000])  # 打印前1000个字符

        # 提取留言者ID和留言内容
        comments_data = []
        for comment in comments:
            commenter = comment.find('span', class_='f3 hl push-userid')
            content = comment.find('span', class_='f3 push-content')
            if commenter and content:
                commenter_text = commenter.text.strip()
                content_text = content.text.strip().lstrip(':')
                comments_data.append((commenter_text, content_text))
            else:
                print("无法解析某条留言")  # 调试信息

        # 统计每个留言者的留言次数
        commenter_counts = Counter(commenter for commenter, _ in comments_data)

        # 按留言次数排序
        sorted_commenters = sorted(commenter_counts.items(), key=lambda item: item[1], reverse=True)

        # 打印结果
        print("\n留言者统计:")
        for commenter, count in sorted_commenters:
            print(f"{commenter}: {count}次")
            print("留言内容:")
            for c, content in comments_data:
                if c == commenter:
                    print(f"  - {content}")
            print()  # 添加空行以提高可读性

    except requests.RequestException as e:
        print(f"请求错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

# 使用函数
url = "https://www.ptt.cc/bbs/Gossiping/M.1725918311.A.575.html"
get_ptt_comments(url)
