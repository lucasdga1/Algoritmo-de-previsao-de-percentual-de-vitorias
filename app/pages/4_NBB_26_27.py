import streamlit as st
import base64
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.simulation_pipeline.temporada.monte_carlo import simula_monteCarlo
from styles.paletas import PALETAS

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
# Faça a simulação das chances de uma equipe na temporada NBB 26/27
1. Escolha uma equipe e clique em "Obter previsões";
2. O app fará 10.000 simulações da temporada para a equipe escolhida (os resultados demoram cerca de 4 minutos para serem exibidos);
3. Será exibido:
   * **Percentual de vitórias:** A chance percentual para cada número total de vitórias ao final da temporada.
   * **Posição na tabela:** O percentual de chance para cada posição final na tabela de classificação.
   * **Espectro de vitórias:** Um espectro de vitórias ao longo de cada rodada para as simulações realizadas.


"""
)
nbb_26 = pd.read_csv(NBB_26)
times = sorted(set(nbb_26["Casa"].dropna()) | set(nbb_26["Visitante"].dropna()))

st.divider()

st.markdown("""## Escolha a equipe para obter as previsões:""")
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

with st.container():
    time = st.selectbox("Equipe", times, index=0)
    st.image(LOGOS / TEAM_LOGOS[time], caption=time, width=140)
st.divider()

if st.button("Obter previsões", type="primary"):
    posicoes, vitorias = simula_monteCarlo(time)

    time_campeao = np.sum(posicoes == 1) / len(posicoes)
    time_top4 = np.sum(posicoes <= 4) / len(posicoes)
    time_playoffs = np.sum(posicoes <= 8) / len(posicoes)
    
    st.markdown(f"""
            ### Resultados das simulações para a equipe {time}:

            Probabilidade do {time} ser campeão: {time_campeao:.2%}

            Probabilidade do {time} ficar entre os 4 primeiros: {time_top4:.2%}

            Probabilidade do {time} ficar entre os 8 primeiros (playoffs): {time_playoffs:.2%}
""")

    st.divider()
    st.markdown(f"### Distribuição de vitórias ao longo das 10.000 simulações para a equipe {time}:")
    hist_vitorias = {'Posição':posicoes, 'Vitórias':vitorias[:,33]}

    previsao_df = pd.DataFrame(hist_vitorias)
    distribuicao_vitorias = (
        previsao_df['Vitórias']
        .value_counts(normalize=True)
        .mul(100)
        .reset_index(name='Percentual')
    )
    fig = px.area(
        distribuicao_vitorias,
        x='Vitórias',
        y='Percentual',
        color_discrete_sequence=[PALETAS[time].primaria],
        labels={'Vitórias': 'Número de Vitórias', 'Percentual': 'Percentual (%)'},
    )
    fig.update_layout(
    template = 'plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend = dict(
        bgcolor='rgba(0,0,0,0)',
        font = dict(family = "Segoe UI", size = 12)
    ),
    xaxis = dict(
        title = 'Número de Vitórias',
        title_font = dict(family = "Segoe UI", size = 14),
        tickfont = dict(family = "Segoe UI", size = 12)
    ),
    yaxis = dict(
            title = 'Percentual (%)',
            title_font = dict(family = "Segoe UI", size = 14),
            tickfont = dict(family = "Segoe UI", size = 12)
        ),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.divider()

    st.markdown(f"### Distribuição de posições ao longo das 10.000 simulações para a equipe {time}:")
    posicoes_barra = (
    previsao_df['Posição']
    .value_counts(normalize=True)
    .mul(100)
    .reset_index(name='Percentual')
    )
    fig2 = px.histogram(
        posicoes_barra,
        x='Posição',
        y='Percentual',
        nbins=14,
        labels={'Posição': 'Posição Final', 'Percentual': 'Percentual (%)'},
        color_discrete_sequence=[PALETAS[time].primaria],
    )
    fig2.update_layout(
    template = 'plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend = dict(
        bgcolor='rgba(0,0,0,0)',
        font = dict(family = "Segoe UI", size = 12)
    ),
    xaxis = dict(
        title = 'Posição',
        title_font = dict(family = "Segoe UI", size = 14),
        tickfont = dict(family = "Segoe UI", size = 12)
    ),
    yaxis = dict(
            title = 'Percentual (%)',
            title_font = dict(family = "Segoe UI", size = 14),
            tickfont = dict(family = "Segoe UI", size = 12)
        ),
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.divider()

    st.markdown(f"### Espectro de vitórias por rodada ao longo das 10.000 simulações para a equipe {time}:")
    
    if vitorias.ndim != 2:
        raise ValueError("O caminho de vitórias precisa ser um array 2D.")
    rodadas = np.arange(1, vitorias.shape[1] + 1)

    p05, p25, media, p75, p95 = np.percentile(
        vitorias, [5, 25, 50, 75, 95], axis=0
    )

    fig3 = go.Figure()

    # Faixa externa: percentis 5–95
    fig3.add_trace(go.Scatter(
        x=rodadas, y=p95,
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip"
    ))
    fig3.add_trace(go.Scatter(
        x=rodadas, y=p05,
        mode="lines",
        line=dict(width=0),
        fill="tonexty",
        fillcolor=PALETAS[time].terciaria,
        name="Percentis 5–95",
        hoverinfo="skip"
    ))

    # Faixa interna: percentis 25–75
    fig3.add_trace(go.Scatter(
        x=rodadas, y=p75,
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip"
    ))
    fig3.add_trace(go.Scatter(
        x=rodadas, y=p25,
        mode="lines",
        line=dict(width=0),
        fill="tonexty",
        fillcolor=PALETAS[time].secundaria,
        name="Percentis 25–75",
        hoverinfo="skip"
    ))

    # Linha central: média das simulações
    fig3.add_trace(go.Scatter(
        x=rodadas,
        y=media,
        mode="lines",
        line=dict(color=PALETAS[time].primaria, width=3),
        name="Média simulada"
    ))

    fig3.update_layout(
    template = 'plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend = dict(
        bgcolor='rgba(0,0,0,0)',
        font = dict(family = "Segoe UI", size = 12)
    ),
    xaxis = dict(
        title = 'Rodada',
        title_font = dict(family = "Segoe UI", size = 14),
        tickfont = dict(family = "Segoe UI", size = 12)
    ),
    yaxis = dict(
            title = 'Vitórias acumuladas',
            title_font = dict(family = "Segoe UI", size = 14),
            tickfont = dict(family = "Segoe UI", size = 12)
        ),
    hovermode="x unified"
    )

    st.plotly_chart(fig3, use_container_width=True)




st.divider()

st.caption(
    "Projeto independente e sem fins lucrativos. "
    "As previsões possuem finalidade acadêmica e recreativa. "
    "Não utilize as informações para apostas esportivas."
)