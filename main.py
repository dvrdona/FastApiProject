from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api.user_api.user import user_router
from api.categories.categories import category_router
from api.product_api.product import product_router
from api.card_api.card import cart_router
from api.payment_api.payment import payment_router, order_router
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(docs_url="/docs")
app = FastAPI(docs_url="/")


templates = Jinja2Templates(directory="templates")

# Настройка CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение

app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(payment_router)

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(name="index.html", request=request)