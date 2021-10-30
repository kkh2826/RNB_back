from pykrx import stock as PK
import FinanceDataReader as FDR
import pandas as PD
import urllib.parse as URLPARSE
import datetime
from dateutil.relativedelta import relativedelta
import json

# For Crawling
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup


'''
    FinanceDataReader 모듈을 사용한 주식정보를 가져온다.
    종목코드(Symbol), 시장종류(Market), 종목명(Name)
    market = (KRX, KOSPI, KOSDAQ)
'''
def GetStockBaseInfoByFinanceDataReader(market):
    stockBaseInfo = FDR.StockListing(market)
    stockBaseInfo = stockBaseInfo[['Symbol', 'Market', 'Name']]
    stockBaseInfo = stockBaseInfo.rename(columns={'Symbol': 'stockCode', 'Market': 'market', 'Name': 'stockName'})

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
    # if market == 'KOSPI':
    #     market = 'stockMkt'
    # elif market == 'KOSDAQ':
    #     market = 'kosdaqMkt'
    # else:
    #     market = ''

    # DOWNLOAD_URL = 'kind.krx.co.kr/corpgeneral/corpList.do'

    # params = {'method': 'download', 'marketType': ''}
    # params['marketType'] = market

    # str_params = URLPARSE.urlencode(params)
    # url = URLPARSE.urlunsplit(['http', DOWNLOAD_URL, '', str_params, ''])

    # df = PD.read_html(url, header=0)[0]

    # print(df)

    # df.종목코드 = df.종목코드.map('{:06d}'.format)
    # df = df[['회사명', '종목코드']]
    # df = df.rename(columns={'회사명': 'stockName', '종목코드': 'stockCode'})

    # stockBaseInfo = df

    OTP_URL = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'

    params = {
        'mktId': 'ALL',
        'share': '1',
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/standard/MDCSTAT01901'
    }

    otp_response = requests.post(url=OTP_URL, data=params, headers={'User-agent': 'Mozilla/5.0'})

    DOWNLOAD_URL = 'data.krx.co.kr/comm/fileDn/download_excel/download.cmd'

    params = {
        'code': otp_response.content
    }

    str_params = URLPARSE.urlencode(params)
    url = URLPARSE.urlunsplit(['http', DOWNLOAD_URL, '', str_params, ''])

    df = PD.read_excel(url, header=0)
    df = df[['단축코드', '한글 종목약명', '시장구분']]
    df = df.rename(columns={'단축코드': 'stockCode', '한글 종목약명': 'stockName', '시장구분': 'market'})

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

    TODAY = datetime.datetime.strftime(datetime.datetime.now().date() - relativedelta(days=1), '%Y%m%d')
    
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
    특정 종목에 대한 전영업일 종가, 현재가격을 가져온다. (NAVER 증시 기준)
'''
def GetStockPreviosCurrentPrice(stockCode):

    # 전영업일을 통해 전영업일 종가 구하기 (현재일 기준)
    TODAY = datetime.datetime.strftime(datetime.datetime.now().date(), '%Y%m%d')
    PREVMONTH = datetime.datetime.strftime(datetime.datetime.now().date() - relativedelta(weeks=2), '%Y%m%d')

    previousInfo = PK.get_market_ohlcv_by_date(fromdate=PREVMONTH, todate=TODAY, ticker=stockCode).reset_index()

    previousInfo = previousInfo.tail(2)

    previousPrice = previousInfo['종가'].iloc[0]
    currentPrice = previousInfo['종가'].iloc[-1]

    currentPrice = "{:,}".format(currentPrice)
    previousPrice = "{:,}".format(previousPrice)


    # 현재 가격 구하기 (네이버 증시기준으로 Crawling)
    # url = f"http://finance.naver.com/item/main.nhn?code={stockCode}"

    # ua = UserAgent()
    # headers = { 'User-agent': ua.ie }

    # response = requests.get(url, headers=headers)
    # content = BeautifulSoup(response.text, 'lxml')

    # info = content.select_one('p.no_today')
    # currentPrice = info.select_one('span.blind')


    return previousPrice, currentPrice
