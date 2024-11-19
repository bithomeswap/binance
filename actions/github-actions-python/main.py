import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import datetime
# ping www.binance.com【服务器上可以ping通】
# curl -v https://www.binance.com【使用其他工具（如curl）来测试443端口的连接是否正常】
# dig www.binance.com
# sudo systemctl restart networking#【重启网络】
#443的报错是网络问题

def postmessage(text):
    BASEURL = 'http://wxpusher.zjiecode.com/api'

    # #查询订阅用户数量
    # pagenum=1
    # payload = {
    #     'appToken': "AT_tFRZgjToc6XnG5dzR2MGyv1DzECNYOIU",
    #     'page': str(pagenum),
    #     'pageSize': "50",
    # }
    # query_user=requests.get(url=f'{BASEURL}/fun/wxuser', params=payload).json()
    # print(query_user)
    # uidslist=[]
    # if len(query_user["data"]["records"])>0:
    #     for query in query_user["data"]["records"]:
    #         print(query["uid"])
    #         uidslist.append(query["uid"])
    # print(uidslist)

    #推送消息
    payload = {
        'appToken': "AT_tFRZgjToc6XnG5dzR2MGyv1DzECNYOIU",
        'content': str(text),#文本消息
        'topicIds':["12417"],
        'uids': ["UID_qkmjMTBknX0I5ZZoVY3IBFv7WVV1"],
        # 'uids':uidslist,#搁置
    }
    requests.post(url=f'{BASEURL}/send/message', json=payload).json()

#香港IP无法访问换成美国或者新加坡的就好，一个IP还有访问次数限制，需要多个ip组合
while True:
    # #中文公告
    # headers = {
    #     "Referer": "https://www.binance.com/zh-CN/support/announcement",
    #     "Upgrade-Insecure-Requests": "1",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    #     "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    #     "sec-ch-ua-mobile": "?0",
    #     "sec-ch-ua-platform": "\"Windows\""
    # }
    # url = "https://www.binance.com/zh-CN/support/announcement/%E6%95%B0%E5%AD%97%E8%B4%A7%E5%B8%81%E5%8F%8A%E4%BA%A4%E6%98%93%E5%AF%B9%E4%B8%8A%E6%96%B0"
    # params = {
    #     "c": "48",
    #     "navId": "48",
    #     "hl": "zh-CN"
    # }
    # response = requests.get(url, headers=headers, params=params)
    # # print(response.text)
    # # print(response)



    #英文公告
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
    # print(response.text)
    # print(response)



    soup = BeautifulSoup(response.text,'html.parser')# 使用BeautifulSoup解析响应内容
    content = soup.body# 提取body标签内容下的script
    content = content.find('script', id='__APP_DATA')# 提取<body>标签下的<script>标签
    # print(content)
    # print(content.text,type(content.text))#取目标标签的值
    mes=json.loads(content.text)['appState']['loader']['dataByRouteId']['d9b2']['catalogs']#['dynamicIds']
    # print(mes)
    for info in mes:
        print(info['catalogName'])#前面是中文的后面是英文的
        if (info['catalogName']=="数字货币及交易对上新")or(info['catalogName']=="New Cryptocurrency Listing"):
            df=pd.DataFrame(info['articles'])
    # df=df[df["title"].str.contains("上市")]#只要上市信息【中文频道】
    df=df[df["title"].str.contains("List")]#只要上市信息【英文频道】
    df["releaseDate"]=pd.to_datetime(df['releaseDate'],unit='ms')
    df["releaseDate转换后"]=df["releaseDate"].dt.strftime('%Y-%m-%d %H:%M:%S')#这里是标准时9.30，东八区就是17.30
    df=df.reset_index(drop=True)#重置索引避免后面越界
    df.to_csv("content.csv")
    thisutc=datetime.datetime.utcnow()
    thisnow=thisutc.strftime('%Y-%m-%d %H:%M:%S')
    print(df,thisnow)
    newsnum=0
    for n in range(0,len(df)):
        print(n,df.loc[n])#每一行是index+1
        thisdf=df.loc[n]
        print(thisutc-thisdf.releaseDate)
        # if thisutc-thisdf.releaseDate<=datetime.timedelta(seconds=10*60*60*24*9):#9天
        if thisutc-thisdf.releaseDate<=datetime.timedelta(seconds=15):#10秒内持续下买单，每秒都是不成交就按照对手盘一档（滑点百分之一）进行下单
            newsnum+=0#判断是否有新公告，有新公告就执行下单任务
            print("目标上市公告在10秒内")
            mes="公告内容："+thisdf.title+"公告时间（标准时）："+thisdf.releaseDate转换后+"当前时间（标准时）："+thisnow
            postmessage(mes)
            #需要提前验证一下对手盘一档的金额，单次下单就按照对手盘一档的金额进行
            # thisdf.title#拆解thisdf.title当中（）内的标的，在bitget下对应的订单
    if newsnum==0:
        print("当前没有新公告")
        # if 
        # print("最新一次公告的时间在15分钟之前则清仓换成USDT")
    time.sleep(0.5)
    #休息时间对之前不成交的部分进行撤单处理


# 47.242.111.133【阿里云服务器IP】绑定了之后需要等几分钟才能使用
import pandas as pd
import math
import time
import datetime
#配置gate服务器【下面的报错应该是改了api了】
import gate_api
configuration=gate_api.Configuration(
host="https://api.gateio.ws/api/v4",
key="7bbe5f1899b5fcfdf05b57d92ba603c1",
secret="9e073f55f7abc9bb856c3c02f14e8c44adb1da791f7d0950d13cda3f04579c0c",
)
gateclient=gate_api.ApiClient(configuration)

#查询账户信息
gate_accountclient=gate_api.AccountApi(gateclient)#启动账户API服务器
gate_account=gate_accountclient.get_account_detail()
print("account账户信息",gate_account)

# 获取钱包总余额
gate_walletclient=gate_api.WalletApi(gateclient)#启动钱包API服务器
gate_account=gate_walletclient.get_total_balance()#检查各模块余额
print("各模块资产余额",gate_account,"期货",gate_account.details["futures"].amount,"现货",gate_account.details["spot"].amount)
# gate_account=gate_walletclient.list_sub_account_balances()#检查子账户余额
# gate_account=gate_walletclient.list_sub_account_margin_balances()#检查子账户保证金余额
# gate_account=gate_walletclient.list_sub_account_futures_balances()#检查子账户期货账户余额

# #【合约现货平衡】改成理财现货平衡[应该就是金融账户]gate_spot
# details【-cross_margin:全仓杠杆账户
# -spot:现货账户
# -finance:金融账户
# -margin:杠杆账户
# -quant:量化账户
# -futures:永续合约账户
# -delivery:交割合约账户
# -warrant:warrant 账户
# -cbbc:牛熊证账户】
# gate_futures_amount=float(gate_account.details["futures"].amount)
# gate_spot_amount=float(gate_account.details["spot"].amount)
# print("合约余额",gate_futures_amount,"现货余额",gate_spot_amount)
# if (gate_spot_amount>0)or(gate_futures_amount>0):
#     if (gate_spot_amount-gate_futures_amount)>(gate_spot_amount+gate_futures_amount)*0.1:#这里是差大概百分之五【0.1的一半】就会触发资金管理
#         thisamount=(gate_spot_amount-gate_futures_amount)/2
#         print("现货仓位减去合约仓位较重，需要平衡以下金额的仓位",thisamount)
#         transfer_response =gate_walletclient.transfer(gate_api.Transfer(currency='USDT',settle="USDT",_from='spot',to='futures',amount=thisamount))#合约转现货
#     elif (gate_futures_amount-gate_spot_amount)>(gate_spot_amount+gate_futures_amount)*0.1:#这里是差大概百分之五【0.1的一半】就会触发资金管理
#         thisamount=(gate_spot_amount-gate_futures_amount)/2
#         print("现货仓位减去合约仓位较轻，需要平衡以下金额的仓位",thisamount)
#         transfer_response =gate_walletclient.transfer(gate_api.Transfer(currency='USDT',settle="USDT",_from='futures',to='spot',amount=-thisamount))#合约转现货
#     else:
#         print("资金均匀不用调整")

gate_spotclient=gate_api.SpotApi(gateclient)#启动现货API服务器
#获取gate合约各个标的的手续费
gate_spot_fee=gate_spotclient.get_fee()
print(gate_spot_fee)#gt_maker_fee是使用gt抵扣后的费用{'currency_pair': None, 'debit_fee': 1, 'gt_discount': True, 'gt_maker_fee': '0.0009', 'gt_taker_fee': '0.0009', 'loan_fee': '0.18', 'maker_fee': '0.001', 'point_type': '1', 'taker_fee': '0.001', 'user_id': 462377}
print("手续费",gate_spot_fee.maker_fee,gate_spot_fee.taker_fee)

# 查询深度信息
buysymbol="BTC_USDT"
gate_ticker=gate_spotclient.list_order_book(currency_pair=buysymbol)#当前买卖十档
bid1=gate_ticker.bids[0][0]
bid1v=gate_ticker.bids[0][1]
bid2=gate_ticker.bids[1][0]
bid2v=gate_ticker.bids[1][1]
ask1=gate_ticker.asks[0][0]
ask1v=gate_ticker.asks[0][1]
ask2=gate_ticker.asks[1][0]
ask2v=gate_ticker.asks[1][1]
print("当前十档",gate_ticker)
print(bid1,bid1v,bid2,bid2v,ask1,ask1v,ask2,ask2v,)


# dfordercancelled=pd.DataFrame({})#初始化存储已经撤销订单的列表【只初始化一次,不要重置】
# buysymbol="BTC_USDT"
# while True:
#     dfordercancelled.to_csv(f"___dfordercancelled.csv")
#     dforderthiscancelled=pd.DataFrame({})#初始化存储全部订单的列表【每一轮都可以重置】【仅仅针对开放订单】
#     time.sleep(2)#在这里为撤单函数保留时间【不通过计算挂单时间，因为这里没有针对持仓的冻结说明】
#     # 遍历所有合约交易对，并获取历史 K 线数据  
#     klines = gate_spotclient.list_futures_candlesticks(settle='usdt',contract=buysymbol, limit=20, interval="1m")  
#     data_list = []  
#     for kline in klines: 
#         timestamp = int(kline.t)  
#         date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp))  
#         data_list.append({  
#             "timestamp": timestamp,  
#             "代码": buysymbol,  
#             "日期": date,  
#             "成交额": float(kline.sum),  
#             "收盘": float(kline.c),  
#             "最高": float(kline.h),  
#             "最低": float(kline.l),  
#             "开盘": float(kline.o),  
#             "成交量": float(kline.v),  
#         })  
#     df_line = pd.DataFrame(data_list)
#     df_line["grow"]=df_line["收盘"]/df_line["开盘"]
#     # df_line=df_line[df_line["grow"]>1.001]
#     # print(df_line,len(df_line))
#     # if len(df_line)>=20:
#     df_line=df_line[df_line["grow"]>0.5]#测试
#     print(df_line,len(df_line))
#     if len(df_line)>=2:#测试
#         # thisticker=gate_spotclient.list_futures_order_book(settle='usdt',contract=buysymbol)#当前买卖十档
#         # ask_price_1=thisticker.asks[0].p#卖一价
#         # ask_vol_1=thisticker.asks[0].s#卖一量
#         # bid_price_1=thisticker.bids[0].p#买一价
#         # bid_vol_1=thisticker.bids[0].s#买一量
#         # print("当前十档",thisticker,"卖一",ask_price_1,"买一",bid_price_1)
#         # open_price=ask_price_1#多头开单价格为卖一价格
#         # # futures_order=gate_spotclient.create_futures_order(settle='usdt',futures_order = gate_api.FuturesOrder(contract=buysymbol,size=int(100),price=open_price))
#         # futures_order=gate_spotclient.create_futures_order(
#         #     settle='usdt',futures_order = gate_api.FuturesOrder(
#         #         contract=buysymbol,size=int(100),price="40000"))
#         # print(f"~~~创建新的订单",futures_order)

#         # {'amend_text': '-',
#         # 'auto_size': None,
#         # 'biz_info': '-',
#         # 'close': False,#设置为“true”平仓，“size”设置为 0
#         # 'contract': 'BTC_USDT',#期货交易合同
#         # 'create_time': 1702883594.174,
#         # 'fill_price': '0',
#         # 'finish_as': None,#订单是如何完成的。-filled： 全部填充 -cancelled：手动取消 -liquidated：因清算而取消 -ioc：生效时间为“IOC”，立即完成 -auto_deleveraged：由 ADL 完成 -reduce_only：由
#         # 'finish_time': None,#订单完成时间。如果订单未结，则不予退还
#         # 'iceberg': 0,
#         # 'id': 933479298,
#         # 'is_close': False,#是平仓订单
#         # 'is_liq': False,
#         # 'is_reduce_only': False,
#         # 'left': 100,#剩余待交易规模
#         # 'mkfr': '0.00015',
#         # 'price': '40000',#订单价格。0 表示市价单，将“tif”设置为“ioc”
#         # 'reduce_only': False,
#         # 'refu': 0,
#         # 'size': 100,#订单大小【单位是张】，指定正数进行出价，指定负数进行询价
#         # 'status': 'open',#订单状态 -'open'： 等待交易 -'finished'： 完成
#         # 'stp_act': '-',
#         # 'stp_id': 0,
#         # 'text': 'api',
#         # 'tif': 'gtc',
#         # 'tkfr': '0.00046',
#         # 'user': 462377}
#         open_futures_orders=gate_spotclient.list_futures_orders(settle='usdt',status='open')#获取未成交订单
#         print(f"~~~获取未成交订单",open_futures_orders)
#         # # cancel_futures_orders=gate_spotclient.cancel_futures_orders(settle='usdt',contract=buysymbol)#好像是因为没钱报错
#         # # print(f"~~~撤销所有订单",cancel_futures_orders)
#         for open_futures_order in open_futures_orders:
#             print(open_futures_order)
#             this_futures_order=open_futures_order.id#获取开放订单的id
#             cancel_futures_order=gate_spotclient.cancel_futures_order(settle='usdt',order_id=this_futures_order)#撤空单的返回值是没找到这个订单
#             print(f"~~~撤销个别订单",cancel_futures_order)
#             cancel_vol=cancel_futures_order.left#撤销掉的数量【剩余数量】
#             trade_vol=cancel_futures_order.size-cancel_futures_order.left#已经成交的数量


#     # 固定时间清仓【这里是获取持仓状态】
#     list_futures_positions=gate_spotclient.list_positions(settle='usdt')
#     for futures_position in list_futures_positions:
#         print(f"~~~持仓处理",futures_position)
#         close_contract=futures_position.contract
#         close_size=futures_position.size
#         thisticker=gate_spotclient.list_futures_order_book(settle='usdt',contract=buysymbol)#当前买卖十档
#         ask_price_1=thisticker.asks[0].p#卖一价
#         ask_vol_1=thisticker.asks[0].s#卖一量
#         bid_price_1=thisticker.bids[0].p#买一价
#         bid_vol_1=thisticker.bids[0].s#买一量
#         if close_size>0:
#             #清仓成功之后数据仍然保留在持仓列表当中，但是size为0，这样的话有一个好处，就是所有平仓都是将仓位调整为0，不会过度平仓导致了仓位反转
#             close_price=bid_price_1
#             close_futures_order=gate_spotclient.create_futures_order(
#                 settle='usdt',futures_order = gate_api.FuturesOrder(
#                     contract=close_contract,size=0,price=close_price,close=True))
#             print(close_futures_order)
#     break