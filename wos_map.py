import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os

st.set_page_config(page_title="WoS Tactical Map", layout="wide")
st.title("❄️ WoS State Tactical Command")

# --- DATA FILES ---
ALLIANCE_FILE = "wos_alliances.csv"
CLAIMS_FILE = "wos_claims.csv"
PATHS_FILE = "wos_paths.csv"

# --- PERSISTENCE LOGIC ---
def load_data():
    alliances = {
        'HEL': {'x': [728, 697], 'y': [902, 755], 'color': '#6600CC'},
        'KOR': {'x': [610, 518], 'y': [285, 444], 'color': '#993333'},
        'TTN': {'x': [1023, 437], 'y': [275, 643], 'color': '#003366'},
        'PNT': {'x': [781, 764], 'y': [1166, 706], 'color': '#330099'},
        'JFF': {'x': [514, 558], 'y': [908, 756], 'color': '#00FF00'},
        'DRK': {'x': [516, 423], 'y': [129, 539], 'color': '#FF00FF'},
        'ttn': {'x': [288], 'y': [510], 'color': '#415466'}
    }
    if os.path.exists(ALLIANCE_FILE):
        df = pd.read_csv(ALLIANCE_FILE)
        alliances = {row['tag']: {'x': [float(i) for i in str(row['x']).split('|')], 
                                  'y': [float(i) for i in str(row['y']).split('|')], 
                                  'color': row['color']} for _, row in df.iterrows()}
    
    claims = pd.read_csv(CLAIMS_FILE).to_dict('records') if os.path.exists(CLAIMS_FILE) else []
    paths = pd.read_csv(PATHS_FILE).to_dict('records') if os.path.exists(PATHS_FILE) else []
    
    # Convert string paths back to lists
    for p in paths:
        p['x'] = [float(i) for i in str(p['x']).split('|')]
        p['y'] = [float(i) for i in str(p['y']).split('|')]
        
    return alliances, claims, paths

def save_all(alliances, claims, paths):
    # Save Alliances
    a_rows = [{'tag': t, 'x': "|".join(map(str, a['x'])), 'y': "|".join(map(str, a['y'])), 'color': a['color']} for t, a in alliances.items()]
    pd.DataFrame(a_rows).to_csv(ALLIANCE_FILE, index=False)
    # Save Claims
    pd.DataFrame(claims).to_csv(CLAIMS_FILE, index=False)
    # Save Paths
    p_rows = [{'x': "|".join(map(str, p['x'])), 'y': "|".join(map(str, p['y'])), 'color': p['color']} for p in paths]
    pd.DataFrame(p_rows).to_csv(PATHS_FILE, index=False)

# --- INITIALIZE ---
if 'alliances' not in st.session_state:
    st.session_state.alliances, st.session_state.claims, st.session_state.paths = load_data()

# Base Facility Data
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

# --- SIDEBAR ---
with st.sidebar:
    st.header("Alliance Controls")
    
    # 1. Manage HQs
    with st.expander("Move/Add Alliance HQ"):
        allies = list(st.session_state.alliances.keys())
        tag = st.selectbox("Alliance", allies + ["New..."])
        if tag == "New...": tag = st.text_input("New Tag")
        
        col = st.color_picker("Color", st.session_state.alliances.get(tag, {'color': '#FFFFFF'})['color'])
        new_x = st.number_input("X", 0, 1200, value=600)
        new_y = st.number_input("Y", 0, 1200, value=600)
        if st.button("Save HQ"):
            st.session_state.alliances[tag] = {'x': [new_x], 'y': [new_y], 'color': col}
            save_all(st.session_state.alliances, st.session_state.claims, st.session_state.paths)
            st.rerun()

    # 2. Circle Facilities
    with st.expander("🚩 Claim Facility"):
        claim_ally = st.selectbox("Claiming Alliance", list(st.session_state.alliances.keys()))
        fac_type = st.selectbox("Facility", list(facilities.keys()))
        coords = [f"{x},{y}" for x, y in zip(facilities[fac_type]['x'], facilities[fac_type]['y'])]
        coord = st.selectbox("Location", coords)
        if st.button("Mark Claim"):
            cx, cy = map(float, coord.split(','))
            st.session_state.claims.append({'x': cx, 'y': cy, 'color': st.session_state.alliances[claim_ally]['color'], 'ally': claim_ally})
            save_all(st.session_state.alliances, st.session_state.claims, st.session_state.paths)
            st.rerun()

    # 3. Draw Lines
    with st.expander("🛣️ Draw Path"):
        path_ally = st.selectbox("Path Color", list(st.session_state.alliances.keys()), key="p_ally")
        x1 = st.number_input("Start X", 0, 1200)
        y1 = st.number_input("Start Y", 0, 1200)
        x2 = st.number_input("End X", 0, 1200)
        y2 = st.number_input("End Y", 0, 1200)
        if st.button("Add Line"):
            st.session_state.paths.append({'x': [x1, x2], 'y': [y1, y2], 'color': st.session_state.alliances[path_ally]['color']})
            save_all(st.session_state.alliances, st.session_state.claims, st.session_state.paths)
            st.rerun()

    if st.button("Clear All Claims & Paths"):
        st.session_state.claims = []
        st.session_state.paths = []
        save_all(st.session_state.alliances, [], [])
        st.rerun()

# --- DRAW ---
fig = go.Figure()

# Paths (Behind everything)
for p in st.session_state.paths:
    fig.add_trace(go.Scatter(x=p['x'], y=p['y'], mode='lines', line=dict(color=p['color'], width=4), showlegend=False))

# Facilities
for name, attr in facilities.items():
    fig.add_trace(go.Scatter(x=attr['x'], y=attr['y'], name=name, mode='markers', marker=dict(color=attr['color'], size=attr['size'])))

# Claim Circles (Only for facilities)
for c in st.session_state.claims:
    fig.add_trace(go.Scatter(x=[c['x']], y=[c['y']], mode='markers', showlegend=False, hoverinfo='skip',
                             marker=dict(size=40, color='rgba(0,0,0,0)', line=dict(color=c['color'], width=4))))

# Alliances (Clean diamonds)
for tag, attr in st.session_state.alliances.items():
    fig.add_trace(go.Scatter(x=attr['x'], y=attr['y'], name=tag, mode='markers+text', text=[tag]*len(attr['x']),
                             textposition="top center", marker=dict(size=28, color=attr['color'], symbol='diamond')))

fig.update_layout(template="plotly_dark", height=850, xaxis=dict(range=[0, 1200]), yaxis=dict(range=[0, 1200]))
st.plotly_chart(fig, use_container_width=True)
