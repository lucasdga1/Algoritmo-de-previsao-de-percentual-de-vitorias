# ====================================================================================
# Teste de funcionalidade da função de temporada completa
# ====================================================================================


import pandas as pd
import numpy as np
from pathlib import Path
import pytest
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.simulation_pipeline.temporada import temporada



nbb_26 = pd.read_csv(ROOT /'historico_nbb' / 'data' / 'calendario_26_nbb.csv')
times_nbb = nbb_26['Casa'].unique()

import pytest
import pandas as pd

@pytest.fixture
def final_nbb():
    _, final_nbb = temporada.simula_temporada()
    return final_nbb

@pytest.fixture
def df_times_4as(final_nbb):
    _, df_times_4as = temporada.playoffs_8va(final_nbb)
    return df_times_4as

@pytest.fixture
def playoff_class_semi_df(df_times_4as):
    _, playoff_class_semi_df = temporada.playoffs_4as(df_times_4as)
    return playoff_class_semi_df

@pytest.fixture
def playoff_class_final_df(playoff_class_semi_df):
    _, playoff_class_final_df = temporada.playoffs_semi(playoff_class_semi_df)
    return playoff_class_final_df


def test_temporada_regular():
    rodadas_resultados, final_nbb  = temporada.simula_temporada()
    assert isinstance(rodadas_resultados, pd.DataFrame)
    assert isinstance(final_nbb, pd.DataFrame)
    
    print(f"{final_nbb}")
    print("✅ Teste de temporada regular concluido.")
    
def test_8vas(final_nbb):
    df_result_8va, df_times_4as = temporada.playoffs_8va(final_nbb)
    assert isinstance(df_result_8va, pd.DataFrame)
    assert isinstance(df_times_4as, pd.DataFrame)
    
    print(f"{df_times_4as}")
    print("✅ Teste de oitavas concluido.")
    
def test_4as(df_times_4as):
    playoff_resultados_4as_df, playoff_class_semi_df = temporada.playoffs_4as(df_times_4as)
    assert isinstance(playoff_resultados_4as_df, pd.DataFrame)
    assert isinstance(playoff_class_semi_df, pd.DataFrame)
    
    print(f"{playoff_class_semi_df}")
    print("✅ Teste de quartas concluido.")
    

def test_semi(playoff_class_semi_df):
    playoff_resultados_semi_df, playoff_class_final_df = temporada.playoffs_semi(playoff_class_semi_df)
    assert isinstance(playoff_resultados_semi_df, pd.DataFrame)
    assert isinstance(playoff_class_final_df, pd.DataFrame)
    
    print(f"{playoff_class_final_df}")
    print("✅ Teste de semis concluido.")    

def test_final(playoff_class_final_df):
    playoff_resultados_final_df, playoff_campeao_df = temporada.playoffs_finais(playoff_class_final_df)
    assert isinstance(playoff_resultados_final_df, pd.DataFrame)
    assert isinstance(playoff_campeao_df, pd.DataFrame)
    
    print(f"{playoff_campeao_df}")
    print("✅ Teste de finais concluido.")
