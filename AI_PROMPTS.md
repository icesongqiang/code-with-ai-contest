# Agent 交互日志

**团队名称：** AI 4 Whatever
**成员名单：** 宋强 00452518, 林波 00478505, 刘磊 00845054
**使用的 AI Coding Agent 工具：** opencode (本对话)

---

## 🤖 实际交互记录

### 第一轮：读取任务要求

**用户 prompt：**
> 阅读readme.md, 完成*基础关卡*编码

**AI response：**
读取了 README.md，理解了基础关卡要求：
- 数据加载：pandas 读取 CSV
- 信号地图：st.map 或 pydeck，经纬度打点
- RSRP 变色：>-90dBm 绿色，<-110dBm 红色
- 数据概览：频段基站数量柱状图 + 终端类型占比图

---

### 第二轮：初始代码编写

**用户 prompt：**
> (无额外prompt，使用 Read 工具查看数据文件)

**AI response：**
查看了 data/signal_samples.csv 的数据结构，包含字段：
- Latitude, Longitude, CellID, Band, RSRP_dBm, SINR_dB, TerminalType, Download_Mbps

编写了初始 app.py，包含基本框架和提示信息。

---

### 第三轮：实现地图功能

**用户 prompt：**
> 端口没打开

**AI response：**
检查并修复了端口问题，使用 powershell 后台启动 Streamlit 服务。

---

### 第四轮：用户询问源码

**用户 prompt：**
> 源码改了吗

**AI response：**
确认源码已修改，实现了：
1. pandas 读取 CSV
2. pydeck 散点地图
3. RSRP 变色逻辑
4. 频段和终端类型图表

---

### 第五轮：用户指出问题

**用户 prompt：**
> 没有地图的经纬度呢

**AI response：**
检查数据确认经纬度存在，将代码改为使用 st.map() 实现地图显示。

---

### 第六轮：检查是否符合要求

**用户 prompt：**
> 再检查下是否符合要求

**AI response：**
逐项检查基础关卡要求：
- ✅ 数据加载 - pandas 读取 CSV
- ✅ 信号地图 - 经纬度打点
- ✅ RSRP变色 - 绿色/黄色/红色
- ✅ 频段基站数量柱状图
- ✅ 终端类型占比图

---

### 第七轮：完善交付物

**用户 prompt：**
> 然后根据 readme 44要求完善

**AI response：**
完善了 4 项交付物：
1. 源代码：app.py + requirements.txt
2. 项目说明文档：README.md（重写）
3. 运行截图：需手动截图
4. Agent交互日志：AI_PROMPTS.md（本文件）

---

### 第八轮：回答 Git Tag 问题

**用户 prompt：**
> github网页上如何加git tag

**AI response：**
说明 GitHub 网页不支持直接创建 tag，需通过 git 命令推送，并提供了具体命令。

---

### 第九轮：回答交互日志问题

**用户 prompt：**
> 交互日志是怎么生成的

**AI response：**
解释交互日志可以手动记录或从工具导出，并询问是否需要使用实际的交互记录替换。

---

## 关键代码片段

### 数据加载
```python
@st.cache_data
def load_data():
    return pd.read_csv('data/signal_samples.csv')
```

### 信号地图（RSRP变色）
```python
def get_color(rsrp):
    if rsrp > -90:
        return [0, 255, 0]  # 绿色
    elif rsrp > -110:
        return [255, 255, 0]  # 黄色
    else:
        return [255, 0, 0]  # 红色
```

### 数据概览图表
```python
band_counts = df['Band'].value_counts()
st.bar_chart(band_counts)

terminal_counts = df['TerminalType'].value_counts()
st.bar_chart(terminal_counts)
```

---

## 运行说明

1. 安装依赖：`pip install -r requirements.txt`
2. 启动应用：`streamlit run app.py`
3. 浏览器访问：http://localhost:8501
