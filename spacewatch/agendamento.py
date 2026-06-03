"""Agendamento do robô: expressão cron e execução via biblioteca schedule."""

import time

import schedule

from .rpa_bot import executar_monitoramento


# Cron equivalente (minuto hora dia mes dia_semana): todo dia às 08:00.
CRON_DIARIO_8H = "0 8 * * *"


def iniciar_agendador():
    """Mantém o robô rodando automaticamente, sem intervenção humana.

    Equivalente prático do cron '0 8 * * *' (todo dia às 08:00),
    porém funcionando no Windows com a biblioteca 'schedule'.
    """
    schedule.every().day.at("08:00").do(executar_monitoramento, dias=1)

    print("[AGENDADOR] Robô agendado para rodar todos os dias às 08:00.")
    print("[AGENDADOR] (equivalente ao cron:  " + CRON_DIARIO_8H + ")")
    print("[AGENDADOR] Mantenha esta janela aberta. Ctrl+C para parar.")

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    iniciar_agendador()
