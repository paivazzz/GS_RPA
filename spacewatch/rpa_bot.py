"""
O ROBÔ (RPA) propriamente dito.

Aqui orquestramos todo o fluxo automatizado, juntando os 3 tópicos:
    1. REST API  -> busca dados na NASA (nasa_client)
    2. Database  -> salva no SQLite (repository)
    + Arquivos   -> gera planilha Excel (relatorio)
    + IA/decisão -> classifica o risco (classificador)

Esta é a "integração de fluxos digitais" que o enunciado da GS pede:
um processo que antes seria manual (entrar no site da NASA, copiar
dados, montar planilha) feito de forma 100% automática.
"""

from datetime import date, timedelta

from . import nasa_client, relatorio
from .classificador import classificar
from .repository import Repository


def executar_monitoramento(dias: int = 1) -> dict:
    """Executa o ciclo completo do robô.

    Parâmetros:
        dias: quantos dias à frente monitorar (a NASA aceita até 7).

    Retorna:
        Um resumo (dict) com as estatísticas da execução.
    """
    print("=" * 60)
    print("SPACEWATCH RPA - iniciando monitoramento de asteroides")
    print("=" * 60)

    # 1) Define o intervalo de datas (hoje até 'dias' à frente).
    hoje = date.today()
    fim = hoje + timedelta(days=dias)
    data_inicio = hoje.strftime("%Y-%m-%d")
    data_fim = fim.strftime("%Y-%m-%d")

    # 2) TÓPICO 1 - REST API: busca os dados brutos na NASA.
    brutos = nasa_client.buscar_asteroides(data_inicio, data_fim)

    # 3) IA/decisão: converte e classifica cada asteroide por risco.
    asteroides = [classificar(item) for item in brutos]

    # 4) TÓPICO 2 - Database: salva tudo no SQLite (limpa antes p/ não duplicar).
    banco = Repository()
    banco.limpar_tabela()
    for asteroide in asteroides:
        banco.inserir_asteroide(asteroide)

    # 5) Arquivos: gera a planilha Excel a partir do banco.
    linhas = banco.selecionar_asteroides()
    caminho_excel = relatorio.gerar_excel(linhas)

    # 6) Monta um resumo para exibir no console / vídeo de apresentação.
    criticos = [a for a in asteroides if a.nivel_risco == "CRITICO"]
    altos = [a for a in asteroides if a.nivel_risco == "ALTO"]

    print("-" * 60)
    print(f"Total coletado:        {len(asteroides)} asteroides")
    print(f"Risco CRITICO:         {len(criticos)}")
    print(f"Risco ALTO:            {len(altos)}")
    print(f"Planilha gerada em:    {caminho_excel}")
    print("-" * 60)

    # Mostra os 3 mais perigosos (já vêm ordenados do banco).
    print("TOP 3 asteroides mais perigosos do periodo:")
    for linha in linhas[:3]:
        nome, nivel, pontos = linha[2], linha[11], linha[10]
        print(f"   - {nome}  |  {nivel}  |  pontuacao {pontos}/100")
    print("=" * 60)

    return {
        "total": len(asteroides),
        "criticos": len(criticos),
        "altos": len(altos),
        "arquivo_excel": caminho_excel,
    }


if __name__ == "__main__":
    # Permite rodar o robô direto: python -m spacewatch.rpa_bot
    executar_monitoramento(dias=1)
