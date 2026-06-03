"""API REST (FastAPI) para consultar os asteroides e disparar o robô."""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from .repository import COLUNAS, Repository
from .rpa_bot import executar_monitoramento

app = FastAPI(title="SpaceWatch RPA", version="0.1.0")
banco = Repository()


def _para_json(linhas: list) -> list[dict]:
    """Converte as linhas (tuplas) do banco em dicionários nome->valor.

    Sem isso, a API devolveria listas cruas (ex.: [1, "54016", ...]) e
    quem consome não saberia qual valor é qual. Com os nomes das colunas
    o JSON fica autoexplicativo — boa prática de API REST.
    """
    return [dict(zip(COLUNAS, linha)) for linha in linhas]

# Libera o acesso de qualquer origem (útil para um dashboard front-end).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
def raiz():
    """Redireciona a página inicial para a documentação automática."""
    return RedirectResponse(url="/docs")


@app.get("/asteroides")
def listar_asteroides():
    """READ: lista todos os asteroides já coletados (ordenados por risco)."""
    return _para_json(banco.selecionar_asteroides())


@app.get("/asteroides/{nivel}")
def listar_por_nivel(nivel: str):
    """READ filtrado: ex. /asteroides/CRITICO ou /asteroides/ALTO."""
    return _para_json(banco.selecionar_por_nivel(nivel.upper()))


@app.post("/executar")
def executar_robo(dias: int = 1):
    """Dispara o robô RPA manualmente pela API e devolve o resumo."""
    return executar_monitoramento(dias=dias)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
