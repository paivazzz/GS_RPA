"""
TÓPICO 1 do semestre: REST API.

Este módulo consome a API pública da NASA (NeoWs - Near Earth Object
Web Service) usando requisições HTTP GET, como visto no slide
"Introdução ao REST" e "AJAX e Fetch API".

A API é gratuita. A chave "DEMO_KEY" funciona sem cadastro (com um
limite baixo de requisições). Se quiser, gere uma chave grátis em
https://api.nasa.gov e troque o valor de API_KEY abaixo.

Endpoint usado:
GET https://api.nasa.gov/neo/rest/v1/feed?start_date=...&end_date=...&api_key=...
"""

import requests

# URL base do recurso (Resource) da API REST da NASA
URL_BASE = "https://api.nasa.gov/neo/rest/v1/feed"

# Chave de acesso. DEMO_KEY funciona sem cadastro (limite ~30 req/hora).
API_KEY = "DEMO_KEY"


def buscar_asteroides(data_inicio: str, data_fim: str) -> list[dict]:
    """Faz o GET na API da NASA e devolve a lista "crua" de asteroides.

    Parâmetros:
        data_inicio: data inicial no formato 'AAAA-MM-DD'
        data_fim:    data final no formato 'AAAA-MM-DD' (máx. 7 dias depois)

    Retorna:
        Uma lista de dicionários, cada um representando um asteroide
        exatamente como a NASA devolve (em JSON).
    """
    # Parâmetros da query string (?start_date=...&end_date=...)
    parametros = {
        "start_date": data_inicio,
        "end_date": data_fim,
        "api_key": API_KEY,
    }

    print(f"[NASA] Consultando asteroides de {data_inicio} até {data_fim}...")
    resposta = requests.get(URL_BASE, params=parametros, timeout=30)

    # Levanta um erro se o status HTTP não for 200 (boa prática de REST)
    resposta.raise_for_status()

    dados = resposta.json()

    # A NASA organiza os asteroides por data dentro de "near_earth_objects".
    # Aqui "achatamos" tudo em uma lista única para facilitar o processamento.
    asteroides = []
    for lista_do_dia in dados.get("near_earth_objects", {}).values():
        asteroides.extend(lista_do_dia)

    print(f"[NASA] {len(asteroides)} asteroides recebidos.")
    return asteroides
