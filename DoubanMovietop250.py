# DoubanMovietop250
#!/usr/bin/python
# -*- coding:utf8 -*-
import os
import time

import sys
import requests
from bs4 import BeautifulSoup

__author__ = 'Jason'

file_name = 'movies_top250.txt'
file_content = ''
file_content += 'Created at\t' + time.asctime() + '\n'
target_dir = os.getcwd() + '/douban/'

def movies_spider(start):
    global file_content
    url = "https://movie.douban.com/top250?start=%d" % start
    response = requests.get(url).text
    soup = BeautifulSoup(response)
    movie_list = soup.find_all('div', {'class': 'item'})
    for item in movie_list:
        order = int(item.find('em').string)
        icon_path = item.find('img').get('src')

        info = item.find('div', {'class': 'info'})
        name = str(order)+ info.find('span', {'class': 'title'}).string
        save_pic(icon_path, name)
        rating_num = info.find('span', {'class': 'rating_num'}).string
        total = info.find('span', {'class': 'rating_num'}).find_next_sibling().find_next_sibling().string
        inq = info.find('span', {'class': 'inq'})
        try:
            quote = inq.get_text()
        except AttributeError:
            quote = 'None'
            print("Type error")

        #file_content += "%d\t%s\trate:%s\n\t%s\tquote:%s\n\n" % (order, name, rating_num, total, quote)


def do_spider():
    for start in (range(250)[::25]):
        movies_spider(start)


def save_pic(path, name):
    file = requests.get(path, stream=True).content
    with open(get_dir() + '/' + name + '.jpg', 'wb') as jpg:
        jpg.write(file)


def get_dir():
    path = os.path.join(os.getcwd(), "doubanTop250")
    if os.path.exists(path):
        return path
    os.mkdir(path)
    return path


if __name__ == '__main__':
    do_spider()
    #with open(get_dir() + '/' + file_name, 'w') as f:
    #    f.write(file_content)

    print("DONE")
