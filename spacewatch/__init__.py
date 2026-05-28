"""
SpaceWatch RPA - Pacote principal.

Robô de automação (RPA) que monitora asteroides próximos à Terra
usando dados reais da NASA. Projeto da disciplina AI for Robotic
Process Automation (GS 2026.1 - FIAP).
"""

import logging

__version__ = "0.1.0"

# Configuração central de logging (usado por todos os módulos no lugar
# de print()). Mensagens saem com data/hora, nível e origem.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
