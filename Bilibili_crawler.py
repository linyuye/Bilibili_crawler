from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from requests.packages.urllib3.util.retry import Retry
import time
import math
from urllib.parse import urlparse, parse_qs
import requests
import csv
import json
import pytz
import datetime
from fake_useragent import UserAgent
import random
from requests.adapters import HTTPAdapter
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    ps = config['ps']
    file_path_1 = config['file_path_1']
    file_path_2 = config['file_path_2']
    file_path_3 = config['file_path_3']
    down = config['down']
    up = config['up']
options = {
        'ignore_http_methods': ['GET', 'POST'],  # 提取XHR请求，通常为GET或POST。如果你不希望忽略任何方法，可以忽略此选项或设置为空数组
        'custom_headers': {
            'X-Requested-With': 'XMLHttpRequest'  # 筛选XHR请求
        }
    }
input_method = input("请选择输入方式：\n 1. 通过文件读取（cookie，oid等等）\n 2. 打开浏览器（强烈建议第一次启动使用2，除非您知道您的cookie，视频/动态oid等等）\n")
if input_method == '1':
    # 通过文件读取cookie和csrf等内容
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        oid = config['oid']
        type = config['type']
        cookies_str = config['cookies_str']
        sessdata = config['sessdata']
        bili_jct = config['bili_jct']
else:

    # 配置Selenium

    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)

    print("已经打开浏览器，请耐心等待，模式二运行速度较慢")

    try:
        # 打开目标网页
        driver.get("https://www.bilibili.com/video/BV1Sb421E7rX/?spm_id_from=333.1007.top_right_bar_window_history.content.click")
        print("已经打开网页，请耐心等待，模式二运行速度较慢")
        # 等待直到登录按钮可见
        login_div = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'right-entry__outside') and contains(@class, 'go-login-btn')]"))
        )
        # 点击登录按钮
        login_div.click()

        # 等待一段时间以确保登录界面加载完全
        time.sleep(3)

        # 查找用户名输入框并输入用户名
        username_input = driver.find_element(By.XPATH, "//input[@placeholder='请输入账号']")
        username_input.send_keys("")
        # 查找密码输入框并输入密码
        password_input = driver.find_element(By.XPATH, "//input[@placeholder='请输入密码']")
        password_input.send_keys("")

        # 查找登录按钮并点击
        login_button = driver.find_element(By.XPATH,
                                           "//div[contains(@class,'btn_primary') and contains(text(),'登录')]")
        login_button.click()

        # 等待一段时间确保登录成功
        time.sleep(5)

        print("请点击验证码！")

        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")



    except Exception as e:
        print(
            f"等待或查找元素时出现异常:，可能是由于网络波动或者加载速度过慢，请您重试，推荐您获取cookie后，更改config.json参数，使用模式一")

    # 获取捕获的网络请求
    # 初始化一个变量，用来保存最后一个符合条件的请求
    last_request = None
    # 遍历所有请求
    for request in driver.requests:
        if "main?oid=" in request.url and request.response:
            # 更新last_request为当前请求
            last_request = request
    # 检查是否找到了符合条件的请求
    if last_request:
        print("URL:", last_request.url)
        # 从URL中提取oid
        parsed_url = urlparse(last_request.url)
        query_params = parse_qs(parsed_url.query)
        oid = query_params.get("oid", [None])[0]
        type = query_params.get("type", [None])[0]
        print("OID:", oid)
        print("type:", type)
        # 从WebDriver中获取所有cookies
        all_cookies = driver.get_cookies()

        cookies_dict = {cookie['name']: cookie['value'] for cookie in all_cookies}
        cookies_str = '; '.join([f"{name}={value}" for name, value in cookies_dict.items()])
        # 从cookies中获取bili_jct的值
        bili_jct = cookies_dict.get('bili_jct', '')
        print("bili_jct（就是jscf）:", bili_jct)
        sessdata = cookies_dict.get('SESSDATA', '')
        print("SESSDATA:", sessdata)
        print("Cookies:", all_cookies)
        # 打印请求头
        response = last_request.response
    driver.quit()


# 重试次数限制
MAX_RETRIES = 5
# 重试间隔（秒）
RETRY_INTERVAL = 10
beijing_tz = pytz.timezone('Asia/Shanghai')#时间戳转换为北京时间
ua=UserAgent()#创立随机请求头
one_comments = []
all_comments = []#构造数据放在一起的容器  总共评论
all_2_comments = []#构造数据放在一起的容器 二级评论
comments_current = []
comments_current_2 = []

        # 将所有评论数据写入CSV文件
with open(file_path_1, mode='a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['昵称', '性别', '时间', '点赞', '评论', 'IP属地','二级评论条数','等级','uid','rpid'])
    writer.writerows(all_comments)
with open(file_path_2, mode='a', newline='', encoding='utf-8-sig') as file:#二级评论条数
    writer = csv.writer(file)
    writer.writerow(['昵称', '性别', '时间', '点赞', '评论', 'IP属地','二级评论条数,条数相同说明在同一个人下面','等级','uid','rpid'])
    writer.writerows(all_2_comments)
with open(file_path_3, mode='a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['昵称', '性别', '时间', '点赞', '评论', 'IP属地', '二级评论条数', '等级', 'uid', 'rpid'])
    writer.writerows(all_comments)


def fetch_comments(session, url, params, headers):
    response = session.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def process_comment(comment, file_path_1, file_path_3):
    rpid = str(comment['rpid'])
    name = comment['member']['uname']
    sex = comment['member']['sex']
    ctime = comment['ctime']
    dt_object = datetime.datetime.fromtimestamp(ctime, datetime.timezone.utc)
    formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S') + ' 北京时间'
    like = comment['like']
    message = comment['content']['message'].replace('\n', ',')
    location = comment['reply_control'].get('location', '未知')
    location = location.replace('IP属地：', '') if location else location
    current_level = comment['member']['level_info']['current_level']
    mid = str(comment['member']['mid'])
    count = comment['rcount']

    comment_data = [name, sex, formatted_time, like, message, location, count, current_level, mid, rpid]

    write_to_csv(file_path_1, [comment_data])
    write_to_csv(file_path_3, [comment_data])

    return count, rpid


def process_reply(comment, file_path_2, file_path_3):
    rpid = str(comment['rpid'])
    name = comment['member']['uname']
    sex = comment['member']['sex']
    ctime = comment['ctime']
    dt_object = datetime.datetime.fromtimestamp(ctime, datetime.timezone.utc)
    formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S') + ' 北京时间'
    like = comment['like']
    message = comment['content']['message'].replace('\n', ',')
    location = comment['reply_control'].get('location', '未知')
    location = location.replace('IP属地：', '') if location else location
    current_level = comment['member']['level_info']['current_level']
    mid = str(comment['member']['mid'])
    count = 0  # 二级评论没有回复数

    reply_data = [name, sex, formatted_time, like, message, location, count, current_level, mid, rpid]

    write_to_csv(file_path_2, [reply_data])
    write_to_csv(file_path_3, [reply_data])


def write_to_csv(file_path, data):
    with open(file_path, mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def fetch_replies(session, url_reply, type, oid, ps, rpid, count, headers, file_path_2, file_path_3):
    if count is None or count <= 0:
        print(f"评论 {rpid} 没有回复或回复数量异常")
        return
    total_pages = math.ceil(int(count) / int(ps)) if count > 0 else 0
    for page_pn in range(1, total_pages + 1):  # 从1开始,跳过第0页
        data_2 = {
            'type': type,
            'oid': oid,
            'ps': ps,
            'pn': str(page_pn),
            'root': rpid
        }
        json_data = fetch_comments(session, url_reply, data_2, headers)
        if json_data and 'data' in json_data and 'replies' in json_data['data']:
            if not json_data['data']['replies']:
                print(f"该页replies为空，没有评论")
                continue
            for comment in json_data['data']['replies']:
                process_reply(comment, file_path_2, file_path_3)
        time.sleep(random.uniform(0.05, 0.1))


def main_scraper(session, headers, url_long, url_reply, type, oid, ps, down, up, file_path_1, file_path_2, file_path_3):
    # 处理置顶评论
    data = {
        'next': '1',
        'type': type,
        'oid': oid,
        'ps': ps,
        'mode': '3'
    }
    json_data = fetch_comments(session, url_long, data, headers)
    if json_data and 'data' in json_data:
        if 'top_replies' in json_data['data'] and json_data['data']['top_replies']:
            print("本次爬取含有置顶评论")
            for reply in json_data['data']['top_replies']:
                count, rpid = process_comment(reply, file_path_1, file_path_3)
                if count != 0:
                    print(f"在置顶评论中, 该条回复下面总共含有{count}个二级评论")
                    fetch_replies(session, url_reply, type, oid, ps, rpid, count, headers, file_path_2, file_path_3)
        else:
            print("该视频/动态不含有置顶评论")

    # 处理普通评论
    for page in range(down, up + 1):
        data = {
            'next': str(page),
            'type': type,
            'oid': oid,
            'ps': ps,
            'mode': '3'
        }
        json_data = fetch_comments(session, url_long, data, headers)
        if json_data and 'data' in json_data and 'replies' in json_data['data']:
            for comment in json_data['data']['replies']:
                count, rpid = process_comment(comment, file_path_1, file_path_3)
                if count != 0:
                    print(f"在第{page}页中第{rpid}含有二级评论, 该条回复下面总共含有{count}个二级评论")
                    fetch_replies(session, url_reply, type, oid, ps, rpid, count, headers, file_path_2, file_path_3)
            print(f"已经成功爬取第{page}页。")
        else:
            print(f"在页面 {page} 的JSON响应中缺少必要的键。跳过此页。")
        time.sleep(random.uniform(0.1, 0.2))


def run_scraper(cookies_str, sessdata, bili_jct, type, oid, ps, down, up, file_path_1, file_path_2, file_path_3):
    with requests.Session() as session:
        retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        session.mount('https://', requests.adapters.HTTPAdapter(max_retries=retries))

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Cookie': cookies_str,
            'SESSDATA': sessdata,
            'csrf': bili_jct,
        }

        url_long = 'https://api.bilibili.com/x/v2/reply/main'
        url_reply = 'https://api.bilibili.com/x/v2/reply/reply'

        main_scraper(session, headers, url_long, url_reply, type, oid, ps, down, up, file_path_1, file_path_2,
                     file_path_3)

run_scraper(cookies_str, sessdata, bili_jct, type, oid, ps, down, up, file_path_1, file_path_2, file_path_3)

