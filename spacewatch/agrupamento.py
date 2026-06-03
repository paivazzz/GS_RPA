"""Agrupa os asteroides por perfil semelhante com K-Means (aprendizado não supervisionado)."""

import logging

import pandas as pd

from .repository import COLUNAS

logger = logging.getLogger(__name__)

# Características numéricas usadas para agrupar (todas já existem no banco).
FEATURES = ["pontuacao_risco", "diametro_max_m", "distancia_lunar", "velocidade_kmh"]


def agrupar_por_perfil(linhas: list, n_clusters: int = 3) -> pd.DataFrame:
    """Agrupa os asteroides em perfis semelhantes com K-Means.

    Normaliza as características numéricas e aplica K-Means. Devolve um
    DataFrame com a coluna `cluster` (número do grupo) e `perfil` (nome
    legível, ordenado do menor para o maior risco médio).

    Requer scikit-learn; se faltar, levanta ImportError com instrução.
    """
    try:
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
    except ImportError as erro:
        raise ImportError(
            "Este recurso precisa do scikit-learn. Instale com: pip install scikit-learn"
        ) from erro

    df = pd.DataFrame(linhas, columns=COLUNAS)

    # Com poucos asteroides não faz sentido formar muitos grupos.
    n_clusters = min(n_clusters, len(df))
    if n_clusters < 2:
        df["cluster"] = 0
        df["perfil"] = "Grupo único"
        return df

    # Padroniza para que nenhuma feature (ex.: velocidade) domine pela escala.
    X = StandardScaler().fit_transform(df[FEATURES])
    modelo = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["cluster"] = modelo.fit_predict(X)

    # Nomeia os grupos do menor para o maior risco médio (mais fácil de ler).
    ordem = df.groupby("cluster")["pontuacao_risco"].mean().sort_values().index.tolist()
    nomes = _nomes_dos_perfis(len(ordem))
    rotulo = {cluster: nomes[i] for i, cluster in enumerate(ordem)}
    df["perfil"] = df["cluster"].map(rotulo)

    logger.info("K-Means agrupou %d asteroides em %d perfis.", len(df), n_clusters)
    return df


def _nomes_dos_perfis(qtd: int) -> list:
    """Nomes legíveis dos grupos, do menor para o maior risco."""
    if qtd == 2:
        return ["Menor risco", "Maior risco"]
    if qtd == 3:
        return ["Menor risco", "Risco intermediário", "Maior risco"]
    return [f"Perfil {i + 1}" for i in range(qtd)]
