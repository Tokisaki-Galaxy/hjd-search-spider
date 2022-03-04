# coding utf-8
from dataclasses import replace
import os
import sqlite3
import time
from bs4 import BeautifulSoup
import requests
import random
import re
import tqdm

# hjd网友自拍抓取（搜索）
# 页面url地址
url = 'https://lsp.qb1234.com/2048/thread.php?fid-23-page-'
picurl = 'https://lsp.qb1234.com/2048/'
max = 2122

file_name = 'data-'
sqlite_name = 'data.db'
page_text = []

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0',
]
proxy = {
    'https': '127.0.0.1:50033'
}


def catch_a_page(i_url, page):
    agent = random.choice(user_agents)

    # 发送请求，r为页面响应
    headers = {
        'user-agent': agent
    }
    r = requests.get(i_url, headers=headers, proxies=proxy)
    r.encoding = 'utf-8'

    if r.status_code != 200:
        return
    r.close()

    # r.text获取页面代码
    # 使用lxml解析页面代码
    soup = BeautifulSoup(r.text, 'html.parser')

    # 两次定位，先找到整个信息区域
    info_list = soup.find_all('tbody', style="table-layout:fixed;")

    # 在此区域内获取游戏名，find_all返回的是list
    tit_list = info_list[0].find_all(attrs={'class': 'tal'})

    # 遍历获取游戏名
    # .text可获取文本内容，替换掉文章中的换行符
#    page_text = []
    for link in soup.find_all('a'):  # 遍历网页中所有的超链接（a标签）
        link = str(link)
        link = re.findall(r'<a class="subject"(.{1,})', link)
        if link == []:
            continue
        for a in link:
            a = '<a'+a
#            a.replace('href="state/p','href="'+picurl+'state/p')
            page_text.append(a)
#    return page_text


"""
def deal_data(idata):
    result={}
    for item in idata:
        result={
            "title":item.get_text(),
            "link":item.get('href'),
            'ID':re.findall('\d+',item.get('href'))
        }
    print(result)
    return result
"""

if __name__ == '__main__':
    start = time.perf_counter()
    try:
        for page in range(728, max+1):
            page_data = catch_a_page(url+str(page)+'.html', page)
            print('已完成第', page, '页抓取')
            time.sleep(0.7)
    finally:
        with open(file_name+str(page)+'.html', mode='w', encoding='utf-8') as file_obj:
            for x in page_text[6::]:
                file_obj.write(x)
                file_obj.write('\n<br>\n')
                end = time.perf_counter()
        print('Running time: %s Seconds' % (end-start))

"""
    if os.path.isfile(sqlite_name):
        print("已有一个数据库，你想删除现在已有的数据库吗？\n如果不删除，将停止运行")

    # 加载并初始化
    conn = sqlite3.connect(sqlite_name)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS hjd(
        id           INTEGER     PRIMARY KEY,
        title        TEXT        NOT NULL,
        url          TEXT        NOT NULL,
        page_num     INTEGER,
        update_time  default (datetime('now', 'localtime')));
        ''')

    # 处理数据
    for page in range(1, max+1):
        page_data = catch_a_page(url+str(page)+'.html', page)
        cur.execute(
            'INSERT INTO hjd VALUES (NULL, ?,?, ?,CURRENT_TIMESTAMP);', page_data, page)

    conn.commit()
    conn.close()
"""
