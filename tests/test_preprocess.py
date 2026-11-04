# Teste do funcionamento do script de pré-processamento

import pandas as pd
import numpy as np
import pytest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.feature_pipeline.feature_engineering import feature_pipeline


def test_feature_pipeline():
    # Criando DataFrames de teste
    df_17 = pd.DataFrame({
        'Team': ['A', 'B'],
        "W's": [10, 20],
        'Win %': [0.5, 0.6]
    })
    df_18 = pd.DataFrame({
        'Team': ['C', 'D'],
        "W's": [15, 25],
        'Win %': [0.55, 0.65]
    })
    df_20 = pd.DataFrame({
        'Team': ['E', 'F'],
        "W's": [12, 22],
        'Win %': [0.52, 0.62]
    })
    df_21 = pd.DataFrame({
        'Team': ['G', 'H'],
        "W's": [14, 24],
        'Win %': [0.54, 0.64]
    })
    df_22 = pd.DataFrame({
        'Team': ['I', 'J'],
        "W's": [16, 26],
        'Win %': [0.56, 0.66]
    })
    df_23 = pd.DataFrame({
        'Team': ['K', 'L'],
        "W's": [18, 28],
        'Win %': [0.58, 0.68]
    })
    df_24 = pd.DataFrame({
        'Team': ['M', 'N'],
        "W's": [20, 30],
        'Win %': [0.6, 0.7]
    })
    df_25 = pd.DataFrame({
        'Team': ['O', 'P'],
        "W's": [22, 32],
        'Win %': [0.62, 0.72]
    })

    feature_columns = [
        "FG%", "3P%", "TS%", "eFG%", "FT%", "Ast/TO",
        "BPG", "TOV", "SPG", "PPG", "ORtg",
    ]
    for df in (df_17, df_18, df_20, df_21, df_22, df_23, df_24, df_25):
        for column in feature_columns:
            df[column] = 0.5

    # Chamando a função feature_pipeline
    X_train, Y_train, X_test, Y_test, temporada_array = feature_pipeline(df_17, df_18, df_20, df_21, df_22, df_23, df_24, df_25)

    # Verificando os resultados
    assert isinstance(X_train, pd.DataFrame)
    assert isinstance(Y_train, pd.Series)
    assert isinstance(X_test, pd.DataFrame)
    assert isinstance(Y_test, pd.Series)
    assert isinstance(temporada_array, np.ndarray)