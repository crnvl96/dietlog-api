from fastapi import FastAPI

from .api.endpoints.diet import diet_router

app = FastAPI()
app.include_router(diet_router)
