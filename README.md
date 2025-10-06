# Bilibili_crawler 

> **基于 Bilibili API 的评论爬取工具集**  
> 支持视频评论、动态评论的批量爬取，包含主评论和楼中楼评论，并提供数据可视化分析功能

---

## 📋 项目简介

本项目是一个完整的 B 站评论爬虫工具集，基于 Bilibili 懒加载 API 实现。主要功能包括：

- ✅ 爬取视频评论（支持 BV 号和 AV 号）
- ✅ 爬取动态评论
- ✅ 批量爬取指定用户的所有动态及其评论
- ✅ 支持主评论和二级评论（楼中楼）的完整获取
- ✅ 自动处理置顶评论
- ✅ 支持断点续爬（手动）
- ✅ 数据可视化分析（时间分布、地域分布、等级分布等）

> ⚠️ **重要提示**：  
> - 爬取的 UID 和 RPID 数字较长，Excel 打开时会自动转为科学计数法，**请勿直接保存**，否则数据会失效
> - 建议使用 CSV 编辑器或导入 Excel 时设置为文本格式
> - 本工具仅供学习交流使用，请遵守 Bilibili 相关协议，勿用于商业用途

---

## 🚀 快速开始

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

**依赖包列表**：
- `requests` - HTTP 请求库
- `urllib3` - URL 处理库
- `pandas` - 数据分析（用于 common_func.py）
- `matplotlib` - 数据可视化（用于 common_func.py）
- `seaborn` - 高级数据可视化（用于 common_func.py）
- `pytz` - 时区处理

### 2️⃣ 配置文件设置

编辑 `config.json` 文件，填入您的 Bilibili 账号信息：

```json
{
  "cookies_str": "写入您的cookies",
  "bili_jct": "cookie中的bili_jct",
  "ps": "20",
  "start": 1,
  "end": 99999
}
```

#### 如何获取 Cookie 和参数：

1. 打开 Bilibili 网站，登录您的账号
2. 按 `F12` 打开浏览器开发者工具
3. 切换到 `Network`（网络）选项卡
4. 刷新页面并向下滑动评论区
5. 在请求列表中找到 `main?oid=` 开头的请求
6. 点击该请求，在 `Headers` 中可以找到：
   - `Cookie`：复制完整的 Cookie 字符串到 `cookies_str`
   - `bili_jct`：从 Cookie 中提取 `bili_jct` 字段的值
   - `oid`：视频或动态的 ID
   - `type`：类型（1=视频，11=图文动态，17=转发/纯文字动态等）

**参数说明**：
- `cookies_str`：您的完整 Cookie 字符串（必填）
- `bili_jct`：CSRF Token，从 Cookie 中提取（必填）
- `ps`：每页评论数量，建议 20（1-20）
- `start`：起始页码，默认 1（可选）
- `end`：结束页码，默认 99999（可选）

---

## 📦 项目文件说明

### 核心爬虫文件

| 文件名 | 功能描述 | 使用场景 |
|--------|---------|---------|
| `bili_user_space.py` | 爬取指定用户的所有动态列表 | 批量爬取某个 UP 主的所有动态(视频)oid |
| `Bilibili_crawler.py` | 批量爬取评论主程序 | 根据 user 文件夹中的列表批量爬取 |
| `simple_bili_crawler.py` | 单个视频/动态评论爬取 | 快速爬取单个目标的评论 |
| `b站使用wbi签名的爬取方式.py` | 使用 WBI 签名的爬取方式（仅作学习用） | 应对 B 站 API 签名验证 |
| `bv2oid.py` | BV 号与 AV 号互转工具 | 视频 ID 格式转换 |
| `common_func.py` | 数据分析和可视化脚本 | 对爬取的数据进行统计分析 |

### 配置和数据文件

| 文件/文件夹 | 说明 |
|------------|------|
| `config.json` | 配置文件（Cookie、参数等） |
| `user/` | 存放待爬取的动态列表（CSV 格式） |
| `comments/` | 存放爬取的评论数据（CSV 格式） |
| `记录.csv` / `记录.txt` | 爬取进度记录，用于断点续爬 |

---

## 📖 使用教程

### 方式一：爬取指定用户的所有动态评论

**步骤：**

1. **编辑 `bili_user_space.py`**
   - 修改第 8 行的 `mid` 为目标用户的 UID
   ```python
   mid = 'xxxxxx'  # 替换为目标用户的 UID
   ```

2. **运行脚本获取动态列表**
   ```bash
   python bili_user_space.py
   ```
   - 会在 `user/` 文件夹中生成 `{uid}.csv` 文件
   - 该文件包含该用户所有动态的 `comment_id_str` 和 `comment_type`

3. **批量爬取评论**
   ```bash
   python Bilibili_crawler.py
   ```
   - 自动读取 `user/` 文件夹中的所有 CSV 文件
   - 逐个爬取每条动态的评论
   - 评论保存在 `comments/` 文件夹中

**输出文件说明**：
- `{标题}_1.csv`：主评论（一级评论）
- `{标题}_2.csv`：子评论（楼中楼，二级评论）
- `{标题}_3.csv`：总评论（包含一级和二级）

### 方式二：爬取单个视频/动态的评论

**步骤：**

1. **修改 `config.json`**
   - 添加以下字段：
   ```json
   {
     "oid": "视频或动态的ID",
     "type": 1,
     "file_path_1": "comments/主评论.csv",
     "file_path_2": "comments/子评论.csv",
     "file_path_3": "comments/总评论.csv",
     "down": 1,
     "up": 100
   }
   ```

2. **运行脚本**
   ```bash
   python simple_bili_crawler.py
   ```

**type 参数说明**：
- `1`：视频评论
- `11`：图文动态评论
- `17`：转发/文字动态评论

### 方式三：使用 WBI 签名方式爬取

部分接口需要 WBI 签名验证，可使用此方式：

1. **编辑 `b站使用wbi签名的爬取方式.py`**
   - 修改第 54 行和第 82 行的 `oid` 参数

2. **运行脚本**
   ```bash
   python b站使用wbi签名的爬取方式.py
   ```

---

## 📊 数据分析功能

使用 `common_func.py` 可以对爬取的评论数据进行可视化分析：

### 功能列表

1. **昵称发言次数统计**：生成 `nickname_counts.csv`
2. **时间分布折线图**：
   - `time_plot_min.png`（按分钟）
   - `time_plot_hour.png`（按小时）
3. **IP 属地分布饼图**：`top_25_ip_pie_chart.png`（前 25 名）
4. **等级分布饼图**：`level_pie_chart.png`（0-6 级）
5. **性别分布饼图**：`gender_pie_chart.png`
6. **等级与点赞数热力图**：`level_likes_heatmap.png`

### 使用方法

```bash
python common_func.py
```

**注意**：需要将爬取的评论 CSV 文件重命名为 `data.csv` 并放在同一目录下。

---

## 🔧 工具函数

### BV 号与 AV 号互转

```bash
python bv2oid.py
```

功能：
- `av2bv(aid)`：AV 号转 BV 号
- `bv2av(bvid)`：BV 号转 AV 号

---

## 📌 常见问题

### Q1：爬虫中断后如何继续？
**A**：将生成的 `记录.csv` 放入 `user/` 文件夹，删除原来的 CSV 文件，脚本会自动跳过已爬取的内容。

### Q2：为什么爬取的数据有重复？
**A**：由于 API 懒加载机制，可能存在重复数据，请在分析前进行去重处理。

### Q3：Excel 打开 CSV 后数字变成科学计数法？
**A**：
- 方法 1：使用记事本或 VS Code 打开 CSV
- 方法 2：导入 Excel 时将 UID 和 RPID 列设置为文本格式
- 方法 3：使用 pandas 读取：`pd.read_csv('file.csv', dtype={'uid': str, 'rpid': str})`

### Q4：Cookie 失效怎么办？
**A**：重新登录 Bilibili，按照上述方法重新获取 Cookie 和 bili_jct。

### Q5：爬取速度太快会被封吗？
**A**：脚本已内置随机延时（0.2-0.4 秒），正常使用不会被封。如果担心，可以适当增加延时时间。

---

## ⚠️ 免责声明

- 本项目仅供学习交流使用，请勿用于商业用途
- 使用本工具时请遵守 Bilibili 用户协议和相关法律法规
- 请勿频繁大量爬取，避免对服务器造成压力
- 因使用本工具产生的任何法律责任由使用者自行承担

---

## 📝 开发日志

- **2024 年**：初始版本发布
- 支持视频和动态评论爬取
- 新增批量爬取功能
- 新增数据可视化分析
- 新增 WBI 签名支持

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

如果本项目对您有帮助，欢迎点个 Star ⭐

---

**最后更新时间**：2025 年 10 月 6 日  
