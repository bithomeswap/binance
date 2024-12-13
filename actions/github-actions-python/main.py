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

# #【安装binance】这种方式不能从美国IP获取数据
# # pip install python-binance
# from binance.client import Client as BinanceClient
# # 币安的api配置
# api_key = "0jmNVvNZusoXKGkwnGLBghPh8Kmc0klh096VxNS9kn8P0nkAEslVUlsuOcRoGrtm"
# api_secret = "PbSWkno1meUckhmkLyz8jQ2RRG7KgmZyAWhIF0qPdCJrmDSFxoxGdMG5gZeYYCgy"
# binanceclient = BinanceClient(api_key, api_secret)# 创建Binance客户端
# # binanceclient = BinanceClient()# 创建Binance客户端【在公共数据上不限制IP也不需要添加密钥】

# pip install python-bitget
# 【参考文档】https://bitgetlimited.github.io/apidoc/en/mix/#get-account-list
from pybitget import Client
from pybitget.utils import *
from pybitget.enums import *
# from pybitget import logger

# logger.add(
#     sink=f"log.log",#sink:创建日志文件的路径。
#     level="INFO",#level:记录日志的等级,低于这个等级的日志不会被记录。等级顺序为 debug < info < warning < error。设置 INFO 会让 logger.debug 的输出信息不被写入磁盘。
#     rotation="00:00",#rotation:轮换策略,此处代表每天凌晨创建新的日志文件进行日志 IO；也可以通过设置 "2 MB" 来指定 日志文件达到 2 MB 时进行轮换。   
#     retention="7 days",#retention:只保留 7 天。 
#     encoding="utf-8",#encoding:编码方式
#     enqueue=True,#enqueue:队列 IO 模式,此模式下日志 IO 不会影响 python 主进程,建议开启。
#     format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"#format:定义日志字符串的样式,这个应该都能看懂。
# )

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
    # print(f"res,{type(res)},{res}")
    return res
# spotbalance=getspotbalance(coin="USDT")
# usdtbalance=[balance for balance in spotbalance if balance["coin"]=="USDT"][0]["available"]
# print(f"usdtbalance,{usdtbalance},{type(usdtbalance)}")

#【获取理财产品列表】这里只要活期存款
def getsavingslist(coin):#10次/1s (Uid)
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
    # print(f"res,{type(res)},{res}")
    return res
# savingslist=getsavingslist(coin="USDT")#10次/1s (Uid)
# print(f"savingslist,{savingslist},{type(savingslist)}")
# usdtproductId=str(savingslist[0]["productId"])#取出来产品ID
# print(f"usdtproductId,{usdtproductId},{type(usdtproductId)}")

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
    # print(f"{query_user}")
    uidslist=[]
    if len(query_user["data"]["records"])>0:
        for query in query_user["data"]["records"]:
            print(query["uid"])
            uidslist.append(query["uid"])
    # print(f"{uidslist}")
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
        # print(f"{response.text}")
        # print(f"{response}")
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
        # print(f"{response.text}")
        # print(f"{response}")

    soup = BeautifulSoup(response.text,'html.parser')# 使用BeautifulSoup解析响应内容
    content = soup.body# 提取body标签内容下的script
    #【一秒一次的时候这里容易抓到空值】
    content = content.find('script', id='__APP_DATA')# 提取<body>标签下的<script>标签
    # print(f"{content}")
    # print(f"{content.text},{type(content.text)}")#取目标标签的值
    supportinfo=json.loads(content.text)['appState']['loader']['dataByRouteId']
    return supportinfo

async def main():#bitget交易所的频率限制一般是每秒10次/（IP）、20次/（UID）
    tradenum=0
    #无论牛市熊市上市币安都是好事：合约上线{英文公告叫做Add}，现货上市{英文公告叫做List}，但是容量不大{4w美金能打出来60%的滑点}
    #香港IP无法访问换成美国或者新加坡的就好，一个IP还有访问次数限制，需要多个ip组合
    while True:#每一轮任务执行时间比较短主要耗时在time.sleep上了
        #【使用tru、except模式之后代码即便报错也不会导致进程终止】
        #【多个进程任务同时监控进行交易的情况下一个任务失败了但是没有导致订单错乱，理财申购上其他任务前后脚下出去了但是直接返回下单失败而没有报错】
        #【while true下下了几百笔金额溢出的失败订单，并没有导致其他模块受限说明频率限制可能不是一个字段超频就会导致整个账户或者IP无法使用】
        tradenum+=1
        print(f"当前交易轮次为{tradenum}")



        #【第3部分】没新出的公告就卖出闲置资产同时存理财账户【需要加一个卖出失败的报错处理避免直接停止任务】
        try:
            # 【公告出来的时候这里直接没数据了】
            supportinfo=getsupport(supporttype="英文公告")#这个公告打出来的日志是必须要看的
            print(f"supportinfo,{supportinfo},{type(supportinfo)}")
            # #需要查询latestArticles字段才代表的新公告{只在新币上线后才出现}，之前查询的articles字段其实是全部的历史公告{滞后一分钟左右}
            # supportinfo={'e084': {}, 'd34e': {'ssrUserIsLoggedIn': False, 'catalogDetail': {'catalogId': 48, 'parentCatalogId': None, 'icon': 'https://public.bnbstatic.com/image/cms/content/body/202202/9252ba30f961b1a20d49e622a0ecfad5.png', 'catalogName': 'New Cryptocurrency Listing', 'description': None, 'catalogType': 1, 'total': 1609, 'articles': [{'id': 219513, 'code': '5cbdc8e506644364a281d614a19afbb6', 'title': 'Binance Will Add Movement (MOVE) on Earn, Buy Crypto, Convert, Margin & Futures', 'type': 1, 'releaseDate': 1733746147487}, {'id': 219510, 'code': '601c0c23d12e40ee80310ac5e7c6369e', 'title': 'Movement (MOVE) Listing Will Be Advanced', 'type': 1, 'releaseDate': 1733744707679}, {'id': 219471, 'code': '8a585286abc547d293e269beeb6b9bf3', 'title': 'Introducing Movement (MOVE) on Binance HODLer Airdrops! Subscribe your BNB to Simple Earn', 'type': 1, 'releaseDate': 1733732956897}, {'id': 219327, 'code': 'bb1e28bf562341cfbd67791081533fa0', 'title': 'Binance Will Add Across Protocol (ACX) and Orca (ORCA) on Earn, Buy Crypto, Convert, Margin & Futures', 'type': 1, 'releaseDate': 1733488747249}, {'id': 219276, 'code': 'b8b988973b88493192f2e43ba26da331', 'title': 'Binance Will List Across Protocol (ACX) and Orca (ORCA) with Seed Tag Applied', 'type': 1, 'releaseDate': 1733474058953}, {'id': 219122, 'code': 'aa40cb409c5444068432164c3c916f3a', 'title': 'Notice on New Trading Pairs & Trading Bots Services on Binance Spot - 2024-12-06', 'type': 1, 'releaseDate': 1733385601771}, {'id': 219071, 'code': 'beac1e0a0edf4fe69d5e5c45f9d60343', 'title': 'Binance Futures Will Launch USDⓈ-Margined KAIAUSDT and AEROUSDT Perpetual Contracts With up to 75x Leverage', 'type': 1, 'releaseDate': 1733313823583}, {'id': 218928, 'code': '6be3b4cf73684f4a89be236abb0fe61f', 'title': 'Notice on New Trading Pairs & Trading Bots Services on Binance Spot - 2024-12-04', 'type': 1, 'releaseDate': 1733212803588}, {'id': 218915, 'code': 'c04318cda6bc4fa6865235f1dfa77dba', 'title': 'Binance Futures Copy Trading Adds New USDⓈ-M Perpetual Contracts (2024-12-03)', 'type': 1, 'releaseDate': 1733211012825}, {'id': 218471, 'code': '7700345477ea4c0fb89b1ddce0d28979', 'title': 'Binance Futures Will Launch USDⓈ-Margined MORPHOUSDT and CHILLGUYUSDT Perpetual Contracts With up to 75x Leverage', 'type': 1, 'releaseDate': 1732710701624}, {'id': 218444, 'code': 'e5a9c33ac55043808e202dde68774ac2', 'title': 'Binance Will Add Thena (THE) on Earn, Buy Crypto, Convert, Margin & Futures', 'type': 1, 'releaseDate': 1732699831890}, {'id': 218416, 'code': '87748909170b4c0bada2aeac2447aa70', 'title': 'Notice on New Trading Pairs and Trading Bots Services on Binance Spot - 2024-11-28 and 2024-11-29', 'type': 1, 'releaseDate': 1732694432674}, {'id': 218294, 'code': '7c06e61804694408b3401e0a380f954f', 'title': 'Introducing Thena (THE) on Binance HODLer Airdrops! Subscribe your BNB to Simple Earn', 'type': 1, 'releaseDate': 1732607852153}, {'id': 218188, 'code': '3dd2c1e3f5f040ac9f7a94c6597ef842', 'title': 'Binance Futures Will Launch USDⓈ-Margined 1000WHYUSDT and 1000CHEEMSUSDT Perpetual Contracts With up to 75x Leverage', 'type': 1, 'releaseDate': 1732527302268}, {'id': 218165, 'code': '02067834ba564042aa7e5f0d30eb2731', 'title': 'Binance Options Will Launch BNBUSDT and SOLUSDT Monthly Options', 'type': 1, 'releaseDate': 1732510801511}, {'id': 218065, 'code': 'cb5e509a881640938eaa1eca26b4b413', 'title': 'Binance Margin Adds New USDC Pairs - 2024-11-25', 'type': 1, 'releaseDate': 1732501821187}, {'id': 217985, 'code': 'c214b24b9f004196aa12fb1e6736572b', 'title': 'Binance Futures Will Launch USDⓈ-Margined SLERFUSDT and SCRTUSDT Perpetual Contracts With up to 75x Leverage', 'type': 1, 'releaseDate': 1732181402071}, {'id': 217887, 'code': '72ba79e3212848bcb6aba53eb6e55d4c', 'title': 'Notice on New Trading Pairs & Trading Bots Services on Binance Spot - 2024-11-22', 'type': 1, 'releaseDate': 1732096809305}, {'id': 217727, 'code': '67e7da69b8e541c1bfacac7f43f75d78', 'title': 'Notice on New Trading Pairs & Trading Bots Services on Binance Spot - 2024-11-20', 'type': 1, 'releaseDate': 1732006802967}, {'id': 217630, 'code': 'f6577bdd30d542e0af4f76a14dfeb241', 'title': 'Binance Futures Will Launch USDⓈ-Margined BANUSDT and AKTUSDT Perpetual Contracts With up to 75x Leverage', 'type': 1, 'releaseDate': 1731922212272}, {'id': 217573, 'code': '8061c9b481244c88be73a68980db5761', 'title': 'Binance Margin Adds New USDC Pairs - 2024-11-18', 'type': 1, 'releaseDate': 1731906001533}, {'id': 217499, 'code': 'e25f171ca86342e9b7c160cc1697a090', 'title': 'Binance Futures Will Launch USDⓈ-Margined DEGENUSDT Perpetual Contract With up to 75x Leverage', 'type': 1, 'releaseDate': 1731663013144}, {'id': 217413, 'code': 'b50b0a2d80024a8b8765af2eb8560cd0', 'title': 'Notice on New Trading Pairs & Trading Bots Services on Binance Spot - 2024-11-15', 'type': 1, 'releaseDate': 1731574815563}, {'id': 217379, 'code': '7c4bf0dac2de4842984fc7c066204b05', 'title': 'Introducing Usual (USUAL) on Binance Launchpool and Pre-Market!', 'type': 1, 'releaseDate': 1731569529354}, {'id': 217261, 'code': '220339ba12bd451c8362ad8501ea87e9', 'title': 'Binance Futures Will Launch USDⓈ-Margined HIPPOUSDT and 1000XUSDT Perpetual Contract With up to 75x Leverage', 'type': 1, 'releaseDate': 1731493800839}, {'id': 217145, 'code': '59687cb3396e469cb602d286e8d74088', 'title': 'Notice on New Trading Pairs & Trading Bots Services on Binance Spot - 2024-11-13', 'type': 1, 'releaseDate': 1731402006478}, {'id': 217041, 'code': 'f689ebe21cdb4eda91bd0071de48e6f8', 'title': 'Binance Will Add Act I : The AI Prophecy (ACT) and Peanut the Squirrel (PNUT) on Earn, Buy Crypto, Convert, Margin & Futures', 'type': 1, 'releaseDate': 1731317423797}, {'id': 216994, 'code': 'd16d96c136154680a6373225d592bca1', 'title': 'Binance Will List Act I : The AI Prophecy (ACT) and Peanut the Squirrel (PNUT) with Seed Tag Applied', 'type': 1, 'releaseDate': 1731303569462}, {'id': 216852, 'code': '8f3b03e494c94360b9985edc5402fbac', 'title': 'Binance Futures Will Launch USDⓈ-Margined GRASSUSDT, DRIFTUSDT, and SWELLUSDT Perpetual Contracts With up to 75x Leverage', 'type': 1, 'releaseDate': 1731074582460}, {'id': 216744, 'code': '209355888f0042f788899dd1a04a0052', 'title': 'Binance Futures Will Launch USDⓈ-Margined 1000000MOGUSDT Perpetual Contract With up to 75x Leverage', 'type': 1, 'releaseDate': 1730975333236}, {'id': 216599, 'code': 'd19f7ec8ab8349fba6fd3749a80e07c9', 'title': 'Binance Will Add Cow Protocol (COW) and Cetus Protocol (CETUS) on Earn, Buy Crypto, Convert, Margin & Futures', 'type': 1, 'releaseDate': 1730892607366}, {'id': 216473, 'code': '2faa229be2ba4b758bbeb1859f63ba36', 'title': 'Binance Will List Cow Protocol (COW) and Cetus Protocol (CETUS) with Seed Tag Applied', 'type': 1, 'releaseDate': 1730869807602}, {'id': 216417, 'code': '2f31d829c9154042888b906d8b04f004', 'title': 'Binance Futures Copy Trading Adds New USDⓈ-M Perpetual Contracts (2024-11-05)', 'type': 1, 'releaseDate': 1730790010168}, {'id': 216392, 'code': 'a55d38732b34452ab9f78ac8832af59c', 'title': 'Binance Futures Will Launch USDⓈ-Margined PONKEUSDT Perpetual Contract With up to 75x Leverage', 'type': 1, 'releaseDate': 1730716223083}, {'id': 216263, 'code': 'bab086aed6a2414a8de85e45b6f54714', 'title': 'Binance Futures Will Launch USDⓈ-Margined TROYUSDT Perpetual Contract With up to 75x Leverage', 'type': 1, 'releaseDate': 1730372403363}, {'id': 216184, 'code': 'd898f94ad35b478a8f60e12025c8ea2b', 'title': 'Binance Will Add Kaia (KAIA) on Earn, Buy Crypto, Convert, and Margin', 'type': 1, 'releaseDate': 1730359816080}, {'id': 215934, 'code': '1956ee23ec9f49eab2323a33852caf3b', 'title': 'Binance Futures Copy Trading Adds New USDⓈ-M Perpetual Contracts (2024-10-29)', 'type': 1, 'releaseDate': 1730167208125}, {'id': 215898, 'code': 'dbd05b4f89ae4974912d790eba516b4c', 'title': 'Binance Futures Will Launch USDⓈ-Margined SANTOSUSDT Perpetual Contract With up to 75x Leverage', 'type': 1, 'releaseDate': 1730116800976}, {'id': 215763, 'code': '7b091f5c38324434a9bdd252e4788442', 'title': 'Binance Futures Will Launch USDⓈ-Margined SAFEUSDT Perpetual Contract With up to 75x Leverage', 'type': 1, 'releaseDate': 1729852200674}, {'id': 215707, 'code': '5e93f7cd3f9a47e194085f969ac57b85', 'title': 'Binance Futures Will Launch USDⓈ-Margined MOODENGUSDT Perpetual Contract With up to 75x Leverage', 'type': 1, 'releaseDate': 1729843231189}, {'id': 215677, 'code': 'ff1a4c64f1aa4fef870adc7ef802d700', 'title': 'Binance Futures Will Launch USDⓈ-Margined GOATUSDT Perpetual Contract With up to 75x Leverage', 'type': 1, 'releaseDate': 1729769672095}, {'id': 215222, 'code': '4e1e3eda477349068ecec191a7b16c5b', 'title': 'Binance Will Add Scroll (SCR) on Earn, Buy Crypto, Convert, Margin & Futures', 'type': 1, 'releaseDate': 1729585806416}, {'id': 215164, 'code': 'ed43b9b4d8f8471087b6d200bffcb4ff', 'title': 'Binance Futures Will Launch USDⓈ-Margined 1000CATUSDT Perpetual Contract With up to 75x Leverage', 'type': 1, 'releaseDate': 1729506638455}, {'id': 214941, 'code': 'a6d2ae0b765c4bb79b192f3904fc5757', 'title': 'Binance Will Add Lumia (LUMIA) on Earn, Buy Crypto, Convert & Margin', 'type': 1, 'releaseDate': 1729240205707}, {'id': 214915, 'code': '31020fc6cfab4ff18867a0dc3c33e52f', 'title': 'Binance Has Added Binance Staked SOL (BNSOL) on Auto-Invest, Buy Crypto & Loans', 'type': 1, 'releaseDate': 1729238405403}, {'id': 214841, 'code': '765ca1b5b58848fd88c9ee3684b91201', 'title': 'Binance Will End the Scroll (SCR) Pre-Market and List Scroll (SCR) with Seed Tag Applied', 'type': 1, 'releaseDate': 1729214529998}, {'id': 214749, 'code': 'b1e67c2d4e8e4807a5592ccd6c559155', 'title': 'Notice on New Trading Pairs & Trading Bots Services on Binance Spot and Margin - 2024-10-17', 'type': 1, 'releaseDate': 1729062001941}, {'id': 214550, 'code': '60c0525da44448f9907322f23098c045', 'title': 'Notice on New Trading Pairs & Trading Bots Services on Binance Spot - 2024-10-16', 'type': 1, 'releaseDate': 1728979209984}, {'id': 214361, 'code': 'f6d2a85234594827b9e078bfed5e72c3', 'title': 'Binance Will Add Binance Staked SOL (BNSOL) on Earn, Convert & Margin', 'type': 1, 'releaseDate': 1728545405645}, {'id': 214289, 'code': '56398cfbd9c4419d9c0b54a0d1da2a7b', 'title': 'Binance Will List Binance Staked SOL (BNSOL) and Introduce BNSOL Boosted APR Promotion', 'type': 1, 'releaseDate': 1728457213876}], 'catalogs': []}, 'articleDetail': None, 
            #                                   'latestArticles': [{'id': 219677, 'code': 'd4f72bdd82d44a0591ee40d41f0b44d5', 'title': 'Binance Will List Magic Eden (ME) with Seed Tag Applied', 'imageLink': None, 'shortLink': None, 'body': None, 'type': 1, 'catalogId': 48, 'catalogName': 'New Cryptocurrency Listing', 'publishDate': 1733815340546, 'footer': None}, {'id': 219593, 'code': '41bd87af5772450f948181eb4b9504fb', 'title': 'Binance Pool Supports Luckycoin (LKY) Merged Mining with Zero Fees', 'imageLink': None, 'shortLink': None, 'body': None, 'type': 1, 'catalogId': 49, 'catalogName': 'Latest Binance News', 'publishDate': 1733810401571, 'footer': None}, {'id': 219623, 'code': '6cd13a9337404a1caa1bb55ac9175d2a', 'title': 'Binance Will Support the Sei (SEI) Network Upgrade', 'imageLink': None, 'shortLink': None, 'body': None, 'type': 1, 'catalogId': 157, 'catalogName': 'Wallet Maintenance Updates', 'publishDate': 1733803202721, 'footer': None}, {'id': 219596, 'code': '4ee88af1c2ab4cec9b5f66d0a57a6147', 'title': 'Binance Upgrades Binance Loans (Flexible Rate) (2024-12-10)', 'imageLink': None, 'shortLink': None, 'body': None, 'type': 1, 'catalogId': 49, 'catalogName': 'Latest Binance News', 'publishDate': 1733799602853, 'footer': None}, {'id': 219569, 'code': '064513c6458f42bcb99b2779cc031284', 'title': "Binance x CR7 'ForeverSkills' Digital Collectibles Are Now Available", 'imageLink': None, 'shortLink': None, 'body': None, 'type': 1, 'catalogId': 49, 'catalogName': 'Latest Binance News', 'publishDate': 1733792401775, 'footer': None}], 'relatedArticles': [], 'hotArticles': [], 'catalogs': [], 'lastCategory': {}, 'coinPairs': [], 'coinPriceVisible': False, 'needEnForDefault': False}}
            # print("latestArticles",supportinfo['d34e']["latestArticles"])
            # 【使用递归函数直接查询articles字段的值】避免binance变更公告路径
            def find_data(data):
                target="latestArticles"#设置需要监控的字段
                if isinstance(data, dict):
                    if target in data:#当字段在当前元素下
                        yield data[target]#返回对象的目标字段
                    for value in data.values():
                        yield from find_data(value)#继续遍历
                elif isinstance(data, list):
                    for item in data:
                        yield from find_data(item)
            articles = list(find_data(data=supportinfo))
            print("articles",articles)
            df=pd.DataFrame({})
            for article in articles:#目前这个格式无论是深一层只有一层的字典还是多层字典都可以成功转换了
                print("article",article)
                try:
                    df=pd.concat([df,pd.DataFrame(article)])
                    print("当前公告有很多行直接拼接")
                except Exception as e:
                    df=pd.concat([df,pd.DataFrame([article])])
                    print("当前公告只有一行需要特殊处理")
            print("全部公告",df)
            # df.to_csv("df.csv")

            # # 【中文公告筛选】
            # df=df[df["title"].str.contains("上市")
            #     #   |
            #     #   df["title"].str.contains("上线")#上线【效果不好容易亏损】实盘的时候记得注销
            #       ]#只要上市信息【中文频道】
            # #【英文公告筛选】一般就是will list公告发布比较早且普遍都是有价值的标的
            df=df[df["title"].str.contains("Will List")#上市【退市也有提到List XXX with，意思是去掉相关列表，但是下架的英文开头是Will End】
                |
                df["title"].str.contains("Will Add")#上线【效果不好容易亏损】实盘的时候记得注销
                ]#只要上市信息【英文频道】
            
            #【正则表达式匹配代币名称】1个币2个币都是返回一个列表
            pattern=r'\(([^)]+)\)'#正则表达式【用来从公告中过滤目标代币】
            df["token"]=df["title"].apply(lambda x:re.findall(pattern,x))#使用findall方法查找所有匹配的内容

            #【同一个代币只要最开始上线的那一次才有利润】当前公告是推送时间publishDate，历史公告是存储时间releaseDate
            df["timestampdatetime"]=pd.to_datetime(df['publishDate'],unit='ms')#转datetime格式
            df["timestampdatetime标准时"]=df["timestampdatetime"].dt.strftime('%Y-%m-%d %H:%M:%S')#这里是标准时9.30，东八区就是17.30
            
            #【对token列值相同的数据只保留timestampdatetime列值最小的行】
            # df.to_csv('df过滤前.csv')
            df=df.explode('token')#把一行公告拆分成多行方便选中和下单
            # df.to_csv('df过滤中.csv')
            df=df.groupby('token', as_index=False).apply(lambda x: x.nsmallest(1,'timestampdatetime'))
            print(f"对关联代币进行去重后{df}")

            #【根据时间降序排列】
            print(f"目标公告排序前,{df},{type(df)}")
            df=df.sort_values(by='timestampdatetime',ascending=False)#timestampdatetime为datetime形式时进行排序，ascending=True是升序排列，ascending=False是降序排列，本身就是降序，暂时没问题的
            print(f"目标公告排序后,{df},{type(df)}")
            #【重置索引避免后面越界】
            df=df.reset_index(drop=True)
            supportdf=df.copy()

            # supportdf.to_csv('supportdf.csv')#【存储supportdf】
            # supportdf=supportdf[supportdf.index==0]#【测试】截取第一行，返回值是dataframe{.iloc截取出来是字典对象格式了，.loc不能截取只有一行的数据}
            print(f"supportdf,{supportdf},{type(supportdf)}")
        except Exception as e:
            print(f"公告获取报错,{e}")



        newsnum=0#【可能try\except也是比较耗时的代码】去掉之后速度明显提高
        #如果没符合要求的公告这里整体都不会执行所以这块不需要验证
        for index in range(0,len(df)):#如果只有一行会不会报错
            try:
                #【数据截取】
                thisdf=df.iloc[index]
                print(f"{index},thisdf,{thisdf},{type(thisdf)}")#每一行是index+1
                print('thisdf["token"]',thisdf["token"],type(thisdf["token"]))#无论几个币类型都是列表
                # thissymbol=thisdf["token"]
                # print(f"新上市标的为,{thissymbol},{type(thissymbol)}")

                #【获取当前时间】
                thisutc=datetime.datetime.utcnow()
                thisnow=thisutc.strftime('%Y-%m-%d %H:%M:%S')
                print(f"thisnow,{thisnow}")
                print(f"第{index}条现货上币公告与当时时间的差值{thisutc-thisdf.timestampdatetime}")
                if (thisutc-thisdf.timestampdatetime)<=datetime.timedelta(seconds=
                                                                # #【实盘】
                                                                # 60#【实际上真正抓到公告跟公告发布时间的差值大概30秒，所以验证是否交易可以多等一会儿】时间内持续下单{对手盘一档溢价百二}
                                                                #【测试】
                                                                60*60*24*20+#19天
                                                                60*60*0+#21小时
                                                                60*10+#30分钟
                                                                50#50秒
                                                                ):
                    newsnum+=1#判断是否有新公告，有新公告就执行下单任务【+=只要有新公告就不为0了】
                    print("目标上市公告刚刚发布")

                    # #【VELODROME】这个标的在当前的bitget上找不到这个简称，它的简称是VELO，完全没有信息能够将两者联系在一起
                    # request_path="/api/v2/spot/public/coins"
                    # params={}
                    # thistoken = client._request_with_params(params=params,request_path=request_path,method="GET")["data"]#quantityScale可能是精度
                    # # print("thistoken",thistoken,len(thistoken))
                    # # pd.DataFrame(thistoken).to_csv("thistoken.csv")

                    thissymbol=thisdf["token"]#这里可能binance公告的简称和bitget的交易对简称对不上导致无法买入
                    print(f"新上市标的为,{thissymbol}")

                    #【通过小时K线验证上市时间是否比币安公告时间早】时间验证K线时长超过8小时
                    params={"symbol":str(thissymbol+"USDT"),
                        "granularity":"1h",
                        # "granularity":"1M",#【测试】
                        }
                    request_path="/api/v2/spot/market/candles"
                    thiskline = client._request_with_params(params=params,request_path=request_path,method="GET")["data"]#quantityScale可能是精度
                    print("thiskline",thiskline,len(thiskline))
                    if len(thiskline)>=8:
                        print("binance新上市币种在bitget已经上市超过8小时值得买入")
                        #存储需要发送的消息的内容【避免后面导致内容变更】
                        mes="公告内容："+thisdf.title+"标的列表："+str(thissymbol)+"公告时间（标准时）："+thisdf.timestampdatetime标准时+"当前时间（标准时）："+thisnow
                        try:
                            print("近期有新出上市公告赎回活期理财产品买入现货")
                            #【理财资产信息】10次/1s (Uid)查询活期存款持仓对其进行赎回
                            request_path="/api/v2/earn/savings/assets"
                            params = {"periodType":"flexible",}#只要活期存款
                            savingsList=client._request_with_params(params=params,request_path=request_path,method="GET")["data"]["resultList"]
                            print(savingsList)
                            for savings in savingsList:
                                thisproductId=savings['productId']
                                thisorderId=savings['orderId']
                                thisholdAmount=savings["holdAmount"]
                                print(f"thisproductId,{thisproductId},{type(thisproductId)},thisholdAmount,{thisholdAmount},{type(thisholdAmount)}")
                                #【赎回理财产品】10次/1s (Uid)
                                request_path="/api/v2/earn/savings/redeem"
                                params = {"productId":thisproductId,
                                        "orderId":thisorderId,
                                        "periodType":"flexible",#只要活期存款
                                        "amount":thisholdAmount,
                                        }
                                res=client._request_with_params(params=params,request_path=request_path,method="POST")
                                res=res["data"]
                                print(f"赎回理财产品,{res}")
                            #【查询现货USDT余额】对赎回后的USDT余额进行统计方便后面计算下单金额
                            spotbalance=getspotbalance(coin="USDT")
                            usdtbalance=[balance for balance in spotbalance if balance["coin"]=="USDT"][0]["available"]
                            print(f"usdtbalance,{usdtbalance},{type(usdtbalance)}")
                        except Exception as e:
                            print(f"{thissymbol}理财赎回报错{e}")
                        try:
                            if float(usdtbalance)>0:#只在有余额的情况下交易
                                tradeusdt=float(usdtbalance)
                                maxusdtbalance=20000#设置单次打新最大的单笔下单金额【余额过多则分多次下单】
                                if float(usdtbalance)>maxusdtbalance:
                                    print(f"USDT余额大于{maxusdtbalance}重置下单金额为{maxusdtbalance}")
                                    tradeusdt=float(maxusdtbalance)
                                #【交易精度】#20次/1s (IP)
                                params={"symbol":thissymbol+"USDT"}
                                request_path="/api/v2/spot/public/symbols"
                                thisinfo = client._request_with_params(params=params,request_path=request_path,method="GET")["data"]#quantityScale可能是精度
                                print(f"{thisinfo}")
                                minTradeAmount=int(thisinfo[0]["minTradeAmount"])#最小交易数量
                                maxTradeAmount=int(thisinfo[0]["maxTradeAmount"])#最大交易数量
                                quantityPrecision=int(thisinfo[0]["quantityPrecision"])#代币精度
                                pricePrecision=int(thisinfo[0]["pricePrecision"])#价格精度
                                print(f"quantityPrecision,{quantityPrecision},{type(quantityPrecision)},pricePrecision,{pricePrecision},{type(pricePrecision)}")#字符串
                                # {'code': '00000', 'msg': 'success', 'requestTime': 1732951086595, 'data': {'symbol': 'BTCUSDT_SPBL', 'symbolName': 'BTCUSDT', 'symbolDisplayName': 'BTCUSDT', 'baseCoin': 'BTC', 'baseCoinDisplayName': 'BTC', 'quoteCoin': 'USDT', 'quoteCoinDisplayName': 'USDT', 'minTradeAmount': '0', 'maxTradeAmount': '0', 'takerFeeRate': '0.002', 'makerFeeRate': '0.002', 'priceScale': '2', 'quantityScale': '6', 'quotePrecision': '8', 'status': 'online', 'minTradeUSDT': '1', 'buyLimitPriceRatio': '0.05', 'sellLimitPriceRatio': '0.05', 'maxOrderNum': '500'}}
                                
                                #【盘口深度】#20次/1s (IP)
                                params={"symbol":str(thissymbol+"USDT"), "limit":'150', "type":'step0'}
                                request_path="/api/v2/spot/market/orderbook"
                                thisdepth = client._request_with_params(params=params,request_path=request_path,method="GET")["data"]#quantityScale可能是精度
                                # print(thisdepth)
                                bid1=thisdepth["bids"][0][0]#买一
                                bid1v=thisdepth["bids"][0][1]
                                ask1=thisdepth["asks"][0][0]#卖一
                                ask1v=thisdepth["asks"][0][1]
                                print(f"""买入
                                    {bid1},{type(bid1)},bid1
                                    {bid1v},{type(bid1v)},bid1v
                                    {ask1},{type(ask1)},ask1
                                    {ask1v},{type(ask1v)},ask1v
                                    """
                                    )
                                #【计算】buyprice和buyvolume
                                buyprice=round(float(ask1)*(1+0.02),
                                                pricePrecision)#对手盘一档上浮百分之二避免无法成交，之后保留pricePrecision位小数
                                buyvolume=round(math.floor(float(tradeusdt)/buyprice*(10**quantityPrecision))/(10**quantityPrecision),
                                                quantityPrecision)#quantityPrecision代表代币精度
                                print(f"buyprice,{buyprice},buyvolume,{buyvolume}")
                                #目标下单金额跟最大最小下单金额对比
                                if buyvolume>float(maxTradeAmount):
                                    buyvolume=round(maxTradeAmount,
                                                    quantityPrecision)
                                    print("目标下单金额大于最大下单金额")
                                else:
                                    print("目标下单金额正常")
                                if buyvolume<float(minTradeAmount):
                                    buyvolume=round(minTradeAmount,
                                                    quantityPrecision)
                                    print("目标下单金额大于最大下单金额")
                                else:
                                    print("目标下单金额正常")
                                if buyvolume>0:#有余额才下单的
                                    #【现货下单】#10次/1s (UID)
                                    # symbol, quantity, side, orderType, force, price='', clientOrderId=None)
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
                                    print(f"{thisorder}")
                        except Exception as e:
                            print(f"{thissymbol}公告买入报错{e}")
                        #【将公告信息推送到微信】
                        res=postmessage(mes)
                    else:
                        print("binance新上市币种在bitget上市时间不足8小时不执行交易")
                    #【推送准备进行的交易记录】验证了一下没错恰好是在限制的时间内还在推送公告超时之后就不推送了
                    print("公告推送",res)
            except Exception as e:
                print(f"公告理财赎回买入报错组合模块报错{e}")
                


        print("newsnum",newsnum)
        if newsnum==0:
            print("近期无新出上市公告卖出现货申购活期理财产品")
            try:
                #【查询现货非USDT余额】之前报错是现货闲置的BGB一直卖出失败导致后续无法执行
                spotbalance=getspotbalance(coin="")
                allbalance=[balance for balance in spotbalance if balance["coin"]!="USDT"]#只卖出非USDT的现货代币
                print(f"allbalance,{allbalance},{type(allbalance)}")
                for balance in allbalance:
                    print("balance",balance)#balance,[{'coin': 'BGB', 'available': '0.23676071', 'limitAvailable': '0', 'frozen': '0.00000000', 'locked': '0.00000000', 'uTime': '1733983259291'}],<class 'list'>balance {'coin': 'BGB', 'available': '0.23676071', 'limitAvailable': '0', 'frozen': '0.00000000', 'locked': '0.00000000', 'uTime': '1733983259291'}
                    try:
                        #从持仓信息处获取建仓时间【如果存过理财则会返回从理财划转会现货账户的时间{链上转入同理}】
                        thisuTime=balance["uTime"]#1733983259291
                        print("thisuTime",thisuTime,type(thisuTime))
                        holdtime = datetime.datetime.utcfromtimestamp(int(thisuTime)/1000)#时间戳转datetime格式
                        print("建仓时间holdtime",holdtime.strftime('%Y-%m-%d %H:%M:%S'))

                        #标的信息和可用余额
                        thissymbol=balance["coin"]
                        sellvolume=balance["available"]

                        #验证当前公告名单当中是否有该持仓标的【生成supportdf之前已经确认过是只要上币公告了】df["title"].str.contains("Will List")|df["title"].str.contains("Will Add")
                        thisdf=supportdf[supportdf["title"].str.contains(thissymbol)]#这个截取出来的切片还是dataframe的格式跟之前的截取出来一个对象的情况不一样，取值需要加上[0]
                        
                        print(f"thisdf,{thisdf},{type(thisdf)},{str(len(thisdf))},{str(thisdf.empty)}")#如果为空len(thisdf)=0且thisdf.empty为True
                        if len(thisdf)>0:#如果整体符合要求的公告为空则这里也是空
                            print("当前有新公告验证时间")
                            thisdf=thisdf[thisdf["timestampdatetime"]==thisdf["timestampdatetime"].max()]#取最大的一行【看看只有一行会不会报错】
                            print(f"thisdf保留timestampdatetime最大的行,{thisdf},{type(thisdf)}")
                            thisdf=thisdf.iloc[0]#这样截取出来就跟上面一样了
                            print(f"thisdf截取第一行后,{thisdf},{type(thisdf)}")
                            #【获取当前时间】
                            thisutc=datetime.datetime.utcnow()
                            thisnow=thisutc.strftime('%Y-%m-%d %H:%M:%S')
                            print(f"thisnow,{thisnow}")
                            print(f"当前持仓标的{thissymbol}最新一条现货上币公告与当时时间的差值{thisutc-thisdf.timestampdatetime}")
                            if (thisutc-thisdf.timestampdatetime)<=datetime.timedelta(seconds=
                                                                    #【实盘】
                                                                    60*60*8#【超过这个时间就执行卖出】
                                                                    # #【测试】
                                                                    # 60*60*24*19+#19天
                                                                    # 60*60*24+#21小时
                                                                    # 60*20+#30分钟
                                                                    # 50#50秒
                                                                    ):
                                print("该标的上市公告结束不足8小时不执行卖出")
                                continue#这里直接跳出去了不执行后面内容
                            else:
                                print("该标的上市公告结束较长时间直接卖出")
                        else:
                            print("当前没有新公告验证持仓标的在币安是否已经上市超过一定时间")
                            print("thissymbol",thissymbol)
                            #【以是否持仓超过8小时作为验证条件】
                            # 【获取当前时间】
                            thisutc=datetime.datetime.utcnow()
                            thisnow=thisutc.strftime('%Y-%m-%d %H:%M:%S')
                            print(f"thisnow,{thisnow}")
                            if (thisutc-holdtime)<=datetime.timedelta(seconds=
                                                                    #【实盘】
                                                                    60*60*8#【超过这个时间就执行卖出】
                                                                    # #【测试】
                                                                    # 60*60*24*19+#19天
                                                                    # 60*60*24+#21小时
                                                                    # 60*20+#30分钟
                                                                    # 50#50秒
                                                                    ):
                                print("该标的在bitget持仓时间不超过8小时不执行卖出")
                                continue#这里直接跳出去了不执行后面内容
                            else:
                                print("该标的在bitget持仓时间超过8小时执行卖出")
                            #【以是否在bitget上买入订单最后一条买入订单达到8小时】
                            params={}
                            request_path="/api/v2/spot/trade/history-orders"#【获取全部订单】#10次/1s (UID)(仅支持查询90天内数据，超过90天数据可以在网页端导出)
                            all_orders = client._request_with_params(params=params,request_path=request_path,method="GET")["data"]
                            print(f"all_orders,{len(all_orders)}")
                            # [{'userId': '4664965813', 'symbol': 'MOVEUSDT', 'orderId': '1250108230597697537', 'clientOid': 'd408bcc4-96f9-4444-8384-5f14006702b6', 'price': '0.7931000000000000', 'size': '285.8700000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'filled', 'priceAvg': '0.7931000000000000', 'baseVolume': '285.8700000000000000', 'quoteVolume': '226.7234970000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.226723497,"t":-0.226723497,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.2267234970000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'MOVE', 'cancelReason': '', 'cTime': '1733774948739', 'uTime': '1733774949273'}, {'userId': '4664965813', 'symbol': 'MOVEUSDT', 'orderId': '1249988777562169354', 'clientOid': '456cb32f-dc41-49fc-b68c-c109f958d63b', 'price': '0.8118000000000000', 'size': '286.1600000000000000', 
                            # 'orderType': 'limit', 'side': 'buy', 'status': 'filled', 'priceAvg': '0.8106514886776629', 'baseVolume': '286.1600000000000000', 'quoteVolume': '231.9760300000000000', 'enterPointSource': 'ANDROID', 'feeDetail': '{"MOVE":{"deduction":false,"feeCoinCode":"MOVE","totalDeductionFee":0,"totalFee":-0.2861600000000000},"newFees":{"c":0,"d":0,"deduction":false,"r":-0.28616,"t":-0.28616,"totalDeductionFee":0}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'MOVE', 'cancelReason': '', 'cTime': '1733746468916', 'uTime': '1733746469004'}, {'userId': '4664965813', 'symbol': 'MOVEUSDT', 'orderId': '1249988735216476190', 'clientOid': 'f6192dcb-4825-4779-8969-7e34a5c89848', 'price': '0.8045000000000000', 'size': '288.7600000000000000', 'orderType': 'limit', 'side': 'buy', 'status': 
                            # 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'ANDROID', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'MOVE', 'cancelReason': 'normal_cancel', 'cTime': '1733746458820', 'uTime': '1733746465273'}, {'userId': '4664965813', 'symbol': 'SOLUSDT', 'orderId': '1247467172877393922', 'clientOid': '7952d8fd-d66f-4fa3-99ec-a4093e86c73f', 'price': '223.4600000000000000', 'size': '0.6156000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'filled', 'priceAvg': '223.4600000000000000', 'baseVolume': '0.6156000000000000', 'quoteVolume': '137.5619760000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.137561976,"t":-0.137561976,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.1375619760000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'SOL', 'cancelReason': '', 'cTime': '1733145271510', 'uTime': '1733145274914'}, {'userId': '4664965813', 'symbol': 'SOLUSDT', 'orderId': '1247467149573840897', 'clientOid': '0984f31f-4adb-4c02-9f96-6b5148ea492c', 'price': '223.4100000000000000', 'size': '0.8031000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '223.4100000000000000', 'baseVolume': '0.1875000000000000', 'quoteVolume': '41.8893750000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.041889375,"t":-0.041889375,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.0418893750000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'SOL', 'cancelReason': 'normal_cancel', 'cTime': '1733145265954', 'uTime': '1733145270053'}, {'userId': '4664965813', 'symbol': 'SOLUSDT', 'orderId': '1247467125125242888', 'clientOid': '33019855-75d7-449c-af30-e85de0533a58', 'price': '223.5100000000000000', 'size': '0.8031000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'SOL', 'cancelReason': 'normal_cancel', 'cTime': '1733145260125', 'uTime': '1733145264549'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246995591017357314', 'clientOid': '2db3e907-1a01-43d9-a0d4-4913aba22f32', 'price': 
                            # '0.5751000000000000', 'size': '3.1600000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'filled', 'priceAvg': '0.5751000000000000', 'baseVolume': '3.1600000000000000', 'quoteVolume': '1.8173160000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.001817316,"t":-0.001817316,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.0018173160000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733032837633', 'uTime': '1733032837715'}, {'userId': '4664965813', 
                            # 'symbol': 'ACTUSDT', 'orderId': '1246995570121334799', 'clientOid': '8868e15d-2ebf-40da-b343-023e53bf9a0e', 'price': '0.5752000000000000', 'size': '3.1600000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': 'normal_cancel', 'cTime': '1733032832651', 'uTime': '1733032836263'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246995549128843267', 'clientOid': '48de23aa-07a1-49b4-92d7-ab3c7e9ff99f', 'price': '0.5750000000000000', 'size': '3.1600000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': 'normal_cancel', 'cTime': '1733032827646', 'uTime': '1733032831237'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246995526357966861', 'clientOid': 'aaeee2d5-1f74-4c21-9735-71b083e2474a', 'price': '0.5757000000000000', 'size': '3.1600000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': 'normal_cancel', 'cTime': '1733032822217', 'uTime': '1733032825844'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246989126898638853', 'clientOid': 'cd96cbe4-01cf-499a-a735-7f71a94af757', 'price': '0.5872000000000000', 'size': '3.1700000000000000', 'orderType': 'limit', 'side': 'buy', 'status': 'filled', 'priceAvg': '0.5757000000000000', 'baseVolume': '3.1700000000000000', 'quoteVolume': '1.8249690000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.00317,"t":-0.00317,"totalDeductionFee":0},"ACT":{"deduction":false,"feeCoinCode":"ACT","totalDeductionFee":0,"totalFee":-0.0031700000000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733031296467', 'uTime': '1733031296562'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246982283157659656', 'clientOid': '8801dd9f-4b38-4a38-b150-429c197ae22f', 'price': '0.5739000000000000', 'size': '3.1800000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'filled', 'priceAvg': '0.5739000000000000', 'baseVolume': '3.1800000000000000', 'quoteVolume': '1.8250020000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.001825002,"t":-0.001825002,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.0018250020000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 
                            # 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733029664792', 'uTime': '1733029667855'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246982261296947203', 'clientOid': 'cd2c8c9e-02f0-4bbd-9bd5-84c4aab6db6f', 'price': '0.5737000000000000', 'size': '3.1800000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': 'normal_cancel', 'cTime': '1733029659580', 'uTime': '1733029663152'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246982241621467136', 'clientOid': 'ff424d28-16fa-4333-8d46-528c0c772f00', 'price': '0.5740000000000000', 'size': '3.1800000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': 'normal_cancel', 'cTime': '1733029654889', 'uTime': '1733029658391'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246982221539139597', 'clientOid': 'b447ba67-5593-4e59-a162-0ef647d6761e', 'price': '0.5746000000000000', 'size': '3.1800000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 
                            # 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': 'normal_cancel', 'cTime': '1733029650101', 'uTime': '1733029653629'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246968779998584832', 'clientOid': 'a8ce1e40-22db-4e9f-8918-2aaa29e7fbdd', 'price': '0.5878000000000000', 'size': '3.1800000000000000', 'orderType': 'limit', 'side': 'buy', 'status': 'filled', 'priceAvg': '0.5758000000000000', 'baseVolume': '3.1800000000000000', 'quoteVolume': '1.8310440000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.00318,"t":-0.00318,"totalDeductionFee":0},"ACT":{"deduction":false,"feeCoinCode":"ACT","totalDeductionFee":0,"totalFee":-0.0031800000000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733026445388', 'uTime': '1733026445467'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246965792953688065', 'clientOid': '5993c844-5a46-49f9-b7f4-cf179ba5418f', 'price': '0.5694000000000000', 'size': '3.2200000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'filled', 'priceAvg': '0.5694000000000000', 'baseVolume': '3.2200000000000000', 'quoteVolume': '1.8334680000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.001833468,"t":-0.001833468,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.0018334680000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733025733221', 'uTime': '1733025736016'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246965767271964672', 'clientOid': '660a0363-ba54-4128-a5ad-e7d7e3751556', 'price': '0.5693000000000000', 'size': '3.2200000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': 'normal_cancel', 'cTime': '1733025727098', 'uTime': '1733025730732'}, 
                            # {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246965744459145240', 'clientOid': '3c7e2b31-fb73-43bc-a5fa-e4037188acc2', 'price': '0.5696000000000000', 'size': '3.2200000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': 'normal_cancel', 'cTime': '1733025721659', 'uTime': '1733025725565'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246964908450471936', 'clientOid': '607e5bf1-94ad-45f7-bc1e-bb981fbcb1db', 'price': '0.5774000000000000', 'size': '3.2200000000000000', 'orderType': 'limit', 'side': 'buy', 'status': 'filled', 
                            # 'priceAvg': '0.5661000000000000', 'baseVolume': '3.2200000000000000', 'quoteVolume': '1.8228420000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.00322,"t":-0.00322,"totalDeductionFee":0},"ACT":{"deduction":false,"feeCoinCode":"ACT","totalDeductionFee":0,"totalFee":-0.0032200000000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733025522339', 'uTime': '1733025522417'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246956558522343440', 'clientOid': '705a3268-28eb-4142-acb6-6319cb05cd8b', 'price': '0.5650000000000000', 'size': '3.2300000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'filled', 'priceAvg': '0.5650000000000000', 'baseVolume': '3.2300000000000000', 'quoteVolume': '1.8249500000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.00182495,"t":-0.00182495,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.0018249500000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733023531561', 'uTime': '1733023533321'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246950350528798725', 'clientOid': '02ee03eb-5344-4099-8448-74c3af8303f0', 'price': '0.5683000000000000', 'size': '3.2400000000000000', 'orderType': 'limit', 'side': 'buy', 'status': 'filled', 'priceAvg': '0.5570000000000000', 'baseVolume': '3.2400000000000000', 'quoteVolume': '1.8046800000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.00324,"t":-0.00324,"totalDeductionFee":0},"ACT":{"deduction":false,"feeCoinCode":"ACT","totalDeductionFee":0,"totalFee":-0.0032400000000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733022051460', 'uTime': '1733022051546'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246944282734059535', 'clientOid': '1bfcfd34-1dce-42f0-827a-a622805fe636', 'price': '0.5546000000000000', 'size': '3.2600000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'filled', 'priceAvg': '0.5546000000000000', 'baseVolume': '3.2600000000000000', 'quoteVolume': '1.8079960000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.001807996,"t":-0.001807996,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.0018079960000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733020604785', 'uTime': '1733020608066'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246944250555359243', 'clientOid': '1d01febf-0b05-4bed-bef8-b0c4fc34765f', 'price': '0.5551000000000000', 'size': '3.2600000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 
                            # 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': 'normal_cancel', 'cTime': '1733020597113', 'uTime': '1733020600774'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246944218494099468', 'clientOid': '54affdae-deaa-46a4-98e9-d8244760d70f', 'price': '0.5552000000000000', 'size': '3.2600000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': 'normal_cancel', 'cTime': '1733020589469', 'uTime': '1733020593171'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246944207286919177', 'clientOid': '2e41afe5-540b-433f-b066-74f4e1603b7c', 'price': 
                            # '0.5663000000000000', 'size': '3.2600000000000000', 'orderType': 'limit', 'side': 'buy', 'status': 'filled', 'priceAvg': '0.5552000000000000', 'baseVolume': '3.2600000000000000', 'quoteVolume': '1.8099520000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.00326,"t":-0.00326,"totalDeductionFee":0},"ACT":{"deduction":false,"feeCoinCode":"ACT","totalDeductionFee":0,"totalFee":-0.0032600000000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733020586797', 'uTime': '1733020586884'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246944187393335337', 'clientOid': '59040719-c0b9-4c7f-81ed-70331291c8ff', 'price': '0.5551000000000000', 'size': '3.2600000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'filled', 'priceAvg': '0.5551000000000000', 'baseVolume': '3.2600000000000000', 'quoteVolume': '1.8096260000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.001809626,"t":-0.001809626,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.0018096260000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733020582054', 'uTime': '1733020585123'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246944175653478414', 'clientOid': '94ca6ed1-c9a2-4dfa-9d53-084a8e9f7ff8', 'price': '0.5660000000000000', 'size': '3.2600000000000000', 'orderType': 'limit', 'side': 'buy', 'status': 'filled', 'priceAvg': '0.5550000000000000', 'baseVolume': '3.2600000000000000', 'quoteVolume': '1.8093000000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.00326,"t":-0.00326,"totalDeductionFee":0},"ACT":{"deduction":false,"feeCoinCode":"ACT","totalDeductionFee":0,"totalFee":-0.0032600000000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733020579255', 'uTime': '1733020579353'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246944155881529349', 'clientOid': '5d5a5e22-0329-4871-a3d3-aa3914f39fd4', 'price': '0.5545000000000000', 'size': '3.2700000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'filled', 'priceAvg': '0.5545000000000000', 'baseVolume': '3.2700000000000000', 'quoteVolume': '1.8132150000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.001813215,"t":-0.001813215,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.0018132150000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733020574541', 'uTime': '1733020576751'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246944144842121241', 'clientOid': '2ee4ea96-6956-4854-9ca7-acb9b68340b5', 'price': '0.5658000000000000', 'size': '3.2800000000000000', 'orderType': 'limit', 'side': 'buy', 'status': 'filled', 'priceAvg': '0.5546000000000000', 'baseVolume': '3.2800000000000000', 'quoteVolume': '1.8190880000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.00328,"t":-0.00328,"totalDeductionFee":0},"ACT":{"deduction":false,"feeCoinCode":"ACT","totalDeductionFee":0,"totalFee":-0.0032800000000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733020571909', 'uTime': '1733020571997'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246944124969508879', 'clientOid': '4ad02633-0cc0-46ff-a4b6-c6f0d4e44272', 'price': '0.5548000000000000', 'size': '3.2800000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'filled', 'priceAvg': '0.5548000000000000', 'baseVolume': '3.2800000000000000', 'quoteVolume': '1.8197440000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.001819744,"t":-0.001819744,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.0018197440000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733020567171', 'uTime': '1733020567602'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246944112797638657', 'clientOid': '0e90543a-fe45-4f5c-ac09-b30d3c437220', 'price': '0.5656000000000000', 'size': '3.2800000000000000', 'orderType': 'limit', 'side': 'buy', 'status': 'filled', 'priceAvg': '0.5544000000000000', 'baseVolume': '3.2800000000000000', 'quoteVolume': '1.8184320000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.00328,"t":-0.00328,"totalDeductionFee":0},"ACT":{"deduction":false,"feeCoinCode":"ACT","totalDeductionFee":0,"totalFee":-0.0032800000000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733020564269', 'uTime': '1733020564362'}, {'userId': '4664965813', 'symbol': 
                            # 'ACTUSDT', 'orderId': '1246944059139907605', 'clientOid': '98085e85-afc9-4ce2-aad9-0245a29ec2d1', 'price': '0.5541000000000000', 'size': '3.2900000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'filled', 'priceAvg': '0.5542000000000000', 'baseVolume': '3.2900000000000000', 'quoteVolume': '1.8233180000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.001823318,"t":-0.001823318,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.0018233180000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733020551476', 'uTime': '1733020551561'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246944026399170562', 'clientOid': 'a0613fd1-afe3-4eed-9d97-a232cc6a18ac', 'price': '0.5552000000000000', 'size': '3.2900000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': 'normal_cancel', 'cTime': '1733020543670', 'uTime': '1733020547350'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246943994157555724', 'clientOid': '40cb41cd-0dbc-4c71-aa91-91acae0a65cb', 'price': '0.5551000000000000', 'size': '3.2900000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': 'normal_cancel', 'cTime': '1733020535983', 'uTime': '1733020539606'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246943961408430107', 'clientOid': '4b0a285c-7dee-4dd2-84db-cdc119566e53', 'price': '0.5552000000000000', 'size': '3.2900000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': 'normal_cancel', 'cTime': '1733020528175', 'uTime': '1733020531829'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246943949635018753', 'clientOid': 'e09c6644-f67a-462c-95c6-c51f4d5d1a40', 'price': '0.5664000000000000', 'size': '3.2900000000000000', 'orderType': 'limit', 'side': 'buy', 'status': 'filled', 'priceAvg': '0.5552000000000000', 'baseVolume': '3.2900000000000000', 'quoteVolume': '1.8266080000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.00329,"t":-0.00329,"totalDeductionFee":0},"ACT":{"deduction":false,"feeCoinCode":"ACT","totalDeductionFee":0,"totalFee":-0.0032900000000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733020525368', 'uTime': '1733020525452'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246943929850486798', 'clientOid': '5cce4cde-f2ad-4b11-87a6-b1309969d837', 'price': '0.5549000000000000', 'size': '3.2900000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'filled', 'priceAvg': '0.5549000000000000', 'baseVolume': '3.2900000000000000', 'quoteVolume': '1.8256210000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.001825621,"t":-0.001825621,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.0018256210000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 
                            # 'cTime': '1733020520651', 'uTime': '1733020523167'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246943897176858662', 'clientOid': '4d380bcb-945a-48d1-b01c-cfb606ea9452', 'price': '0.5552000000000000', 'size': '3.2900000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': 'normal_cancel', 'cTime': '1733020512861', 'uTime': '1733020516559'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246943864062828552', 'clientOid': 'cfd6e2a1-882a-47b7-b1fd-570c92f4dea8', 'price': '0.5555000000000000', 'size': '3.2900000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 
                            # 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': 'normal_cancel', 'cTime': '1733020504966', 'uTime': '1733020508601'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246943831133347842', 'clientOid': 'fd727a2e-98bd-4415-ba07-581357351531', 'price': '0.5558000000000000', 'size': '3.2900000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': 'normal_cancel', 'cTime': '1733020497115', 'uTime': '1733020500813'}, {'userId': '4664965813', 'symbol': 'ACTUSDT', 'orderId': '1246943818810482692', 'clientOid': 'fefd31f9-e1e6-4016-ab7f-8658a0d63ff6', 'price': '0.5668000000000000', 'size': '3.3000000000000000', 'orderType': 'limit', 'side': 'buy', 'status': 'filled', 'priceAvg': '0.5557000000000000', 'baseVolume': '3.3000000000000000', 'quoteVolume': '1.8338100000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.0033,"t":-0.0033,"totalDeductionFee":0},"ACT":{"deduction":false,"feeCoinCode":"ACT","totalDeductionFee":0,"totalFee":-0.0033000000000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ACT', 'cancelReason': '', 'cTime': '1733020494177', 'uTime': '1733020494272'}, {'userId': '4664965813', 'symbol': 'ETHUSDT', 'orderId': '1246942838672941058', 'clientOid': 'b5d213b1-e24c-476f-a439-d0ed88867237', 'price': '3684.8200000000000000', 'size': '0.0005000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'filled', 'priceAvg': '3685.0200000000000000', 'baseVolume': '0.0005000000000000', 'quoteVolume': '1.8425100000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.00184251,"t":-0.00184251,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.0018425100000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ETH', 'cancelReason': '', 'cTime': '1733020260494', 'uTime': '1733020260581'}, {'userId': '4664965813', 'symbol': 'ETHUSDT', 'orderId': '1246942817814667288', 'clientOid': '3bf1dc2f-50a8-48af-b9f1-14a767fea457', 'price': '3684.8700000000000000', 'size': '0.0005000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ETH', 'cancelReason': 'normal_cancel', 'cTime': '1733020255521', 'uTime': '1733020259374'}, {'userId': '4664965813', 'symbol': 'ETHUSDT', 'orderId': '1246942797212246018', 'clientOid': 'd049ea18-44e1-4e13-bdbf-9022e919b429', 'price': '3685.3000000000000000', 'size': '0.0005000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ETH', 'cancelReason': 'normal_cancel', 'cTime': '1733020250609', 'uTime': '1733020254456'}, {'userId': '4664965813', 'symbol': 'ETHUSDT', 'orderId': '1246942776408498180', 'clientOid': '2d7d5668-e9e1-4cd0-b7c7-54c79cb0ed75', 'price': '3686.0100000000000000', 'size': '0.0005000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ETH', 'cancelReason': 'normal_cancel', 'cTime': '1733020245649', 'uTime': '1733020249477'}, {'userId': '4664965813', 'symbol': 'ETHUSDT', 'orderId': '1246942755311149083', 'clientOid': '6d043dc6-1111-48a0-8dda-5f68c33a8890', 'price': '3686.0900000000000000', 'size': '0.0005000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ETH', 'cancelReason': 'normal_cancel', 'cTime': '1733020240619', 'uTime': '1733020244482'}, {'userId': '4664965813', 'symbol': 'ETHUSDT', 'orderId': '1246942734691950647', 'clientOid': '801ccb35-89d2-4cd4-a7a2-3945a56bdb19', 'price': '3686.3300000000000000', 'size': '0.0005000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ETH', 'cancelReason': 'normal_cancel', 'cTime': '1733020235703', 'uTime': '1733020239567'}, {'userId': '4664965813', 'symbol': 'ETHUSDT', 'orderId': '1246942046880620547', 'clientOid': '37371671-a5e5-495d-a34c-28d83013eee2', 'price': '3691.4100000000000000', 'size': '0.0005000000000000', 'orderType': 'limit', 'side': 'buy', 'status': 'filled', 'priceAvg': '3691.4100000000000000', 'baseVolume': '0.0005000000000000', 'quoteVolume': '1.8457050000000000', 'enterPointSource': 'ANDROID', 'feeDetail': '{"ETH":{"deduction":false,"feeCoinCode":"ETH","totalDeductionFee":0,"totalFee":-5.000000000E-7},"newFees":{"c":0,"d":0,"deduction":false,"r":-5E-7,"t":-5E-7,"totalDeductionFee":0}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ETH', 'cancelReason': '', 'cTime': '1733020071716', 'uTime': '1733020202738'}, {'userId': '4664965813', 'symbol': 'ETHUSDT', 'orderId': '1246941284045774865', 'clientOid': 'd948e2e7-5049-4f50-97fa-917d92b8782b', 'price': '3690.0100000000000000', 'size': '0.0005000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'filled', 'priceAvg': '3690.0100000000000000', 'baseVolume': '0.0005000000000000', 'quoteVolume': '1.8450050000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.001845005,"t":-0.001845005,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.0018450050000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ETH', 'cancelReason': '', 'cTime': '1733019889842', 'uTime': '1733019893753'}, {'userId': '4664965813', 'symbol': 'ETHUSDT', 'orderId': '1246941220204273666', 'clientOid': '2b894ed6-d05f-4866-acd7-6332a1ff824a', 'price': '3691.8900000000000000', 'size': '0.0005000000000000', 'orderType': 'limit', 'side': 'buy', 'status': 'filled', 'priceAvg': '3691.2100000000000000', 'baseVolume': '0.0005000000000000', 'quoteVolume': '1.8456050000000000', 'enterPointSource': 'ANDROID', 'feeDetail': '{"ETH":{"deduction":false,"feeCoinCode":"ETH","totalDeductionFee":0,"totalFee":-5.000000000E-7},"newFees":{"c":0,"d":0,"deduction":false,"r":-5E-7,"t":-5E-7,"totalDeductionFee":0}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ETH', 'cancelReason': '', 'cTime': '1733019874621', 'uTime': '1733019874705'}, {'userId': '4664965813', 'symbol': 'TRXUSDT', 'orderId': '1246930970717806596', 'clientOid': 'e2184f1b-2152-4a89-9d8c-510cd14bf98a', 'price': '0.2047000000000000', 'size': '4.9950000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'filled', 'priceAvg': '0.2047000000000000', 'baseVolume': '4.9950000000000000', 'quoteVolume': '1.0224765000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.0010224765,"t":-0.0010224765,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.0010224765000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'TRX', 'cancelReason': '', 'cTime': '1733017430953', 'uTime': '1733017557686'}, {'userId': '4664965813', 'symbol': 'TRXUSDT', 'orderId': '1246930945132552201', 'clientOid': '7f23ca52-5d7f-4bec-b827-975fdc0114dc', 'price': '0.2047000000000000', 'size': '4.9950000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 
                            # 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'TRX', 'cancelReason': 'normal_cancel', 'cTime': '1733017424853', 'uTime': '1733017429488'}, {'userId': '4664965813', 'symbol': 'TRXUSDT', 'orderId': '1246930919417274368', 'clientOid': 'b866af1a-2388-403c-b223-aa2184ba1482', 'price': '0.2047000000000000', 'size': '4.9950000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'TRX', 'cancelReason': 'normal_cancel', 'cTime': '1733017418722', 'uTime': '1733017423361'}, {'userId': '4664965813', 'symbol': 'TRXUSDT', 'orderId': '1246930893462921232', 'clientOid': 
                            # '0180fb88-73c3-4cf6-ba7c-eabed0351aed', 'price': '0.2047000000000000', 'size': '4.9950000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'API', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'TRX', 'cancelReason': 'normal_cancel', 'cTime': '1733017412534', 'uTime': '1733017417185'}, {'userId': '4664965813', 'symbol': 'ETHUSDT', 'orderId': '1246930863318458369', 'clientOid': 'ce930225-356e-40b3-92cb-025def906a99', 'price': '3704.5600000000000000', 'size': '0.0003000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'filled', 'priceAvg': '3704.5600000000000000', 'baseVolume': '0.0003000000000000', 'quoteVolume': '1.1113680000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.001111368,"t":-0.001111368,"totalDeductionFee":0},"USDT":{"deduction":false,"feeCoinCode":"USDT","totalDeductionFee":0,"totalFee":-0.0011113680000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 
                            # 'quoteCoin': 'USDT', 'baseCoin': 'ETH', 'cancelReason': '', 'cTime': '1733017405347', 'uTime': '1733017405970'}, {'userId': '4664965813', 'symbol': 'TRXUSDT', 'orderId': '1246744642113855488', 'clientOid': '31101e6e-7bdd-48e0-964d-36a61fb0b223', 'price': '54.0000000000000000', 'size': '4.9950000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'ANDROID', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'TRX', 'cancelReason': 'normal_cancel', 'cTime': '1732973006752', 'uTime': '1733017411075'}, {'userId': '4664965813', 'symbol': 'TRXUSDT', 'orderId': '1246743657844924434', 'clientOid': 'ee1b08f3-0569-49f1-ace9-db01a14bf889', 
                            # 'price': '0.5400000000000000', 'size': '4.9950000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'ANDROID', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'TRX', 'cancelReason': 'normal_cancel', 'cTime': '1732972772084', 'uTime': '1732972948995'}, {'userId': '4664965813', 'symbol': 'TRXUSDT','orderId': '1246743390856503318', 'clientOid': '435805eb-18db-4902-b2cb-01d923ea498f', 'price': '0.5500000000000000', 'size': '4.9950000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume':'0.0000000000000000', 'enterPointSource': 'ANDROID', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'TRX', 'cancelReason':'normal_cancel', 'cTime': '1732972708429', 'uTime': '1732972746124'}, 
                            # {'userId': '4664965813', 'symbol': 'TRXUSDT', 'orderId': '1246727715102482458', 'clientOid': '1921b15b-08d4-4a14-9e0b-6967bcf58b2e', 'price': '0.2043000000000000', 'size': '5.0000000000000000', 'orderType': 'limit', 'side': 'buy', 'status': 'filled', 'priceAvg': '0.2043000000000000', 'baseVolume': '5.0000000000000000', 'quoteVolume': '1.0215000000000000', 'enterPointSource': 'ANDROID', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.005,"t":-0.005,"totalDeductionFee":0},"TRX":{"deduction":false,"feeCoinCode":"TRX","totalDeductionFee":0,"totalFee":-0.0050000000000000}}', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'TRX', 'cancelReason': '', 'cTime': '1732968971038', 'uTime': '1732968971114'}, {'userId': '4664965813', 'symbol': 'ETHUSDT', 'orderId': '1246676540521013250', 'clientOid': 'd4677c61-81ae-48a6-8c70-e826e857a0d5', 'price': '36994.9200000000000000', 'size': '0.0003000000000000', 'orderType': 'limit', 'side': 'sell', 'status': 'cancelled', 'priceAvg': '0', 'baseVolume': '0.0000000000000000', 'quoteVolume': '0.0000000000000000', 'enterPointSource': 'ANDROID', 'feeDetail': '', 'orderSource': 'normal', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ETH', 'cancelReason': 'normal_cancel', 'cTime': '1732956770067', 'uTime': '1732957071568'}, {'userId': '4664965813', 'symbol': 'ETHUSDT', 'orderId': '1246673624825421829', 'clientOid': '3931d618-a6ca-4435-b578-4f79bf435bb1', 'price': '0', 'size': '1.5000000000000000', 'orderType': 'market', 'side': 'buy', 'status': 'filled', 'priceAvg': '3694.2300000000000000', 'baseVolume': '0.0004000000000000', 'quoteVolume': '1.4776920000000000', 'enterPointSource': 'API', 'feeDetail': '{"ETH":{"deduction":false,"feeCoinCode":"ETH","totalDeductionFee":0,"totalFee":-4.000000000E-7},"newFees":{"c":0,"d":0,"deduction":false,"r":-4E-7,"t":-4E-7,"totalDeductionFee":0}}', 'orderSource': 'market', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ETH', 'cancelReason': '', 'cTime': '1732956074911', 'uTime': '1732956075007'}]

                            # thissymbol="MOVE"#【测试】K线长度【实盘的时候要注销】
                            # all_orders=[order for order in all_orders if (order["symbol"]==thissymbol+"USDT")and(order["side"]=="buy")]
                            all_orders=[order for order in all_orders if (order["baseCoin"]==thissymbol)and(order["side"]=="buy")]
                            print(f"all_orders,{len(all_orders)}")
                            # cTime	String	创建时间{略快一秒}，Unix毫秒时间戳，例如1690196141868
                            # uTime	String	更新时间{略慢一秒}，Unix毫秒时间戳，例如1690196141868
                            lasttime=[order["cTime"] for order in all_orders]
                            print("lasttime",lasttime,type(lasttime))#数据类型为字典
                            lasttime=max(lasttime)#直接max就能取出来其中最大的值
                            # lasttime=max([lasttime[0]])#直接max就能取出来其中最大的值#【测试】只有一个order的时候能否找到最大值答案是可以
                            datetimelasttime=datetime.datetime.fromtimestamp(int(lasttime)//1000, tz=datetime.timezone.utc)
                            print("datetimelasttime",datetimelasttime)#创建时间2024-12-09 12:14:28+00:00，更新时间2024-12-09 12:14:29+00:00
                            #【获取当前时间】
                            thistime=datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
                            print(f"thistime,{thistime}")
                            if (thistime-datetimelasttime)<=datetime.timedelta(seconds=
                                                                    #【实盘】
                                                                    60*60*8#【超过这个时间就执行卖出】
                                                                    # #【测试】
                                                                    # 60*60*24*19+#19天
                                                                    # 60*60*24+#21小时
                                                                    # 60*20+#30分钟
                                                                    # 50#50秒
                                                                    ):
                                print("该标的在bitget最后买入时间不超过8小时不执行卖出")
                                continue#这里直接跳出去了不执行后面内容
                            else:
                                print("该标的在bitget最后买入时间超过8小时执行卖出")



                            # #【以是否在binance上市作为验证条件{当IP地址为美国本土时无法使用}】需要提前【安装binance】
                            # thissymbol="ME"#【测试】K线长度【实盘的时候要注销】
                            # try:
                            #     klines = binanceclient.get_klines(symbol=thissymbol+"USDT",
                            #                             # interval=binanceclient.KLINE_INTERVAL_1DAY,#时间周期（1日）
                            #                             # interval=binanceclient.KLINE_INTERVAL_1HOUR,#时间周期（1小时）
                            #                             interval=binanceclient.KLINE_INTERVAL_15MINUTE,#时间周期（15分钟）
                            #                             limit=10,#取样数量
                            #                             )#2024.12.12ME的月K有1条{日K有3条}，BTC的月K有10条
                            #     print("klines",len(klines),klines)
                            #     if not len(klines)<=2:#15分钟K小于等于2条（上市时间在30分钟内）
                            #         print("该标的在币安上市时间不超过30分钟不执行卖出")
                            #         continue#这里直接跳出去了不执行后面内容
                            #     else:
                            #         print("该标的在币安上市时间超过30分钟执行卖出")
                            # except:
                            #     print("该标的尚未在币安上市USDT交易对")
                            #     continue#这里直接跳出去了不执行后面内容
                                


                        #【交易精度】#20次/1s (IP)
                        params={"symbol":thissymbol+"USDT"}
                        request_path="/api/v2/spot/public/symbols"
                        thisinfo = client._request_with_params(params=params,request_path=request_path,method="GET")["data"]#quantityScale可能是精度
                        print(f"{thisinfo}")# [{'symbol': 'BGBUSDT', 'baseCoin': 'BGB', 'quoteCoin': 'USDT', 'minTradeAmount': '0', 'maxTradeAmount': '10000000000', 'takerFeeRate': '0.001', 'makerFeeRate': '0.001', 'pricePrecision': '4', 'quantityPrecision': '4', 'quotePrecision': '8', 'status': 'online', 'minTradeUSDT': '1', 'buyLimitPriceRatio': '0.05', 'sellLimitPriceRatio': '0.05', 'areaSymbol': 'no', 'orderQuantity': '200'}]
                        minTradeAmount=int(thisinfo[0]["minTradeAmount"])#最小交易数量
                        maxTradeAmount=int(thisinfo[0]["maxTradeAmount"])#最大交易数量
                        quantityPrecision=int(thisinfo[0]["quantityPrecision"])#代币精度
                        pricePrecision=int(thisinfo[0]["pricePrecision"])#价格精度
                        print(f"quantityPrecision,{quantityPrecision},{type(quantityPrecision)},pricePrecision,{pricePrecision},{type(pricePrecision)}")#字符串
                        # {'code': '00000', 'msg': 'success', 'requestTime': 1732951086595, 'data': {'symbol': 'BTCUSDT_SPBL', 'symbolName': 'BTCUSDT', 'symbolDisplayName': 'BTCUSDT', 'baseCoin': 'BTC', 'baseCoinDisplayName': 'BTC', 'quoteCoin': 'USDT', 'quoteCoinDisplayName': 'USDT', 'minTradeAmount': '0', 'maxTradeAmount': '0', 'takerFeeRate': '0.002', 'makerFeeRate': '0.002', 'priceScale': '2', 'quantityScale': '6', 'quotePrecision': '8', 'status': 'online', 'minTradeUSDT': '1', 'buyLimitPriceRatio': '0.05', 'sellLimitPriceRatio': '0.05', 'maxOrderNum': '500'}}
                        

                        sellvolume=round(math.floor(float(sellvolume)*(10**quantityPrecision))/(10**quantityPrecision),
                                        quantityPrecision)#为防止余额不足需要先乘后除再取位数
                        print(f"{thissymbol},sellvolume,{sellvolume},{type(sellvolume)}")
                        #目标下单金额跟最大最小下单金额对比
                        if sellvolume>float(maxTradeAmount):
                            sellvolume=round(maxTradeAmount,
                                            quantityPrecision)
                            print("目标下单金额大于最大下单金额")
                        else:
                            print("目标下单金额正常")
                        if sellvolume<float(minTradeAmount):
                            sellvolume=round(minTradeAmount,
                                            quantityPrecision)
                            print("目标下单金额大于最大下单金额")
                        else:
                            print("目标下单金额正常")

                        # 【盘口深度】#20次/1s (IP)
                        params={"symbol":str(thissymbol+"USDT"), "limit":'150', "type":'step0'}
                        request_path="/api/v2/spot/market/orderbook"
                        thisdepth = client._request_with_params(params=params,request_path=request_path,method="GET")["data"]#quantityScale可能是精度
                        # print(thisdepth)
                        bid1=thisdepth["bids"][0][0]#买一
                        bid1v=thisdepth["bids"][0][1]
                        ask1=thisdepth["asks"][0][0]#卖一
                        ask1v=thisdepth["asks"][0][1]
                        print(f"""卖出
                            {bid1},{type(bid1)},bid1
                            {bid1v},{type(bid1v)},bid1v
                            {ask1},{type(ask1)},ask1
                            {ask1v},{type(ask1v)},ask1v
                            """
                            )
                        
                        sellprice=round(float(ask1),pricePrecision)#卖的时候不急了在自己这边挂卖单就行
                        print(f"sellvolume,{sellvolume}")
                        if sellvolume>0:#有余额才下单的
                            #【现货下单】#10次/1s (UID)
                            # symbol, quantity, side, orderType, force, price='', clientOrderId=None)
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
                            print(f"{thisorder}")
                    except Exception as e:
                        print(f"{balance}公告卖出报错{e}")
            except Exception as e:
                print(f"公告卖出整体模块报错{e}")



            # #【现货理财采用自动申购模式，避免手动干预无法微操】
            # try:
            #     #【查询现货余额并转入理财账户】卖出大概一秒左右就转到理财账户了
            #     spotbalance=getspotbalance(coin="USDT")
            #     usdtbalance=[balance for balance in spotbalance if balance["coin"]=="USDT"][0]["available"]
            #     print(f"{usdtbalance},{type(usdtbalance)}")
            #     if float(usdtbalance)>=1:#现货资产余额大于等于1的时候进行活期理财申购{避免余额不足报错}【验证后是对的，usdtbalance="0"时usdtbalance="0"验证为False】
            #         print("余额大于1USDT执行理财申购")
            #         #【获取理财产品列表】#10次/1s (Uid)
            #         savingslist=getsavingslist(coin="USDT")
            #         print(f"{savingslist},{type(savingslist)}")
            #         usdtproductId=str(savingslist[0]["productId"])#取出来产品ID
            #         print(f"{usdtproductId},{type(usdtproductId)}")
            #         #【申购理财产品】10次/1s (Uid)
            #         request_path="/api/v2/earn/savings/subscribe"
            #         params = {"productId":usdtproductId,
            #                 "periodType":"flexible",#只要活期存款
            #                 "amount":usdtbalance
            #                 }
            #         res=client._request_with_params(params=params,request_path=request_path,method="POST")
            #         res=res["data"]
            #         print(f"申购理财产品,{res}")
            #     else:
            #         print(f"余额不足不进行申购")
            # except Exception as e:
            #     print(f"闲置资金活期理财报错,{e}")



        try:#真正的交易机会就很短时间休息久了容易错过机会
            #【休息】避免速度过快限制IP
            time.sleep(2.5)#2秒一次容易抓不到公告【报错抓到的是空值{也可能是IP问题}】，2.5秒一次就正常了
            thistime=datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
            print(f"thistime,{thistime}")
            # #【获取全部订单】#10次/1s (UID)(仅支持查询90天内数据，超过90天数据可以在网页端导出)
            # params={}
            # request_path="/api/v2/spot/trade/history-orders"
            # all_orders = client._request_with_params(params=params,request_path=request_path,method="GET")["data"]
            # print(f"all_orders,{all_orders}")
            #【获取未成交订单】#10次/1s (UID)
            params={}
            request_path="/api/v2/spot/trade/unfilled-orders"
            open_orders = client._request_with_params(params=params,request_path=request_path,method="GET")["data"]
            print(f"open_orders,{open_orders}")
            for thisorder in open_orders:
                print(f"{thisorder}")
                thissymbol=thisorder["symbol"]
                thisorderId=thisorder["orderId"]
                ctime=thisorder["cTime"]#1732973006752创建时间{略快一秒}
                utime=thisorder["uTime"]#1732973006818更新时间{略慢一秒}
                print(f"ctime,{ctime},{type(ctime)}")
                thisdt = datetime.datetime.fromtimestamp(int(ctime)//1000, tz=datetime.timezone.utc)
                print(f"{thisdt}")
                print(f"{thistime-thisdt}")
                if thistime-thisdt>=datetime.timedelta(seconds=3):
                    print("该订单挂起超时执行撤单")
                    #【现货撤单】#10次/1s (UID)
                    params={"symbol":thissymbol,
                            "orderId":thisorderId,
                            }
                    request_path="/api/v2/spot/trade/cancel-order"
                    cance_order = client._request_with_params(params=params,request_path=request_path,method="POST")
                    print(f"cance_order,{cance_order}")#撤单成功
        except Exception as e:
            print("撤单报错",e)

# 【github action能够最大程度避免IP报错】main这个异步函数的作用是处理公告监控问题
if __name__ == '__main__':
    # 运行主函数【使用异步可以规避github action的时间限制问题】
    asyncio.run(main())
