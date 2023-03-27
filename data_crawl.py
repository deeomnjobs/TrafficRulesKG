import json
import logging

import pandas as pd
import requests
import lxlm
# # 获取表格
# html_data = pd.read_html("http://jgj.wuhan.gov.cn/wfcl/42811.jhtml", encoding='utf-8')[0]
# # 处理成csv数据
# html_data.to_csv(r'D:\Python_Programe\PandasTest\resources\table.csv', index=False, header=None)
# csv_data = pd.read_csv(r'D:\Python_Programe\PandasTest\resources\table.csv')
# csv_data.columns=["code", "act", "law", "punish_basis", "score", "fine", "other_punish", "force_measure", "force_measure_basis", "other_measure", "other_masure_basis"]
# csv_data.to_csv(r'D:\Python_Programe\PandasTest\resources\table.csv',index=False)

# gov_html_data = pd.read_html("http://js.122.gov.cn/#/viopubdetail?vioid=32003610000000816871")[0]
# print(gov_html_data)

import requests

logging.getLogger().setLevel(logging.INFO)
cookies_list = {
    '_uab_collina': '167884451608101158023961',
    'JSESSIONID-L': 'cc350e99-6ec9-4b7e-b6f1-0a3d7cba9796',
}

headers_list = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '_uab_collina=167884451608101158023961; JSESSIONID-L=5efa3ad6-adae-4c4d-8c3f-c400e02bb94d',
    'Origin': 'https://js.122.gov.cn',
    'Referer': 'https://js.122.gov.cn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data_list = {
    'page': '0',
    'size': '20',
    'startTime': '',
    'endTime': '',
    'gsyw': '01',
}

cookies_detail = {
    '_uab_collina': '167884451608101158023961',
    'JSESSIONID-L': '5efa3ad6-adae-4c4d-8c3f-c400e02bb94d',
}

headers_detail = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '_uab_collina=167884451608101158023961; JSESSIONID-L=5efa3ad6-adae-4c4d-8c3f-c400e02bb94d',
    'Origin': 'https://js.122.gov.cn',
    'Referer': 'https://js.122.gov.cn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data_detail = {
    'id': '32003610000000812307',
}

def get_vioid_list():
    vioid_list = []
    for i in range(200):
        data_list['page'] = i
        # 获取response
        response = requests.post('https://js.122.gov.cn/m/viopub/getVioPubList', cookies=cookies_list, headers=headers_list, data=data_list)
        response_data = json.loads(response.text)
        code = response_data['code']
        if (code != 200):
            # cookie has expired
            logging.info("cookies_list has expired. Pls renew it.")
            return
        for content in response_data['data']['list']['content']:
            vioid_list.append(content['id'])
    with open("./resources/vioid.txt", 'w+') as f:
        for vioid in vioid_list:
            f.write(vioid+'\n')

# response = requests.post('https://js.122.gov.cn/m/viopub/getVioPubDetail', cookies=cookies_detail, headers=headers_detail, data=data_detail)
#
# print(response.json())
