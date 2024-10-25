from fastapi import FastAPI
from routes.user import user 

app = FastAPI(
    title = "Documentación para fast-api",
    description= "Esta es la documentación para el crud básico utiliznado Fast-API con mysql",
    version="0.0.1",
    openapi_tags=[{
        "name": "users",
        "description": "Rutas para usuarios"
    }]
)

app.include_router(user)


