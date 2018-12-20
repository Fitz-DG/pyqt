#-*-coding:utf-8
import sys
import io
import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
from pandas.io.json import json_normalize
from IPython.display import display_html
import numpy as np

class Crawler():
    def __init__(self):
        pass

    def getFStatementsFromNaverFinance(self, iCode=None):
        # iCode = '005930'
        # iCode = '000660'
        first_url = 'http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd=' + str(iCode)
        print(first_url)
        first_html_text = requests.get(first_url).text
        # print(first_html_text)

        encparam = re.findall("encparam: '(.*?)'", first_html_text)[0]
        print(encparam)
        id = re.findall("id: '(.*?)'", first_html_text)[0]
        print(id)
        ##########################################################################################

        soup = BeautifulSoup(first_html_text, "lxml")
        res = soup.find('table', attrs={'class': 'gHead'})
        # print(str(res))
        small = pd.read_html(str(res))
        small = small[0]
        # display_html(str(res), raw=True)

        # df = df[0]
        # \print(res)
        # result = soup.find('table', attrs={'summary':'시가총액 정보'})
        # print(result)
        # 시총 = soup.find(string="시가총액")
        # print(시총)

        ##########################################################################################
        # headers={'Accept': 'application/json, text/javascript, */*; q=0.01','Referer': 'http://companyinfo.stock.naver.com'}
        # headers ={'Accept': 'application/json'}
        header = {
            'Referer': 'https://companyinfo.stock.naver.com/v1/company/c1010001.aspx',
        }
        second_url = 'http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd=' + str(
            iCode) + '&fin_typ=0&freq_typ=Y&encparam=' + encparam + '&id=' + id
        print(second_url)
        second_html_text = requests.get(second_url, headers=header).text
        # second_html_text = requests.get(second_url, headers={'Accept': 'application/json'}).text
        # second_html_text = requests.get(second_url).text
        # display_html(second_html_text, raw=True)
        # print('result :' + second_html_text)

        soup = BeautifulSoup(second_html_text, "lxml")
        # td = soup.find('table', attrs={'class':'gHead01 all-width'})
        # table = soup.find('div', attrs={'id':'bG05RlB6cn'})
        td = soup.find('table', attrs={'class': 'gHead01 all-width'})
        # print('len = '+str(len(td)))
        # bG05RlB6cn
        ##########################################################################################
        # print(second_html_text)
        # print(str(td))

        ###display_html(str(td), raw=True)

        # print(str(td))
        # df = pd.read_html(str(td), skiprows=1)
        df = pd.read_html(str(td))
        df = df[0]
        df.fillna(0)
        # print(df.dtypes)

        temp_col = ['구분']
        # for i in range(8):
        #    temp_col.append(df.columns[i][1])

        for i in range(8):
            result = re.search("[0-9]*/[0-9]*", str(df.columns[i][1]))
            try :
                data_str = result.group()
                data_str = data_str.replace('/', '-')
                temp_col.append(data_str)
            except AttributeError :
                print("iCode : "+str(iCode))
                print("AttributeError : "+str(df.columns[i][1]))
        # print(data_str)
        df.columns = temp_col
        df = df.set_index('구분')
        df = df.fillna(0)
        df.loc['발행주식수(보통주)'] = df.loc['발행주식수(보통주)'].astype(np.int64)
        df = df.T
        df.astype(int)  # 모든 컬럼에 대해 형변환
        df.index = pd.to_datetime(df.index)
        return df

        #print(df)
        # df
        # df.columns
        # df.index
