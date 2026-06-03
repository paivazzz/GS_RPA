"""Consome a API da NASA (NeoWs) para buscar asteroides, com retry automático."""

import logging
import os
import time

import requests

logger = logging.getLogger(__name__)

URL_BASE = "https://api.nasa.gov/neo/rest/v1/feed"
API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
MAX_TENTATIVAS = 3
ESPERA_BASE_SEGUNDOS = 5


def buscar_asteroides(data_inicio: str, data_fim: str) -> list[dict]:
    """Faz o GET na API da NASA e devolve a lista "crua" de asteroides.

    Parâmetros:
        data_inicio: data inicial no formato 'AAAA-MM-DD'
        data_fim:    data final no formato 'AAAA-MM-DD' (máx. 7 dias depois)

    Retorna:
        Lista de dicionários (cada asteroide como a NASA devolve em JSON).
        Em caso de falha após todas as tentativas, devolve lista vazia
        para que o robô continue funcionando sem travar.
    """
    parametros = {
        "start_date": data_inicio,
        "end_date": data_fim,
        "api_key": API_KEY,
    }

    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            logger.info(
                "Consultando NASA de %s a %s (tentativa %d/%d)...",
                data_inicio, data_fim, tentativa, MAX_TENTATIVAS,
            )
            resposta = requests.get(URL_BASE, params=parametros, timeout=30)
            resposta.raise_for_status()

            dados = resposta.json()

            # A NASA organiza os asteroides por data dentro de
            # "near_earth_objects". Aqui "achatamos" tudo numa lista única.
            asteroides = []
            for lista_do_dia in dados.get("near_earth_objects", {}).values():
                asteroides.extend(lista_do_dia)

            logger.info("%d asteroides recebidos.", len(asteroides))
            return asteroides

        except requests.exceptions.HTTPError as erro:
            status = resposta.status_code
            if status == 429:
                logger.warning("Limite de requisições atingido (HTTP 429).")
            else:
                logger.error("Erro HTTP %s da NASA: %s", status, erro)

        except requests.exceptions.RequestException as erro:
            # Cobre timeout, falta de internet, DNS, etc.
            logger.error("Falha de conexão com a NASA: %s", erro)

        if tentativa < MAX_TENTATIVAS:
            espera = ESPERA_BASE_SEGUNDOS * tentativa
            logger.info("Nova tentativa em %d segundos...", espera)
            time.sleep(espera)

    logger.error(
        "Não foi possível obter dados da NASA após %d tentativas.",
        MAX_TENTATIVAS,
    )
    return []
