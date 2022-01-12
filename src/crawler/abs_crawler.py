#coding:utf-8
from requests_html import HTMLSession
import json
import time

session = HTMLSession()


def crawl_page(get_url):
    res = session.get(get_url)
    lines = []
    for tr in res.html.find('tr'):
        tds = tr.find('td')
        if len(tds)==0:
            continue
        field = tds[0].text
        name = tds[1].text
        issn = tds[2].text
        star = tds[3].text

        line = f"{field}=={name}=={issn}=={star}"

        lines.append(line)
    
    return lines
        


if __name__ == "__main__":
    lines = ['field==name==issn==start']
    for i in range(1,16):
        print(f'progress {i},size:{len(lines)}')
        get_url = f'https://www.datalearner.com/academic/ajg2018/{i}'
        lines.extend(crawl_page(get_url))
        time.sleep(5)
    
    open('data/abs.journal.txt','w',encoding='utf-8').write('\n'.join(lines))
