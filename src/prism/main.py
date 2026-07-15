"""Prism Intelligence - FastAPI Application Entry Point."""

from fastapi import FastAPI


app = FastAPI(
    title="Prism Intelligence",
    version="1.0.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok", "service": "prism-intelligence"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)