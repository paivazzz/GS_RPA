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

O enunciado exige combinar **pelo menos 2 grandes tópicos**. Este projeto usa **3**:

| Tópico do semestre | Onde aparece no código |
|---|---|
| **1. REST API** | `spacewatch/nasa_client.py` — consome a API pública da NASA (NeoWs) via HTTP GET. |
| **2. Arquivos & Database (SQLite)** | `spacewatch/repository.py` — classe `Repository` com CRUD em SQLite + `relatorio.py` gera Excel/CSV com pandas. |
| **3. Execução de scripts & Agendamento (cron)** | `spacewatch/agendamento.py` — agenda o robô para rodar todo dia às 08:00. |

Ainda usa **FastAPI (REST API + padrão MVC)** em `spacewatch/api.py` para servir os dados,
exatamente como visto em aula, e um **dashboard em Streamlit** (`dashboard.py`) que adiciona
o tópico de **Front End (Disciplina 04)** — totalizando **4 tópicos integrados**.

---

## 📂 Estrutura do projeto

```
SpaceWatch-RPA/
├── main.py                 # roda o robô uma vez
├── pyproject.toml          # dependências (Poetry)
├── spacewatch/
│   ├── models.py           # MODEL: classe Asteroide (Pydantic BaseModel)
│   ├── nasa_client.py      # TÓPICO 1: consumo da REST API da NASA
│   ├── classificador.py    # IA/regra: calcula o risco (0 a 100)
│   ├── repository.py        # TÓPICO 2: CRUD no banco SQLite
│   ├── relatorio.py         # Arquivos: gera planilha Excel com pandas
│   ├── rpa_bot.py           # O robô: integra todo o fluxo
│   ├── agendamento.py       # TÓPICO 3: agendamento (cron / schedule)
│   └── api.py               # CONTROLLER: API REST com FastAPI (MVC)
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
pip install requests pandas openpyxl fastapi uvicorn schedule
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

## 🔑 Sobre a chave da NASA

O projeto usa a chave pública `DEMO_KEY` (funciona sem cadastro, com limite baixo).
Para uso intenso, gere uma chave grátis em https://api.nasa.gov e troque o valor de
`API_KEY` em `spacewatch/nasa_client.py`.

---

## 🎬 Roteiro sugerido para o vídeo (pitch)

1. Mostrar o problema (monitorar asteroides manualmente é inviável).
2. Rodar `python main.py` ao vivo e mostrar a planilha sendo gerada.
3. Abrir o `/docs` do FastAPI e consultar os asteroides de risco CRÍTICO.
4. Explicar onde estão os 3 tópicos integrados (tabela acima).
5. Mostrar o agendamento rodando sozinho.
