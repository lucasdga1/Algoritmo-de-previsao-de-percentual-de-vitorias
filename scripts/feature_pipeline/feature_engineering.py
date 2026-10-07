# =======================================================================================================
# Script para limpeza e preparação de dados para o treino do modelo de previsão de percentual de vitórias
# =======================================================================================================
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path.cwd().parent.parent
OUT_DIR = ROOT / 'data' 


# Carregamento dos dados
def load_data():
    df_17 = pd.read_csv(r'Classificacao_NBB\NBB_17_teams.csv')
    df_18 = pd.read_csv(r'Classificacao_NBB\NBB_18_teams.csv')
    df_20 = pd.read_csv(r'Classificacao_NBB\NBB_20_teams.csv')
    df_21 = pd.read_csv(r'Classificacao_NBB\NBB_21_teams.csv')
    df_22 = pd.read_csv(r'Classificacao_NBB\NBB_22_teams.csv')
    df_23 = pd.read_csv(r'Classificacao_NBB\NBB_23_teams.csv')
    df_24 = pd.read_csv(r'Classificacao_NBB\NBB_24_teams.csv')
    df_25 = pd.read_csv(r'Classificacao_NBB\NBB_25_teams.csv')
    return df_17, df_18, df_20, df_21, df_22, df_23, df_24, df_25

def prepare_data(df_17, df_18, df_20, df_21, df_22, df_23, df_24):
    # Atribuição da coluna 'Season' para cada DataFrame
    df_17['Season'] = 2017
    df_18['Season'] = 2018
    df_20['Season'] = 2020
    df_21['Season'] = 2021
    df_22['Season'] = 2022
    df_23['Season'] = 2023
    df_24['Season'] = 2024

    # Concatenando todos os DataFrames que serão utiziados para o treino do modelo
    df_modelo = pd.concat([df_17, df_18, df_20, df_21, df_22, df_23, df_24], ignore_index=True)

    return df_modelo

def feature_pipeline(df_17, df_18, df_20, df_21, df_22, df_23, df_24, df_25):
    df_17, df_18, df_20, df_21, df_22, df_23, df_24, df_25 = load_data()
    df_modelo = prepare_data(df_17, df_18, df_20, df_21, df_22, df_23, df_24)

    X_train = df_modelo.drop(columns=["Team", "W's", "Win %", "Season"])
    Y_train = df_modelo["Win %"]
    X_test = df_25.drop(columns=["Team", "W's", "Win %"])
    Y_test = df_25["Win %"]

    return X_train, Y_train, X_test, Y_test

if __name__ == "__main__":
    feature_pipeline()