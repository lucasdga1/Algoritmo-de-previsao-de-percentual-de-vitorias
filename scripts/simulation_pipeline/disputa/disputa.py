# ====================================================================================
# Função para demonstrar as chances de vitória em um confronto direto
# O usuário escolhe as equipes, vantagem natural para equipes que jogam em casa
# A função retorna o percentual de vitória baseado no cálculo do Elo
# O resultado é demonstrado num gráfico plotly no app
# ====================================================================================

import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path.cwd()
df_elo = pd.read_csv(ROOT /'historico_nbb' / 'data' / 'historico_elo.csv')
nbb_26 = pd.read_csv(ROOT /'historico_nbb' / 'data' / 'calendario_26_nbb.csv')
elo_26 = df_elo[df_elo['Season'] == 2025].groupby('Time').last().reset_index()[['Time', 'Elo']]

def disputa_direta(casa: str,
                   fora: str
                   ):
    mandante = 60                    # Vantagem adicional de Elo para a equipe mandante
    
    casa_elo = elo_26[elo_26['Time'] == casa].iloc[0]['Elo']
    fora_elo = elo_26[elo_26['Time'] == fora].iloc[0]['Elo']
    vtg =  (casa_elo + mandante) - fora_elo

    prob_casa = 1 / (1 + 10 ** ((-vtg) / 400))
    prob_fora = 1 - prob_casa
    
    return prob_casa, prob_fora
    


if __name__ == "__main__":
    disputa_direta()