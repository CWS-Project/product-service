from fastapi import FastAPI, Response
from dtypes import make_response
from controllers import product_router

app = FastAPI()
app.include_router(product_router)

@app.get("/healthz")
def health_check(response: Response):
    return make_response(response, 200, "OK")

@app.get("/")
def health_check(response: Response):
    return make_response(response, 200, "OK")