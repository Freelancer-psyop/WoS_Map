import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os

st.set_page_config(page_title="WoS Alliance & Facility Map", layout="wide")
st.title("❄️ Whiteout Survival: State Tactical Command")

DATA_FILE = "wos_map_data.csv"

# --- HELPER: COORDINATE CONVERSION ---
def load_alliances():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        return {row['tag']: {'x': [float(i) for i in str(row['x']).split('|')], 
                             'y': [float(i) for i in str(row['y']).split('|')], 
                             'color': row['color']} for _, row in df.iterrows()}
    return {
        'HEL': {'x': [728, 697], 'y': [902, 755], 'color': '#6600CC'},
        'KOR': {'x': [610, 518], 'y': [285, 444], 'color': '#993333'},
        'TTN': {'x': [1023, 437], 'y': [275, 643], 'color': '#003366'},
        'PNT': {'x': [781, 764], 'y': [1166, 706], 'color': '#330099'},
        'JFF': {'x': [514, 558], 'y': [908, 756], 'color': '#00FF00'},
        'DRK': {'x': [516, 423], 'y': [129, 539], 'color': '#FF00FF'},
        'ttn': {'x': [288], 'y': [510], 'color': '#415466'}
    }

def save_alliances(data):
    rows = [{'tag': t, 'x': "|".join(map(str, a['x'])), 'y': "|".join(map(str, a['y'])), 'color': a['color']} for t, a in data.items()]
    pd.DataFrame(rows).to_csv(DATA_FILE, index=False)

# --- DATASETS ---
if 'alliances' not in st.session_state:
    st.session_state.alliances = load_alliances()

facilities = {
    'Construction Lvl 1': {'x': [1068, 537, 138, 138, 138, 666, 1068, 1068], 'y': [138, 138, 138, 666, 1038, 1068, 567, 1068], 'color': '#1f77b4', 'size': 12},
    'Construction Lvl 3': {'x': [486, 768, 867, 327], 'y': [327, 867, 567, 666], 'color': '#1f77b4', 'size': 20},
    'Defense Lvl 2': {'x': [666, 438, 138, 237, 537, 738, 1068, 957], 'y': [138, 267, 537, 768, 1038, 957, 666, 438], 'color': '#d62728', 'size': 15},
    'Defense Lvl 4': {'x': [816, 387, 588], 'y': [717, 717, 327], 'color': '#d62728', 'size': 24},
    'Tech Lvl 1': {'x': [957, 666, 237, 267, 237, 537, 936, 957], 'y': [237, 267, 237, 537, 957, 936, 537, 957], 'color': '#7f7f7f', 'size': 12},
    'Tech Lvl 3': {'x': [867, 327, 327, 867], 'y': [327, 327, 867, 867], 'color': '#7f7f7f', 'size': 20},
    'Weapon Lvl 2': {'x': [867, 366, 138, 138, 438, 1068, 1068, 867], 'y': [138, 138, 438, 867, 1068, 327, 867, 1068], 'color': '#9467bd', 'size': 15},
    'Weapon Lvl 4': {'x': [816, 387, 588], 'y': [486, 486, 867], 'color': '#9467bd', 'size': 24},
    'Gathering Lvl 1': {'x': [957, 537, 138, 87, 267, 636, 1137, 1068], 'y': [138, 87, 237, 666, 1068, 1137, 567, 936], 'color': '#2ca02c', 'size': 12},
    'Production Lvl 1': {'x': [1068, 768, 237, 138, 138, 327, 1068, 957], 'y': [237, 138, 138, 327, 957, 1038, 747, 1068], 'color': '#bcbd22', 'size': 12},
    'Training Lvl 2': {'x': [237, 138, 486, 768, 957, 1068, 486, 768], 'y': [486, 747, 957, 1038, 747, 486, 138, 237], 'color': '#ff7f0e', 'size': 16},
    'Expedition Lvl 3': {'x': [768, 327, 486, 867], 'y': [327, 567, 867, 666], 'color': '#17becf', 'size': 20}
}

# --- SIDEBAR TOOLS ---
with st.sidebar:
    st.header("Strategic Tools")
    with st.expander("Register/Move Alliance"):
        tag = st.text_input("Alliance Tag")
        col = st.color_picker("Color", "#FFFFFF")
        x_c = st.number_input("X Coord", 0, 1200)
        y_c = st.number_input("Y Coord", 0, 1200)
        if st.button("Save Changes"):
            if tag:
                st.session_state.alliances[tag] = {'x': [x_c], 'y': [y_c], 'color': col}
                save_alliances(st.session_state.alliances)
                st.rerun()

# --- MAP RENDERING ---
fig = go.Figure()

# Facilities Layer
for name, attr in facilities.items():
    fig.add_trace(go.Scatter(x=attr['x'], y=attr['y'], name=name, mode='markers', 
                             marker=dict(color=attr['color'], size=attr['size']), legendgroup="Facilities"))

# Alliances Layer (Main HQ)
for tag, attr in st.session_state.alliances.items():
    fig.add_trace(go.Scatter(x=attr['x'], y=attr['y'], name=tag, mode='markers+text',
                             text=[tag]*len(attr['x']), textposition="top center",
                             marker=dict(size=28, color=attr['color'], symbol='diamond'), legendgroup="Alliances"))

# Alliance "Claim" Circles
for tag, attr in st.session_state.alliances.items():
    fig.add_trace(go.Scatter(x=attr['x'], y=attr['y'], mode='markers', showlegend=False, hoverinfo='skip',
                             marker=dict(size=45, color='rgba(0,0,0,0)', line=dict(color=attr['color'], width=3))))

fig.update_layout(template="plotly_dark", height=850, xaxis=dict(range=[0, 1200]), yaxis=dict(range=[0, 1200]),
                  legend=dict(groupclick="toggleitem"))

st.plotly_chart(fig, use_container_width=True)
