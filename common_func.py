import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows下可以使用'SimHei'
# 读取数据
file_path = 'data.csv'  # 请替换为您的文件路径
data = pd.read_csv(file_path)
print(data.head(10))

# 1.只针对 'uid' 列检查空值并移除行
initial_rows = len(data)
data = data.dropna(subset=['uid'])  # 仅检查 'uid' 列
removed_rows = initial_rows - len(data)
print(f"只针对 'uid' 列，去除了 {removed_rows} 行数据")


# 2. 统计每个昵称发言的次数
nickname_counts = data['昵称'].value_counts().reset_index()
nickname_counts.columns = ['昵称', '发言次数']
nickname_counts.to_csv('nickname_counts.csv', index=False, encoding='utf-8-sig')

# 3. 去掉时间列中 "北京时间" 并绘制折线图
data['时间'] = data['时间'].str.replace(' 北京时间', '', regex=False)
data['时间'] = pd.to_datetime(data['时间'])  # 转换为日期时间格式
time_counts_min = data['时间'].dt.floor('min').value_counts().sort_index()  # t 表示分钟

plt.figure(figsize=(40, 24))
plt.plot(time_counts_min.index, time_counts_min.values, marker='o', label="发言人数")
plt.title('不同时间下的发言人数')
plt.xlabel('时间 (按分钟)')
plt.ylabel('发言人数')

# 设置 x 轴显示间隔为每 10 分钟
interval = 30  # 每 10 分钟一个点
tick_positions = time_counts_min.index[::interval]
plt.xticks(tick_positions, labels=[t.strftime('%Y-%m-%d %H:%M') for t in tick_positions], rotation=45)

plt.tight_layout()
plt.savefig('time_plot_min.png')
print("时间折线图已保存为 time_plot_min.png")

# 3.5 去掉时间列中 "北京时间" 并绘制折线图
time_counts_hour = data['时间'].dt.floor('h').value_counts().sort_index()  # h 表示小时

plt.figure(figsize=(10, 6))
plt.plot(time_counts_hour.index, time_counts_hour.values, marker='o', label="发言人数")
plt.title('不同时间下的发言人数')
plt.xlabel('时间 (按小时)')
plt.ylabel('发言人数')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('time_plot_hour.png')
print("时间折线图已保存为 time_plot_hour.png")

# 4. 统计IP属地发言次数并保存
ip_counts = data['IP属地'].value_counts().head(25)

plt.figure(figsize=(10, 8))
ip_counts.plot.pie(autopct='%1.1f%%', startangle=90, labels=ip_counts.index, legend=False, cmap='viridis')
plt.title('IP属地发言次数分布 (前25名)')
plt.tight_layout()
plt.savefig('top_25_ip_pie_chart.png')
print("IP属地发言次数饼状图已绘制并保存为 top_25_ip_pie_chart.png")

# 5. 统计等级并绘制饼状图
valid_levels = [0, 1, 2, 3, 4, 5, 6]
level_counts = data['等级'][data['等级'].isin(valid_levels)].value_counts().sort_index()
# 绘制饼状图
plt.figure(figsize=(8, 8))
level_counts.plot.pie(
    autopct='%1.1f%%',
    startangle=90,
    labels=level_counts.index,
    legend=False,
    cmap='Set3'  # 使用颜色映射
)
plt.title('等级分布 (0-6级)')
plt.ylabel('')  # 去掉默认的y轴标签
# 保存并显示图表
plt.tight_layout()
plt.savefig('level_pie_chart.png')
print("等级饼状图已绘制并保存为 level_pie_chart.png")


# 6. 统计性别并绘制饼状图
data['性别'] = data['性别'].apply(lambda x: x if x in ['男', '女'] else '保密')  # 只保留男女和保密
gender_counts = data['性别'].value_counts()
plt.figure(figsize=(8, 8))
gender_counts.plot.pie(autopct='%1.1f%%', startangle=90, labels=gender_counts.index, legend=True)
plt.title('性别分布')
plt.ylabel('')  # 去掉默认的y轴标签
plt.savefig('gender_pie_chart.png')
print("性别饼状图已保存为 gender_pie_chart.png")

# 7.绘制热力图，统计等级和点赞数的关系
import seaborn as sns
import matplotlib.pyplot as plt
# 过滤等级为 0-6 的数据
valid_levels = [0, 1, 2, 3, 4, 5, 6]
filtered_data = data[data['等级'].isin(valid_levels)]
# 按等级分组，统计点赞数的平均值
heatmap_data = filtered_data.groupby('等级')['点赞'].mean().reset_index()
# 将数据转换为热力图适合的格式
heatmap_pivot = heatmap_data.pivot_table(index='等级', values='点赞')
plt.figure(figsize=(8, 6))
sns.heatmap(
    heatmap_pivot,
    annot=True,  # 在热力图上显示数值
    fmt=".1f",   # 保留一位小数
    cmap="YlGnBu",  # 配色方案
    cbar_kws={'label': '平均点赞数'}  # 设置色条标签
)
plt.title('等级与点赞数关系的热力图')
plt.xlabel('点赞')
plt.ylabel('等级')

# 保存并显示图表
plt.tight_layout()
plt.savefig('level_likes_heatmap.png')
print("等级与点赞数关系的热力图已保存为 level_likes_heatmap.png")


# plt.show() # 可选，直接展示在python中
