from fastapi import FastAPI
from app.api.slack import router as slack_router

app = FastAPI(
    title="Slack Data Bot",
    version="1.0.0"
)

app.include_router(slack_router, prefix="/slack")

@app.get("/")
async def main():
    return "APP RUNNING"

@app.get("/health")
@app.head("/health") 
async def health():
    return {"status": "ok"}

