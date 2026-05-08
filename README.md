# 5G 信号可视化看板

## 项目介绍

本项目是"Code with AI"海选赛参赛作品，使用 Python + Streamlit 框架开发，将 5G 路测数据转化为交互式 Web 看板。

## 功能特性

### 基础关卡 ✅
- **数据加载**：使用 pandas 读取 CSV 数据
- **信号地图**：交互式散点地图，经纬度打点显示
- **信号变色**：根据 RSRP 强度变色（绿/黄/红）
- **数据概览**：频段基站数量柱状图 + 终端类型占比图

### 进阶关卡 ⏳
- 侧边栏联动筛选
- 3D 地图展示
- 单元测试

## 交付物清单

1. **源代码** - `app.py` + `requirements.txt`
2. **项目说明文档** - 本 README.md
3. **运行截图** - 截图中
4. **Agent 交互日志** - `AI_PROMPTS.md`

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
streamlit run app.py
```

### 访问看板

浏览器打开：http://localhost:8501

## 数据说明

- **数据来源**：`data/signal_samples.csv`
- **字段说明**：
  - Latitude/Longitude：经纬度
  - CellID：小区ID
  - Band：频段（n28/n41/n78）
  - RSRP_dBm：信号强度
  - SINR_dB：信噪比
  - TerminalType：终端类型（Smartphone/CPE/IoT）
  - Download_Mbps：下载速率

## 技术栈

- Python 3.x
- Streamlit - Web 框架
- Pandas - 数据处理
- Pydeck - 地图可视化
