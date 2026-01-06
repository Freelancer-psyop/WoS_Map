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
    'Training Lvl 2': {'x': [237, 138, 486, 768, 957, 1068, 4
