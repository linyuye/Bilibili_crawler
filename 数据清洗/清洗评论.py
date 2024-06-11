import pandas as pd

# 读取CSV文件
df = pd.read_csv('用来筛选的数据集.csv', dtype={'rpid': str})
cols_to_check = ['昵称', '时间', '评论']
oid = 自己修改，爬虫告诉你了

unique_df = df.drop_duplicates(subset=cols_to_check, keep='first').copy()

unique_df['rpid'] = unique_df['rpid'].astype(str)

# 构造新列，如果是动态就用动态的链接，
# 样例 https://t.bilibili.com/xxxxxxxxxx/
unique_df['新列'] = 'https://www.bilibili.com/video/BVxxxxxxx/' + '#reply' + unique_df['rpid'].fillna('')

# 将结果保存到新的CSV文件
unique_df.to_csv('comments/带有跳转链接的评论.csv', index=False, encoding='utf-8-sig')
