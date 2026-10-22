# ======================================================================
# Simulador da temporda NBB com monte carlo
# O usuário escolhe uma equipe
# O script faz 10.000 simulações da temporada 26/27 para aquele time
# Retorna uma lista com posições finais em cada simulação e 
# Retorna o caminho de vitórias ao longo dos 34 jogos de cada simulação
# ======================================================================= 


import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path.cwd()
df_elo = pd.read_csv(ROOT /'historico_nbb' / 'data' / 'historico_elo.csv')
nbb_26 = pd.read_csv(ROOT /'historico_nbb' / 'data' / 'calendario_26_nbb.csv')
elo_26 = df_elo[df_elo['Season'] == 2025].groupby('Time').last().reset_index()[['Time', 'Elo']]

# O dataframe NBB_26 só contém os confrontos do 1º turno
# Criação de um dataframe com os 2 turnos 

turno_2 = nbb_26.rename(columns={"Casa": "Visitante", "Visitante": "Casa"}) 
turno_2 = turno_2[nbb_26.columns]
temporada = pd.concat([nbb_26, turno_2], ignore_index=True)

def simula_monteCarlo(equipe: str) -> tuple[np.ndarray, np.ndarray]:
    time_alvo = equipe
    elo_dict = dict(zip(elo_26['Time'], elo_26['Elo']))
    historico_posicoes = []
    historico_vitorias = []

    for simulacao in range(10000):  # Simulando 100 temporadas
        tabela = {time: 0 for time in elo_26['Time']}  # Inicializando a tabela de vitórias
        caminho_vitorias = []

        for row in temporada.itertuples():
            casa = row.Casa
            fora = row.Visitante
            
            elo_casa = elo_dict[casa]
            elo_fora = elo_dict[fora]
            vtg = (elo_casa + 60) - elo_fora  # Adicionando vantagem de casa de 60 pontos
            
            prob_casa = 1 / (1 + 10 ** ((-vtg) / 400))
            
            vencedor = np.random.choice([casa, fora], p=[prob_casa, 1 - prob_casa])
            tabela[vencedor] += 1

            if casa == time_alvo or fora == time_alvo:
                caminho_vitorias.append(tabela[time_alvo])

        historico_vitorias.append(caminho_vitorias)

        # Calcula a classificação somente ao final da simulação
        classificacao = sorted(
            tabela.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for posicao, (time, vitorias) in enumerate(classificacao, start=1):
            if time == time_alvo:
                historico_posicoes.append(posicao)
                break

    caminhos_vitorias = np.array(historico_vitorias)
    caminhos_posicoes = np.array(historico_posicoes)

    return caminhos_posicoes, caminhos_vitorias

if __name__ == "__main__":
    simula_monteCarlo()