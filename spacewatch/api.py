"""
Camada CONTROLLER do MVC, usando FastAPI (slide "Restful APIs").

Depois que o robô coletou e salvou os dados no SQLite, esta API REST
deixa qualquer pessoa (ou um dashboard) consultar os asteroides pelo
navegador. É o mesmo padrão de Controllers que o professor mostrou:
o FastAPI conversa com o Repository (Model) e devolve JSON.

Como rodar:
    poetry run uvicorn spacewatch.api:app --reload
Depois abra:  http://127.0.0.1:8000/docs
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from .repository import Repository
from .rpa_bot import executar_monitoramento

app = FastAPI(title="SpaceWatch RPA", version="0.1.0")
banco = Repository()

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
    return banco.selecionar_asteroides()


@app.get("/asteroides/{nivel}")
def listar_por_nivel(nivel: str):
    """READ filtrado: ex. /asteroides/CRITICO ou /asteroides/ALTO."""
    return banco.selecionar_por_nivel(nivel.upper())


@app.post("/executar")
def executar_robo(dias: int = 1):
    """Dispara o robô RPA manualmente pela API e devolve o resumo."""
    return executar_monitoramento(dias=dias)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
