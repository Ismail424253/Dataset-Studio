"""
AI Prompt & Dataset Studio — FastAPI uygulama giris noktasi.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import prompts, tags

app = FastAPI(
    title="AI Prompt & Dataset Studio API",
    description="LLM fine-tuning icin prompt ve dataset yonetim araci.",
    version="0.1.0",
)

# ---------- CORS Ayarlari ----------
# Frontend dev sunucusunun (Vite, varsayilan port: 5173) backend'e erisimini saglar.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# ---------- Health Check ----------

@app.get(
    "/health",
    tags=["System"],
    summary="Sistem saglik kontrolu",
)
def health_check():
    """Sunucunun calistigini dogrular."""
    return {"status": "ok"}


# ---------- Router Kayitlari ----------

app.include_router(prompts.router)
app.include_router(tags.router)
