from pykrx import stock
from rest_framework.views import APIView
from rest_framework.response import Response
import json

from rest_framework.permissions import AllowAny, IsAuthenticated

from CommonFunction.StockFactory import *

# Create your views here.
class StockBaseInfoByFinanceDataReader(APIView):
    '''
        FinanceDataReader 모듈을 사용한 주식정보를 가져온다.
        종목코드(Symbol), 시장종류(Market), 종목명(Name)
    '''
    permission_classes = [AllowAny]

    def get(self, request, market):
        stockBaseInfoByMarket = GetStockBaseInfoByFinanceDataReader(market)

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

        stockBaseInfoByMarket = stockBaseInfoByMarket.to_json(orient='records', force_ascii=False)

        return Response(stockBaseInfoByMarket)


class StockBaseInfoByPYKRX(APIView):
    '''
        PyKrx 모듈을 사용한 주식정보를 가져온다.
        종목코드, 종목명
    '''

    permission_classes = [AllowAny]

    def get(self, request, market):
        stockBaseInfoByMarket = GetStockBaseInfoByPYKRX(market)
        stockBaseInfoByMarket = stockBaseInfoByMarket.to_json(orient='records', force_ascii=False)

        return Response(stockBaseInfoByMarket)


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


class StockBasicPriceInfo(APIView):

    permission_classes = [AllowAny]

    def get(self, request, stockCode):

        str_previousPrice, str_currentPrice = GetStockPreviosCurrentPrice(stockCode)

        previousPrice = int(str_previousPrice.replace(',', ''))
        currentPrice = int(str_currentPrice.replace(',', ''))

        updownRate = (float)("{:.2f}".format((currentPrice - previousPrice) * 100 / currentPrice))
        positiveFlag = 1 if updownRate >= 0 else 0
        
        stockBasicPrice = {
            'PREVIOS': str_previousPrice,
            'CURRENT': str_currentPrice,
            'UPDOWNRATE': updownRate,
            'POSITIVEFLAG': positiveFlag
        }

        stockBasicPrice = json.dumps(stockBasicPrice, ensure_ascii=False)

        return Response(stockBasicPrice)
