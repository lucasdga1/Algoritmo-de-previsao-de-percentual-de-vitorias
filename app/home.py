import streamlit as st
import base64
from pathlib import Path



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


ROOT = Path(__file__).resolve().parent.parent
QUADRA = ROOT / "app" / "img" / "quadra_background.png"

set_background(QUADRA)

st.title("Previsões de basquete 🏀")
st.header("Bem vindo ao app de simulações e previsões de jogos de basquete!")

st.markdown("""

Este projeto utiliza modelos estatísticos, probabilísticos e simulações de Monte Carlo para estimar resultados de partidas, confrontos diretos e cenários de classificação ao longo da temporada.

⚠️ **Aviso Importante**

- Este aplicativo possui finalidade exclusivamente acadêmica, educacional e recreativa.
- Todas as previsões apresentadas são estimativas matemáticas e não representam garantias de resultados futuros.
- O conteúdo disponibilizado **não constitui recomendação para apostas esportivas**.
- O autor desencoraja o uso de plataformas de apostas, jogos de azar, cassinos ou atividades similares.
- Os dados utilizados são provenientes de fontes públicas e oficiais, sem finalidade comercial ou lucrativa.
- A tabela de jogos utilizada nas simulações foi obtida a partir das informações disponibilizadas pela Liga Nacional de Basquete (LNB).

Ao utilizar este aplicativo, você concorda que as análises possuem caráter meramente informativo e experimental.
""")

st.divider()
st.markdown("""## Qual aplicação você quer utilizar hoje?""")
st.page_link(
    "pages/1_Preveja_seu_desempenho.py",
    label="📈 Preveja seu desempenho:",
)
st.markdown(
    """
Você vai digitar as estatísticas do seu time (real ou fictício) e a IA vai te dizer como seria o desempenho em termos de vitórias, além da classificação baseada na temporada 25/26 da NBB"""
)
st.divider()
st.page_link(
    "pages/2_Confronto_direto.py",
    label="🥊 Confronto direto:",
)
st.markdown("""
Selecione as equipes madante e visitante e veja quais as chances de vitória cada um tem na partida""")
st.divider()
st.page_link(
    "pages/3_Simule_uma_temporada.py",
    label="⛹️ Simule uma temporada:",
)
st.markdown("""
Faça a simulação da temporada regular 26/27 da NBB e veja os resultados dos jogos e a classificação final""")
st.divider()
st.page_link(
    "pages/4_NBB_26_27.py",
    label="🏆 NBB 26/27:",
)
st.markdown("""
Escolha uma equipe e veja quais as probabilidades de vitórias e clasificações ao longo da temporada baseado em um algorítmo de 10.000 simulações. 
""")

st.divider()
st.info(
    "Para mais informações sobre metodologia, fontes de dados e termos de utilização, consulte a página 'Sobre'."
)

st.divider()

st.caption(
    "Projeto independente e sem fins lucrativos. "
    "As previsões possuem finalidade acadêmica e recreativa. "
    "Não utilize as informações para apostas esportivas."
)