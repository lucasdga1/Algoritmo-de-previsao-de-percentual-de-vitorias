import streamlit as st
import base64
from io import BytesIO
from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
from PIL import Image
from scripts.simulation_pipeline.temporada.temporada import simula_temporada

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

        </style>
        """,
        unsafe_allow_html=True
    )


QUADRA = ROOT / "app" / "img" / "quadra_background.png"
LOGOS = ROOT / "Logos"
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
# Faça a simulação de uma temporada regular do NBB 26 e veja as performances de cada time!
1. Aperte o botão "Simular Temporada" para gerar uma temporada regular do NBB 26;
2. O app faz os cálculos de cada confronto e gera a tabela de classificação final;
"""
)
st.divider()

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

if st.button("Simular Temporada", type="primary"):
    result_jogos, tabela = simula_temporada()

    st.markdown("### Resultados dos jogos da temporada:")

    jogos = pd.DataFrame(result_jogos)
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

    for team_column, logo_column in (
        ("Casa", "Logo Casa"),
        ("Visitante", "Logo Visitante"),
    ):
        jogos.insert(
            jogos.columns.get_loc(team_column),
            logo_column,
            jogos[team_column].map(logo_data_uris),
        )
    st.dataframe(jogos,
                column_config={
                    "Logo Casa": st.column_config.ImageColumn("Logo Casa", width="small"),
                    "Logo Visitante": st.column_config.ImageColumn(
                        "Logo Visitante", width="small"
                    ),
                },
                use_container_width=True,
                hide_index=True,)

    st.divider()
    st.markdown("### Tabela de Classificação Final:")
    tabela = tabela[~tabela['Time'].isin(['Vasco da Gama', 'Rio Claro'])]
    for team_column, logo_column in (
            ("Time", "Logo"),
        ):
            tabela.insert(
                tabela.columns.get_loc(team_column),
                logo_column,
                tabela[team_column].map(logo_data_uris),
            )

    st.dataframe(tabela,
                column_config={
                    "Logo": st.column_config.ImageColumn("Logo", width="small"),
                },
                use_container_width=True,
                hide_index=True)






st.divider()

st.caption(
    "Projeto independente e sem fins lucrativos. "
    "As previsões possuem finalidade acadêmica e recreativa. "
    "Não utilize as informações para apostas esportivas."
)