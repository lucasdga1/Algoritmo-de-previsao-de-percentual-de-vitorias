# ====================================================================================
# Teste de funcionalidade da função de confronto direto
# ====================================================================================


import pandas as pd
import numpy as np
from pathlib import Path
import pytest
from scripts.simulation_pipeline.disputa.disputa import disputa_direta

ROOT = Path.cwd()

nbb_26 = pd.read_csv(ROOT /'historico_nbb' / 'data' / 'calendario_26_nbb.csv')
times_nbb = nbb_26['Casa'].unique()

times = {}
def equipes() -> tuple[str, str]:
    
    while True:
        casa = input("Informe o nome da equipe mandante: ").strip()
        if casa not in times_nbb:
            print("Escolha uma equipe participante do NBB 26/27")
            continue

        fora = input("Informe o nome da equipe visitante: ").strip()
        if fora not in times_nbb:
            print("Escolha uma equipe participante do NBB 26/27")
            continue


        if casa == fora:
            print("A equipe mandante não pode ser igual à visitante!")
            continue
        
        return casa, fora

def test_disputa():
    casa, fora = equipes()

    prob_casa, prob_fora= disputa_direta(casa, fora)

    assert isinstance(prob_casa, float)
    assert isinstance(prob_fora, float)

    print("✅ Teste de disputa concluido.")
    print(f"Probabilidade de vitória da equipe {casa}: {prob_casa:.2f}%")
    print(f"Probabilidade de vitória da equipe {fora}: {prob_fora:.2f}%")
