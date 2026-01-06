import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 1. Page Setup
st.set_page_config(page_title="WoS Facility Map", layout="wide")
st.title("❄️ Whiteout Survival: Interactive Facility Map")

# 2. Data Storage Initialization
# We use st.session_state to store custom markers/lines added during the session
if 'custom_markers' not in st.session_state:
    st.session_state.custom_markers = []
if 'custom_lines' not in st.session_state:
    st.session_state.custom_lines = []

# 3. Base Data from your HTML
# We organize your data into a dictionary for easy plotting
facilities = {
    'Construction Lvl 1': {'x': [1068, 537, 138, 138, 138, 666, 1068, 1068], 'y': [138, 138, 138, 666, 1038, 1068, 567, 1068], 'color': '#1f77b4', 'size': 12},
    'Construction Lvl 3': {'x': [486, 768, 867, 327], 'y': [327, 867, 567, 666], 'color': '#1f77b4', 'size': 20},
    'Defense Lvl 2': {'x': [666, 438, 138, 237, 537, 738, 1068, 957], 'y': [138, 267, 537, 768, 1038, 957, 666, 438], 'color': '#d62728', 'size': 15},
    'Defense Lvl 4': {'x': [816, 387, 588], 'y': [717, 717, 327], 'color': '#d62728', 'size': 24},
    'Tech Lvl 1': {'x': [957, 666, 237, 267, 237, 537, 936, 957], 'y': [237, 267, 237, 537, 957, 936, 537, 957], 'color': '#7f7f7f', 'size': 12},
    'Weapon Lvl 4': {'x': [816, 387, 588], 'y': [486, 486, 867], 'color': '#9467bd', 'size': 24},
}

alliances = {
    'HEL HQ': {'x': [728, 697], 'y': [902, 755], 'color': '#6600CC'},
    'KOR HQ': {'x': [610, 518], 'y': [285, 444], 'color': '#993333'},
    'TTN HQ': {'x': [1023, 437], 'y': [275, 643], 'color': '#003366'},
}

# 4. Sidebar Controls for Discord Users
with st.sidebar:
    st.header("🛠️ Tactical Tools")
    
    with st.expander("Add Tactical Marker"):
        m_name = st.text_input("Label", "Enemy Portal")
        m_x = st.number_input("X Coord", 0, 1200, 500)
        m_y = st.number_input("Y Coord", 0, 1200, 500)
        if st.button("Drop Marker"):
            st.session_state.custom_markers.append({'name': m_name, 'x': m_x, 'y': m_y})
            st.rerun()

    with st.expander("Draw March Path"):
        l_x1 = st.number_input("Start X", 0, 1200, 100)
        l_y1 = st.number_input("Start Y", 0, 1200, 100)
        l_x2 = st.number_input("End X", 0, 1200, 300)
        l_y2 = st.number_input("End Y", 0, 1200, 300)
        l_color = st.color_picker("Line Color", "#FF0000")
        if st.button("Draw Path"):
            st.session_state.custom_lines.append({'x': [l_x1, l_x2], 'y': [l_y1, l_y2], 'color': l_color})
            st.rerun()
            
    if st.button("Clear Custom Data"):
        st.session_state.custom_markers = []
        st.session_state.custom_lines = []
        st.rerun()

# 5. Build the Plotly Figure
fig = go.Figure()

# Add Facility Data
for name, attr in facilities.items():
    fig.add_trace(go.Scatter(
        x=attr['x'], y=attr['y'], name=name,
        mode='markers', marker=dict(size=attr['size'], color=attr['color']),
        hovertemplate=f"<b>{name}</b><br>X: %{{x}}<br>Y: %{{y}}<extra></extra>"
    ))

# Add Alliance HQ
for name, attr in alliances.items():
    fig.add_trace(go.Scatter(
        x=attr['x'], y=attr['y'], name=name,
        mode='markers+text', textposition="top center",
        marker=dict(size=28, color=attr['color'], symbol='diamond'),
    ))

# Add Custom User Lines
for line in st.session_state.custom_lines:
    fig.add_trace(go.Scatter(
        x=line['x'], y=line['y'], mode='lines',
        line=dict(color=line['color'], width=3, dash='dash'),
        showlegend=False
    ))

# Add Custom User Markers
if st.session_state.custom_markers:
    df_custom = pd.DataFrame(st.session_state.custom_markers)
    fig.add_trace(go.Scatter(
        x=df_custom['x'], y=df_custom['y'], text=df_custom['name'],
        mode='markers+text', textposition="bottom center",
        marker=dict(size=15, color='yellow', symbol='x'),
        name="Tactical Markers"
    ))

# 6. Layout Styling
fig.update_layout(
    template="plotly_dark",
    xaxis=dict(range=[0, 1200], gridcolor='#333'),
    yaxis=dict(range=[0, 1200], gridcolor='#333'),
    height=800,
    margin=dict(l=0, r=0, t=40, b=0),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)
