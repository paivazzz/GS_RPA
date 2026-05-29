"""
TÓPICO 3 do semestre: Execução de scripts & Agendamento (cron).

O robô RPA só tem valor se rodar SOZINHO, sem ninguém clicar nada.
Aqui mostramos as duas formas vistas em aula:

(A) A EXPRESSÃO CRON  -> o "padrão" universal de agendamento. Documentamos
    a expressão certa para rodar o robô todo dia às 08:00, no formato de
    5 campos: minuto hora dia mês dia-da-semana.

(B) A EXECUÇÃO REAL no Windows -> como o Windows não tem o cron do Linux,
    usamos a biblioteca 'schedule', que faz o mesmo papel de forma
    multiplataforma e mantém o script rodando em loop.

Para usar o cron de verdade (em Linux/servidor), bastaria colocar a
linha CRON_DIARIO_8H no crontab apontando para o main.py.
"""

import time

import schedule

from .rpa_bot import executar_monitoramento


# (A) Expressões cron de referência (formato: minuto hora dia mes dia_semana)
#     - de segunda a sexta, 18h:  0 18 * * 1-5
#     - a cada 6 horas:           0 */6 * * *
# A que o robô usa de fato é a diária às 08:00:
CRON_DIARIO_8H = "0 8 * * *"


def iniciar_agendador():
    """Mantém o robô rodando automaticamente, sem intervenção humana.

    Equivalente prático do cron '0 8 * * *' (todo dia às 08:00),
    porém funcionando no Windows com a biblioteca 'schedule'.
    """
    # Agenda: todo dia, às 08:00, executar o monitoramento.
    schedule.every().day.at("08:00").do(executar_monitoramento, dias=1)

    print("[AGENDADOR] Robô agendado para rodar todos os dias às 08:00.")
    print("[AGENDADOR] (equivalente ao cron:  " + CRON_DIARIO_8H + ")")
    print("[AGENDADOR] Mantenha esta janela aberta. Ctrl+C para parar.")

    # Loop infinito que verifica, a cada 60s, se chegou a hora de executar.
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    iniciar_agendador()
