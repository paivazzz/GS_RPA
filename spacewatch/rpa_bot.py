"""Orquestra o fluxo do robô: NASA → classificação → banco → planilha."""

import logging
from datetime import date, timedelta

from . import nasa_client, relatorio
from .classificador import classificar, detectar_anomalias
from .repository import Repository

logger = logging.getLogger(__name__)


def executar_monitoramento(dias: int = 1, limpar_historico: bool = False) -> dict:
    """Executa o ciclo completo do robô.

    Parâmetros:
        dias: quantos dias à frente monitorar (a NASA aceita até 7).
        limpar_historico: se True, zera o banco antes de coletar.

    Retorna:
        Um resumo (dict) com as estatísticas da execução.
    """
    logger.info("=== SpaceWatch RPA: iniciando monitoramento ===")

    hoje = date.today()
    fim = hoje + timedelta(days=dias)
    data_inicio = hoje.strftime("%Y-%m-%d")
    data_fim = fim.strftime("%Y-%m-%d")

    brutos = nasa_client.buscar_asteroides(data_inicio, data_fim)

    if not brutos:
        logger.warning("Nenhum dado retornado pela NASA. Encerrando sem alterações.")
        # Mesmo formato do retorno de sucesso para o dashboard/API não quebrar.
        return {
            "total": 0,
            "novos": 0,
            "criticos": 0,
            "altos": 0,
            "anomalias": 0,
            "arquivo_excel": None,
        }

    asteroides = [classificar(item) for item in brutos]
    detectar_anomalias(asteroides)

    banco = Repository()
    if limpar_historico:
        banco.limpar_tabela()

    novos = 0
    for asteroide in asteroides:
        if banco.inserir_asteroide(asteroide):
            novos += 1
    logger.info("%d novos asteroides inseridos (%d já existiam no histórico).",
                novos, len(asteroides) - novos)

    linhas = banco.selecionar_asteroides()
    caminho_excel = relatorio.gerar_excel(linhas)

    criticos = [a for a in asteroides if a.nivel_risco == "CRITICO"]
    altos = [a for a in asteroides if a.nivel_risco == "ALTO"]
    anomalias = [a for a in asteroides if a.anomalia]

    print("=" * 60)
    print("SPACEWATCH RPA - RESUMO DA EXECUCAO")
    print("=" * 60)
    print(f"Coletados neste periodo:  {len(asteroides)} asteroides")
    print(f"Novos no historico:        {novos}")
    print(f"Total no banco (historico):{len(linhas)}")
    print(f"Risco CRITICO:             {len(criticos)}")
    print(f"Risco ALTO:                {len(altos)}")
    print(f"Anomalias detectadas:      {len(anomalias)}")
    print(f"Planilha gerada em:        {caminho_excel}")
    print("-" * 60)
    print("TOP 3 asteroides mais perigosos do periodo:")
    for a in sorted(asteroides, key=lambda x: x.pontuacao_risco, reverse=True)[:3]:
        flag = " [ANOMALIA]" if a.anomalia else ""
        print(f"   - {a.nome}  |  {a.nivel_risco}  |  {a.pontuacao_risco}/100{flag}")
    print("=" * 60)

    return {
        "total": len(asteroides),
        "novos": novos,
        "criticos": len(criticos),
        "altos": len(altos),
        "anomalias": len(anomalias),
        "arquivo_excel": caminho_excel,
    }


if __name__ == "__main__":
    executar_monitoramento(dias=1)
