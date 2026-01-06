import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="WoS Tactical Map", layout="wide")
st.title("🛡️ WoS Alliance Territory & Path Planner")

# 1. Initialize custom storage for the session
if 'claims' not in st.session_state:
    st.session_state.claims = [] # Stores which alliance claimed which facility
if 'paths' not in st.session_state:
    st.session_state.paths = []  # Stores tactical lines

# 2. Your Data
facilities = {
    'Construction Lvl 1': {'x': [1068, 537, 138, 138, 138, 666, 1068, 1068], 'y': [138, 138, 138, 666, 1038, 1068, 567, 1068], 'color': '#1f77b4', 'size': 12},
    'Construction Lvl 3': {'x': [486, 768, 867, 327], 'y': [327, 867, 567, 666], 'color': '#1f77b4', 'size': 20},
    'Defense Lvl 2': {'x': [666, 438, 138, 237, 537, 738, 1068, 957], 'y': [138, 267, 537, 768, 1038, 957, 666, 438], 'color': '#d62728', 'size': 15},
    'Defense Lvl 4': {'x': [816, 387, 588], 'y': [717, 717, 327], 'color': '#d62728', 'size': 24},
    'Tech Lvl 1': {'x': [957, 666, 237, 267, 237, 537, 936, 957], 'y': [237, 267, 237, 537, 957, 936, 537, 957], 'color': '#7f7f7f', 'size': 12},
    'Weapon Lvl 4': {'x': [816, 387, 588], 'y': [486, 486, 867], 'color': '#9467bd', 'size': 24},
    'Gathering Lvl 1': {'x': [957, 537, 138, 87, 267, 636, 1137, 1068], 'y': [138, 87, 237, 666, 1068, 1137, 567, 936], 'color': '#2ca02c', 'size': 12},
    'Production Lvl 1': {'x': [1068, 768, 237, 138, 138, 327, 1068, 957], 'y': [237, 138, 138, 327, 957, 1038, 747, 1068], 'color': '#bcbd22', 'size': 12},
    'Training Lvl 2': {'x': [237, 138, 486, 768, 957, 1068, 486, 768], 'y': [486, 747, 957, 1038, 747, 486, 138, 237], 'color': '#ff7f0e', 'size': 16},
    'Expedition Lvl 3': {'x': [768, 327, 486, 867], 'y': [327, 567, 867, 666], 'color': '#17becf', 'size': 20}
}

alliances = {
    'HEL': {'x': [728, 697], 'y': [902, 755], 'color': '#6600CC'},
    'KOR': {'x': [610, 518], 'y': [285, 444], 'color': '#993333'},
    'TTN': {'x': [1023, 437], 'y': [275, 643], 'color': '#003366'},
    'PNT': {'x': [781, 764], 'y': [1166, 706], 'color': '#330099'},
    'JFF': {'x': [514, 558], 'y': [908, 756], 'color': '#00FF00'},
    'DRK': {'x': [516, 423], 'y': [129, 539], 'color': '#FF00FF'},
    'ttn': {'x': [288], 'y': [510], 'color': '#415466'}
}

# 3. Sidebar: User Interaction
with st.sidebar:
    st.header("Alliance Tools")
    
    # Tool 1: Mark Facility Ownership
    with st.expander("🚩 Claim a Facility"):
        target_alliance = st.selectbox("Select Alliance", list(alliances.keys()))
        target_fac_type = st.selectbox("Facility Type", list(facilities.keys()))
        
        # Filter coordinates for that facility type
        coords = [f"{x}, {y}" for x, y in zip(facilities[target_fac_type]['x'], facilities[target_fac_type]['y'])]
        selected_coord = st.selectbox("Exact Coordinates", coords)
        
        if st.button("Mark as Claimed"):
            cx, cy = map(int, selected_coord.split(", "))
            st.session_state.claims.append({
                'alliance': target_alliance, 
                'x': cx, 'y': cy, 
                'color': alliances[target_alliance]['color']
            })
            st.rerun()

    # Tool 2: Draw Path
    with st.expander("🛣️ Draw Connection Path"):
        path_alliance = st.selectbox("Alliance Path Color", list(alliances.keys()), key="path_ally")
        p_x1 = st.number_input("Start X", 0, 1200, 500)
        p_y1 = st.number_input("Start Y", 0, 1200, 500)
        p_x2 = st.number_input("End X", 0, 1200, 600)
        p_y2 = st.number_input("End Y", 0, 1200, 600)
        
        if st.button("Add Path Segment"):
            st.session_state.paths.append({
                'x': [p_x1, p_x2], 
                'y': [p_y1, p_y2], 
                'color': alliances[path_alliance]['color']
            })
            st.rerun()

    if st.button("Reset Map"):
        st.session_state.claims = []
        st.session_state.paths = []
        st.rerun()

# 4. Create Figure
fig = go.Figure()

# Draw User-Defined Paths FIRST (so they stay behind markers)
for path in st.session_state.paths:
    fig.add_trace(go.Scatter(
        x=path['x'], y=path['y'], mode='lines',
        line=dict(color=path['color'], width=4),
        hoverinfo='skip', showlegend=False
    ))

# Draw Facility Base Markers
for name, attr in facilities.items():
    fig.add_trace(go.Scatter(
        x=attr['x'], y=attr['y'], name=name,
        mode='markers', marker=dict(size=attr['size'], color=attr['color']),
        legendgroup="Facilities"
    ))

# Draw Alliance HQ Markers
for name, attr in alliances.items():
    fig.add_trace(go.Scatter(
        x=attr['x'], y=attr['y'], name=name,
        mode='markers+text', text=[name]*len(attr['x']),
        textposition="top center",
        marker=dict(size=25, color=attr['color'], symbol='diamond'),
        legendgroup="Alliances"
    ))

# Draw "Claim" Circles around facilities
for claim in st.session_state.claims:
    fig.add_trace(go.Scatter(
        x=[claim['x']], y=[claim['y']],
        mode='markers',
        marker=dict(
            size=35, color='rgba(0,0,0,0)',
            line=dict(color=claim['color'], width=4)
        ),
        name=f"Claimed by {claim['alliance']}",
        showlegend=False
    ))

# 5. Final Styling
fig.update_layout(
    template="plotly_dark",
    xaxis=dict(range=[0, 1200], title="X Coordinate"),
    yaxis=dict(range=[0, 1200], title="Y Coordinate"),
    height=850,
    legend=dict(groupclick="toggleitem")
)

st.plotly_chart(fig, use_container_width=True)
