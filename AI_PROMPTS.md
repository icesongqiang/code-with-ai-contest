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

### 第十轮：完成进阶关卡

**用户 prompt：**
> 继续完成进阶关卡

**AI response：**
实现进阶关卡三项功能：
1. 侧边栏联动筛选（频段多选、RSRP滑动条、终端类型多选）
2. 3D地图（ColumnLayer，高度随下载速率变化，pitch=45）
3. 实时联动（筛选器变化时地图和图表自动更新）

---

### 第十一轮：补充单元测试

**用户 prompt：**
> ut测试在哪里

**AI response：**
创建了 tests/test_app.py，包含7个测试用例：
- 数据加载测试（3个）
- 颜色映射测试（3个）
- RSRP阈值测试（1个）
- 全部通过验证

---

## 关键代码片段

### 侧边栏筛选器
```python
st.sidebar.header("🔍 数据筛选")
selected_bands = st.sidebar.multiselect("选择频段", bands, default=bands)
rsrp_range = st.sidebar.slider("RSRP 范围 (dBm)", rsrp_min, rsrp_max, (rsrp_min, rsrp_max))
selected_terminals = st.sidebar.multiselect("终端类型", terminals, default=terminals)

df_filtered = df[
    (df['Band'].isin(selected_bands)) &
    (df['RSRP_dBm'] >= rsrp_range[0]) &
    (df['RSRP_dBm'] <= rsrp_range[1]) &
    (df['TerminalType'].isin(selected_terminals))
]
```

### 3D地图（ColumnLayer）
```python
layer = pdk.Layer(
    'ColumnLayer',
    df_map,
    get_position='[Longitude, Latitude]',
    get_fill_color='color',
    get_radius=50,
    pickable=True,
    elevation_scale=1,
    elevation_range=[0, 500],
    extruded=True,
)

st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=df_filtered['Latitude'].mean(),
        longitude=df_filtered['Longitude'].mean(),
        zoom=12,
        pitch=45,
    ),
    layers=[layer],
))
```

### 单元测试
```python
class TestDataLoading:
    def test_load_data_returns_dataframe(self):
        df = load_data()
        assert isinstance(df, pd.DataFrame)

    def test_load_data_has_required_columns(self):
        df = load_data()
        required_cols = ['Latitude', 'Longitude', 'Band', 'RSRP_dBm', 'TerminalType', 'Download_Mbps']
        for col in required_cols:
            assert col in df.columns

class TestColorMapping:
    def test_strong_signal_green(self):
        assert get_color(-80) == [0, 255, 0]
```

---

## 运行说明

1. 安装依赖：`pip install -r requirements.txt`
2. 启动应用：`streamlit run app.py`
3. 浏览器访问：http://localhost:8501
4. 运行测试：`pytest tests/test_app.py -v`

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
