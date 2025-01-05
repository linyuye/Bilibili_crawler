from urllib3.util.retry import Retry
import requests
import json
import csv
import time
import random

# 爬取目标uid
mid = 'xxxxxx'  
# 可自定义头
send_header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'

def write_to_csv(filename, data:list):
    with open(filename, mode='a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data)
def extract_basic_info(item):
    basic = item.get('basic', {})
    return [basic.get('comment_id_str', ''),basic.get('comment_type', '')]


    
# 读取设置内容
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    try:
        cookies_str = config.get('cookies_str')
        bili_jct = config.get('bili_jct')
    except KeyError:
        print("config.json文件中缺少必要的键")
        exit()

# 创建CSV文件并写入表头
csv_filename = "./user/"+f'{mid}.csv'
# 写入表头
write_to_csv(csv_filename, ['comment_id_str', 'comment_type'])

# 请求
with requests.Session() as session:
    retries = Retry(
        total=3,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504]
    )
    headers = {
        'User-Agent':send_header,
        'Cookie': cookies_str,
        'csrf': bili_jct,
    }
    url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space'
    data = {'host_mid': mid}

    response = session.get(url, params=data, headers=headers)
    result = response.json()

    # 提取items中的comment_id_str和comment_type
    if 'data' in result and 'items' in result['data']:
        items:list = result.get('data').get('items')
        [write_to_csv(csv_filename, extract_basic_info(item)) for item in items]    

        
    # 初始化offset
    offset = result.get('data').get('offset', None)
    print("the offset is:", offset, "\n\n")

    while True:
        data = {
            'host_mid': mid,
            'next': '2',  # 确保next是字符串
            'offset': str(offset) if offset else ''
        }

        try:
            response = session.get(url, params=data, headers=headers)
            response.raise_for_status()  # 检查请求是否成功
            result = response.json()
            print("the result is:", json.dumps(result, ensure_ascii=False, indent=4))

            # 提取新的offset
            offset = result['data'].get('offset', None)
            if offset is not None:
                print(f"Next offset: {offset}\n\n")
            else:
                print("Offset not found in response data.\n\n")
                break  # 如果没有offset，退出循环

            # 提取items中的comment_id_str和comment_type
            if 'data' in result and 'items' in result['data']:
                items = result['data']['items']
                [write_to_csv(csv_filename, extract_basic_info(item)) for item in items]    
                

            else:
                print("No items found in response data.\n\n")
                break  # 如果没有items，退出循环

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}\n\n")
            break  # 如果请求失败，退出循环

        if 'data' in result and result['data'].get('has_more', False):
            time.sleep(random.uniform(0.1, 0.2))
        else:
            exit()
