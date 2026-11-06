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

ROOT = Path(__file__).resolve().parents[3]
df_elo = pd.read_csv(ROOT /'historico_nbb' / 'data' / 'historico_elo.csv')
nbb_26 = pd.read_csv(ROOT /'historico_nbb' / 'data' / 'calendario_26_nbb.csv')
elo_26 = df_elo[df_elo['Season'] == 2025].groupby('Time').last().reset_index()[['Time', 'Elo']]

# O dataframe NBB_26 só contém os confrontos do 1º turno
# Criação de um dataframe com os 2 turnos 

turno_2 = nbb_26.rename(columns={"Casa": "Visitante", "Visitante": "Casa"}) 
turno_2 = turno_2[nbb_26.columns]
temporada = pd.concat([nbb_26, turno_2], ignore_index=True)

# ====================================================================================
# Simulando a série mélhor de 5 da NBB
# ====================================================================================
class Series:
    def __init__(self, time_a, time_b, melhor_de=5):
        self.time_a = time_a
        self.time_b = time_b
        self.vitorias_a = 0
        self.vitorias_b = 0
        self.target = melhor_de // 2 + 1

    def add_vitorias(self, time):
        if time == self.time_a:
            self.vitorias_a += 1
        elif time == self.time_b:
            self.vitorias_b += 1

    def vencedor(self):
        if self.vitorias_a >= self.target:
            return self.time_a
        elif self.vitorias_b >= self.target:
            return self.time_b
        else:
            return None


def simula_temporada():
    # ====================================================================================
    # Simulando uma temporada da NBB 2026 com base no histórico de elo
    # ====================================================================================
    ultimo_turno = 0
    ultima_rodada = 0
    elo_dict = dict(zip(elo_26['Time'], elo_26['Elo']))
    times_calendario = pd.unique(nbb_26[["Casa", "Visitante"]].to_numpy().ravel())
    tabela = {time: 0 for time in times_calendario}
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

    rodadas_resultados = pd.DataFrame(resultados_jogos)
    final_nbb = pd.DataFrame(posicoes, columns=["Time", "Posição", "Vitórias"])

    return rodadas_resultados, final_nbb


def playoffs_8va(df: pd.DataFrame):
    # ====================================================================================
    # Simula a primeira rodada dos playoffs com base no histórico de Elo
    # ====================================================================================
    elo_dict = dict(zip(elo_26["Time"], elo_26["Elo"]))
    posicoes = dict(zip(df["Time"], df["Posição"]))
    playoff_times = (
        df.loc[df["Posição"] <= 16]
        .sort_values("Posição")["Time"]
        .tolist()
    )

    playoff_resultados = []
    playoff_class_4as = []
    rodada = 1

    while len(playoff_times) > 8:
        if len(playoff_times) % 2 != 0:
            raise ValueError("O número de times na rodada precisa ser par.")

        vencedores_rodada = []
        metade = len(playoff_times) // 2

        for i in range(metade):
            casa = playoff_times[i]
            fora = playoff_times[-(i + 1)]

            elo_casa = elo_dict[casa]
            elo_fora = elo_dict[fora]
            vantagem_casa = (elo_casa + 60) - elo_fora
            vantagem_fora = (elo_fora + 60) - elo_casa
            prob_ida = 1 / (1 + 10 ** (-vantagem_casa / 400))
            prob_volta = 1 / (1 + 10 ** (-vantagem_fora / 400))

            serie = Series(casa, fora, melhor_de=5)
            jogo = 0

            while jogo < 5 and serie.vencedor() is None:
                # prob_ida: chance de vitória de casa quando tem mando.
                # prob_volta: chance de vitória de casa quando fora tem mando.
                prob_casa = prob_ida if jogo in (0, 1, 4) else prob_volta
                vencedor_partida = np.random.choice(
                        [casa, fora],
                        p=[prob_casa, 1 - prob_casa],
                    )
                serie.add_vitorias(vencedor_partida)
                jogo += 1   

                playoff_resultados.append({
                    "Rodada": rodada,
                    "Jogo da série": jogo,
                    "Casa": casa,
                    "Visitante": fora,
                    "Vencedor": vencedor_partida,
                    "Vitórias Casa": serie.vitorias_a,
                    "Vitórias Visitante": serie.vitorias_b,
                })

            vencedor_serie = serie.vencedor()
            vencedores_rodada.append(vencedor_serie)
            playoff_class_4as.append({
                "Time": vencedor_serie,
                "Posição": posicoes[vencedor_serie],
            })

        playoff_times = vencedores_rodada
        rodada += 1

    df_result_8va = pd.DataFrame(playoff_resultados)
    df_times_4as = pd.DataFrame(playoff_class_4as)
    df_times_4as = df_times_4as.sort_values("Posição").reset_index(drop=True)

    return df_result_8va, df_times_4as


def playoffs_4as(df: pd.DataFrame):
    # ====================================================================================
    # Simula a segunda rodada dos playoffs com base no histórico de Elo
    # ====================================================================================
    elo_dict = dict(zip(elo_26["Time"], elo_26["Elo"]))
    posicoes = dict(zip(df["Time"], df["Posição"]))
    playoff_times = (df.sort_values("Posição")["Time"].tolist())
    playoff_resultados_4as = []
    playoff_class_semi = []
    rodada = 1

    while len(playoff_times) > 4:
        if len(playoff_times) % 2 != 0:
            raise ValueError("O número de times na rodada precisa ser par.")

        vencedores_rodada = []
        metade = len(playoff_times) // 2

        for i in range(metade):
            casa = playoff_times[i]
            fora = playoff_times[-(i + 1)]

            elo_casa = elo_dict[casa]
            elo_fora = elo_dict[fora]
            vantagem_casa = (elo_casa + 60) - elo_fora
            vantagem_fora = (elo_fora + 60) - elo_casa
            prob_ida = 1 / (1 + 10 ** (-vantagem_casa / 400))
            prob_volta = 1 / (1 + 10 ** (-vantagem_fora / 400))

            serie = Series(casa, fora, melhor_de=5)
            jogo = 0

            while jogo < 5 and serie.vencedor() is None:
                # prob_ida: chance de vitória de casa quando tem mando.
                # prob_volta: chance de vitória de casa quando fora tem mando.
                prob_casa = prob_ida if jogo in (0, 1, 4) else prob_volta
                vencedor_partida = np.random.choice(
                        [casa, fora],
                        p=[prob_casa, 1 - prob_casa],
                    )
                serie.add_vitorias(vencedor_partida)
                jogo += 1   

                playoff_resultados_4as.append({
                    "Rodada": rodada,
                    "Jogo da série": jogo,
                    "Casa": casa,
                    "Visitante": fora,
                    "Vencedor": vencedor_partida,
                    "Vitórias Casa": serie.vitorias_a,
                    "Vitórias Visitante": serie.vitorias_b,
                })

            vencedor_serie = serie.vencedor()
            vencedores_rodada.append(vencedor_serie)
            playoff_class_semi.append({
                "Time": vencedor_serie,
                "Posição": posicoes[vencedor_serie],
            })

        playoff_times = vencedores_rodada
        rodada += 1

    playoff_resultados_4as_df = pd.DataFrame(playoff_resultados_4as)
    playoff_class_semi_df = pd.DataFrame(playoff_class_semi)

    playoff_class_semi_df = playoff_class_semi_df.sort_values("Posição").reset_index(drop=True)

    return playoff_resultados_4as_df, playoff_class_semi_df


def playoffs_semi(df: pd.DataFrame):
    # ====================================================================================
    # Simula a semi-final dos playoffs com base no histórico de Elo
    # ====================================================================================
    elo_dict = dict(zip(elo_26["Time"], elo_26["Elo"]))
    posicoes = dict(zip(df["Time"], df["Posição"]))
    playoff_times = (df.sort_values("Posição")["Time"].tolist())
    playoff_resultados_semi = []
    playoff_class_final = []
    rodada = 1

    while len(playoff_times) > 2:
        if len(playoff_times) % 2 != 0:
            raise ValueError("O número de times na rodada precisa ser par.")

        vencedores_rodada = []
        metade = len(playoff_times) // 2

        for i in range(metade):
            casa = playoff_times[i]
            fora = playoff_times[-(i + 1)]

            elo_casa = elo_dict[casa]
            elo_fora = elo_dict[fora]
            vantagem_casa = (elo_casa + 60) - elo_fora
            vantagem_fora = (elo_fora + 60) - elo_casa
            prob_ida = 1 / (1 + 10 ** (-vantagem_casa / 400))
            prob_volta = 1 / (1 + 10 ** (-vantagem_fora / 400))

            serie = Series(casa, fora, melhor_de=5)
            jogo = 0

            while jogo < 5 and serie.vencedor() is None:
                # prob_ida: chance de vitória de casa quando tem mando.
                # prob_volta: chance de vitória de casa quando fora tem mando.
                prob_casa = prob_ida if jogo in (0, 1, 4) else prob_volta
                vencedor_partida = np.random.choice(
                        [casa, fora],
                        p=[prob_casa, 1 - prob_casa],
                    )
                serie.add_vitorias(vencedor_partida)
                jogo += 1   

                playoff_resultados_semi.append({
                    "Rodada": rodada,
                    "Jogo da série": jogo,
                    "Casa": casa,
                    "Visitante": fora,
                    "Vencedor": vencedor_partida,
                    "Vitórias Casa": serie.vitorias_a,
                    "Vitórias Visitante": serie.vitorias_b,
                })

            vencedor_serie = serie.vencedor()
            vencedores_rodada.append(vencedor_serie)
            playoff_class_final.append({
                "Time": vencedor_serie,
                "Posição": posicoes[vencedor_serie],
            })

        playoff_times = vencedores_rodada
        rodada += 1

    playoff_resultados_semi_df = pd.DataFrame(playoff_resultados_semi)
    playoff_class_final_df = pd.DataFrame(playoff_class_final)

    playoff_class_final_df = playoff_class_final_df.sort_values("Posição").reset_index(drop=True)
    
    return playoff_resultados_semi_df, playoff_class_final_df


def playoffs_finais(df: pd.DataFrame):
    # ====================================================================================
    # Simula a final dos playoffs com base no histórico de Elo
    # ====================================================================================
    elo_dict = dict(zip(elo_26["Time"], elo_26["Elo"]))
    posicoes = dict(zip(df["Time"], df["Posição"]))
    playoff_times = (df.sort_values("Posição")["Time"].tolist())
    playoff_resultados_final = []
    playoff_campeao = []
    rodada = 1

    while len(playoff_times) > 1:
        if len(playoff_times) % 2 != 0:
            raise ValueError("O número de times na rodada precisa ser par.")

        vencedores_rodada = []
        metade = len(playoff_times) // 2

        for i in range(metade):
            casa = playoff_times[i]
            fora = playoff_times[-(i + 1)]

            elo_casa = elo_dict[casa]
            elo_fora = elo_dict[fora]
            vantagem_casa = (elo_casa + 60) - elo_fora
            vantagem_fora = (elo_fora + 60) - elo_casa
            prob_ida = 1 / (1 + 10 ** (-vantagem_casa / 400))
            prob_volta = 1 / (1 + 10 ** (-vantagem_fora / 400))

            serie = Series(casa, fora, melhor_de=5)
            jogo = 0

            while jogo < 5 and serie.vencedor() is None:
                # prob_ida: chance de vitória de casa quando tem mando.
                # prob_volta: chance de vitória de casa quando fora tem mando.
                prob_casa = prob_ida if jogo in (0, 1, 4) else prob_volta
                vencedor_partida = np.random.choice(
                        [casa, fora],
                        p=[prob_casa, 1 - prob_casa],
                    )
                serie.add_vitorias(vencedor_partida)
                jogo += 1   

                playoff_resultados_final.append({
                    "Rodada": rodada,
                    "Jogo da série": jogo,
                    "Casa": casa,
                    "Visitante": fora,
                    "Vencedor": vencedor_partida,
                    "Vitórias Casa": serie.vitorias_a,
                    "Vitórias Visitante": serie.vitorias_b,
                })

            vencedor_serie = serie.vencedor()
            vencedores_rodada.append(vencedor_serie)
            playoff_campeao.append({
                "Time": vencedor_serie,
                "Posição": posicoes[vencedor_serie],
            })

        playoff_times = vencedores_rodada
        rodada += 1

    playoff_resultados_final_df = pd.DataFrame(playoff_resultados_final)
    playoff_campeao_df = pd.DataFrame(playoff_campeao)
    return playoff_resultados_final_df, playoff_campeao_df

if __name__=="__main__":
    rodadas_resultados, final_nbb  = simula_temporada()
    df_result_8va, df_times_4as = playoffs_8va(final_nbb)
    playoff_resultados_4as_df, playoff_class_semi_df = playoffs_4as(df_times_4as)
    playoff_resultados_semi_df, playoff_class_final_df = playoffs_semi(playoff_class_semi_df)
    playoff_resultados_final_df, playoff_campeao_df = playoffs_finais(playoff_class_final_df)

