"""Modelos de dados (Pydantic) do projeto."""

from typing import Optional

from pydantic import BaseModel


class Asteroide(BaseModel):
    """Representa um asteroide (NEO - Near Earth Object) coletado da NASA.

    Cada atributo tem um tipo definido; se a NASA mandar algo fora do
    formato, o Pydantic acusa o erro na hora (validação robusta).
    """

    neo_id: str
    nome: str
    data_aproximacao: str
    diametro_min_m: float
    diametro_max_m: float
    velocidade_kmh: float
    distancia_km: float
    distancia_lunar: float            # 1 = distância Terra-Lua
    potencialmente_perigoso: bool     # flag oficial da NASA

    # Campos preenchidos pela classificação:
    pontuacao_risco: Optional[int] = None   # 0 a 100
    nivel_risco: Optional[str] = None        # BAIXO / MEDIO / ALTO / CRITICO
    anomalia: Optional[bool] = None
