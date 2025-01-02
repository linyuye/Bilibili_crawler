from urllib3.util.retry import Retry
import requests
import json
import csv
import time
import random

mid = '356113685'

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    cookies_str = config['cookies_str']
    bili_jct = config['bili_jct']
# 创建CSV文件并写入表头
csv_filename = f'{mid}.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['comment_id_str', 'comment_type'])  # 写入表头

with requests.Session() as session:
    retries = Retry(total=3,  # 最大重试次数，好像没有这个函数
                    backoff_factor=0.1,  # 间隔时间会乘以这个数
                    status_forcelist=[500, 502, 503, 504])
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Cookie': cookies_str,
        'csrf': bili_jct,
    }
    url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space'
    data = {
        'host_mid': mid,
    }
    response = session.get(url, params=data, headers=headers)
    result = response.json()
    # 提取items中的comment_id_str和comment_type
    if 'data' in result and 'items' in result['data']:
        items = result['data']['items']
        for item in items:
            if 'basic' in item:
                comment_id_str = item['basic'].get('comment_id_str', '')
                comment_type = item['basic'].get('comment_type', '')
                # 将数据写入CSV文件
                with open(csv_filename, mode='a', newline='', encoding='utf-8') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([comment_id_str, comment_type])
    # 初始化offset
    if 'data' in result and 'offset' in result['data']:
        offset = result['data']['offset']
        print(offset)
    while True:
        data = {
            'host_mid': mid,
            'next': '2',  # 确保next是字符串
            'offset': str(offset)
        }

        try:
            response = session.get(url, params=data, headers=headers)
            response.raise_for_status()  # 检查请求是否成功
            result = response.json()
            print(result)

            # 提取新的offset
            if 'data' in result and 'offset' in result['data']:
                offset = result['data']['offset']
                print(f"Next offset: {offset}")  # 打印新的offset值
            else:
                print("Offset not found in response data.")
                break  # 如果没有offset，退出循环

            # 提取items中的comment_id_str和comment_type
            if 'data' in result and 'items' in result['data']:
                items = result['data']['items']
                for item in items:
                    if 'basic' in item:
                        comment_id_str = item['basic'].get('comment_id_str', '')
                        comment_type = item['basic'].get('comment_type', '')
                        # 将数据写入CSV文件
                        with open(csv_filename, mode='a', newline='', encoding='utf-8') as csv_file:
                            csv_writer = csv.writer(csv_file)
                            csv_writer.writerow([comment_id_str, comment_type])
            else:
                print("No items found in response data.")
                break  # 如果没有items，退出循环
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break  # 如果请求失败，退出循环
        if 'data' in result and result['data']['has_more']:
            time.sleep(random.uniform(0.1, 0.2))
        else:
            exit()
