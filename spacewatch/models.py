"""
Camada MODEL (do padrão MVC visto em aula).

Aqui definimos a estrutura dos dados usando Pydantic (BaseModel),
exatamente como o professor mostrou no slide "Estrutura MVC - Modelo".
O Pydantic valida automaticamente os tipos quando criamos o objeto.
"""

from typing import Optional

from pydantic import BaseModel


class Asteroide(BaseModel):
    """Representa um asteroide (NEO - Near Earth Object) coletado da NASA.

    Cada atributo tem um tipo definido; se a NASA mandar algo fora do
    formato, o Pydantic acusa o erro na hora (validação robusta).
    """

    neo_id: str                      # identificador único do asteroide na NASA
    nome: str                        # nome/designação (ex.: "(2024 AB1)")
    data_aproximacao: str            # data da maior aproximação (AAAA-MM-DD)
    diametro_min_m: float            # diâmetro estimado mínimo, em metros
    diametro_max_m: float            # diâmetro estimado máximo, em metros
    velocidade_kmh: float            # velocidade relativa, em km/h
    distancia_km: float              # distância da Terra na aproximação, em km
    distancia_lunar: float           # distância em "distâncias lunares" (1 = Terra-Lua)
    potencialmente_perigoso: bool    # flag oficial da NASA (is_potentially_hazardous)

    # Campos preenchidos pela nossa "IA"/análise:
    pontuacao_risco: Optional[int] = None   # 0 a 100
    nivel_risco: Optional[str] = None        # BAIXO / MEDIO / ALTO / CRITICO
    anomalia: Optional[bool] = None          # risco estatisticamente atípico no lote
