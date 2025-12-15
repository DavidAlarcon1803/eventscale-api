from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from src.database import engine, Base
from src.routers import tickets, auth, events, admin, users
from src.docs_custom import custom_openapi, custom_css
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="EventScale API", 
    lifespan=lifespan,
    docs_url=None, 
    redoc_url=None
)

origins = [
    "http://localhost:5173",
    "https://portafolio-blond-five-68.vercel.app",
    "https://portafolio-blond-five-68.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    html = custom_openapi(app)
    return HTMLResponse(content=html.body.decode("utf-8").replace("</body>", f"{custom_css}</body>"))

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
app.include_router(events.router, prefix="/events", tags=["Events"]) 
app.include_router(admin.router, prefix="/admin", tags=["Admin Panel"])
app.include_router(users.router, prefix="/users", tags=["User Management (Admin Only)"])

@app.get("/")
def root():
    return {"message": "EventScale API is running 🚀"}
