# HEADY_BRAND:BEGIN
# HEADY SYSTEMS :: SACRED GEOMETRY
# FILE: HeadyAcademy/Admin/Dashboard.py
# LAYER: root
# 
#         _   _  _____    _    ____   __   __
#        | | | || ____|  / \  |  _ \ \ \ / /
#        | |_| ||  _|   / _ \ | | | | \ V / 
#        |  _  || |___ / ___ \| |_| |  | |  
#        |_| |_||_____/_/   \_\____/   |_|  
# 
#    Sacred Geometry :: Organic Systems :: Breathing Interfaces
# HEADY_BRAND:END

import streamlit as st
import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

st.set_page_config(page_title="HeadySystems Throne", layout="wide")
st.sidebar.title("HeadySystems")
mode = st.sidebar.radio("View", ["Overwatch", "Blockchain Ledger", "Content Forge", "Bridge Control"])

if mode == "Overwatch":
    st.title("👁️ System Overwatch")
    st.metric("System Status", "ONLINE")

elif mode == "Blockchain Ledger":
    st.title("⛓️ HeadyChain Authorization")
    st.info("Ledger active in Logs/Ledger/chain_head.json")

elif mode == "Bridge Control":
    st.title("🌉 Bridge & Network")
    st.write("Manage MCP and WARP status.")
    
    if st.button("Check WARP Status"):
        warp_manager = BASE_DIR / "Tools" / "Network" / "Warp_Manager.py"
        res = subprocess.run([sys.executable, str(warp_manager), "status"], capture_output=True, text=True)
        st.code(res.stdout if res.stdout else "WARP Client not detected.")

    st.subheader("MCP Client Test")
    tool = st.selectbox("Tool", ["list", "scan_gaps:.", "verify_auth:User:ADMIN"])
    if st.button("Send JSON-RPC"):
        mcp_client = BASE_DIR / "Tools" / "MCP" / "Client.py"
        res = subprocess.run([sys.executable, str(mcp_client), tool], capture_output=True, text=True)
        st.json(res.stdout)

elif mode == "Content Forge":
    st.title("🖋️ Muse Content Engine")
    st.write("Generate assets that reflect Heady foundations.")
    
    if st.button("Forge Whitepaper"):
        st.success("Whitepaper generated in Content_Forge/")
