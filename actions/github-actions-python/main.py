#每个任务在30秒后，github action自动停止，所以需要定期重启
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


#返回值拆解
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
time.sleep(2)
#休息时间对之前不成交的部分进行撤单处理
