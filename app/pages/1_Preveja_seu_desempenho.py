import streamlit as st
import base64
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from joblib import load
import pickle

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


ROOT = Path(__file__).resolve().parent.parent.parent
QUADRA = ROOT / "app" / "img" / "quadra_background.png"

set_background(QUADRA)

# Carregamento do modelo e tabela 
MODEL = ROOT / "models" / "en_best_model.pkl"
DF = ROOT / "Classificacao_NBB" / "NBB_25_teams.csv"
LOGOS = ROOT / "Logos"

TEAM_LOGOS = {
    "Franca": "Franca.png",
    "Minas": "Minas.png",
    "Flamengo": "Flamengo.png",
    "Pinheiros Sky": "Pinheiros.png",
    "Corinthians": "Corinthians.png",
    "Paulistano": "Paulistano.png",
    "Sao Jose Unimed Vinac": "São José.png",
    "Unifacisa Paraiba": "UNIFACISA.png",
    "Uniceub-BRB-Brasilia": "Brasília.png",
    "Bauru": "Bauru.png",
    "Cruzeiro": "Cruzeiro.png",
    "Uniao Corinthians": "União Corinthians.png",
    "Rio Claro Basquete": "Rio Claro Basquete.png",
    "Mogi das Cruzes": "Mogi.png",
    "Basquete Cearense": "Basquete Cearense.png",
    "Osasco Basquete": "Basket Osasco.png",
    "Caxias Do Sul Basquetetriches": "Caxias do Sul Basquete.png",
    "Botafogo F.R.": "Botafogo.png",
    "Pato Basquete": "Pato Basquete.png",
    "Vasco da Gama": "Vasco da Gama.png",
    "Seu Time": "Seu Time.png",
}

try:
    df_nbb = pd.read_csv(DF)
except FileNotFoundError:
    print (f"Arquivo não localizado no diretório{DF}")

try:
    model = load(MODEL)
except FileNotFoundError:
    print (f"Arquivo não localizado no diretório{MODEL}")
except Exception as e:
    print(f"Ocorreu um erro inesperado ao carregar o modelo: {e}")

st.divider()

# Definição dos stats a serem colocados pelo usuário
stats_config = {
    "FG%": {"titulo":"Acertos de Quadra %", 
            "exemplo": "Ex: 0.42 (para 42% de FG%)"},
    "3P%": {"titulo":"3 Pontos %", 
            "exemplo": "Ex: 0.39 (para 39% de 3P%)"}, 
    "TS%": {"titulo":"True Shooting %", 
            "exemplo": "Ex: 0.53 (ou multiplique seu FG% por 1,25)"}, 
    "eFG%": {"titulo":"Effective FG %", 
            "exemplo": "Ex: 0.50 (ou multiplique por 1,16)"}, 
    "FT%": {"titulo":"Lances Livres %", 
            "exemplo": "Ex: 0.72 (para 72% de FT%)"}, 
    "Ast/TO": {"titulo":"Assistência / Turnover", 
            "exemplo": "Ex: 1.28 (média de mais de 1 assistência para cada turnover)"}, 
    "BPG": {"titulo":"Tocos por jogo", 
            "exemplo": "Ex: 1.99 (média da liga)"}, 
    "TOV": {"titulo":"Turnovers por jogo", 
            "exemplo": "Ex: 13.22 (média da liga)"}, 
    "SPG": {"titulo":"Roubos de bola por jogo", 
            "exemplo": "Ex: 6.93 (média da liga)"}, 
    "PPG": {"titulo":"Pontos por jogo", 
            "exemplo": "Ex: 77.96 (média da liga)"}, 
    "ORtg": {"titulo":"Pontos por 100 posses", 
            "exemplo": "Ex: 107.18 (ou multiplique por 1,37)"}
}

dados = {}

st.markdown(
    """
    # Preveja o desempenho do seu time
    
## Esta página utiliza os dados inseridos por você para:
* Fazer uma previsão de vitórias totais considerando o números de jogos de uma temporada regular da NBB (34);
* Fazer uma previsão do percentual total de vitórias esperadas;
* Classificar o resultado do seu time de acordo com a tabela da temporada 25/26 da NBB
* Para obter exemplos reais de estatísticas de várias ligas e seus significados acesse:
[Estatísticas NBB](https://basketball.realgm.com/international/league/59/Brazilian-NBB/team-stats)
    
## Insira os dados estatísticos do seu time nos campos abaixo
"""
)
# Caixa de input do usuário
with st.expander("📊 Inserir Estatísticas do seu time", expanded=True):
    for stat, info in stats_config.items():
        st.markdown(f"**{info['titulo']}**")
        st.caption(info["exemplo"])
        dados[stat] = st.number_input(
            label=info["titulo"],
            label_visibility="collapsed",
            key=stat
        )

# Botão para salvar as stats
if st.button("Salvar"):
    df = pd.DataFrame([dados])
    st.success("Dados salvos com sucesso!")
    st.dataframe(df)
    st.session_state["df_stats"] = df
st.divider()

if "df_stats" not in st.session_state:
    st.stop()

df = st.session_state["df_stats"]

if st.button("Preveja os resultados do seu time"):
    previsao = model.predict(df)[0]
    percentual = previsao
    total_vitorias = int(previsao * 36)

    st.markdown(f""" 
                ### ✅ Previsão concluida.
                ### Percentual previsto de vitorias na temporada: {percentual * 100:.2f}%.
                ### Total previsto de vitorias na temporada: {total_vitorias}
    """)

    st.divider()

    st.markdown(""" ### Confira abaixo o desempenho do seu time""")
    df_nbb = df_nbb[["Team","W's", "Win %"]]
    seuTime = {
        "Team": ["Seu Time"],
        "W's": [total_vitorias],
        "Win %": [percentual]
    }
    df_seuTime = pd.DataFrame(seuTime)
    df_final = pd.concat([df_nbb, df_seuTime], ignore_index=True)
    df_final = df_final.sort_values(by=["W's", "Win %"], ascending = False)
    df_final.index = pd.RangeIndex(start=1, stop=len(df_final) + 1)
    
    missing_logos = set(df_final["Team"]) - TEAM_LOGOS.keys()
    missing_logo_files = [
        LOGOS / TEAM_LOGOS[team]
        for team in df_final["Team"]
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

    df_final.insert(
        0,
        "Logo",
        df_final["Team"].map(
            lambda team: "data:image/png;base64,"
            + base64.b64encode((LOGOS / TEAM_LOGOS[team]).read_bytes()).decode("ascii")
        ),
    )
    st.dataframe(
        df_final,
        column_config={"Logo": st.column_config.ImageColumn("Logo", width="small")},
    )

st.caption(
    "Projeto independente e sem fins lucrativos. "
    "As previsões possuem finalidade acadêmica e recreativa. "
    "Não utilize as informações para apostas esportivas."
)