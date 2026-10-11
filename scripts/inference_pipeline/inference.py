"""
Esse script pega stats colocados pelos usuários no app,
e alimenta o modelo salvo pelo script de treinamento
para obter uma inferência acerca do percentual total de vitórias uma
equipe com aquelas estatísticas pode obter em uma temporada atual da NBB.
"""

from pathlib import Path      # Biblioteca de caminhos de diretórios
import pandas as pd           # Biblioteca de manibulação de tabelas e dados
from joblib import load       # Biblioteca para importação do modelo salvo
import json

# ===========================================================================
# Caminhos padrões
# ===========================================================================
ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "models" / "en_best_model.pkl"

print("Inference using project root:", ROOT)

with (ROOT / "features.json").open(encoding="utf-8") as features_file:
    train_cols = json.load(features_file)

# ===========================================================================
# Função para previsões
# ===========================================================================
def predict(
        input_data: pd.DataFrame,
        model_path: Path | str = MODEL
) -> float:
    # Dados a serem previstos
    df_inferencia = input_data[train_cols]

    # Carregamento do modelo e realização da previsão
    model = load(model_path)
    pred = model.predict(df_inferencia)
    resultado_total = int(pred[0] * 36)
    
    return float(pred[0] * 100), resultado_total



if __name__ == "__main__":
    predict()