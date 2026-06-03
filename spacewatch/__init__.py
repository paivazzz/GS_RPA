"""SpaceWatch RPA — pacote principal do robô de monitoramento de asteroides."""

import logging

__version__ = "0.1.0"

# Configuração central de logging (usado por todos os módulos no lugar
# de print()). Mensagens saem com data/hora, nível e origem.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
