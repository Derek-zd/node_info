# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import logging
import time
import requests
from bs4 import BeautifulSoup

FilFox = "https://filfox.info/zh/"

logging.basicConfig(level=logging.INFO, format='%(asctime)-10s    %(levelname)-20s    %(name)-20s        %(message)-s')


# 爬取首页
def get_html_text(url):
    logger = logging.getLogger("get_html_text")
    logger.info("0")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69"}
        file = requests.get(url, headers=headers)
        file.raise_for_status()  # 如果状态码不是200，引发异常
        file.encoding = 'utf-8'
        return file.text
    except:
        return ""


# 爬取 miner 页面
def get_html_miner_text(url):
    logger = logging.getLogger("get_html_miner_text")
    logger.info("0")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69"}
        file = requests.get(url, headers=headers)
        file.raise_for_status()  # 如果状态码不是200，引发异常
        file.encoding = 'utf-8'
        return file.text
    except:
        logger.error("1")
        return ""


# 获取 首页信息
def get_network_info(fil_fox):
    logger = logging.getLogger("get_network_info")
    logger.info("0")
    soup = BeautifulSoup(fil_fox, 'html.parser')
    block_info = soup.findAll('div', class_='text-left lg:text-center text-sm lg:text-2xl items-start lg:mx-auto')

    block_count = block_info[3].text
    block_reward = block_info[4].text
    # 返回区块奖励，24h挖矿收益
    return [block_count, block_reward]


# 获取miner信息
def get_miner_info(miner_html, id):
    logger = logging.getLogger("get_miner_info")
    logger.info("0")
    soup = BeautifulSoup(miner_html, 'html.parser')

    miner_info = soup.findAll('div', class_='flex items-center justify-between mx-3 mt-2')

    miner_info_reward = miner_info[4].findAll('p', attrs={'text-xs text-gray-800'})[1].text

    # 获取封存效率
    miner_info_mining_efficiency = miner_info[7].findAll('p', attrs={'text-xs text-gray-800'})[1].text

    # 获取lucky 值
    miner_info_lucky = miner_info[8].find('p', attrs={'text-xs text-gray-800'}).text

    # 返回 封存效率效率，lucky 值
    return [miner_info_reward, miner_info_mining_efficiency, miner_info_lucky]


# 主方法，爬取信息
def miner():
    logger = logging.getLogger("miner")
    fil_fox = get_html_text(FilFox)
    block = get_network_info(fil_fox)
    miner = []
    logger.info("区块奖励：" + block[0] + "全网24h挖矿收益：" + block[1])

    miner_id = ['f01155', 'f029585', 'f010202', 'f014699', 'f014686', 'f060805', 'f010038']
    for id in miner_id:
        miner_html = get_html_miner_text(FilFox + "address/" + id)
        miner_info = get_miner_info(miner_html, id)
        logger.info(
            "miner: " + id + "  24h 产币量" + miner_info[0] + "  24h封存效率：" + miner_info[1] + "  Lucky值: " + miner_info[2])
        miner_tmp = "miner:" + id + "--24h产币量" + miner_info[0] + "--24h封存效率:" + miner_info[1] + "--Lucky值:" + \
                    miner_info[2]

        miner.append(miner_tmp)
    miner_tmp = get_network_info(fil_fox)

    miner.append("区块奖励：" + miner_tmp[0]+"全网平均挖矿效率："+miner_tmp[1])
    m = miner[0] + '\n' + miner[1] + '\n' + miner[2] + '\n' + miner[3] + '\n' + miner[4] + '\n' + miner[5] + '\n' + \
        miner[6]+'\n'+miner[7]

    return m


# webhook 发送消息到飞书
def feishu(data):
    webhook = "https://open.feishu.cn/open-apis/bot/hook/502a8627-5913-4201-99f7-baee853a0ed2"
    headers = {'Content-type': 'application/json'}
    r = requests.post(webhook, headers=headers, data=json.dumps(data).encode('utf-8'))

    print(r.text)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 定时执行任务
    while True:
        time_now = time.strftime("%H:%M", time.localtime())
        if time_now == "00:05":
            info = miner()
            data = {
                 "title": "每日节点汇报",
                 "text": "%s" % info
            }
            feishu(data)
            time.sleep(58)

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
