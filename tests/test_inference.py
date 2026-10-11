"""
Teste do script de previsões
"""
import sys
from pathlib import Path

import pandas as pd
import json

from scripts.inference_pipeline.inference import predict

# ======================================================
# Adicionando a raiz do projeto ao caminho do sistema
# ======================================================
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

def sample_df() -> pd.DataFrame:
    """Pede os valores das features e monta a linha que será prevista."""
    with (ROOT / "features.json").open(encoding="utf-8") as features_file:
        train_cols = json.load(features_file)

    valores = {}
    for coluna in train_cols:
        while True:
            entrada = input(
                f"Informe o valor para {coluna} "
                "(use ponto no lugar da virgula): "
            )
            try:
                valores[coluna] = float(entrada)
                break
            except ValueError:
                print("Valor invalido. Digite um numero decimal.")

    return pd.DataFrame([valores], columns=train_cols)


def test_inference():
    dados = sample_df()
    percentual, total_vitorias = predict(dados)

    assert isinstance(percentual, float)
    assert isinstance(total_vitorias, int)

    print("✅ Teste de inferencia concluido.")
    print(f"Percentual previsto de vitorias na temporada: {percentual:.2f}%")
    print(f"Total previsto de vitorias na temporada: {total_vitorias}")