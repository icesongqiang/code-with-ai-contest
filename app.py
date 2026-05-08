import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="5G 信号可视化看板", layout="wide")

st.title("📡 5G 信号可视化看板")
st.markdown("欢迎来到 **'Code with AI' 极客探索赛**！")

# 数据加载
@st.cache_data
def load_data():
    return pd.read_csv('data/signal_samples.csv')

df = load_data()

# 信号热力/散点地图
st.subheader("🗺️ 信号覆盖地图")

def get_color(rsrp):
    if rsrp > -90:
        return [0, 255, 0]
    elif rsrp > -110:
        return [255, 255, 0]
    else:
        return [255, 0, 0]

df_map = df[['Latitude', 'Longitude', 'RSRP_dBm']].copy()
df_map['color'] = df_map['RSRP_dBm'].apply(get_color)

layer = pdk.Layer(
    'ScatterplotLayer',
    df_map,
    get_position='[Longitude, Latitude]',
    get_fill_color='color',
    get_radius=80,
    pickable=True,
    opacity=0.8,
)

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=df['Latitude'].mean(),
        longitude=df['Longitude'].mean(),
        zoom=12,
        pitch=0,
    ),
    layers=[layer],
))

# 数据概览图表
st.subheader("📊 数据概览")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**各频段基站数量**")
    band_counts = df['Band'].value_counts()
    st.bar_chart(band_counts)

with col2:
    st.markdown("**终端类型占比**")
    terminal_counts = df['TerminalType'].value_counts()
    st.bar_chart(terminal_counts)

# 显示数据预览
st.subheader("📋 数据预览")
st.dataframe(df.head(10))
