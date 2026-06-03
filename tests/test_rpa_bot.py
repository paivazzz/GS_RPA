"""Testes do robô (orquestração do fluxo), com a NASA simulada."""

from spacewatch import rpa_bot

# Um asteroide "cru" no formato que a NASA devolve (o mínimo que o código usa).
ASTEROIDE_CRU = {
    "id": "111",
    "name": "(2026 TESTE)",
    "is_potentially_hazardous_asteroid": False,
    "estimated_diameter": {
        "meters": {"estimated_diameter_min": 50.0, "estimated_diameter_max": 120.0}
    },
    "close_approach_data": [
        {
            "close_approach_date": "2026-06-01",
            "relative_velocity": {"kilometers_per_hour": "50000"},
            "miss_distance": {"kilometers": "1000000", "lunar": "3.0"},
        }
    ],
}


def test_executar_sem_dados_nao_quebra(monkeypatch, tmp_path):
    """Quando a NASA não devolve nada, o resumo deve ter TODAS as chaves."""
    monkeypatch.chdir(tmp_path)  # isola banco/planilha numa pasta temporária
    monkeypatch.setattr(rpa_bot.nasa_client, "buscar_asteroides",
                        lambda inicio, fim: [])

    resumo = rpa_bot.executar_monitoramento(dias=1)

    # O dashboard lê todas estas chaves; faltar uma quebrava a página.
    assert set(resumo) == {"total", "novos", "criticos", "altos",
                           "anomalias", "arquivo_excel"}
    assert resumo["total"] == 0
    assert resumo["novos"] == 0
    assert resumo["arquivo_excel"] is None


def test_executar_com_dados_salva_e_nao_duplica(monkeypatch, tmp_path):
    """Com dados, salva e gera a planilha; rodar de novo não duplica."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(rpa_bot.nasa_client, "buscar_asteroides",
                        lambda inicio, fim: [ASTEROIDE_CRU])

    resumo = rpa_bot.executar_monitoramento(dias=1)
    assert resumo["total"] == 1
    assert resumo["novos"] == 1
    assert resumo["arquivo_excel"] is not None
    assert (tmp_path / "relatorio_asteroides.xlsx").exists()

    # Segunda execução: o mesmo asteroide (neo_id+data) não pode duplicar.
    resumo2 = rpa_bot.executar_monitoramento(dias=1)
    assert resumo2["total"] == 1
    assert resumo2["novos"] == 0
