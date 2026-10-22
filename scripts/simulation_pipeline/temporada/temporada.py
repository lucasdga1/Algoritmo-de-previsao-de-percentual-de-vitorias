# ======================================================================
# Simulador da temporda NBB com monte carlo
# O usuário executa o comando
# O script faz 1 simulação da temporada 26/27
# Retorna uma lista com posições finais, resultados das partidas e 
# Quantidade de vitórias para cada equipe 
# Retorna resultado por jogo, rodada e turno
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

def simula_temporada():
    # ====================================================================================
    # Simulando uma temporada da NBB 2026 com base no histórico de elo
    # ====================================================================================
    ultimo_turno = 0
    ultima_rodada = 0
    elo_dict = dict(zip(elo_26['Time'], elo_26['Elo']))
    tabela ={time: 0 for time in elo_26['Time']}
    posicoes =[]
    resultados_jogos = []
    
    for idx, row in enumerate(temporada.itertuples(), start=0):
        casa = row.Casa
        fora = row.Visitante
        
        elo_casa = elo_dict[casa]
        elo_fora = elo_dict[fora]
        vtg = (elo_casa + 60) - elo_fora  # Adicionando vantagem de casa de 60 pontos
        
        prob_casa = 1 / (1 + 10 ** ((-vtg) / 400))
        
        result = np.random.choice([casa, fora], p=[prob_casa, 1 - prob_casa])
        tabela[result] +=1

        rodada_atual = (idx // 9) + 1
        turno_atual = 1 if rodada_atual <= 17 else 2
        
        if rodada_atual > ultima_rodada or turno_atual > ultimo_turno:
            print(f"-------------------------------------------------------------Turno {turno_atual}: Rodada {rodada_atual}-------------------------------------------------------------\n")
            ultima_rodada = rodada_atual
            ultimo_turno = turno_atual
        print(f"Jogo: {casa:<15} vs {fora:<15} | Resultado: {result:<15} | Probabilidade de vitória do {casa}: {prob_casa:.2%}")
        resultados_jogos.append({
            "Turno": turno_atual,
            "Rodada": rodada_atual,
            "Casa": casa,
            "Visitante": fora,
            "Resultado": result,
            "Probabilidade de vitória da casa": prob_casa,
        })

    classificacao = sorted(
                tabela.items(),
                key=lambda x: x[1],
                reverse=True
            )
    for posicao, (time, vitorias) in enumerate(classificacao, start=1):
        posicoes.append({
            "Time": time,
            "Posição": posicao,
            "Vitórias": vitorias,
        })

    final_nbb = pd.DataFrame(posicoes, columns=["Time", "Posição", "Vitórias"])

    return resultados_jogos, final_nbb


if __name__=="__main__":
    simula_temporada()