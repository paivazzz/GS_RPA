# SpaceWatch RPA — Monitoramento de Asteroides com Dados da NASA

Robô de automação (RPA) da disciplina **AI for Robotic Process Automation** — Global Solution 2026.1 

Todo dia a NASA publica dados dos asteroides que passam perto da Terra. Acompanhar isso na mão é
trabalhoso e repetitivo — o tipo de tarefa que um robô resolve melhor. O SpaceWatch faz o ciclo
inteiro sozinho: busca os asteroides do dia na API da NASA, calcula o risco de cada um, guarda no
banco, gera uma planilha e ainda agrupa os asteroides por perfil com um modelo de IA.

Integra 3 tópicos da disciplina: **REST API** (`nasa_client.py`), **Arquivos & Database**
(`repository.py`) e **Execução & Agendamento** (`agendamento.py`).

## O fluxo, em ordem

1. **Coleta** — consome a API da NASA (NeoWs) e baixa os asteroides do período.
2. **Análise** — pontua o risco de cada um (0–100), classifica em BAIXO/MÉDIO/ALTO/CRÍTICO e marca anomalias estatísticas.
3. **Armazenamento** — salva num banco SQLite, acumulando histórico sem duplicar.
4. **Saída** — gera a planilha `relatorio_asteroides.xlsx` e mostra no terminal os 3 mais perigosos.
5. **Extras** — API REST para consulta, agendamento diário, dashboard web e agrupamento por K-Means.

## Como rodar

Tudo a partir da pasta `SpaceWatch-RPA`. Instale as dependências uma vez:

```bash
pip install -r requirements.txt
```

**Robô (uma execução):**

```bash
python main.py
```

**Dashboard web** — três páginas: Painel, Agrupamento (IA) e Histórico de uso:

```bash
python -m streamlit run dashboard.py
```

**API REST** — abre em `http://127.0.0.1:8000/docs`:

```bash
python -m uvicorn spacewatch.api:app --reload
```

Rotas: `GET /asteroides`, `GET /asteroides/{nivel}` (ex.: `CRITICO`), `POST /executar`.

**Agendamento** — passa a rodar sozinho todo dia às 08:00 (equivale ao cron `0 8 * * *`):

```bash
python -m spacewatch.agendamento
```

**Testes:**

```bash
python -m pytest
```