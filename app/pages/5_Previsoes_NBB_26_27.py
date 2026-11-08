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

times = temporada['Time'].unique()
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
* Cada coluna representa a posição ao final da temporada regular
* Os valores são as porcentagens das vezes que esses times apareceram naquelas posições
""")
temporada = temporada[~temporada['Time'].isin(['Vasco da Gama', 'Rio Claro'])]

group_temporada = (
    temporada[["Time", "Posição"]].groupby("Time")["Posição"]
    .value_counts(normalize=True)
    .unstack(fill_value=0) * 100
).reset_index()

for team_column, logo_column in (
        ("Time", "Logo"),
    ):
        group_temporada.insert(
            group_temporada.columns.get_loc(team_column),
            logo_column,
            group_temporada[team_column].map(logo_data_uris),
        )

lista_posicoes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
group_temporada = group_temporada.sort_values(lista_posicoes, ascending=False).reset_index(drop=True)

fig = px.bar(
    group_temporada,
    x = "Time",
    y = 1,
    color = 'Time',
    color_discrete_map={
        time: PALETAS[time].primaria for time in group_temporada["Time"].unique()
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
        text = "<b>Chances para 1º colocado na temporada regular<b>",
        font=dict(family="Segoe UI", size=20)
    ),
    yaxis = dict(
        title = "Percentual de chance para 1º colocado"
    )
)
st.plotly_chart(fig, use_container_width=True)

st.dataframe(group_temporada,
            column_config={
                "Logo": st.column_config.ImageColumn("Logo", width="small"),
            },
            use_container_width=True,
            hide_index=True)

st.divider()

st.markdown("""
## Semifinais: veja as chances de cada equipe chegar às semifinais 
""")

group_semifinalistas = (semifinalistas["Time"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
    .reset_index())
group_semifinalistas.columns = ["Time", "% Semifinal"]

for team_column, logo_column in (
        ("Time", "Logo"),
    ):
        group_semifinalistas.insert(
            group_semifinalistas.columns.get_loc(team_column),
            logo_column,
            group_semifinalistas[team_column].map(logo_data_uris),
        )

fig2 = px.bar(
    group_semifinalistas,
    x = "Time",
    y = "% Semifinal",
    color = 'Time',
    color_discrete_map={
        time: PALETAS[time].primaria for time in group_semifinalistas["Time"].unique()
    }
)
fig2.update_layout(
    template = 'plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend = dict(
        bgcolor='rgba(0,0,0,0)',
        font = dict(family = "Segoe UI", size = 12)
    ),
    title = dict(
        text = "<b>Chances de aparecer nas semifinais da NBB 26/27<b>",
        font=dict(family="Segoe UI", size=20)
    ),
    yaxis = dict(
        title = "Percentual de aparições na semifinal"
    )
)
st.plotly_chart(fig2, use_container_width=True)

st.dataframe(group_semifinalistas,
            column_config={
                "Logo": st.column_config.ImageColumn("Logo", width="small"),
            },
            use_container_width=True,
            hide_index=True)

st.divider()

st.markdown("""
## Finais: veja as chances de cada equipe chegar às semifinais 
""")

group_finalistas = (finalistas["Time"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
    .reset_index())
group_finalistas.columns = ["Time", "% Finais"]

for team_column, logo_column in (
        ("Time", "Logo"),
    ):
        group_finalistas.insert(
            group_finalistas.columns.get_loc(team_column),
            logo_column,
            group_finalistas[team_column].map(logo_data_uris),
        )

fig3 = px.bar(
    group_finalistas,
    x = "Time",
    y = "% Finais",
    color = 'Time',
    color_discrete_map={
        time: PALETAS[time].primaria for time in group_finalistas["Time"].unique()
    }
)
fig3.update_layout(
    template = 'plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend = dict(
        bgcolor='rgba(0,0,0,0)',
        font = dict(family = "Segoe UI", size = 12)
    ),
    title = dict(
        text = "<b>Chances de aparecer nas Finais da NBB 26/27<b>",
        font=dict(family="Segoe UI", size=20)
    ),
    yaxis = dict(
        title = "Percentual de aparições nas Finais"
    )
)
st.plotly_chart(fig3, use_container_width=True)

st.dataframe(group_finalistas,
            column_config={
                "Logo": st.column_config.ImageColumn("Logo", width="small"),
            },
            use_container_width=True,
            hide_index=True)

st.divider()

st.markdown("""
## Campeões: veja as chances de cada equipe ser campeã na temporada 26/27 da NBB
""")

group_campeoes = (campeoes["Time"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
    .reset_index())
group_campeoes.columns = ["Time", "% Campeão"]

for team_column, logo_column in (
        ("Time", "Logo"),
    ):
        group_campeoes.insert(
            group_campeoes.columns.get_loc(team_column),
            logo_column,
            group_campeoes[team_column].map(logo_data_uris),
        )

fig4 = px.bar(
    group_campeoes,
    x = "Time",
    y = "% Campeão",
    color = 'Time',
    color_discrete_map={
        time: PALETAS[time].primaria for time in group_campeoes["Time"].unique()
    }
)
fig4.update_layout(
    template = 'plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend = dict(
        bgcolor='rgba(0,0,0,0)',
        font = dict(family = "Segoe UI", size = 12)
    ),
    title = dict(
        text = "<b>Chances de ser campeão da NBB 26/27<b>",
        font=dict(family="Segoe UI", size=20)
    ),
    yaxis = dict(
        title = "Chances de ser campeão"
    )
)
st.plotly_chart(fig4, use_container_width=True)

st.dataframe(group_campeoes,
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