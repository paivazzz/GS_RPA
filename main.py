"""Ponto de entrada: executa o robô SpaceWatch RPA uma vez."""

from spacewatch.rpa_bot import executar_monitoramento

if __name__ == "__main__":
    # Monitora os asteroides dos próximos 1 dia.
    # Você pode aumentar para até 7 (limite da API da NASA).
    executar_monitoramento(dias=1)
