import streamlit as st
import base64
from io import BytesIO
from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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

        [data-testid="stMarkdownContainer"]:has(> p, > h1, > h2, > h3, > h4, > h5, > h6, > ol, > ul, > blockquote) {{
            background: rgba(0, 0, 0, 0.65);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


QUADRA = ROOT / "app" / "img" / "quadra_background.png"
LOGOS = ROOT / "Logos"
SIMUL_NBB_26 = ROOT / "historico_nbb" / "full_nbb"
NBB_26 = ROOT / "historico_nbb" / "data" / "calendario_26_nbb.csv"

TEAM_LOGOS = {
    "Basket Osasco": "Basket Osasco.png",
    "Basquete Cearense": "Basquete Cearense.png",
    "Bauru": "Bauru.png",
    "Botafogo": "Botafogo.png",
    "Brasília": "Brasília.png",
    "Caxias do Sul Basquete": "Caxias do Sul Basquete.png",
    "Corinthians": "Corinthians.png",
    "Cruzeiro": "Cruzeiro.png",
    "Flamengo": "Flamengo.png",
    "Franca": "Franca.png",
    "Minas": "Minas.png",
    "Mogi": "Mogi.png",
    "Pato Basquete": "Pato Basquete.png",
    "Paulistano": "Paulistano.png",
    "Pinheiros": "Pinheiros.png",
    "São José": "São José.png",
    "UNIFACISA": "UNIFACISA.png",
    "União Corinthians": "União Corinthians.png",
}

set_background(QUADRA)

st.markdown(
    """
# Veja as previsões para a temporada 26/27 da NBB após 10.000 simulações
"""
)
st.divider()

temporada = pd.read_csv(SIMUL_NBB_26 / "regular_full_nbb.csv")
semifinalistas = pd.read_csv(SIMUL_NBB_26 / "semifinalistas_full_nbb.csv")
finalistas = pd.read_csv(SIMUL_NBB_26 / "finalistas_full_nbb.csv")
campeoes = pd.read_csv(SIMUL_NBB_26 / "campeoes_full_nbb.csv")

times = pd.read_csv(NBB_26)['Casa'].unique()
missing_logos = set(times) - TEAM_LOGOS.keys()
missing_logo_files = [
    LOGOS / TEAM_LOGOS[team]
    for team in times
    if team in TEAM_LOGOS and not (LOGOS / TEAM_LOGOS[team]).is_file()
]
if missing_logos:
    st.error(f"Não há logo configurado para: {', '.join(sorted(missing_logos))}.")
    st.stop()
if missing_logo_files:
    st.error(
        "Não foi possível localizar os arquivos de logo: "
        + ", ".join(str(path) for path in missing_logo_files)
    )
    st.stop()
logo_data_uris = {}
for team in times:
    with Image.open(LOGOS / TEAM_LOGOS[team]) as logo:
        logo.thumbnail((96, 96), Image.Resampling.LANCZOS)
        optimized_logo = BytesIO()
        logo.save(optimized_logo, format="PNG", optimize=True)
    logo_data_uris[team] = (
        "data:image/png;base64,"
        + base64.b64encode(optimized_logo.getvalue()).decode("ascii")
    )

st.markdown("""
## Temporada regular: veja a classificação das equipes na temporada regular 
""")
temporada = temporada[~temporada['Time'].isin(['Vasco da Gama', 'Rio Claro'])]
for team_column, logo_column in (
        ("Time", "Logo"),
    ):
        temporada.insert(
            temporada.columns.get_loc(team_column),
            logo_column,
            temporada[team_column].map(logo_data_uris),
        )
temporada = temporada[["Time", "Posição"]]
group_temporada = (
    temporada.groupby("Time")["Posição"]
    .value_counts(normalize=True)
    .unstack(fill_value=0) * 100
)

st.dataframe(group_temporada,
            column_config={
                "Logo": st.column_config.ImageColumn("Logo", width="small"),
            },
            use_container_width=True,
            hide_index=True)