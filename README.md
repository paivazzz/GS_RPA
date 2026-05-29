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

## 🧩 Os 2+ tópicos do semestre que o projeto integra

O enunciado exige combinar **pelo menos 2 grandes tópicos**. Este projeto integra **5**:

| # | Tópico do semestre | Onde aparece no código |
|---|---|---|
| **1** | **REST API** | `spacewatch/nasa_client.py` — consome a API pública da NASA (NeoWs) via HTTP GET, com retry e tratamento de erro. |
| **2** | **Arquivos & Database (SQLite)** | `spacewatch/repository.py` — classe `Repository` com CRUD em SQLite + `relatorio.py` gera Excel/CSV com pandas. |
| **3** | **Execução de scripts & Agendamento (cron)** | `spacewatch/agendamento.py` — agenda o robô para rodar todo dia às 08:00. |
| **4** | **Front End (Disciplina 04)** | `dashboard.py` — dashboard em Streamlit com filtros, indicadores e gráficos. |
| **5** | **Governança em IA (Disciplina 09)** | `spacewatch/auditoria.py` — exige identificação por nome e registra um **histórico auditável** de quem executou o robô e o que cada um consultou. |

Como camada extra, usa **FastAPI (REST API + padrão MVC)** em `spacewatch/api.py` para
servir os dados em JSON, exatamente como visto em aula. A camada de **IA/análise de dados**
fica em `spacewatch/classificador.py` (pontuação de risco 0–100 + detecção de anomalias
estatística com pandas).

---

## 📂 Estrutura do projeto

```
SpaceWatch-RPA/
├── main.py                 # roda o robô uma vez
├── dashboard.py            # TÓPICO 4: front end (Streamlit)
├── pyproject.toml          # dependências (Poetry)
├── requirements.txt        # dependências (caminho via pip)
├── spacewatch/
│   ├── models.py           # MODEL: classe Asteroide (Pydantic BaseModel)
│   ├── nasa_client.py      # TÓPICO 1: consumo da REST API da NASA
│   ├── classificador.py    # IA/análise: risco (0 a 100) + anomalias
│   ├── repository.py       # TÓPICO 2: CRUD no banco SQLite
│   ├── relatorio.py        # Arquivos: gera planilha Excel/CSV com pandas
│   ├── rpa_bot.py          # O robô: integra todo o fluxo
│   ├── agendamento.py      # TÓPICO 3: agendamento (cron / schedule)
│   ├── auditoria.py        # TÓPICO 5: governança (histórico de uso)
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

## 📊 Dashboard visual (Front End — Disciplina 04)

```bash
poetry run streamlit run dashboard.py
```

Abre no navegador uma interface com filtros, indicadores e gráficos
interativos (asteroides por nível de risco, distância x tamanho) e um
botão para disparar o robô na hora.

---

## 🔒 Governança e rastreabilidade (Disciplina 09)

Para usar o painel, a pessoa precisa **se identificar com o nome**. A partir
daí, todo evento relevante é gravado num **histórico auditável** (tabela
`auditoria` no mesmo SQLite):

- quem **executou o robô** (e com quantos dias / quantos asteroides);
- quem **consultou** os dados e qual **filtro** aplicou;
- com **carimbo de data e hora** de cada ação.

Basta clicar em **"📜 Ver histórico de uso"** no dashboard para ver tudo.
Isso dá ao projeto a camada de **governança/rastreabilidade** que a
Disciplina 09 (a integradora da GS) exige.

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
4. Explicar onde estão os 3 tópicos integrados (tabela acima).
5. Mostrar o agendamento rodando sozinho.
