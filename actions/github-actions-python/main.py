# pip install BeautifulSoup4 pandas python-bitget
import asyncio

import requests
# pip install BeautifulSoup4
from bs4 import BeautifulSoup#github action当中不存在内置的这个包需要单独下载
# pip install pandas
import re
import pandas as pd#github action当中不存在内置的这个包需要单独下载
import json
import time
import datetime

# pip install python-bitget
# 【参考文档】https://bitgetlimited.github.io/apidoc/en/mix/#get-account-list
from pybitget import Client
from pybitget.utils import *
from pybitget.enums import *
from pybitget import logger

logger.add(
    sink=f"log.log",#sink:创建日志文件的路径。
    level="INFO",#level:记录日志的等级,低于这个等级的日志不会被记录。等级顺序为 debug < info < warning < error。设置 INFO 会让 logger.debug 的输出信息不被写入磁盘。
    rotation="00:00",#rotation:轮换策略,此处代表每天凌晨创建新的日志文件进行日志 IO；也可以通过设置 "2 MB" 来指定 日志文件达到 2 MB 时进行轮换。   
    retention="7 days",#retention:只保留 7 天。 
    encoding="utf-8",#encoding:编码方式
    enqueue=True,#enqueue:队列 IO 模式,此模式下日志 IO 不会影响 python 主进程,建议开启。
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"#format:定义日志字符串的样式,这个应该都能看懂。
)

import math
#【bitget理财大概一个小时一结算利息】
# 配置您的Bitget API密钥和密码短语
api_key = "bg_5e69f9e32e87c9bb8087f97cc6adb910"
api_secret = 'b0682a6e4a0e0c50493a4be19b4f56de4fa81f07d6e7d010a71e1971a7c3bbb4'#默认HMAC方式解码
api_passphrase = "wthWTH00"
client = Client(api_key, api_secret, passphrase=api_passphrase)

#【获取现货账户余额】
def getspotbalance(coin):
    request_path="/api/v2/spot/account/assets"
    params = {"coin":coin}
    res=client._request_with_params(params=params,request_path=request_path,method="GET",)["data"]
    # logger.info(f"res,{type(res)},{res}")
    return res
# spotbalance=getspotbalance(coin="USDT")
# usdtbalance=[balance for balance in spotbalance if balance["coin"]=="USDT"][0]["available"]
# logger.info(f"usdtbalance,{usdtbalance},{type(usdtbalance)}")

#【获取理财产品列表】这里只要活期存款
def getsavingslist(coin):
    request_path="/api/v2/earn/savings/product"
    params = {"filter":"all",#筛选条件是否可申购
            # available: 可申购的
            # held: 持有中
            # available_and_held: 申购和持有中
            # all: 查询全部 包含下架的
            "coin":coin#需要查询的代币
            }
    res=client._request_with_params(params=params,request_path=request_path,method="GET")["data"]
    res=[r for r in res if r["periodType"]=="flexible"]#只要活期存款
    # logger.info(f"res,{type(res)},{res}")
    return res
# savingslist=getsavingslist(coin="USDT")
# logger.info(f"savingslist,{savingslist},{type(savingslist)}")
# usdtproductId=str(savingslist[0]["productId"])#取出来产品ID
# logger.info(f"usdtproductId,{usdtproductId},{type(usdtproductId)}")

def postmessage(text):
    BASEURL = 'http://wxpusher.zjiecode.com/api'
    #【查询订阅用户数量】
    pagenum=1
    payload = {
        'appToken': "AT_tFRZgjToc6XnG5dzR2MGyv1DzECNYOIU",
        'page': str(pagenum),
        'pageSize': "50",
    }
    query_user=requests.get(url=f'{BASEURL}/fun/wxuser', params=payload).json()
    # logger.info(f"{query_user}")
    uidslist=[]
    if len(query_user["data"]["records"])>0:
        for query in query_user["data"]["records"]:
            logger.info(query["uid"])
            uidslist.append(query["uid"])
    # logger.info(f"{uidslist}")
    #【推送消息】
    payload = {
        'appToken': "AT_tFRZgjToc6XnG5dzR2MGyv1DzECNYOIU",
        'content': str(text),#文本消息
        'topicIds':["12417"],
        # 'uids': ["UID_qkmjMTBknX0I5ZZoVY3IBFv7WVV1"],#消息单发
        'uids':uidslist,#消息群发
    }
    requests.post(url=f'{BASEURL}/send/message', json=payload).json()

def getsupport(supporttype):
    # ping www.binance.com【服务器上可以ping通】
    # curl -v https://www.binance.com【使用其他工具（如curl）来测试443端口的连接是否正常】
    # dig www.binance.com
    # sudo systemctl restart networking#【重启网络】
    # 如果这个函数产生443的报错是网络问题
    if supporttype=="中文公告":
        #【中文公告】
        headers = {
            "Referer": "https://www.binance.com/zh-CN/support/announcement",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        url = "https://www.binance.com/zh-CN/support/announcement/%E6%95%B0%E5%AD%97%E8%B4%A7%E5%B8%81%E5%8F%8A%E4%BA%A4%E6%98%93%E5%AF%B9%E4%B8%8A%E6%96%B0"
        params = {
            "c": "48",
            "navId": "48",
            "hl": "zh-CN"
        }
        response = requests.get(url, headers=headers, params=params)
        # logger.info(f"{response.text}")
        # logger.info(f"{response}")
    if supporttype=="英文公告":
        #【英文公告】{币安英文区公告的上线时间更早一些尽量监控英文区}
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "if-none-match": "9162285b174342211426813153dc0aa85fbefd8e546fc797bf521f4448b1751d",
            "priority": "u=0, i",
            "referer": "https://www.binance.com/en/support/announcement",
            "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
        }
        cookies = {
            "bnc-uuid": "b67a7acc-47ed-4218-879e-fdae2779500b",
            "_gid": "GA1.2.1876042953.1731499685",
            "BNC_FV_KEY": "3354ae5d7030a20aaf5bb3ead0f2841babadb756",
            "OptanonAlertBoxClosed": "2024-11-13T12:10:52.242Z",
            "g_state": "{\"i_p\":1731639933868,\"i_l\":2}",
            "source": "referral",
            "campaign": "www.binance.com",
            "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%22193256c5b0692c-0918050e89cc2b-4c657b58-1327104-193256c5b0778d%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkzMjU2YzViMDY5MmMtMDkxODA1MGU4OWNjMmItNGM2NTdiNTgtMTMyNzEwNC0xOTMyNTZjNWIwNzc4ZCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%221932924079bb0-07b50fa9790305-4c657b58-1327104-1932924079c9eb%22%7D",
            "_gcl_au": "1.1.1186733074.1731562317",
            "_uetsid": "c7066770a24911efa2ed1f6d6dbdb244",
            "_uetvid": "c706ac10a24911efbfc95740e2ff1dec",
            "lang": "en",
            "userPreferredCurrency": "USD_USD",
            "theme": "dark",
            "BNC_FV_KEY_T": "101-zvJuqP%2B8Z4f11aRI1oV%2BMR%2BAEcCeVnA8ap4rE7WOCgIFDK2Ir%2BQxAJ1rVpK1lYvK1UTVOfwOt2baVv6tpwYbNw%3D%3D-car42ABUE0kkUdLGxVYL5g%3D%3D-02",
            "BNC_FV_KEY_EXPIRE": "1731600316248",
            "OptanonConsent": "isGpcEnabled=0&datestamp=Thu+Nov+14+2024+19%3A48%3A07+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202410.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=f00d6ce7-52d4-4160-aa63-0346e6ab55b5&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1&AwaitingReconsent=false&intType=1&geolocation=KR%3B42",
            "_ga_3WP50LGEEC": "GS1.1.1731584299.5.1.1731585055.43.0.0",
            "_ga": "GA1.2.503363109.1731499685",
            "_gat_UA-162512367-1": "1"
        }
        url = "https://www.binance.com/en/support/announcement/new-cryptocurrency-listing"
        params = {
            "c": "48",
            "navId": "48",
            "hl": "en"
        }
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        # logger.info(f"{response.text}")
        # logger.info(f"{response}")

    soup = BeautifulSoup(response.text,'html.parser')# 使用BeautifulSoup解析响应内容
    content = soup.body# 提取body标签内容下的script
    content = content.find('script', id='__APP_DATA')# 提取<body>标签下的<script>标签
    # logger.info(f"{content}")
    # logger.info(f"{content.text},{type(content.text)}")#取目标标签的值
    supportinfo=json.loads(content.text)['appState']['loader']['dataByRouteId']['d9b2']['catalogs']#['dynamicIds']
    return supportinfo

async def main():
    tradenum=0
    #无论牛市熊市上市币安都是好事：合约上线{英文公告叫做Add}，现货上市{英文公告叫做List}，但是容量不大{4w美金能打出来60%的滑点}
    #香港IP无法访问换成美国或者新加坡的就好，一个IP还有访问次数限制，需要多个ip组合
    while True:
        tradenum+=1
        logger.info(f"当前交易轮次为{tradenum}")

        supportinfo=getsupport(supporttype="英文公告")#这个公告打出来的日志是必须要看的
        # logger.info(f"supportinfo,{supportinfo},{type(supportinfo)}")
        for info in supportinfo:
            logger.info(info['catalogName'])#前面是中文的后面是英文的
            if (info['catalogName']=="数字货币及交易对上新")or(info['catalogName']=="New Cryptocurrency Listing"):
                df=pd.DataFrame(info['articles'])
        # df=df[df["title"].str.contains("上市")
        #       |
        #       df["title"].str.contains("上线")
        #       ]#只要上市信息【中文频道】
        df=df[df["title"].str.contains("Will List")#上市【退市也有提到List XXX with，意思是去掉相关列表，但是开头是Will End】
              |
              df["title"].str.contains("Will Add")#上线
              ]#只要上市信息【英文频道】
        df["releaseDate"]=pd.to_datetime(df['releaseDate'],unit='ms')
        df["releaseDate标准时"]=df["releaseDate"].dt.strftime('%Y-%m-%d %H:%M:%S')#这里是标准时9.30，东八区就是17.30

        logger.info(f"df排序前,{df},{type(df)}")
        df=df.sort_values(by='releaseDate', ascending=True)#releaseDate为datetime形式时，对df根据releaseDate降序排列
        logger.info(f"df排序后,{df},{type(df)}")
        df=df.reset_index(drop=True)#重置索引避免后面越界
        # df=df[df.index==0]#【测试】截取第一行，返回值还是dataframe形式不是字典对象，.iloc截取出来就是对象形式了，.loc不能截取只有一行的情况基本忽略了
        supportdf=df.copy()
        logger.info(f"supportdf,{supportdf},{type(supportdf)}")

        newsnum=0
        #如果没符合要求的公告这里整体都不会执行所以这块不需要验证
        for index in range(0,len(df)):#如果只有一行会不会报错
            thisutc=datetime.datetime.utcnow()
            thisnow=thisutc.strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f"thisnow,{thisnow}")
            thisdf=df.iloc[index]
            logger.info(f"{index},thisdf,{thisdf},{type(thisdf)}")#每一行是index+1
            logger.info(f"第{index}条现货上币公告与当时时间的差值{thisutc-thisdf.releaseDate}")
            if (thisutc-thisdf.releaseDate)<=datetime.timedelta(seconds=
                                                              #【实盘】
                                                              30#【实盘时验证公告发布时间不超过30秒】时间内持续下单{对手盘一档溢价百二}
                                                              
                                                            #   # #【测试】
                                                            #   60*60*24*20+#19天
                                                            #   60*60*0+#21小时
                                                            #   60*10+#30分钟
                                                            #   50#50秒
                                                              ):
                try:
                    newsnum+=1#判断是否有新公告，有新公告就执行下单任务【+=只要有新公告就不为0了】
                    logger.info("目标上市公告刚刚发布")
                    # 正则表达式匹配括号内的内容【识别代币名称】
                    pattern=r'\(([^)]+)\)'
                    matches=re.findall(pattern,thisdf.title)# 使用findall方法查找所有匹配的内容
                    logger.info(f"matches,{matches}")#类型是一个列表，对其中的内容处理之后就能识别出来目标代币了【这里整出来就是字符串列表了】
                    #存储需要发送的消息的内容【避免后面导致内容变更】
                    mes="公告内容："+thisdf.title+"标的名称："+str(matches)+"公告时间（标准时）："+thisdf.releaseDate标准时+"当前时间（标准时）："+thisnow
                    
                    #截取公告里面第一个标的作为买入目标
                    thissymbol=matches[0]
                    logger.info(f"新上市标的为,{thissymbol}")

                    logger.info("近期有新出上市公告赎回活期理财产品买入现货")

                    #【理财资产信息】
                    request_path="/api/v2/earn/savings/assets"
                    params = {"periodType":"flexible",}#只要活期存款
                    savingsList=client._request_with_params(params=params,request_path=request_path,method="GET")["data"]["resultList"]
                    logger.info(savingsList)
                    for savings in savingsList:
                        thisproductId=savings['productId']
                        thisorderId=savings['orderId']
                        thisholdAmount=savings["holdAmount"]
                        logger.info(f"thisproductId,{thisproductId},{type(thisproductId)},thisholdAmount,{thisholdAmount},{type(thisholdAmount)}")
                        #【赎回理财产品】
                        request_path="/api/v2/earn/savings/redeem"
                        params = {"productId":thisproductId,
                                "orderId":thisorderId,
                                "periodType":"flexible",#只要活期存款
                                "amount":thisholdAmount,
                                }
                        res=client._request_with_params(params=params,request_path=request_path,method="POST")
                        res=res["data"]
                        logger.info(f"赎回理财产品,{res}")

                    #【查询现货USDT余额】这里再对比一下最大下单金额
                    spotbalance=getspotbalance(coin="USDT")
                    usdtbalance=[balance for balance in spotbalance if balance["coin"]=="USDT"][0]["available"]
                    logger.info(f"usdtbalance,{usdtbalance},{type(usdtbalance)}")
                    if float(usdtbalance)>0:#只在有余额的情况下交易
                        #【交易精度】
                        params={"symbol":thissymbol+"USDT"}
                        request_path="/api/v2/spot/public/symbols"
                        thisinfo = client._request_with_params(params=params,request_path=request_path,method="GET")["data"]#quantityScale可能是精度
                        logger.info(f"{thisinfo}")
                        minTradeAmount=int(thisinfo[0]["minTradeAmount"])#最小交易数量
                        maxTradeAmount=int(thisinfo[0]["maxTradeAmount"])#最大交易数量
                        quantityPrecision=int(thisinfo[0]["quantityPrecision"])#代币精度
                        pricePrecision=int(thisinfo[0]["pricePrecision"])#价格精度
                        logger.info(f"quantityPrecision,{quantityPrecision},{type(quantityPrecision)},pricePrecision,{pricePrecision},{type(pricePrecision)}")#字符串
                        # {'code': '00000', 'msg': 'success', 'requestTime': 1732951086595, 'data': {'symbol': 'BTCUSDT_SPBL', 'symbolName': 'BTCUSDT', 'symbolDisplayName': 'BTCUSDT', 'baseCoin': 'BTC', 'baseCoinDisplayName': 'BTC', 'quoteCoin': 'USDT', 'quoteCoinDisplayName': 'USDT', 'minTradeAmount': '0', 'maxTradeAmount': '0', 'takerFeeRate': '0.002', 'makerFeeRate': '0.002', 'priceScale': '2', 'quantityScale': '6', 'quotePrecision': '8', 'status': 'online', 'minTradeUSDT': '1', 'buyLimitPriceRatio': '0.05', 'sellLimitPriceRatio': '0.05', 'maxOrderNum': '500'}}
                        
                        #【盘口深度】
                        params={"symbol":str(thissymbol+"USDT"), "limit":'150', "type":'step0'}
                        request_path="/api/v2/spot/market/orderbook"
                        thisdepth = client._request_with_params(params=params,request_path=request_path,method="GET")["data"]#quantityScale可能是精度
                        # logger.info(thisdepth)
                        bid1=thisdepth["bids"][0][0]#买一
                        bid1v=thisdepth["bids"][0][1]
                        ask1=thisdepth["asks"][0][0]#卖一
                        ask1v=thisdepth["asks"][0][1]
                        logger.info(f"""
                            {bid1},{type(bid1)},bid1
                            {bid1v},{type(bid1v)},bid1v
                            {ask1},{type(ask1)},ask1
                            {ask1v},{type(ask1v)},ask1v
                            """
                            )
                        
                        #【计算】buyprice和buyvolume
                        buyprice=round(float(ask1)*(1+0.02),
                                        pricePrecision)#对手盘一档上浮百分之二避免无法成交，之后保留pricePrecision位小数
                        buyvolume=round(math.floor(float(usdtbalance)/buyprice*(10**quantityPrecision))/(10**quantityPrecision),
                                        quantityPrecision)#quantityPrecision代表代币精度
                        logger.info(f"buyprice,{buyprice},buyvolume,{buyvolume}")
                        #目标下单金额跟最大最小下单金额对比
                        if buyvolume>float(maxTradeAmount):
                            buyvolume=round(maxTradeAmount,
                                            quantityPrecision)
                            logger.info("目标下单金额大于最大下单金额")
                        else:
                            logger.info("目标下单金额正常")
                        if buyvolume<float(minTradeAmount):
                            buyvolume=round(minTradeAmount,
                                            quantityPrecision)
                            logger.info("目标下单金额大于最大下单金额")
                        else:
                            logger.info("目标下单金额正常")
                        if buyvolume>0:#有余额才下单的
                            #【现货下单】symbol, quantity, side, orderType, force, price='', clientOrderId=None)
                            params={
                                "symbol":str(thissymbol+"USDT"),#"SBTCSUSDT_SUMCBL"
                                "side":"buy",#方向：PS_BUY现货买入，PS_SELL现货卖出

                                #【限价单】
                                "orderType":"limit",#订单类型"limit"、"market"
                                "price":str(buyprice),#限价价格# 价格小数位、价格步长可以通过获取交易对信息接口获取
                                "size":str(buyvolume),# 委托数量# 对于Limit和Market-Sell订单，此参数表示base coin数量;# 对于Market-Buy订单，此参数表示quote coin数量；
                                
                                #【市价单】判断剧烈行情是否一定能够成交
                                # "orderType":"market",#订单类型"limit"、"market"
                                # "size":str(buyusdt),# 委托数量# 对于Limit和Market-Sell订单，此参数表示base coin数量;# 对于Market-Buy订单，此参数表示quote coin数量；
                                
                                "force":"gtc",#执行策略（orderType为market时无效）# gtc：普通限价单，一直有效直至取消# post_only：只做 maker 订单# fok：全部成交或立即取消# ioc：立即成交并取消剩余
                                # "clientOrderId":str(random_string("Cuongitl"))#自定义订单ID
                                "tpslType":"normal",# normal：普通单（默认值）# tpsl：止盈止损单
                            }
                            request_path="/api/v2/spot/trade/place-order"
                            #最小下单金额为1USDT
                            thisorder = client._request_with_params(params=params,request_path=request_path,method="POST")
                            logger.info(f"{thisorder}")
                except Exception as e:
                    logger.info(e)
                
                

                #【推送准备进行的交易记录】验证了一下没错恰好是在限制的时间内还在推送公告超时之后就不推送了
                res=postmessage(mes)
                logger.info("公告推送",res)
                
        if newsnum==0:
            logger.info("近期无新出上市公告卖出现货申购活期理财产品")
            # 【查询现货非USDT余额】
            spotbalance=getspotbalance(coin="")
            allbalance=[balance for balance in spotbalance if balance["coin"]!="USDT"]
            logger.info(f"allbalance,{allbalance},{type(allbalance)}")
            for balance in allbalance:
                thissymbol=balance["coin"]
                sellvolume=balance["available"]
                thisdf=supportdf[supportdf["title"].str.contains(thissymbol)]#这个截取出来的切片还是dataframe的格式跟之前的截取出来一个对象的情况不一样，取值需要加上[0]
                logger.info(f"thisdf,{thisdf},{type(thisdf)},{str(len(thisdf))},{str(thisdf.empty)}")#如果为空len(thisdf)=0且thisdf.empty为True
                if len(thisdf)>0:#如果整体符合要求的公告为空则这里也是空
                    logger.info("当前有新公告验证时间")
                    thisdf=thisdf[thisdf["releaseDate"]==thisdf["releaseDate"].max()]#取最大的一行【看看只有一行会不会报错】
                    logger.info(f"thisdf保留releaseDate最大的行,{thisdf},{type(thisdf)}")
                    thisdf=thisdf.iloc[0]#这样截取出来就跟上面一样了
                    logger.info(f"thisdf截取第一行后,{thisdf},{type(thisdf)}")
                    thisutc=datetime.datetime.utcnow()
                    thisnow=thisutc.strftime('%Y-%m-%d %H:%M:%S')
                    logger.info(f"thisnow,{thisnow}")
                    logger.info(f"当前持仓标的{thissymbol}最新一条现货上币公告与当时时间的差值{thisutc-thisdf.releaseDate}")
                    if (thisutc-thisdf.releaseDate)<=datetime.timedelta(seconds=
                                                            #【实盘】
                                                            60*60*8#8小时【实盘时进行的验证就是8小时】

                                                            # #   #【测试】
                                                            #   60*60*24*19+#19天
                                                            #   60*60*24+#21小时
                                                            #   60*20+#30分钟
                                                            #   50#50秒
                                                            ):
                        logger.info("该标的上市公告结束不足8小时不执行卖出")
                        continue
                    else:
                        logger.info("该标的上市公告结束较长时间直接卖出")
                else:
                    logger.info("当前没有新公告直接卖出")
            
                #【交易精度】
                params={"symbol":thissymbol+"USDT"}
                request_path="/api/v2/spot/public/symbols"
                thisinfo = client._request_with_params(params=params,request_path=request_path,method="GET")["data"]#quantityScale可能是精度
                logger.info(f"{thisinfo}")
                minTradeAmount=int(thisinfo[0]["minTradeAmount"])#最小交易数量
                maxTradeAmount=int(thisinfo[0]["maxTradeAmount"])#最大交易数量
                quantityPrecision=int(thisinfo[0]["quantityPrecision"])#代币精度
                pricePrecision=int(thisinfo[0]["pricePrecision"])#价格精度
                logger.info(f"quantityPrecision,{quantityPrecision},{type(quantityPrecision)},pricePrecision,{pricePrecision},{type(pricePrecision)}")#字符串
                # {'code': '00000', 'msg': 'success', 'requestTime': 1732951086595, 'data': {'symbol': 'BTCUSDT_SPBL', 'symbolName': 'BTCUSDT', 'symbolDisplayName': 'BTCUSDT', 'baseCoin': 'BTC', 'baseCoinDisplayName': 'BTC', 'quoteCoin': 'USDT', 'quoteCoinDisplayName': 'USDT', 'minTradeAmount': '0', 'maxTradeAmount': '0', 'takerFeeRate': '0.002', 'makerFeeRate': '0.002', 'priceScale': '2', 'quantityScale': '6', 'quotePrecision': '8', 'status': 'online', 'minTradeUSDT': '1', 'buyLimitPriceRatio': '0.05', 'sellLimitPriceRatio': '0.05', 'maxOrderNum': '500'}}
                

                sellvolume=round(math.floor(float(sellvolume)*(10**quantityPrecision))/(10**quantityPrecision),
                                quantityPrecision)#为防止余额不足需要先乘后除再取位数
                logger.info(f"{thissymbol},sellvolume,{sellvolume},{type(sellvolume)}")
                #目标下单金额跟最大最小下单金额对比
                if sellvolume>float(maxTradeAmount):
                    sellvolume=round(maxTradeAmount,
                                    quantityPrecision)
                    logger.info("目标下单金额大于最大下单金额")
                else:
                    logger.info("目标下单金额正常")
                if sellvolume<float(minTradeAmount):
                    sellvolume=round(minTradeAmount,
                                    quantityPrecision)
                    logger.info("目标下单金额大于最大下单金额")
                else:
                    logger.info("目标下单金额正常")

                # 【盘口深度】
                params={"symbol":str(thissymbol+"USDT"), "limit":'150', "type":'step0'}
                request_path="/api/v2/spot/market/orderbook"
                thisdepth = client._request_with_params(params=params,request_path=request_path,method="GET")["data"]#quantityScale可能是精度
                # logger.info(thisdepth)
                bid1=thisdepth["bids"][0][0]#买一
                bid1v=thisdepth["bids"][0][1]
                ask1=thisdepth["asks"][0][0]#卖一
                ask1v=thisdepth["asks"][0][1]
                logger.info(f"""
                    {bid1},{type(bid1)},bid1
                    {bid1v},{type(bid1v)},bid1v
                    {ask1},{type(ask1)},ask1
                    {ask1v},{type(ask1v)},ask1v
                    """
                    )
                
                sellprice=round(float(ask1),pricePrecision)#卖的时候不急了在自己这边挂卖单就行
                logger.info(f"sellvolume,{sellvolume}")
                if sellvolume>0:#有余额才下单的
                    #【现货下单】symbol, quantity, side, orderType, force, price='', clientOrderId=None)
                    params={
                        "symbol":str(thissymbol+"USDT"),#"SBTCSUSDT_SUMCBL"
                        "side":"sell",#方向：PS_BUY现货买入，PS_SELL现货卖出

                        #【限价单】
                        "orderType":"limit",#订单类型"limit"、"market"
                        "price":str(sellprice),#限价价格# 价格小数位、价格步长可以通过获取交易对信息接口获取
                        "size":str(sellvolume),# 委托数量# 对于Limit和Market-Sell订单，此参数表示base coin数量;# 对于Market-Buy订单，此参数表示quote coin数量；
                        
                        #【市价单】判断剧烈行情是否一定能够成交
                        # "orderType":"market",#订单类型"limit"、"market"
                        # "size":str(buyusdt),# 委托数量# 对于Limit和Market-Sell订单，此参数表示base coin数量;# 对于Market-Buy订单，此参数表示quote coin数量；
                        
                        "force":"gtc",#执行策略（orderType为market时无效）# gtc：普通限价单，一直有效直至取消# post_only：只做 maker 订单# fok：全部成交或立即取消# ioc：立即成交并取消剩余
                        # "clientOrderId":str(random_string("Cuongitl"))#自定义订单ID
                        "tpslType":"normal",# normal：普通单（默认值）# tpsl：止盈止损单
                    }
                    request_path="/api/v2/spot/trade/place-order"
                    #最小下单金额为1USDT
                    thisorder = client._request_with_params(params=params,request_path=request_path,method="POST")
                    logger.info(f"{thisorder}")

            #【查询现货余额】前面卖出之后大概一秒钟左右就转走了
            spotbalance=getspotbalance(coin="USDT")
            usdtbalance=[balance for balance in spotbalance if balance["coin"]=="USDT"][0]["available"]
            logger.info(f"{usdtbalance},{type(usdtbalance)}")
            if float(usdtbalance)>=1:#现货资产余额大于等于1的时候进行活期理财申购{避免余额不足报错}【验证后是对的，usdtbalance="0"时usdtbalance="0"验证为False】
                logger.info("余额大于1USDT执行理财申购")
                #【获取理财产品列表】
                savingslist=getsavingslist(coin="USDT")
                logger.info(f"{savingslist},{type(savingslist)}")
                usdtproductId=str(savingslist[0]["productId"])#取出来产品ID
                logger.info(f"{usdtproductId},{type(usdtproductId)}")
                #【申购理财产品】
                request_path="/api/v2/earn/savings/subscribe"
                params = {"productId":usdtproductId,
                        "periodType":"flexible",#只要活期存款
                        "amount":usdtbalance
                        }
                res=client._request_with_params(params=params,request_path=request_path,method="POST")
                res=res["data"]
                logger.info(f"申购理财产品,{res}")
            else:
                logger.info(f"余额不足不进行申购")

        #【休息3秒】会不会因为休息时间短速度过快限制IP
        time.sleep(3)
        #【下单3秒不成交就执行超时撤单】
        thistime=datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        logger.info(f"thistime,{thistime}")
        # #【获取全部订单】
        # params={}
        # request_path="/api/v2/spot/trade/history-orders"
        # all_orders = client._request_with_params(params=params,request_path=request_path,method="GET")["data"]
        # logger.info(f"all_orders,{all_orders}")
        #【获取未成交订单】
        params={}
        request_path="/api/v2/spot/trade/unfilled-orders"
        open_orders = client._request_with_params(params=params,request_path=request_path,method="GET")["data"]
        logger.info(f"open_orders,{open_orders}")
        for thisorder in open_orders:
            logger.info(f"{thisorder}")
            thissymbol=thisorder["symbol"]
            thisorderId=thisorder["orderId"]
            ctime=thisorder["cTime"]#1732973006752创建时间
            utime=thisorder["uTime"]#1732973006818更新时间
            logger.info(f"ctime,{ctime},{type(ctime)}")
            thisdt = datetime.datetime.fromtimestamp(int(ctime)//1000, tz=datetime.timezone.utc)
            logger.info(f"{thisdt}")
            logger.info(f"{thistime-thisdt}")
            if thistime-thisdt>=datetime.timedelta(seconds=3):
                logger.info("该订单挂起超时执行撤单")
                #【现货撤单】
                params={"symbol":thissymbol,
                        "orderId":thisorderId,
                        }
                request_path="/api/v2/spot/trade/cancel-order"
                cance_order = client._request_with_params(params=params,request_path=request_path,method="POST")
                logger.info(f"cance_order,{cance_order}")#撤单成功


# 【github action能够最大程度避免IP报错】main这个异步函数的作用是处理公告监控问题
if __name__ == '__main__':
    # 运行主函数【使用异步可以规避github action的时间限制问题】
    asyncio.run(main())
