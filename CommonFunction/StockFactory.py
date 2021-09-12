from pykrx import stock as PK
import FinanceDataReader as FDR
import pandas as PD
import urllib.parse as URLPARSE
import datetime
import json

from dateutil.relativedelta import relativedelta

'''
    FinanceDataReader 모듈을 사용한 주식정보를 가져온다.
    종목코드(Symbol), 시장종류(Market), 종목명(Name)
    market = (KRX, KOSPI, KOSDAQ)
'''
def GetStockBaseInfoByFinanceDataReader(market):
    stockBaseInfo = FDR.StockListing(market)
    stockBaseInfo = stockBaseInfo[['Symbol', 'Market', 'Name']]
    stockBaseInfo = stockBaseInfo.rename(columns={'Symbol': 'StockCode', 'Market': 'Market', 'Name': 'StockName'})

    return stockBaseInfo


'''
    FinanceDataReader 모듈을 사용한 날짜별 주식가격정보를 가져온다.
'''
def GetStockDetailPriceByFinanceDataReader(stockCode):
    TODAY = datetime.datetime.now().date()

    TODAY_BEFORE_ONEYEAR = TODAY - relativedelta(years=1)
    TODAY_BEFORE_ONEMONTH = TODAY - relativedelta(months=1)
    TODAY_BEFORE_THREEMONTH = TODAY - relativedelta(months=3)
    TODAY_BEFORE_SIXMONTH = TODAY - relativedelta(months=6)
    TODAY_BEFORE_TENYEARS = TODAY - relativedelta(years=10)

    stockDetailPrice_ONEYEAR = FDR.DataReader(stockCode, start=TODAY_BEFORE_ONEYEAR).reset_index()
    stockDetailPrice_ONEMONTH = FDR.DataReader(stockCode, start=TODAY_BEFORE_ONEMONTH).reset_index()
    stockDetailPrice_THREEMONTH = FDR.DataReader(stockCode, start=TODAY_BEFORE_THREEMONTH).reset_index()
    stockDetailPrice_SIXMONTH = FDR.DataReader(stockCode, start=TODAY_BEFORE_SIXMONTH).reset_index()
    stockDetailPrice_TENYEARS = FDR.DataReader(stockCode, start=TODAY_BEFORE_TENYEARS).reset_index()

    stockDetailPrice_ONEYEAR['Date'] = stockDetailPrice_ONEYEAR['Date'].apply(str)
    stockDetailPrice_ONEMONTH['Date'] = stockDetailPrice_ONEMONTH['Date'].apply(str)
    stockDetailPrice_THREEMONTH['Date'] = stockDetailPrice_THREEMONTH['Date'].apply(str)
    stockDetailPrice_SIXMONTH['Date'] = stockDetailPrice_SIXMONTH['Date'].apply(str)
    stockDetailPrice_TENYEARS['Date'] = stockDetailPrice_TENYEARS['Date'].apply(str)

    return stockDetailPrice_ONEYEAR, stockDetailPrice_ONEMONTH, stockDetailPrice_THREEMONTH, stockDetailPrice_SIXMONTH, stockDetailPrice_TENYEARS

'''
    https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage에 공시되어 있는 Excel 파일을 통해 주식정보를 가져온다.
    종목코드, 종목명  
'''
def GetStockBaseInfoByCrawling(market):
    if market == 'KOSPI':
        market = 'stockMkt'
    elif market == 'KOSDAQ':
        market = 'kosdaqMkt'
    else:
        market = ''

    DOWNLOAD_URL = 'kind.krx.co.kr/corpgeneral/corpList.do'
    params = {}

    params = {'method': 'download', 'marketType': ''}
    params['marketType'] = market

    str_params = URLPARSE.urlencode(params)
    url = URLPARSE.urlunsplit(['http', DOWNLOAD_URL, '', str_params, ''])

    df = PD.read_html(url, header=0)[0]
    df.종목코드 = df.종목코드.map('{:06d}'.format)
    df = df[['회사명', '종목코드']]
    df = df.rename(columns={'회사명': 'stockName', '종목코드': 'stockCode'})

    stockBaseInfo = df

    return stockBaseInfo



'''
    PyKrx 모듈을 사용한 주식정보를 가져온다.
    종목코드, 종목명
    market = (KRX, KOSPI, KOSDAQ)
'''
def GetStockBaseInfoByPYKRX(market):
    TODAY = datetime.datetime.now().strftime('%Y%m%d')

    stockBaseInfo_stockName = []
    stockBaseInfo_stockCode = PK.get_market_ticker_list(date=TODAY, market=market)

    for stockCode in stockBaseInfo_stockCode:
        stockName = PK.get_market_ticker_name(stockCode)
        stockBaseInfo_stockName.append(stockName)
        
    df_attribute = {
        'stockCode': stockBaseInfo_stockCode,
        'stockName': stockBaseInfo_stockName
    }

    df = PD.DataFrame(df_attribute)
    stockBaseInfo = df

    return stockBaseInfo

'''
    PyKrx 모듈을 사용한 날짜별 주식가격정보를 가져온다.
'''
def GetStockDetailPriceByPYKRX(stockCode):
    TODAY = datetime.datetime.now().date()
    
    TODAY_BEFORE_ONEYEAR = datetime.datetime.strftime(TODAY - relativedelta(years=1), '%Y%m%d')
    TODAY_BEFORE_ONEMONTH = datetime.datetime.strftime(TODAY - relativedelta(months=1), '%Y%m%d')
    TODAY_BEFORE_THREEMONTH = datetime.datetime.strftime(TODAY - relativedelta(months=3), '%Y%m%d')
    TODAY_BEFORE_SIXMONTH = datetime.datetime.strftime(TODAY - relativedelta(months=6), '%Y%m%d')
    TODAY_BEFORE_TENYEARS = datetime.datetime.strftime(TODAY - relativedelta(years=10), '%Y%m%d')

    TODAY = datetime.datetime.now().strftime('%Y%m%d')
    
    stockDetailPrice_ONEYEAR = PK.get_market_ohlcv_by_date(fromdate=TODAY_BEFORE_ONEYEAR, todate=TODAY, ticker=stockCode).reset_index()
    stockDetailPrice_ONEMONTH = PK.get_market_ohlcv_by_date(fromdate=TODAY_BEFORE_ONEMONTH, todate=TODAY, ticker=stockCode).reset_index()
    stockDetailPrice_THREEMONTH = PK.get_market_ohlcv_by_date(fromdate=TODAY_BEFORE_THREEMONTH, todate=TODAY, ticker=stockCode).reset_index()
    stockDetailPrice_SIXMONTH = PK.get_market_ohlcv_by_date(fromdate=TODAY_BEFORE_SIXMONTH, todate=TODAY, ticker=stockCode).reset_index()
    stockDetailPrice_TENYEARS = PK.get_market_ohlcv_by_date(fromdate=TODAY_BEFORE_TENYEARS, todate=TODAY, ticker=stockCode).reset_index()

    stockDetailPrice_ONEYEAR['날짜'] = stockDetailPrice_ONEYEAR['날짜'].apply(str)
    stockDetailPrice_ONEMONTH['날짜'] = stockDetailPrice_ONEMONTH['날짜'].apply(str)
    stockDetailPrice_THREEMONTH['날짜'] = stockDetailPrice_THREEMONTH['날짜'].apply(str)
    stockDetailPrice_SIXMONTH['날짜'] = stockDetailPrice_SIXMONTH['날짜'].apply(str)
    stockDetailPrice_TENYEARS['날짜'] = stockDetailPrice_TENYEARS['날짜'].apply(str)

    return stockDetailPrice_ONEYEAR, stockDetailPrice_ONEMONTH, stockDetailPrice_THREEMONTH, stockDetailPrice_SIXMONTH, stockDetailPrice_TENYEARS


'''
    Session 값으로 저장된 모든 종목에 대해서 종목명이 포함된 정보를 가져온다.
'''
def GetStockBaseInfoByStockName(stockAllInfo, stockName):
    stockAllInfo = json.loads(stockAllInfo)

    stockInfo = list(filter(lambda x: stockName.upper() in x['stockName'].upper(), stockAllInfo))

    stockInfo = json.dumps(stockInfo, ensure_ascii=False)

    return stockInfo