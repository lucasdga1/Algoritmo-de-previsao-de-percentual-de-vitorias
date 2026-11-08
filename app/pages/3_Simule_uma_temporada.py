import streamlit as st
import base64
from io import BytesIO
from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
from PIL import Image
from scripts.simulation_pipeline.temporada.temporada import simula_temporada, playoffs_8va, playoffs_4as, playoffs_semi, playoffs_finais

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
    jogos['Probabilidade de vitória da casa'] = (jogos['Probabilidade de vitória da casa'] * 100).map('{:.2f}'.format)
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
    st.dataframe(jogos.style.set_properties(
                    subset=["Resultado"],
                    **{"font-weight": "bold"},
                ),
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

    vitorias_por_rodada = (
        jogos.assign(Vitoria=1)
        .pivot_table(
            index="Rodada",
            columns="Resultado",
            values="Vitoria",
            aggfunc="sum",
            fill_value=0,
        )
        .reindex(
            index=range(1, int(jogos["Rodada"].max()) + 1),
            columns=times,
            fill_value=0,
        )
        .sort_index()
        .cumsum()
    )
    rodada_vitorias = (
        vitorias_por_rodada.rename_axis(columns="Time")
        .reset_index()
        .melt(id_vars="Rodada", var_name="Time", value_name="Vitorias")
    )

    fig = px.line(
        rodada_vitorias,
        x='Rodada',
        y='Vitorias',
        color='Time',
        color_discrete_map={
            time: PALETAS[time].primaria for time in rodada_vitorias["Time"].unique()
        },
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(family="Segoe UI", size=12),
        ),
        title=dict(
            text="<b>Vitórias acumuladas por rodada</b>",
            font=dict(family="Segoe UI", size=20),
        ),
        xaxis_title="Rodada",
        yaxis_title="Vitórias acumuladas",
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.divider()

    def exibir_fase_playoff(
        nome_fase, resultados_fase, classificados, titulo_classificados
    ):
        st.markdown(f"### {nome_fase}")

        resultados_com_logos = resultados_fase.copy()
        for team_column, logo_column in (
            ("Casa", "Logo Casa"),
            ("Visitante", "Logo Visitante"),
        ):
            resultados_com_logos.insert(
                resultados_com_logos.columns.get_loc(team_column),
                logo_column,
                resultados_com_logos[team_column].map(logo_data_uris),
            )

        st.dataframe(
            resultados_com_logos.style.set_properties(
                subset=["Vencedor"],
                **{"font-weight": "bold"},
            ),
            column_config={
                "Logo Casa": st.column_config.ImageColumn("Logo Casa", width="small"),
                "Logo Visitante": st.column_config.ImageColumn(
                    "Logo Visitante", width="small"
                ),
            },
            use_container_width=True,
            hide_index=True,
        )

        classificados_com_logos = classificados.copy()
        classificados_com_logos.insert(
            classificados_com_logos.columns.get_loc("Time"),
            "Logo",
            classificados_com_logos["Time"].map(logo_data_uris),
        )
        st.markdown(f"**{titulo_classificados}**")
        st.dataframe(
            classificados_com_logos,
            column_config={
                "Logo": st.column_config.ImageColumn("Logo", width="small"),
            },
            use_container_width=True,
            hide_index=True,
        )

        serie = resultados_fase["Casa"] + " x " + resultados_fase["Visitante"]
        jogos_por_time = pd.concat(
            [
                resultados_fase.assign(Time=resultados_fase["Casa"], Serie=serie),
                resultados_fase.assign(
                    Time=resultados_fase["Visitante"], Serie=serie
                ),
            ],
            ignore_index=True,
        )
        jogos_por_time["Vitoria"] = (
            jogos_por_time["Time"] == jogos_por_time["Vencedor"]
        ).astype(int)
        jogos_por_time = jogos_por_time.sort_values(
            ["Rodada", "Serie", "Time", "Jogo da série"]
        )
        jogos_por_time["Vitorias acumuladas"] = (
            jogos_por_time.groupby(["Rodada", "Serie", "Time"])["Vitoria"].cumsum()
        )

        fig_playoff = px.line(
            jogos_por_time,
            x="Jogo da série",
            y="Vitorias acumuladas",
            color="Time",
            line_group="Serie",
            markers=True,
            color_discrete_map={
                time: PALETAS[time].primaria
                for time in jogos_por_time["Time"].unique()
            },
        )
        fig_playoff.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                font=dict(family="Segoe UI", size=12),
            ),
            title=dict(
                text=f"<b>Vitórias acumuladas por jogo — {nome_fase}</b>",
                font=dict(family="Segoe UI", size=20),
            ),
            xaxis_title="Jogo da série",
            yaxis_title="Vitórias acumuladas na série",
            hovermode="x unified",
        )
        st.plotly_chart(fig_playoff, use_container_width=True)
        st.divider()

    df_result_8va, df_times_4as = playoffs_8va(tabela)
    exibir_fase_playoff(
        "Oitavas de final",
        df_result_8va,
        df_times_4as,
        "Classificados para as quartas de final",
    )

    df_result_4as, df_times_semi = playoffs_4as(df_times_4as)
    exibir_fase_playoff(
        "Quartas de final",
        df_result_4as,
        df_times_semi,
        "Classificados para as semifinais",
    )

    df_result_semi, df_times_final = playoffs_semi(df_times_semi)
    exibir_fase_playoff(
        "Semifinais",
        df_result_semi,
        df_times_final,
        "Classificados para a final",
    )

    df_result_final, df_campeao = playoffs_finais(df_times_final)
    exibir_fase_playoff(
        "Final",
        df_result_final,
        df_campeao,
        "Campeão",
    )

st.divider()

st.caption(
    "Projeto independente e sem fins lucrativos. "
    "As previsões possuem finalidade acadêmica e recreativa. "
    "Não utilize as informações para apostas esportivas."
)