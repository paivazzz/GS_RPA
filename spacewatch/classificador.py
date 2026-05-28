"""
Classificador de risco (a parte de "IA / apoio à decisão" do projeto).

Aqui aplicamos uma regra inteligente que transforma os dados brutos da
NASA em uma decisão útil: o quão perigoso é cada asteroide?

Damos uma PONTUAÇÃO de 0 a 100 somando fatores de risco e, a partir
dela, definimos um NÍVEL (BAIXO / MEDIO / ALTO / CRITICO). É isso que
permite ao robô "tomar decisão" e priorizar o que importa.

Esta função recebe o dicionário cru da NASA e devolve um objeto
Asteroide (Pydantic) já preenchido e classificado.
"""

from .models import Asteroide


def _converter_para_asteroide(bruto: dict) -> Asteroide:
    """Extrai do JSON da NASA só os campos que interessam e cria o objeto."""
    # A NASA traz a aproximação dentro de uma lista "close_approach_data".
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
    """Soma fatores de risco e devolve uma pontuação de 0 a 100."""
    pontos = 0

    # Fator 1: a própria NASA já marcou como potencialmente perigoso? (+40)
    if asteroide.potencialmente_perigoso:
        pontos += 40

    # Fator 2: tamanho. Asteroides maiores causam mais estrago.
    if asteroide.diametro_max_m >= 1000:        # 1 km ou mais
        pontos += 30
    elif asteroide.diametro_max_m >= 300:
        pontos += 20
    elif asteroide.diametro_max_m >= 100:
        pontos += 10

    # Fator 3: distância. Quanto mais perto, maior o risco.
    # (distancia_lunar = 1 significa a mesma distância da Lua à Terra)
    if asteroide.distancia_lunar <= 1:
        pontos += 30
    elif asteroide.distancia_lunar <= 5:
        pontos += 20
    elif asteroide.distancia_lunar <= 20:
        pontos += 10

    # Garante que a pontuação fique entre 0 e 100.
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
    """Função principal: recebe o JSON cru da NASA e devolve um
    Asteroide já validado e com risco calculado."""
    asteroide = _converter_para_asteroide(bruto)
    asteroide.pontuacao_risco = _calcular_pontuacao(asteroide)
    asteroide.nivel_risco = _definir_nivel(asteroide.pontuacao_risco)
    return asteroide
