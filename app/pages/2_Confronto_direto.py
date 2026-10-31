import streamlit as st
import base64
from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.simulation_pipeline.disputa.disputa import disputa_direta

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
BOLA = ROOT / "app" / "img" / "bola_basquete.png"
NBB_26 = ROOT / "historico_nbb" / "data" / "calendario_26_nbb.csv"
HISTORICO = ROOT / "historico_nbb" / "data" / "historico_nbb.csv"
LOGOS = ROOT / "Logos"

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
# Faça a simulação de uma partida e veja o resultado
1. Escolha o time mandante e o time visitante;
2. O app faz os cálculos e retorna as chances de vitória de cada um;
"""
)

nbb_26 = pd.read_csv(NBB_26)
times = sorted(set(nbb_26["Casa"].dropna()) | set(nbb_26["Visitante"].dropna()))

st.divider()

st.markdown("""## Escolha as equipes da partida:""")
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

col_casa, col_fora = st.columns(2)

with col_casa:
    casa = st.selectbox("Equipe mandante", times, index=0, key="equipe_mandante")
    st.image(LOGOS / TEAM_LOGOS[casa], caption=casa, width=140)

with col_fora:
    fora = st.selectbox(
        "Equipe visitante",
        times,
        index=1 if len(times) > 1 else 0,
        key="equipe_visitante",
    )
    st.image(LOGOS / TEAM_LOGOS[fora], caption=fora, width=140)

st.divider()

if st.button("Simular partida", type="primary"):
    if casa == fora:
        st.warning("Escolha duas equipes diferentes para simular a partida.")
    else:
        prob_casa, prob_fora = disputa_direta(casa, fora)
        resultado_casa, resultado_fora = st.columns(2)
        resultado_casa.metric(
            f"Chance de vitória do mandante ({casa})",
            f"{prob_casa:.1%}",
        )
        resultado_fora.metric(
            f"Chance de vitória do visitante ({fora})",
            f"{prob_fora:.1%}",
        )
        
        img = Image.open(BOLA)
        probas = {
        'Times':[casa, fora],
        'Porcentagem':[prob_casa, prob_fora]
        }
        data_fig = pd.DataFrame(probas)

        fig = px.pie(
            data_fig,
            values='Porcentagem',
            names='Times',
            hole=.5,
            color_discrete_map={
                f"{casa}" : "blue",
                f"{fora}" : 'orange'
            }
        )
        fig.update_layout(
            template = 'plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend = dict(
                bgcolor='rgba(0,0,0,0)',
                font = dict(family = "Segoe UI", size = 12)
            ),
            title = dict(
                text = "<b>Chances de vitória<b>",
                font=dict(family="Segoe UI", size=20)
            )
        )
        fig.add_layout_image(
            dict(
                source = img,
                xref = "paper",
                yref = "paper",
                x = 0.5,
                y = 0.5,
                sizex = 0.5,
                sizey = 0.5,
                xanchor = "center",
                yanchor = "middle",
                layer = "above"
            )
        )

        st.plotly_chart(fig, use_container_width=True)
        st.divider()

        historico = pd.read_csv(HISTORICO)
        selecao = historico[((historico["Casa"] == casa) & (historico["Visitante"] == fora)) | ((historico["Casa"] == casa) & (historico["Visitante"] == fora))]
        for team_column, logo_column in (
            ("Casa", "Logo Casa"),
            ("Visitante", "Logo Visitante"),
        ):
            selecao.insert(
                selecao.columns.get_loc(team_column),
                logo_column,
                selecao[team_column].map(
                    lambda team: "data:image/png;base64,"
                    + base64.b64encode(
                        (LOGOS / TEAM_LOGOS[team]).read_bytes()
                    ).decode("ascii")
                ),
            )

        st.dataframe(
            selecao,
            column_config={
                "Logo Casa": st.column_config.ImageColumn("Logo Casa", width="small"),
                "Logo Visitante": st.column_config.ImageColumn(
                    "Logo Visitante", width="small"
                ),
            },
            hide_index=True,
        )

st.divider()

st.caption(
    "Projeto independente e sem fins lucrativos. "
    "As previsões possuem finalidade acadêmica e recreativa. "
    "Não utilize as informações para apostas esportivas."
)