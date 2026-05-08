import os
import streamlit as st
import pandas as pd
import pydeck as pdk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'signal_samples.csv')

st.set_page_config(page_title="5G 信号可视化看板", layout="wide")

st.title("📡 5G 信号可视化看板")
st.markdown("欢迎来到 **'Code with AI' 极客探索赛**！")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

st.sidebar.header("🔍 数据筛选")
bands = df['Band'].unique().tolist()
selected_bands = st.sidebar.multiselect("选择频段", bands, default=bands)

rsrp_min, rsrp_max = int(df['RSRP_dBm'].min()), int(df['RSRP_dBm'].max())
rsrp_range = st.sidebar.slider("RSRP 范围 (dBm)", rsrp_min, rsrp_max, (rsrp_min, rsrp_max))

terminals = df['TerminalType'].unique().tolist()
selected_terminals = st.sidebar.multiselect("终端类型", terminals, default=terminals)

df_filtered = df[
    (df['Band'].isin(selected_bands)) &
    (df['RSRP_dBm'] >= rsrp_range[0]) &
    (df['RSRP_dBm'] <= rsrp_range[1]) &
    (df['TerminalType'].isin(selected_terminals))
]

st.sidebar.markdown(f"**筛选后数据: {len(df_filtered)} 条**")

st.subheader("🗺️ 信号覆盖地图 (3D视图)")

def get_color(rsrp):
    if rsrp > -90:
        return [0, 255, 0]
    elif rsrp > -110:
        return [255, 255, 0]
    else:
        return [255, 0, 0]

df_map = df_filtered[['Latitude', 'Longitude', 'RSRP_dBm', 'Download_Mbps']].copy()
df_map['color'] = df_map['RSRP_dBm'].apply(get_color)
df_map['height'] = df_map['Download_Mbps'] * 10

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
    map_style='https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
    initial_view_state=pdk.ViewState(
        latitude=df_filtered['Latitude'].mean(),
        longitude=df_filtered['Longitude'].mean(),
        zoom=12,
        pitch=45,
        bearing=0,
    ),
    layers=[layer],
))

st.subheader("📊 数据概览")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**各频段基站数量**")
    band_counts = df_filtered['Band'].value_counts()
    st.bar_chart(band_counts)

with col2:
    st.markdown("**终端类型占比**")
    terminal_counts = df_filtered['TerminalType'].value_counts()
    st.bar_chart(terminal_counts)

st.subheader("📋 数据预览")
st.dataframe(df_filtered.head(10))
