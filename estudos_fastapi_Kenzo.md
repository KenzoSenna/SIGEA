## Estudando sintaxe e lógica de response/request

```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "sucesso": False,
            "mensagem": exc.detail,
            "rota": str(request.url)
        }
    )

@app.get("/teste")
def teste():
    raise HTTPException(status_code=400, detail="Erro de teste")
```

Usar o *HTTPException* para erros genéricos e de pouca customização,

Usar o *JSONResponse* para customizar.

``` python 
from fastapi.responses import JSONResponse

@app.get("/custom-json")
def custom_json():
    return JSONResponse(
        status_code=400,
        content={
            "sucesso": False,
            "mensagem": "Erro personalizado",
            "codigo": 123
        }
    )

```

