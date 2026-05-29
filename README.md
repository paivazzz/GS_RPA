# 🛰️ SpaceWatch RPA — Monitoramento de Asteroides com Dados da NASA

Projeto da disciplina **AI for Robotic Process Automation** — Global Solution 2026.1 (FIAP).

Um robô (RPA) que automatiza um processo que hoje seria manual: entrar no site da NASA,
coletar os dados dos asteroides que se aproximam da Terra, classificar o risco de cada um,
salvar tudo num banco de dados e gerar uma planilha pronta para a tomada de decisão — **sem
ninguém clicar em nada**.

---

## 🚀 O problema que resolve (narrativa espacial)

A exploração espacial gera uma enxurrada de dados. Um deles é o monitoramento de **NEOs**
(*Near Earth Objects*) — asteroides que passam perto da Terra. Acompanhar isso manualmente
é inviável. O **SpaceWatch RPA** automatiza esse monitoramento e entrega, todo dia, um
relatório priorizado por risco, ajudando na **prevenção de desastres** (um dos temas
sugeridos no desafio da GS).

---

## 🧩 Os grandes tópicos de AI for RPA que o projeto integra

O enunciado exige combinar **pelo menos 2 grandes tópicos** da disciplina.
Este projeto integra **3** dos tópicos vistos em AI for RPA:

| # | Grande tópico (AI for RPA) | Onde aparece no código |
|---|---|---|
| **1** | **Consumo de REST API** | `spacewatch/nasa_client.py` — consome a API pública da NASA (NeoWs) via HTTP GET, com retry e tratamento de erro. |
| **2** | **Arquivos & Database** | `spacewatch/repository.py` — classe `Repository` com CRUD em SQLite + `relatorio.py` gera Excel/CSV com pandas. |
| **3** | **Execução de scripts & Agendamento** | `spacewatch/agendamento.py` — agenda o robô para rodar todo dia às 08:00 (cron / `schedule`). |

Tudo é amarrado pelo robô (`spacewatch/rpa_bot.py`), que orquestra o fluxo de
ponta a ponta — a "integração de fluxos digitais" que o enunciado pede.

---

## 🎯 Como o projeto cobre a matriz de avaliação

| Critério (peso) | Onde o projeto entrega |
|---|---|
| **Domínio Técnico e Integração (40%)** | Integra 3 grandes tópicos de AI for RPA (REST API + Arquivos/DB + Agendamento) num fluxo automatizado funcional. |
| **Arquitetura de Fluxo e Engenharia (25%)** | Padrão MVC + `Repository`, `FastAPI` (`api.py`), tratamento de exceções/retry na API da NASA, testes com `pytest` e um **log de auditoria** (`auditoria.py`) que dá rastreabilidade ao robô. |
| **Inteligência de Dados e IA (20%)** | `classificador.py` — pontuação de risco 0–100 + **detecção de anomalias** estatística com pandas. |
| **Entrega de Artefatos e Outputs (15%)** | Planilha Excel/CSV, banco SQLite, API REST em JSON e **dashboard Streamlit** (carga de dados estruturados para o front-end). |

---

## 📂 Estrutura do projeto

```
SpaceWatch-RPA/
├── main.py                 # roda o robô uma vez
├── dashboard.py            # front end / output (Streamlit) — entrada multipágina
├── pyproject.toml          # dependências (Poetry)
├── requirements.txt        # dependências (caminho via pip)
├── paginas/                # páginas do app Streamlit (st.navigation)
│   ├── painel.py           # página do monitoramento (cards, gráficos, tabela)
│   └── historico.py        # página da auditoria/rastreabilidade
├── spacewatch/
│   ├── models.py           # MODEL: classe Asteroide (Pydantic BaseModel)
│   ├── nasa_client.py      # TÓPICO 1: consumo da REST API da NASA
│   ├── classificador.py    # IA/análise: risco (0 a 100) + anomalias
│   ├── repository.py       # TÓPICO 2: CRUD no banco SQLite
│   ├── relatorio.py        # Arquivos: gera planilha Excel/CSV com pandas
│   ├── rpa_bot.py          # O robô: integra todo o fluxo
│   ├── agendamento.py      # TÓPICO 3: agendamento (cron / schedule)
│   ├── auditoria.py        # robustez: histórico de uso (rastreabilidade)
│   └── api.py              # CONTROLLER: API REST com FastAPI (MVC)
└── tests/
    ├── test_classificador.py   # testes da IA/análise (pytest)
    └── test_auditoria.py       # testes da governança/auditoria (pytest)
```

---

## ⚙️ Como instalar e rodar

### Opção A — com Poetry (como o professor ensinou)

```bash
# 1. instalar as dependências
poetry install

# 2. rodar o robô uma vez
poetry run python main.py
```

### Opção B — com pip (mais simples, se não tiver Poetry)

```bash
pip install -r requirements.txt
python main.py
```

Ao rodar, o robô vai:
1. Buscar os asteroides do dia na NASA;
2. Classificar o risco de cada um;
3. Salvar no banco `spacewatch.db`;
4. Gerar a planilha `relatorio_asteroides.xlsx`;
5. Mostrar no terminal o TOP 3 mais perigosos.

---

## 🌐 Rodar a API REST (opcional, mostra o MVC)

```bash
poetry run uvicorn spacewatch.api:app --reload
```

Depois abra no navegador: **http://127.0.0.1:8000/docs**

Endpoints:
- `GET /asteroides` → lista todos (ordenados por risco)
- `GET /asteroides/CRITICO` → só os de risco crítico
- `POST /executar` → dispara o robô pela API

---

## ⏰ Rodar de forma agendada (automática)

```bash
poetry run python -m spacewatch.agendamento
```

O robô passa a rodar **todo dia às 08:00** automaticamente.
Expressão cron equivalente (Linux/servidor): `0 8 * * *`

---

## 📊 Dashboard visual (output / front-end)

```bash
poetry run streamlit run dashboard.py
```

Abre no navegador um app com **duas páginas** (menu na lateral):

- **🛰️ Painel** — filtros, indicadores e gráficos interativos (asteroides
  por nível de risco, distância x tamanho) e um botão para disparar o robô
  na hora. É a **carga de dados estruturados para o front-end** que a
  rubrica de "Entrega de Artefatos" valoriza.
- **📜 Histórico de uso** — página dedicada à auditoria (veja abaixo).

Antes de tudo, é preciso **digitar o nome** na barra lateral (identificação).

---

## 🔒 Rastreabilidade / histórico de uso

Para usar o painel, a pessoa precisa **se identificar com o nome**. A partir
daí, todo evento relevante é gravado num **histórico auditável** (tabela
`auditoria` no mesmo SQLite):

- quem **executou o robô** (e com quantos dias / quantos asteroides);
- quem **consultou** os dados e qual **filtro** aplicou;
- com **carimbo de data e hora** de cada ação.

Basta clicar em **"📜 Ver histórico de uso"** no dashboard para ver tudo.
É uma boa prática de RPA: o robô fica **auditável** e o fluxo, rastreável
(reforça o critério de "Arquitetura de Fluxo e Engenharia de Software").

---

## 🧪 Testes automatizados

O projeto tem testes com **pytest** (qualidade de código):

```bash
poetry run pytest        # ou simplesmente:  python -m pytest
```

Eles validam a pontuação de risco, a classificação por nível e a detecção de anomalias.

---

## 🔑 Sobre a chave da NASA

O projeto usa a chave pública `DEMO_KEY` (funciona sem cadastro, com limite baixo).
Para uso intenso, gere uma chave grátis em https://api.nasa.gov e defina a **variável
de ambiente** `NASA_API_KEY` (boa prática — não deixa a chave no código):

```powershell
# Windows (PowerShell)
$env:NASA_API_KEY = "sua_chave_aqui"
python main.py
```

Se a NASA estiver fora do ar ou bloquear por excesso de requisições, o robô **não quebra**:
ele tenta novamente (retry automático) e registra tudo via `logging`.

---

## 🎬 Roteiro sugerido para o vídeo (pitch)

1. Mostrar o problema (monitorar asteroides manualmente é inviável).
2. Rodar `python main.py` ao vivo e mostrar a planilha sendo gerada.
3. Abrir o `/docs` do FastAPI e consultar os asteroides de risco CRÍTICO.
4. Explicar os 3 grandes tópicos de AI for RPA integrados (tabela acima).
5. Mostrar o dashboard e o histórico de uso (rastreabilidade do robô).
6. Mostrar o agendamento rodando sozinho.
