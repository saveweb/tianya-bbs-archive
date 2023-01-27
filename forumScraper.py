"""
从天涯论坛版面的帖子列表中抓取帖子的标题、链接、作者、作者uid
"""

import requests
import datetime
import os
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def create_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0'
    })
    return session

def get_page(url, session):
    response = session.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

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
            uid: str|None = a.get('href')
            if uid is not None:
                uid = uid.strip('/').split('/')[-1]
            authors.append( {
                'author': a.get_text().strip(),
                'uid': uid, # None or str
            } )
    if len(titles) != len(authors):
        print('Waring: len(titles) != len(authors), just save "title" and "link"...')
        for i in range(len(titles)):
            yield {
                'title': titles[i]['title'],
                'link': titles[i]['link'],
            }
    else:
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

def isExistForumURL(url: str, session) -> bool:
    response = get_page(url, session)
    if response:
        return True
    else:
        return False

def isExistForumID(forum_id: str, session) -> bool:
    base_url = 'http://bbs.tianya.cn/'
    url = base_url + 'list.jsp?item=' + forum_id + '&order=1'
    return isExistForumURL(url=url,session=session)

def scraper(forum_id: str, session) -> bool:
    if not forum_id or not session:
        sys.exit(1)
    base_url = 'http://bbs.tianya.cn/'
    url = base_url + 'list.jsp?item=' + forum_id + '&order=1'
    if isExistForumURL(url=url,session=session):
        file = open(f'data/{forum_id}-{datetime.datetime.now().strftime("%Y%m%d")}.txt', 'w', encoding='utf-8')
    else:
        print(f'ID: {forum_id} is not exist')
        return False
    while url:
        html = get_page(url, session)
        if not html:
            break
        for item in parse_page(html):
            file.write(str(item) + '\n')
        soup = BeautifulSoup(html, 'lxml')
        nextPage = soup.select('.short-pages-2 a')[-1].get('href')
        if "list.jsp" not in nextPage:
            file.write("--End--")
            print("--End--")
            break
        print(nextPage, end='       \r')
        url = urljoin(base_url, nextPage)

    file.close()
    return True

def main():
    mk_dir('data')
    session = create_session()
    
    # forum_id = input('版id：')
    # scraper(forum_id=str(forum_id), session=session)
    
    for forum_id in range(39,1200):
        print(f'Forum ID: {forum_id} ...')
        scraper(forum_id=str(forum_id), session=session)

if __name__ == '__main__':
    main()
