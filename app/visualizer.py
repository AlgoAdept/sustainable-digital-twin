from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os
import threading
# Color mapping based on node role
ROLE_COLORS = {
    'Product': '#FFADAD',    # soft red
    'Store': '#A0C4FF',      # light blue
    'Supplier': '#B5E48C',   # light green
    'NGO': '#FDCB6E',        # peach
    'default': '#D3D3D3'     # light grey
}

def get_node_color(labels):
    for label in labels:
        if label in ROLE_COLORS:
            return ROLE_COLORS[label]
    return ROLE_COLORS['default']

def get_color_by_carbon(score):
    if score <= 30:
        return '#00cc66'  # green
    elif score <= 60:
        return '#ffcc00'  # yellow
    else:
        return '#ff3300'  # red

def show_graph(data, node_emissions, height=600):
    net = Network(height=f"{height}px", width="100%", directed=True)
    node_map = {n['name']: get_color_by_carbon(n['carbon']) for n in node_emissions}

    for rel in data:
        from_color = node_map.get(rel['from'], '#ADD8E6')
        to_color = node_map.get(rel['to'], '#ADD8E6')

        net.add_node(rel['from'], label=rel['from'], color=from_color)
        net.add_node(rel['to'], label=rel['to'], color=to_color)
        net.add_edge(rel['from'], rel['to'], label=rel['rel'])


    # Save & show
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        path = tmp_file.name
        net.save_graph(path)
        with open(path, 'r', encoding='utf-8') as html_file:
            components.html(html_file.read(), height=height)
        threading.Timer(5, lambda: os.remove(path)).start()

import streamlit as st

def display_legend():
    st.markdown("### 🗂️ Legend")
    st.markdown(
        """
        <div style="line-height: 1.6;">
        <span style='color:#00cc66;'>🟢 Low Emission (≤30 CO₂)</span><br>
        <span style='color:#ffcc00;'>🟡 Moderate Emission (31–60 CO₂)</span><br>
        <span style='color:#ff3300;'>🔴 High Emission (>60 CO₂)</span><br><br>

        <span style='color:#FFADAD;'>🌸 Product Node</span><br>
        <span style='color:#A0C4FF;'>🏬 Store Node</span><br>
        <span style='color:#B5E48C;'>🛒 Supplier Node</span><br>
        <span style='color:#FDCB6E;'>🤝 NGO Node</span>
        </div>
        """,
        unsafe_allow_html=True
    )
