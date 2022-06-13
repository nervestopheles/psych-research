import uvicorn
from fastapi import FastAPI

from routers import user

app = FastAPI(
    title="Psych. testing API",
    version="v0.1.0",
    description="...",
    docs_url="/docs",
    redoc_url=None
)

app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
