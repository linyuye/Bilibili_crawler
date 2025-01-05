# Bilibili_crawler 

## ——基于bilibili懒加载api爬取b站动态，视频等评论区工具

基于bilibili懒加载api爬取b站动态，视频等评论区。  
动态评论，视频评论等均能爬取，对于数据请进行去重，爬取评论存在重复。  
制作的若有不足，望大家提提意见。  
失效时间未知！  

> 爬取下来的uid和rpid由于数字过长，当保存时，excel打开会自动省略掉后面位数/采用科学计数法，如果你退出excel后点击保存，导致数据失效。    

## 使用方法

### 一：安装依赖库

```bash
pip install -r requirements.txt
```

### 二：填入用户信息

1. 修改json内容，如果您不会获取cookie等内容，具体使用方法可以看csdn详细教程
2. （F12打开开发者工具，刷新视频/动态，等待某个视频/动态加载完全，点击Network选项，向下滑动评论区，直到加载出一个main?oid开头的东西，oid，type，cookie均在这里面）
3. 如果爬虫中断，可以把产生的“记录.csv”放入user文件夹，删除原来的csv，即可无间断运行

### 三：使用设置
- bili_user_space.py中的mid(line8),为你想爬取的用户uid  
- 运行 bili_user_space.py,之后会再user文件夹中产生一个 uid.csv
- 运行bili_crawler.py,产生的评论在comments文件夹  
- 后缀解读：_1为一级评论 _2为二级评论 _3为三级评论  
