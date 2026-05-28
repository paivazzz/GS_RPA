"""
Testes automatizados do classificador de risco (pytest).

Garante que a lógica de pontuação, classificação por nível e detecção
de anomalias funcione como esperado. Rodar com:  poetry run pytest
"""

from spacewatch.classificador import (
    _calcular_pontuacao,
    _definir_nivel,
    classificar,
    detectar_anomalias,
)
from spacewatch.models import Asteroide


def _asteroide(perigoso, diametro_max, dist_lunar, velocidade):
    """Helper que cria um Asteroide de teste com os campos relevantes."""
    return Asteroide(
        neo_id="000",
        nome="(teste)",
        data_aproximacao="2026-06-01",
        diametro_min_m=diametro_max / 2,
        diametro_max_m=diametro_max,
        velocidade_kmh=velocidade,
        distancia_km=dist_lunar * 384400,  # 1 distância lunar ≈ 384.400 km
        distancia_lunar=dist_lunar,
        potencialmente_perigoso=perigoso,
    )


def test_asteroide_perigoso_grande_e_proximo_e_critico():
    """Perigoso + grande + perto + rápido deve dar nível CRITICO."""
    a = _asteroide(perigoso=True, diametro_max=1200, dist_lunar=0.5, velocidade=110000)
    pontos = _calcular_pontuacao(a)  # 35 + 25 + 25 + 15 = 100
    assert pontos == 100
    assert _definir_nivel(pontos) == "CRITICO"


def test_asteroide_pequeno_e_distante_e_baixo():
    """Não perigoso + pequeno + longe + lento deve dar nível BAIXO."""
    a = _asteroide(perigoso=False, diametro_max=10, dist_lunar=50, velocidade=10000)
    pontos = _calcular_pontuacao(a)  # 0
    assert pontos == 0
    assert _definir_nivel(pontos) == "BAIXO"


def test_pontuacao_nunca_passa_de_100():
    """A pontuação deve ser sempre limitada a 100."""
    a = _asteroide(perigoso=True, diametro_max=5000, dist_lunar=0.1, velocidade=200000)
    assert _calcular_pontuacao(a) <= 100


def test_fronteiras_dos_niveis():
    """Confere os limites entre os níveis de risco."""
    assert _definir_nivel(70) == "CRITICO"
    assert _definir_nivel(69) == "ALTO"
    assert _definir_nivel(45) == "ALTO"
    assert _definir_nivel(44) == "MEDIO"
    assert _definir_nivel(20) == "MEDIO"
    assert _definir_nivel(19) == "BAIXO"


def test_classificar_a_partir_de_json_da_nasa():
    """A função classificar() deve processar o JSON cru da NASA."""
    bruto = {
        "id": "12345",
        "name": "(2026 TESTE)",
        "is_potentially_hazardous_asteroid": True,
        "estimated_diameter": {
            "meters": {"estimated_diameter_min": 500.0, "estimated_diameter_max": 1100.0}
        },
        "close_approach_data": [
            {
                "close_approach_date": "2026-06-01",
                "relative_velocity": {"kilometers_per_hour": "105000"},
                "miss_distance": {"kilometers": "200000", "lunar": "0.5"},
            }
        ],
    }
    a = classificar(bruto)
    assert a.neo_id == "12345"
    assert a.potencialmente_perigoso is True
    assert a.nivel_risco == "CRITICO"


def test_deteccao_de_anomalias():
    """Um asteroide muito acima da média deve ser marcado como anomalia."""
    baixos = [_asteroide(False, 10, 50, 10000) for _ in range(5)]
    for b in baixos:
        b.pontuacao_risco = 0
    extremo = _asteroide(True, 1200, 0.5, 110000)
    extremo.pontuacao_risco = 100

    lote = baixos + [extremo]
    detectar_anomalias(lote)

    assert extremo.anomalia is True
    assert all(b.anomalia is False for b in baixos)
