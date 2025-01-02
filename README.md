# Bilibili_crawler 基于bilibili懒加载api爬取b站动态，视频等评论区
可以看csdn详细教程
基于bilibili懒加载api爬取b站动态，视频等评论区。
动态评论，视频评论均能爬取。
必须进行去重，爬取评论有重复的。
制作的比较简陋，希望大家提提意见。
失效时间未知！
## 爬取下来的uid和rpid由于数字过长，当你保存时，excel会自动省略掉后面位数/采用科学计数法，导致数据失效，百度一下怎么解决
# 使用方法
## 一：
0.修改json内容，如果您不会获取cookie等内容请在csdn查阅  
0.1（F12打开开发者工具，刷新视频/动态，等待某个视频/动态加载完全，点击Network选项，向下滑动评论区，直到加载出一个main?oid开头的东西，oid，type，cookie均在这里面）   
1.安装所需要的库，`pip install -r requirements.txt`  
## 二：
1.修改bili_user_space.py中的mid(line8),为你想爬取的用户uid  
2.运行 bili_user_space.py,之后会产生一个 uid.csv，把它放入user文件夹  
3.运行bili_crawler.py,产生的评论在comments文件夹  
4.后缀解读：_1为一级评论 _2为二级评论 _3为三级评论  
