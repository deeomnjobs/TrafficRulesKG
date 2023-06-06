# encoding=utf-8
import json
import logging
import pandas as pd
import requests
import lxlm
import os
from bs4 import BeautifulSoup
import requests

cookies = {
    'SINAGLOBAL': '3779841131600.079.1646100789330',
    'UOR': 'cn.bing.com,weibo.com,link.zhihu.com',
    'XSRF-TOKEN': 'ueo_LhlC-aGHg6NDWw3QKI-K',
    '_s_tentry': 'weibo.com',
    'Apache': '4017962063768.8164.1682570004356',
    'ULV': '1682570004362:4:2:2:4017962063768.8164.1682570004356:1682562153539',
    'login_sid_t': 'f136432adc299282087787fca7cc9757',
    'cross_origin_proto': 'SSL',
    'wb_view_log': '2560*14401',
    'appkey': '',
    'WBtopGlobal_register_version': '2023042712',
    'SSOLoginState': '1682570382',
    'WBPSESS': '142h1YMIzPemrIY2h4LuJLLGemanRXhw0JrNfFcH-YZQTkl-Vdd7JkDMMo95rLpNApHY8xIMcF1BzonhuxyoCNtXEoIK0QKpWkmSe02oWJ3evTqVlsUefUACxus6Pc-TrYOAhTEYXPxSdrhqfP-6gw==',
    'SCF': 'AizN2uYViFL_5mwT8y7MRq8W2njQOLbO4jHeDEKE77-rORQpEgfpxrVOFi0zAgffRVL9FBxMtD_Gz7OO0NxHTxg.',
    'SUB': '_2A25JTY4jDeRhGeVL4lYZ8SfNwjmIHXVqOvjrrDV8PUNbmtANLU3GkW9NTDJN7JSKbdLpFdlstmqsLm6eV8H6jZV9',
    'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WhUeB93OJAYlyvunAGiTLyT5JpX5KMhUgL.Foef1KBReK.p1K-2dJLoIEQLxK.L1-zLBKnLxK-LBo.L1K-LxKBLBonLB-BLxKML1-2L1hx29gHadgRt',
    'ALF': '1685162866',
    'PC_TOKEN': '2853e31c18',
    'WBStorage': '4d96c54e|undefined',
}

cookies_1 = {
    'SUB': '_2AkMTF7UYf8NxqwJRmf0Qy2nraY9wyA3EieKlS0TDJRMxHRl-yT9kqhQ-tRB6OJeb9xXgWe0OWR9436PkxihtnWWCoctf',
    'SUBP': '0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFrdo7zkAdVdVlTeTxBW6RP',
    'SINAGLOBAL': '7352561210770.421.1682651697031',
    'PC_TOKEN': '8cd76ddd89',
    '_s_tentry': '-',
    'Apache': '5496570465328.845.1682662732754',
    'ULV': '1682662732757:2:2:2:5496570465328.845.1682662732754:1682651697049',
}

headers = {
    'authority': 'weibo.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'client-version': 'v2.40.43',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'SINAGLOBAL=3779841131600.079.1646100789330; UOR=cn.bing.com,weibo.com,link.zhihu.com; XSRF-TOKEN=ueo_LhlC-aGHg6NDWw3QKI-K; _s_tentry=weibo.com; Apache=4017962063768.8164.1682570004356; ULV=1682570004362:4:2:2:4017962063768.8164.1682570004356:1682562153539; login_sid_t=f136432adc299282087787fca7cc9757; cross_origin_proto=SSL; wb_view_log=2560*14401; appkey=; WBtopGlobal_register_version=2023042712; SSOLoginState=1682570382; WBPSESS=142h1YMIzPemrIY2h4LuJLLGemanRXhw0JrNfFcH-YZQTkl-Vdd7JkDMMo95rLpNApHY8xIMcF1BzonhuxyoCNtXEoIK0QKpWkmSe02oWJ3evTqVlsUefUACxus6Pc-TrYOAhTEYXPxSdrhqfP-6gw==; SCF=AizN2uYViFL_5mwT8y7MRq8W2njQOLbO4jHeDEKE77-rORQpEgfpxrVOFi0zAgffRVL9FBxMtD_Gz7OO0NxHTxg.; SUB=_2A25JTY4jDeRhGeVL4lYZ8SfNwjmIHXVqOvjrrDV8PUNbmtANLU3GkW9NTDJN7JSKbdLpFdlstmqsLm6eV8H6jZV9; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhUeB93OJAYlyvunAGiTLyT5JpX5KMhUgL.Foef1KBReK.p1K-2dJLoIEQLxK.L1-zLBKnLxK-LBo.L1K-LxKBLBonLB-BLxKML1-2L1hx29gHadgRt; ALF=1685162866; PC_TOKEN=2853e31c18; WBStorage=4d96c54e|undefined',
    'referer': 'https://weibo.com/shanghaicity?tabtype=feed',
    'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'server-version': 'v2023.04.26.1',
    'traceparent': '00-b2b535bef662a26fc13bc46c9f97c508-b8ed722b507a9616-00',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': 'ueo_LhlC-aGHg6NDWw3QKI-K',
}

params = {
    'uid': '2539961154',
    'page': '1',
    'feature': '0',
    'q': '交通案例',
}


def url_list_acquire():
    url_list = []

    for i in range(1, 15):
        params['page'] = str(i)
        response = requests.get('https://weibo.com/ajax/profile/searchblog', params=params, cookies=cookies,
                                headers=headers)
        response_json = response.json()
        for data in response_json['data']['list']:
            if 'url_struct' in data:
                for data_url in data['url_struct']:
                    if 'long_url' in data_url:
                        url_list.append(data_url['long_url'])

    with open('./resources/url_list.txt', 'w', encoding='utf-8') as f:
        for url in url_list:
            f.write(url + '\n')

# response = requests.get('https://weibo.com/ttarticle/p/show?id=2309404893730850341459',cookies=cookies_1)
# response.encoding='utf-8'
# soup = BeautifulSoup(response.text,'html.parser')
# # with open('weibo.txt','w',encoding='utf-8') as f:
# #     f.write(soup.text)
# # with open('weibo.txt','r',encoding='utf-8') as f1,open('test_1.txt','w',encoding='utf-8') as f2:
# #     for line in f1.readlines():
# #         if line != '\n':
# #             f2.write(line)
# raw_data = soup.text.split('\n')

def line_data_acquire():
    raw_data_list = []
    with open('./resources/url_list.txt', 'r', encoding='utf-8') as f:
        for url in f.readlines():
            response = requests.get(url, cookies=cookies_1)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            for temp in soup.text.split('\n'):
                if len(temp) >10:
                    raw_data_list.append(temp)
    with open('test_1.txt','w',encoding='utf-8') as f:
        for raw_data in raw_data_list:
            f.write(raw_data)

line_data_acquire()