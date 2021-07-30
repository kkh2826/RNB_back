from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

import FinanceDataReader as FDR
import pandas as PD
import urllib.parse as URLPARSE
import json

# Create your views here.
class StockBaseInfoByFinanceDataReader(APIView):
    '''
        FinanceDataReader 모듈을 사용한 주식정보를 가져온다.
        종목코드(Symbol), 시장종류(Market), 종목명(Name)
    '''

    def get(self, request, market):
        stockBaseInfoByMarket = self.GetStockBaseInfo(market)

        return HttpResponse(stockBaseInfoByMarket.to_json(orient='records', force_ascii=False))


    def GetStockBaseInfo(self, market):
        stockBaseInfo = FDR.StockListing(market)
        stockBaseInfo = stockBaseInfo[['Symbol', 'Market', 'Name']]

        return stockBaseInfo

class StockBaseInfoByCrawling(APIView):
    '''
        https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage에 공시되어 있는 Excel 파일을 통해 주식정보를 가져온다.
        종목코드, 종목명
    '''

    DOWNLOAD_URL = 'kind.krx.co.kr/corpgeneral/corpList.do'
    params = {}

    def get(self, request, market):
        stockBaseInfoByMarket = self.GetStockBaseInfo(market)

        request.session['StockBaseInfo'] = stockBaseInfoByMarket.to_json(orient='records', force_ascii=False)

        return HttpResponse(stockBaseInfoByMarket.to_json(orient='records', force_ascii=False))


    def GetStockBaseInfo(self, market):
        params = {'method': 'download', 'marketType': ''}
        params['marketType'] = market

        str_params = URLPARSE.urlencode(params)
        url = URLPARSE.urlunsplit(['http', self.DOWNLOAD_URL, '', str_params, ''])

        df = PD.read_html(url, header=0)[0]
        df.종목코드 = df.종목코드.map('{:06d}'.format)
        df = df[['회사명', '종목코드']]

        stockBaseInfo = df

        return stockBaseInfo


class StockBaseInfoByStockName(APIView):
    '''
        사용자가 입력한 회사명 문자열이 포함된 주식정보를 가져온다.
    '''
    def get(self, request, stockName):
        stockAllInfo = request.session.get('StockBaseInfo')
        stockAllInfo = json.loads(stockAllInfo)

        stockInfo = list(filter(lambda x: stockName in x['회사명'], stockAllInfo))

        return HttpResponse(json.dumps(stockInfo, ensure_ascii=False))