# SpaceWatch RPA — Monitoramento de Asteroides com Dados da NASA

Projeto da disciplina **AI for Robotic Process Automation** — Global Solution 2026.1 (FIAP).

A ideia é simples: todo dia surgem dados sobre asteroides que passam perto da Terra, e
acompanhar isso na mão seria trabalhoso. Então criei um robô que faz esse trabalho sozinho —
ele entra na API da NASA, pega os asteroides do dia, calcula o quão perigoso é cada um, guarda
tudo num banco de dados e ainda gera uma planilha pronta para olhar. Ninguém precisa clicar
em nada.

## Como instalar e rodar

Abra o terminal **dentro da pasta `SpaceWatch-RPA`** e rode:

```bash
pip install -r requirements.txt
python main.py
```

Quando você roda, o robô busca os asteroides do dia, calcula o risco de cada um, salva tudo no
banco `spacewatch.db`, gera a planilha `relatorio_asteroides.xlsx` e mostra no terminal os 3
mais perigosos.

## API REST (opcional)

```bash
python -m uvicorn spacewatch.api:app --reload
```

Depois é só abrir `http://127.0.0.1:8000/docs` no navegador. De lá dá para:

- `GET /asteroides` — ver todos, do mais perigoso para o menos
- `GET /asteroides/CRITICO` — filtrar só por um nível de risco
- `POST /executar` — disparar o robô na hora

## Agendamento

```bash
python -m spacewatch.agendamento
```

Com isso o robô passa a rodar sozinho todo dia às 08:00. No Linux, o mesmo efeito sairia com o
cron `0 8 * * *`.

## Dashboard

```bash
python -m streamlit run dashboard.py
```

Abre um app com duas páginas: o **Painel**, com filtros, números e gráficos dos asteroides, e
o **Histórico de uso**, que mostra quem mexeu no sistema. Antes de entrar, você digita seu nome
na lateral — assim tudo o que cada pessoa faz fica registrado, dá para saber quem fez o quê.

## Testes

```bash
python -m pytest
```

Os testes conferem se o cálculo de risco, a detecção de anomalias, o banco de dados, a geração
da planilha, o histórico de uso e o robô como um todo estão funcionando direito.

## Chave da NASA

Por padrão o projeto usa a chave pública `DEMO_KEY`, que já funciona, mas tem limite baixo de
uso. Se quiser usar bastante, é só pegar uma chave grátis em https://api.nasa.gov e colocar na
variável de ambiente `NASA_API_KEY`. E não se preocupe: se a NASA cair ou travar, o robô tenta
de novo sozinho e não quebra.
