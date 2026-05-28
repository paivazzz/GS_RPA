"""
Classificador de risco — a camada de "IA / análise de dados" do projeto.

Aqui transformamos os dados brutos da NASA em uma DECISÃO útil:
o quão perigoso é cada asteroide?

Duas técnicas:
1) PONTUAÇÃO ponderada (0 a 100): soma fatores de risco (perigo oficial,
   tamanho, distância e velocidade) → vira um nível BAIXO/MEDIO/ALTO/CRITICO.
2) DETECÇÃO DE ANOMALIAS (estatística com pandas): marca os asteroides
   cujo risco é estatisticamente atípico dentro do lote analisado
   (acima da média + 1 desvio-padrão). Isso é um algoritmo de análise
   de dados, não apenas uma regra fixa.
"""

import logging

import pandas as pd

from .models import Asteroide

logger = logging.getLogger(__name__)


def _converter_para_asteroide(bruto: dict) -> Asteroide:
    """Extrai do JSON da NASA só os campos que interessam e cria o objeto."""
    aproximacao = bruto["close_approach_data"][0]
    diametro = bruto["estimated_diameter"]["meters"]

    return Asteroide(
        neo_id=bruto["id"],
        nome=bruto["name"],
        data_aproximacao=aproximacao["close_approach_date"],
        diametro_min_m=round(diametro["estimated_diameter_min"], 2),
        diametro_max_m=round(diametro["estimated_diameter_max"], 2),
        velocidade_kmh=round(
            float(aproximacao["relative_velocity"]["kilometers_per_hour"]), 2
        ),
        distancia_km=round(float(aproximacao["miss_distance"]["kilometers"]), 2),
        distancia_lunar=round(float(aproximacao["miss_distance"]["lunar"]), 2),
        potencialmente_perigoso=bruto["is_potentially_hazardous_asteroid"],
    )


def _calcular_pontuacao(asteroide: Asteroide) -> int:
    """Soma fatores ponderados de risco. Máximo possível = 100 pontos."""
    pontos = 0

    # Fator 1 (até 35): a NASA já o marcou como potencialmente perigoso?
    if asteroide.potencialmente_perigoso:
        pontos += 35

    # Fator 2 (até 25): tamanho. Asteroides maiores causam mais estrago.
    if asteroide.diametro_max_m >= 1000:        # 1 km ou mais
        pontos += 25
    elif asteroide.diametro_max_m >= 300:
        pontos += 17
    elif asteroide.diametro_max_m >= 100:
        pontos += 8

    # Fator 3 (até 25): distância. Quanto mais perto, maior o risco.
    # (distancia_lunar = 1 equivale à distância Terra-Lua)
    if asteroide.distancia_lunar <= 1:
        pontos += 25
    elif asteroide.distancia_lunar <= 5:
        pontos += 17
    elif asteroide.distancia_lunar <= 20:
        pontos += 8

    # Fator 4 (até 15): velocidade. Mais rápido = mais energia no impacto.
    if asteroide.velocidade_kmh >= 100000:
        pontos += 15
    elif asteroide.velocidade_kmh >= 70000:
        pontos += 10
    elif asteroide.velocidade_kmh >= 40000:
        pontos += 5

    return min(pontos, 100)


def _definir_nivel(pontuacao: int) -> str:
    """Traduz a pontuação numérica em um rótulo fácil de entender."""
    if pontuacao >= 70:
        return "CRITICO"
    if pontuacao >= 45:
        return "ALTO"
    if pontuacao >= 20:
        return "MEDIO"
    return "BAIXO"


def classificar(bruto: dict) -> Asteroide:
    """Recebe o JSON cru da NASA e devolve um Asteroide validado e classificado."""
    asteroide = _converter_para_asteroide(bruto)
    asteroide.pontuacao_risco = _calcular_pontuacao(asteroide)
    asteroide.nivel_risco = _definir_nivel(asteroide.pontuacao_risco)
    return asteroide


def detectar_anomalias(asteroides: list[Asteroide]) -> list[Asteroide]:
    """Marca como anomalia os asteroides com risco estatisticamente atípico.

    Usa pandas para calcular média e desvio-padrão das pontuações do lote.
    Um asteroide é "anomalia" se sua pontuação > média + 1 desvio-padrão.
    Preenche o campo .anomalia de cada objeto (True/False).
    """
    if not asteroides:
        return asteroides

    df = pd.DataFrame({"pontuacao": [a.pontuacao_risco for a in asteroides]})
    media = df["pontuacao"].mean()
    desvio = df["pontuacao"].std()

    # std() é NaN quando há só 1 item; nesse caso não há como ter "anomalia".
    if pd.isna(desvio) or desvio == 0:
        for a in asteroides:
            a.anomalia = False
        return asteroides

    limite = media + desvio
    qtd = 0
    for a in asteroides:
        a.anomalia = bool(a.pontuacao_risco > limite)
        qtd += int(a.anomalia)

    logger.info(
        "Detecção de anomalias: %d de %d acima de média+desvio (limite=%.1f).",
        qtd, len(asteroides), limite,
    )
    return asteroides
