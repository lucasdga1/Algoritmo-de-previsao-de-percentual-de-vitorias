# ====================================================================================
# Teste de funcionalidade da função de confronto direto
# ====================================================================================


import pandas as pd
import numpy as np
from pathlib import Path
import pytest
from scripts.simulation_pipeline.temporada.temporada import simula_monteCarlo

ROOT = Path.cwd()

nbb_26 = pd.read_csv(ROOT /'historico_nbb' / 'data' / 'calendario_26_nbb.csv')
times_nbb = nbb_26['Casa'].unique()


def time_alvo()->str:
    while True:
        time = input("Escolha uma equipe da temporada 26/27 na NBB para simular: ").strip()
        if time not in times_nbb:
            print("Este time não está participando da temporada 26/27, escolha outro por favor: ")
            continue
        return time

def teste_monteCarlo():
    equipe = time_alvo()
    posicoes, vitorias = simula_monteCarlo(equipe)

    campeao = np.sum(posicoes == 1) / len(posicoes)
    top4 = np.sum(posicoes <= 4) / len(posicoes)
    playoffs = np.sum(posicoes <= 8) / len(posicoes) 
    exemplo = vitorias[:5, :5]
    
    assert isinstance(posicoes, np.ndarray)
    assert isinstance(vitorias, np.ndarray)

    print("✅ Teste de Monte Carlo concluido.")
    print(f"Probabilidade do {equipe} ser campeão: {campeao:.2%}")
    print(f"Probabilidade do {equipe} ficar entre os 4 primeiros: {top4:.2%}")
    print(f"Probabilidade do {equipe} ficar entre os 8 primeiros (playoffs): {playoffs:.2%}")
    print(exemplo)