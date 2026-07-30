"""
AI Prompt & Dataset Studio — FastAPI uygulama giris noktasi.
"""

from fastapi import FastAPI
from app.routes import prompts

app = FastAPI(
    title="AI Prompt & Dataset Studio API",
    description="LLM fine-tuning icin prompt ve dataset yonetim araci.",
    version="0.1.0",
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
