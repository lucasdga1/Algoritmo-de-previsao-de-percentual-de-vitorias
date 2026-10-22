import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Previsões de basquete app 🏀")
st.header("Bem vindo ao app de simulações e previsões de jogos de basquete")

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

st.info(
    "Para mais informações sobre metodologia, fontes de dados e termos de utilização, consulte a página 'Sobre'."
)

st.divider()

st.caption(
    "Projeto independente e sem fins lucrativos. "
    "As previsões possuem finalidade acadêmica e recreativa. "
    "Não utilize as informações para apostas esportivas."
)