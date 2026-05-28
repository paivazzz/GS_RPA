"""
Ponto de entrada do projeto SpaceWatch RPA.

Rode este arquivo para executar o robô UMA vez:
    poetry run python main.py

Para rodar de forma AGENDADA (automática), use:
    poetry run python -m spacewatch.agendamento

Para subir a API REST:
    poetry run uvicorn spacewatch.api:app --reload
"""

from spacewatch.rpa_bot import executar_monitoramento

if __name__ == "__main__":
    # Monitora os asteroides dos próximos 1 dia.
    # Você pode aumentar para até 7 (limite da API da NASA).
    executar_monitoramento(dias=1)
