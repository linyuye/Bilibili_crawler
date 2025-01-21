from urllib3.util.retry import Retry
import time
import math
import requests
import csv
import json
import pytz
import datetime
import random
import os
import re
def clean_filename(filename):
    """
    清理文件名，将非法字符替换为下划线 _
    """
    illegal_chars = r'[\\/:*?"<>|]'
    cleaned_filename = re.sub(illegal_chars, '_', filename)
    cleaned_filename_1 = re.sub('\r', '_', cleaned_filename)
    return cleaned_filename_1

XOR_CODE = 23442827791579
MASK_CODE = 2251799813685247
MAX_AID = 1 << 51
ALPHABET = "FcwAPNKTMug3GV5Lj7EJnHpWsx4tb8haYeviqBz6rkCy12mUSDQX9RdoZf"
ENCODE_MAP = 8, 7, 0, 5, 1, 3, 2, 4, 6
DECODE_MAP = tuple(reversed(ENCODE_MAP))
BASE = len(ALPHABET)
PREFIX = "BV1"
PREFIX_LEN = len(PREFIX)
CODE_LEN = len(ENCODE_MAP)
def av2bv(aid):
    bvid = [""] * 9
    tmp = (MAX_AID | aid) ^ XOR_CODE
    for i in range(CODE_LEN):
        bvid[ENCODE_MAP[i]] = ALPHABET[tmp % BASE]
        tmp //= BASE
    return PREFIX + "".join(bvid)

def bv2av(bvid) :
    assert bvid[:3] == PREFIX
    bvid = bvid[3:]
    tmp = 0
    for i in range(CODE_LEN):
        idx = ALPHABET.index(bvid[DECODE_MAP[i]])
        tmp = tmp * BASE + idx
    return (tmp & MASK_CODE) ^ XOR_CODE

# 定义目录路径
directory = 'user'
# 初始化存储数据的列表
comment_id_str_list = []
comment_type_list = []

# 遍历目录下的所有文件
for filename in os.listdir(directory):
    # 检查文件是否为CSV文件
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)

        # 打开CSV文件并读取数据
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # 跳过表头（如果有）

            # 将每行数据分别添加到两个列表中
            for row in csv_reader:
                comment_id_str, comment_type = row
                comment_id_str_list.append(comment_id_str)
                comment_type_list.append(int(comment_type))

comment_id_str_list_copy=comment_id_str_list.copy()
comment_type_list_copy=comment_type_list.copy()

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    ps = config['ps']
    start = config['start']
    end = config['end']
    cookies_str = config['cookies_str']
    bili_jct = config['bili_jct']
i = 1
for oid,type in zip(comment_id_str_list,comment_type_list):
    print(f"第{i}次爬取:")
    i = i + 1
    if type == 1:
        with requests.Session() as session:
            retries = Retry(total=3,  # 最大重试次数，好像没有这个函数
                            backoff_factor=0.1,  # 间隔时间会乘以这个数
                            status_forcelist=[500, 502, 503, 504])
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                'Cookie': cookies_str,
                'csrf': bili_jct,
            }
            url_inf = f'https://api.bilibili.com/x/web-interface/view?bvid={av2bv(int(oid))}'
            data = {
                'bvid': av2bv(int(oid)),
            }
            response = session.get(url_inf, params=data, headers=headers)
            data = response.json()
            title = data["data"]["title"]
            clean_title = clean_filename(title)
            file_path_1 = f"comments/{clean_title}_1.csv"
            file_path_2 = f"comments/{clean_title}_2.csv"
            file_path_3 = f"comments/{clean_title}_3.csv"

    else:
        file_path_1 = f"comments/{oid}_1.csv"
        file_path_2 = f"comments/{oid}_2.csv"
        file_path_3 = f"comments/{oid}_3.csv"
    # 重试次数限制
    start = 1
    page = 1
    MAX_RETRIES = 2
    # 重试间隔（秒）
    RETRY_INTERVAL = 3
    beijing_tz = pytz.timezone('Asia/Shanghai')#时间戳转换为北京时间
    one_comments = []
    all_comments = []#构造数据放在一起的容器  总共评论
    all_2_comments = []#构造数据放在一起的容器 二级评论
    comments_current = []
    comments_current_2 = []
    # 建立csv文件
    # with open(file_path_1, mode='w', newline='', encoding='utf-8-sig') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['昵称', '性别', '时间', '点赞', '评论', 'IP属地','等级','uid','rpid'])
    # with open(file_path_2, mode='w', newline='', encoding='utf-8-sig') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['昵称', '性别', '时间', '点赞', '评论', 'IP属地','等级','uid','rpid'])
    with open(file_path_3, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['昵称', '性别', '时间', '点赞', '评论', 'IP属地', '等级', 'uid', 'rpid'])

    with requests.Session() as session:
        retries = Retry(total=3,
                        backoff_factor=0.1,  # 间隔时间会乘以这个数
                        status_forcelist=[500, 502, 503, 504])
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Cookie': cookies_str,
            'csrf': bili_jct,
        }
        url_long = 'https://api.bilibili.com/x/v2/reply/main'
        url_reply = 'https://api.bilibili.com/x/v2/reply/reply'
        data = {
            'next': str(1),
            'type': type,
            'oid': oid,
            'ps': ps,
            'mode': '3'
        }
        response = session.get(url_long, params=data, headers=headers, verify=True)
        if response.status_code == 200:
                json_data = response.json()
                if 'data' in json_data:
                    if 'top_replies' in json_data['data'] and json_data['data']['top_replies'] not in (None, []):
                        top_replies = json_data['data']['top_replies']
                        print(f"本次爬取含有置顶评论")
                        print(response.url)
                        for reply in top_replies:
                            name = reply['member']['uname']
                            sex = reply['member']['sex']
                            ctime = reply['ctime']
                            dt_object = datetime.datetime.fromtimestamp(ctime, datetime.timezone.utc)
                            formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                            like = reply['like']
                            message = reply['content']['message'].replace('\n', ',')
                            location = reply['reply_control'].get('location', '未知')
                            location = location.replace('IP属地：', '') if location else location
                            current_level = reply['member']['level_info']['current_level']
                            mid = str(reply['member']['mid'])
                            rpid = str(reply['rpid'])
                            count = reply['rcount']
                            all_comments.append([name, sex, formatted_time, like, message, location,current_level,mid,rpid])
                            # with open(file_path_1, mode='a', newline='', encoding='utf-8-sig') as file:
                            #     writer = csv.writer(file)
                            #     writer.writerows(all_comments)
                            with open(file_path_3, mode='a', newline='', encoding='utf-8-sig') as file:
                                writer = csv.writer(file)
                                writer.writerows(all_comments)
                            all_comments.clear()
                            if count != 0:
                                print(f"在置顶评论中, 该条回复下面总共含有{count}个二级评论")
                                total_pages = math.ceil(float(count) / float(ps)) if count > 0 else 0
                                for page_pn in range(1, total_pages + 1):
                                    data_2 = {
                                        'type': type,
                                        'oid': oid,
                                        'ps': ps,
                                        'pn': str(page_pn),
                                        'root': rpid
                                    }
                                    response = session.get(url_reply, params=data_2, headers=headers, verify=True)
                                    if response.status_code == 200:
                                        print(f"请求置顶评论状态码：200")
                                        json_data = response.json()
                                        if 'data' in json_data and 'replies' in json_data['data']:
                                            print(response.url)
                                            if not json_data['data']['replies']:
                                                print(f"该页replies为空，没有评论")
                                                continue
                                            for comment in json_data['data']['replies']:
                                                rpid = str(comment['rpid'])
                                                name = comment['member']['uname']
                                                sex = comment['member']['sex']
                                                ctime = comment['ctime']
                                                dt_object = datetime.datetime.fromtimestamp(ctime, datetime.timezone.utc)
                                                formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                                                like = comment['like']
                                                message = comment['content']['message'].replace('\n', ',')
                                                location = comment['reply_control'].get('location', '未知')
                                                location = location.replace('IP属地：', '') if location else location
                                                current_level = comment['member']['level_info']['current_level']
                                                mid = str(comment['member']['mid'])
                                                all_2_comments.append([name, sex, formatted_time, like, message, location,current_level,mid,rpid])
                                                # with open(file_path_2, mode='a', newline='', encoding='utf-8-sig') as file:
                                                #     writer = csv.writer(file)
                                                #     writer.writerows(all_2_comments)
                                                with open(file_path_3, mode='a', newline='', encoding='utf-8-sig') as file:
                                                    writer = csv.writer(file)
                                                    writer.writerows(all_2_comments)
                                                all_2_comments.clear()
                                        else:
                                            print(f"不含有内容")
                                    else:
                                        print(f"请求错误")
                    else:
                        print("该视频/动态不含有置顶评论")
        for page in range(start, end + 1):
            data = {
                'next': str(page),
                'type': type,
                'oid': oid,
                'ps': ps,
                'mode': '3'
            }
            response = session.get(url_long, params=data, headers=headers, verify=True)
            if response.status_code == 200:
                json_data = response.json()
                if 'data' in json_data:
                    if 'replies' in json_data['data'] and json_data['data']['replies']:
                        print(response.url)
                        for comment in json_data['data']['replies']:
                            count = comment['rcount']
                            rpid = str(comment['rpid'])
                            name = comment['member']['uname']
                            sex = comment['member']['sex']
                            ctime = comment['ctime']
                            dt_object = datetime.datetime.fromtimestamp(ctime, datetime.timezone.utc)
                            formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                            like = comment['like']
                            message = comment['content']['message'].replace('\n', ',')
                            location = comment['reply_control'].get('location', '未知')
                            location = location.replace('IP属地：', '') if location else location
                            current_level = comment['member']['level_info']['current_level']
                            mid = str(comment['member']['mid'])
                            all_comments.append([name, sex, formatted_time, like, message, location,current_level,mid,rpid])
                            # with open(file_path_1, mode='a', newline='', encoding='utf-8-sig') as file:
                            #     writer = csv.writer(file)
                            #     writer.writerows(all_comments)
                            with open(file_path_3, mode='a', newline='', encoding='utf-8-sig') as file:
                                writer = csv.writer(file)
                                writer.writerows(all_comments)
                            all_comments.clear()
                            if count != 0:
                                print(f"在第{page}页中,回复id为:{rpid}的评论下含有二级评论, 该条回复下面总共含有{count}个二级评论")
                                total_pages = math.ceil(float(count) / float(ps)) if count > 0 else 0
                                for page_pn in range(1, total_pages + 1):
                                    data_2 = {
                                        'type': type,
                                        'oid': oid,
                                        'ps': ps,
                                        'pn': str(page_pn),
                                        'root': rpid
                                    }
                                    if page_pn == 0:
                                        continue
                                    response = session.get(url_reply, params=data_2, headers=headers, verify=True)
                                    if response.status_code == 200:
                                        json_data = response.json()
                                        print(response.url)
                                        if 'data' in json_data and 'replies' in json_data['data']:
                                            if not json_data['data']['replies']:
                                                print(f"该页replies为空，没有评论")
                                                continue
                                            for comment in json_data['data']['replies']:
                                                rpid = str(comment['rpid'])
                                                name = comment['member']['uname']
                                                sex = comment['member']['sex']
                                                ctime = comment['ctime']
                                                dt_object = datetime.datetime.fromtimestamp(ctime,datetime.timezone.utc)
                                                formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                                                like = comment['like']
                                                message = comment['content']['message'].replace('\n', ',')
                                                location = comment['reply_control'].get('location', '未知')
                                                location = location.replace('IP属地：', '') if location else location
                                                current_level = comment['member']['level_info']['current_level']
                                                mid = str(comment['member']['mid'])
                                                all_2_comments.append([name, sex, formatted_time, like, message, location,current_level,mid,rpid])
                                                # with open(file_path_2, mode='a', newline='',encoding='utf-8-sig') as file:
                                                #     writer = csv.writer(file)
                                                #     writer.writerows(all_2_comments)
                                                with open(file_path_3, mode='a', newline='',encoding='utf-8-sig') as file:
                                                    writer = csv.writer(file)
                                                    writer.writerows(all_2_comments)
                                                all_2_comments.clear()
                                    else:
                                        print(f"获取第{page_pn + 1}页失败。状态码: {response.status_code}")
                                time.sleep(random.uniform(0.3, 0.4))
                        print(f"已经成功爬取第{page}页。")
                    else:
                        print(f"在页面 {page} 的JSON响应中缺少 'replies' 键。跳过此页。")
                        break
                else:
                    print(f"在页面 {page} 的JSON响应中缺少 'data' 键。跳过此页。")
                    break
            else:
                print(f"获取页面 {page} 失败。状态码: {response.status_code}")
            page = page + 1
            time.sleep(random.uniform(0.3, 0.4))
    with open("记录.txt", mode='a', encoding='utf-8') as file:
        if type == 1:
            text_to_write = f"爬取了{oid}视频,类型:{type}\n"
        else:
            text_to_write = f"爬取了{oid}动态,类型：{type}\n"
        file.write(text_to_write)
    time.sleep(random.uniform(2, 3))

    del comment_id_str_list_copy[0]
    del comment_type_list_copy[0]
    data = [[oid, type] for oid, type in zip(comment_id_str_list_copy, comment_type_list_copy)]
    with open("记录.csv", mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print("数据已保存")
