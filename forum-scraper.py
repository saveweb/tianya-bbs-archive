"""
从天涯论坛版面的帖子列表中抓取帖子的标题、链接、作者、作者uid
"""

import requests
import datetime
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def create_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0'
    })
    return session

def get_page(url, session=None):
    response = session.get(url)
    if response.status_code == 200:
        return response.text

def parse_page(html):
    soup = BeautifulSoup(html, 'lxml')
    titles = []
    authors = []

    for title in soup.select('.tab-bbs-list'):
        for a in title.select('.td-title a'):
            titles.append( {
                'title': a.get_text().strip(),
                'link': a.get('href'),
            } )
    for author in soup.select('.tab-bbs-list'):
        for a in author.select('.author'):
            authors.append( {
                'author': a.get_text().strip(),
                'uid': a.get('href').strip('/').split('/')[-1],
            } )
    if len(titles) != len(authors):
        raise ValueError("len(titles) != len(authors)")
    for i in range(len(titles)):
        yield {
            'title': titles[i]['title'],
            'link': titles[i]['link'],
            'author': authors[i]['author'],
            'uid': authors[i]['uid'],
        }

def mk_dir(dir='data'):
    if not os.path.exists(dir):
        os.mkdir(dir)

def main():
    try:
        session = create_session()
        forum_id = input('版id：')
        base_url = 'http://bbs.tianya.cn/'
        url = base_url + 'list.jsp?item=' + forum_id + '&order=1'
        mk_dir('data')
        file = open(f'data/{forum_id}-{datetime.datetime.now().strftime("%Y%m%d")}.txt', 'w', encoding='utf-8')
        while url:
            html = get_page(url, session)
            for item in parse_page(html):
                file.write(str(item) + '\n')
            soup = BeautifulSoup(html, 'lxml')
            nextPage = soup.select('.short-pages-2 a')[-1].get('href')
            if "list.jsp" not in nextPage:
                file.write("--End--")
                print("--End--")
                break
            print(nextPage)
            url = urljoin(base_url, nextPage)
    except Exception as e:
        print(e)
    finally:
        if 'file' in locals():
            file.close()

if __name__ == '__main__':
    main()
