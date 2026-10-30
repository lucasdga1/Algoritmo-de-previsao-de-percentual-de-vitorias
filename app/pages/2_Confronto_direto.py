import streamlit as st
import base64
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def set_background(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: 100% auto;
            background-attachment: scroll;
            background-position: top center;
            background-repeat: no-repeat;
            background-color: #000000;
        }}

        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}

        [data-testid="stSidebar"] {{
            background: rgba(0,0,0,0.90);
            backdrop-filter: blur(5px);
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


ROOT = Path(__file__).resolve().parent.parent.parent
QUADRA = ROOT / "app" / "img" / "quadra_background.png"

set_background(QUADRA)











st.divider()

st.caption(
    "Projeto independente e sem fins lucrativos. "
    "As previsões possuem finalidade acadêmica e recreativa. "
    "Não utilize as informações para apostas esportivas."
)