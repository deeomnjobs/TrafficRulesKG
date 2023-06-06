import logging

import pandas as pd
import json
import lxml
import numpy as np
import html5lib
import bs4
from typing import List
import re

url1 = 'http://www.jiangyong.gov.cn/jygaj/0400/202203/971344fbe5e941f3ac490a30e4e8807d.shtml'  # 江永县
url2 = 'http://jgj.wuhan.gov.cn/wfcl/42811.jhtml'  # 武汉
url3 = 'https://www.chacheliang.com/weizhangdaima/'  # 车辆网
output_dir = './resources/structed_data'


def data_crawl_JiangYong():
    output_file = 'JiangYong.csv'
    output = output_dir + '/' + output_file

    # 读取数据并将其转化为二维数组
    df = pd.read_html(url1, header=0)[1]
    df = np.array(df)
    print(df[0])

    # 删除多余列
    df = np.delete(df, np.s_[7:], 1)
    enforcement_basis = [''] * len(df)

    # 遍历每个数据
    for i in range(0, len(df)):
        for j in range(7):
            if pd.isna(df[i][j]) or df[i][j] == '' or df[i][j] is None:
                df[i][j] = '####'

        # 记分列
        score = df[i][5]
        if score != 0 and score != '0':
            score = '记' + str(score) + '分'
            df[i][5] = score
        else:
            df[i][5] = '####'

        # punish = df[i][6]
        # punish = punish[1:]
        # print(punish)
        # punish = int(punish)
        # if punish != 0 and pd.notna(punish):
        #     punish = '罚款' + str(punish) + '元'
        #     df[i][2] = punish
        # else:
        #     df[i][2] = "####"

        # # other列
        # other = df[i][3]
        # if other == '' or pd.isna(other) or other == '-' or other == '无':
        #     df[i][3] = '####'

        # 分割处理强制措施及违反条款
        enforcement = df[i][4]
        tmp = ''
        if enforcement != '' and pd.notna(enforcement) and enforcement is not None:
            if enforcement.__contains__('扣留驾驶证') or enforcement.__contains__('《法》第一百一十条第一款'):
                tmp += '扣留驾驶证;'
                enforcement_basis[i] += '《法》第一百一十条第一款;'
            elif enforcement.__contains__('收缴物品') or enforcement.__contains__('《法》第一百条第一款'):
                tmp += '收缴物品;'
                enforcement_basis[i] += '《法》第一百条第一款;'
            elif enforcement.__contains__('可以拖移机动车') or enforcement.__contains__('《条例》第一百零四条'):
                tmp += '可以拖移机动车;'
                enforcement_basis[i] += '《条例》第一百零四条;'
            elif enforcement.__contains__('扣留非机动车') or enforcement.__contains__('《法》第八十九条'):
                tmp += '扣留非机动车;'
                enforcement_basis[i] += '《法》第八十九条;'
        df[i][4] = tmp

    print(len(df), df.shape[1])
    temp = ['江永县地方法规'] * len(df)
    temp = np.array(temp)
    enforcement_basis = np.array(enforcement_basis)
    # temp = temp.reshape(-1, 1)
    # temp = temp.T
    print(temp.shape)
    df = np.insert(df, df.shape[1], enforcement_basis, axis=1)
    df = np.insert(df, df.shape[1], temp, axis=1)
    df = np.delete(df, np.s_[0:2], axis=0)
    pd.DataFrame(df,
                 columns=['CODE', 'ACT', 'LAW', 'PUNISH_BASIS', 'ENFORCEMENT', 'SCORE', 'PUNISH', 'ENFORCEMENT_BASIS',
                          'BELONG']).to_csv(output, index=False)

    # CODE,ACT,LAW,PUNISH_BASIS,ENFORCEMENT,SCORE,PUNISH,ENFORCEMENT_BASIS,REGION
    # "CODE,ACT,LAW,PUNISH_BASIS,SCORE,PUNISH,OTHER_PENALTIES,ENFORCEMENT,ENFORCEMENT_BASIS,OTHER_MEASURES,OTHER_MEASURES_BASIS"


def data_crawl_WuHan():
    output_file = 'WuHan.csv'
    output = output_dir + '/' + output_file

    # 读取数据并将其转化为二维数组
    df = pd.read_html(url2, header=0)[0]
    df = np.array(df)

    # 遍历每个数据
    for i in range(0, len(df)):
        for j in range(11):
            if pd.isna(df[i][j]) or df[i][j] == '' or df[i][j] is None:
                df[i][j] = '####'

        # 记分列
        score = df[i][4]
        if score != 0 and score != '0' and score != '####':
            score = '记' + str(int(score)) + '分'
            df[i][4] = score
        else:
            df[i][4] = '####'

        # 罚款
        punish = df[i][5]
        if punish != 0 and punish != '####':
            punish = '罚款' + str(punish) + '元'
            df[i][5] = punish
        else:
            df[i][5] = '####'

    temp = ['武汉市地方法规'] * len(df)
    temp = np.array(temp)
    df = np.insert(df, df.shape[1], temp, axis=1)
    df = np.delete(df, np.s_[0:1], axis=0)
    pd.DataFrame(df,
                 columns=['CODE', 'ACT', 'LAW', 'PUNISH_BASIS', 'SCORE', 'PUNISH', 'OTHER_PENALTIES', 'ENFORCEMENT',
                          'ENFORCEMENT_BASIS', 'OTHER_MEASURES', 'OTHER_MEASURES_BASIS', 'BElONG']).to_csv(output,
                                                                                                           index=False)


def data_crawl_Nation():
    output_file = 'Nation.csv'
    output = output_dir + '/' + output_file

    # 读取数据并将其转化为二维数组
    df = pd.read_html(url3, header=0)[0]
    df = np.array(df)
    print(df[0])

    # 遍历每个数据
    for i in range(0, len(df)):
        for j in range(len(df[0])):
            if pd.isna(df[i][j]) or df[i][j] == '' or df[i][j] is None:
                df[i][j] = '####'

        # 记分列
        score = df[i][1]
        print(score)
        if score != 0 and score != '0' and score != '####':
            score = '记' + str(int(score)) + '分'
            df[i][1] = score
        else:
            df[i][1] = '####'

        # 罚款
        punish = df[i][2].replace('￥', '')
        if punish != 0 and punish != '####':
            punish = '罚款' + str(punish) + '元'
            df[i][2] = punish
        else:
            df[i][2] = '####'

    temp = ['全国性法规'] * len(df)
    temp = np.array(temp)
    df = np.insert(df, df.shape[1], temp, axis=1)
    df = np.delete(df, np.s_[0:1], axis=0)
    pd.DataFrame(df,
                 columns=['CODE', 'SCORE', 'PUNISH', 'OTHER_PENALTIES', 'ACT', 'BELONG']).to_csv(output,
                                                                                                 index=False)


if __name__ == '__main__':
    logging.info("structed data crawl is running.")
    data_crawl_JiangYong()
    logging.info("JiangYong is done.")
    data_crawl_WuHan()
    logging.info("WuHan is done.")
    data_crawl_Nation()
    logging.info("Nation is done.")
    logging.info("structed data crawl is done.")
