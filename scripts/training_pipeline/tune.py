"""
Esse script é responsável pelo treinamento do modelo, ajuste de hiperparâmetros,
e registro do modelo com as melhores métricas no MLflow.
"""

from pathlib import Path                              # Biblioteca de acesso aos diretórios
from typing import Dict, Optional, Tuple              # Biblioteca de suporte de tipos

import numpy as np                                    # Biblioteca de cálculos matemáticos 
import optuna                                         # Biblioteca de ajuste de hiperparâmetros
import pandas as pd                                   # Biblioteca de Dataframes
from joblib import dump                               # Biblioteca de manipulação de arquivos de modelos
import os                                             # Biblioteca de acesso ao sistema operacional
import json                                           # Biblioteca de escrita em json

from sklearn.model_selection import train_test_split                  # Bibliotecas de importação de modelo de IA,
from sklearn.decomposition import PCA                                 # preparação de dados, pipeline, redução de 
from sklearn.pipeline import Pipeline                                 # dimensionalidade, cross-validation, e avaliação
from sklearn.model_selection import GroupKFold, cross_val_score       # de métricas do modelo.
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

import mlflow                                                         # Bilbioteca de registro de experimentos, treinos
import mlflow.sklearn                                                 # e teste do modelo.
from mlflow.tracking import MlflowClient
from mlflow.exceptions import MlflowException

from scripts.feature_pipeline.feature_engineering import feature_pipeline

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = PROJECT_ROOT / "models" / "en_best_model.pkl"

X_train, Y_train, X_test, Y_test, temporada_array = feature_pipeline()

def tune_model(
        model_output: Path | str = DEFAULT_OUT,
        n_trials: int = 15,
        tracking_uri: Optional[str] = None,
        experiment_name:str = "en_optuna_nbb",
        random_state: int = 42  
) -> Tuple[Dict, Dict]:
    """
    Executar Optuna tuning: salvar o melhor modelo, e retornar as melhores
    métricas e parâmetros
    """
    os.environ["MLFLOW_TMP_DIR"] = "/tmp/mlflow_artifacts"
        # Se não foi passado tracking_uri, usa o do ambiente
    if tracking_uri is None:
        tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)


    outer_cv = GroupKFold(n_splits=7)

    scores = {}

    for train_idx, valid_idx in outer_cv.split(
        X_train,
        Y_train,
        groups=temporada_array
    ):

        X_tr = X_train.iloc[train_idx]
        X_val = X_train.iloc[valid_idx]

        y_tr = Y_train.iloc[train_idx]
        y_val = Y_train.iloc[valid_idx]

        def objective(trial):

            pipe = Pipeline([
                ('scaler', StandardScaler()),
                ('pca', PCA(
                    n_components=trial.suggest_int(
                        'pca_n_components', 5, 9
                    )
                )),
                ('model', ElasticNet(
                    alpha=trial.suggest_float(
                        'alpha', 1e-4, 1e1, log=True
                    ),
                    l1_ratio=trial.suggest_categorical(
                        'l1_ratio',
                        [0.1, 0.3, 0.5, 0.7, 0.9]
                    ),
                    max_iter=5000
                ))
            ])

            score = cross_val_score(
                pipe,
                X_tr,
                y_tr,
                cv=4,
                scoring='neg_mean_squared_error',
                n_jobs=-1
            ).mean()

            return score

        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=60)

        best_params = study.best_trial.params
        print("✅ Best params from Optuna:", best_params)
        
        best_model = Pipeline([
            ('scaler', StandardScaler()),
            ('pca', PCA(
                n_components=study.best_params['pca_n_components']
            )),
            ('model', ElasticNet(
                alpha=study.best_params['alpha'],
                l1_ratio=study.best_params['l1_ratio'],
                max_iter=5000
            ))
        ])

        best_model.fit(X_tr, y_tr)

        pred = best_model.predict(X_test)
        r2 = r2_score(Y_test, pred)
        mse = mean_squared_error(Y_test, pred)

        scores = {"r2": r2, "mse": mse}

        print(f"Resultados do Elastic Net. R2: {r2:.4f}. MSE: {mse:.4f}")

        print("\nMelhores parâmetros:")
        print(study.best_params)

        print(f"\nMelhor MSE médio de validação: {study.best_value:.4f}")

        # Salvar em models/
        out = Path(model_output)
        out.parent.mkdir(parents=True, exist_ok=True)
        dump(best_model, out)
        print(f"✅ Best model saved to {out}")

        # Log final best model to MLflow
        with mlflow.start_run(run_name="best_en_model") as run:
            mlflow.log_params(best_params)
            mlflow.log_metrics(scores)
            mlflow.sklearn.log_model(best_model, artifact_path="model")

            features = list(X_train.columns)
            with open ("features.json", "w") as f:
                json.dump(features, f)
            mlflow.log_artifact("features.json")
            # Registrar no Model Registry
            model_uri = f"runs:/{run.info.run_id}/model"
            model_name = "en_model_nbb"

            try:
                client = MlflowClient(tracking_uri=os.environ.get("MLFLOW_TRACKING_URI"))
                mv = mlflow.register_model(model_uri, model_name)
                print(f"✅ Modelo registrado no MLflow Registry: {model_name}, versão {mv.version}")


                client.set_model_version_tag(model_name, mv.version, "r2", str(scores["r2"]))
                print(f"📊 Tag 'r2' adicionada na versão {mv.version} com valor {scores['r2']}")

            except MlflowException as e:
                print(f"❌ Falha ao registrar modelo no MLflow: {e}")

        return best_params, scores

if __name__ == "__main__":
    tune_model()