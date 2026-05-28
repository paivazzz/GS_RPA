"""
TÓPICO 1 do semestre: REST API.

Este módulo consome a API pública da NASA (NeoWs - Near Earth Object
Web Service) usando requisições HTTP GET, como visto no slide
"Introdução ao REST" e "AJAX e Fetch API".

A chave é lida da variável de ambiente NASA_API_KEY (boa prática: não
deixar credenciais "chumbadas" no código). Se não existir, usa a
chave pública "DEMO_KEY", que funciona sem cadastro (limite baixo).
Para gerar uma chave grátis: https://api.nasa.gov

Robustez (MELHORIA): o consumo da API é envolvido em try/except com
nova tentativa automática (retry). Se a NASA estiver fora do ar ou
bloquear por excesso de requisições (HTTP 429), o robô NÃO quebra —
ele tenta de novo e, no pior caso, devolve uma lista vazia.
"""

import logging
import os
import time

import requests

logger = logging.getLogger(__name__)

# URL base do recurso (Resource) da API REST da NASA
URL_BASE = "https://api.nasa.gov/neo/rest/v1/feed"

# Chave lida do ambiente; "DEMO_KEY" como padrão (funciona sem cadastro).
API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")

# Quantas vezes tentar antes de desistir, e quanto esperar entre tentativas.
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
            resposta.raise_for_status()  # erro se status != 2xx

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

        # Se chegou aqui, a tentativa falhou. Espera e tenta de novo.
        if tentativa < MAX_TENTATIVAS:
            espera = ESPERA_BASE_SEGUNDOS * tentativa
            logger.info("Nova tentativa em %d segundos...", espera)
            time.sleep(espera)

    logger.error(
        "Não foi possível obter dados da NASA após %d tentativas.",
        MAX_TENTATIVAS,
    )
    return []
