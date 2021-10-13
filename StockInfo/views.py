from django.shortcuts import render
from pykrx import stock
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import json

from rest_framework.permissions import AllowAny, IsAuthenticated

from CommonFunction.StockFactory import *

# Create your views here.
class StockBaseInfoByFinanceDataReader(APIView):
    '''
        FinanceDataReader 모듈을 사용한 주식정보를 가져온다.
        종목코드(Symbol), 시장종류(Market), 종목명(Name)
    '''

    def get(self, request, market):
        stockBaseInfoByMarket = GetStockBaseInfoByFinanceDataReader(market)

        request.session['StockBaseInfo'] = stockBaseInfoByMarket.to_json(orient='records', force_ascii=False)

        stockBaseInfoByMarket = stockBaseInfoByMarket.to_json(orient='records', force_ascii=False)

        return Response(stockBaseInfoByMarket)


class StockBaseInfoByCrawling(APIView):
    '''
        https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage에 공시되어 있는 Excel 파일을 통해 주식정보를 가져온다.
        종목코드, 종목명
    '''
    permission_classes = [AllowAny]

    def get(self, request, market):
        stockBaseInfoByMarket = GetStockBaseInfoByCrawling(market)

        request.session['StockBaseInfo'] = stockBaseInfoByMarket.to_json(orient='records', force_ascii=False)

        stockBaseInfoByMarket = stockBaseInfoByMarket.to_json(orient='records', force_ascii=False)

        return Response(stockBaseInfoByMarket)


class StockBaseInfoByPYKRX(APIView):
    '''
        PyKrx 모듈을 사용한 주식정보를 가져온다.
        종목코드, 종목명
    '''

    def get(self, request, market):
        stockBaseInfoByMarket = GetStockBaseInfoByPYKRX(market)
        stockBaseInfoByMarket = stockBaseInfoByMarket.to_json(orient='records', force_ascii=False)

        request.session['StockBaseInfo'] = stockBaseInfoByMarket

        return Response(stockBaseInfoByMarket)

class StockBaseInfoByStockName(APIView):
    '''
        사용자가 입력한 회사명 문자열이 포함된 주식정보를 가져온다.
    '''

    def get(self, request, stockName):
        stockAllInfo = request.session.get('StockBaseInfo')

        stockInfo = GetStockBaseInfoByStockName(stockAllInfo, stockName)

        return Response(stockInfo)


class StockDetailPriceByFinanceDataReader(APIView):
    '''
        종목코드에 맞는 가격정보를 가져온다. (FinanceDataReader)
    '''

    def get(self, request, stockCode):
        stockDetailPrice_ONEYEAR, stockDetailPrice_ONEMONTH, stockDetailPrice_THREEMONTH, stockDetailPrice_SIXMONTH, stockDetailPrice_TENYEARS = GetStockDetailPriceByFinanceDataReader(stockCode)

        stockDetailPrice = {
            'ONEYEAR': stockDetailPrice_ONEYEAR.to_dict(orient="records"),
            'ONEMONTH': stockDetailPrice_ONEMONTH.to_dict(orient="records"),
            'THREEMONTH': stockDetailPrice_THREEMONTH.to_dict(orient="records"),
            'SIXMONTH': stockDetailPrice_SIXMONTH.to_dict(orient="records"),
            'TENYEARS': stockDetailPrice_TENYEARS.to_dict(orient="records")
        }

        stockDetailPrice = json.dumps(stockDetailPrice, ensure_ascii=False)

        return Response(stockDetailPrice)


class StockDetailPriceByPYKRX(APIView):
    '''
        종목코드에 맞는 가격정보를 가져온다. (PyKrx)
    '''
    permission_classes = [AllowAny]

    def get(self, request, stockCode):
        stockDetailPrice_ONEYEAR, stockDetailPrice_ONEMONTH, stockDetailPrice_THREEMONTH, stockDetailPrice_SIXMONTH, stockDetailPrice_TENYEARS = GetStockDetailPriceByPYKRX(stockCode)

        stockDetailPrice = {
            'ONEYEAR': stockDetailPrice_ONEYEAR.to_dict(orient="records"),
            'ONEMONTH': stockDetailPrice_ONEMONTH.to_dict(orient="records"),
            'THREEMONTH': stockDetailPrice_THREEMONTH.to_dict(orient="records"),
            'SIXMONTH': stockDetailPrice_SIXMONTH.to_dict(orient="records"),
            'TENYEARS': stockDetailPrice_TENYEARS.to_dict(orient="records")
        }

        stockDetailPrice = json.dumps(stockDetailPrice, ensure_ascii=False)

        return Response(stockDetailPrice)