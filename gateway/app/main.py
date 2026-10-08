import os
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8002")
ETL_SERVICE_URL = os.getenv("ETL_SERVICE_URL", "http://localhost:8003")

app = FastAPI(title="API Gateway", version="1.0.0")

@app.get("/health")
async def health():
    return {"service": "gateway", "status": "ok"}

async def proxy(request: Request, base_url: str, path: str):
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.request(
            request.method,
            f"{base_url}{path}",
            content=body,
            headers=headers,
            params=request.query_params,
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers={
            k: v for k, v in response.headers.items()
            if k.lower() not in {"content-length", "transfer-encoding", "connection"}
        },
        media_type=response.headers.get("content-type"),
    )

@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def auth_proxy(request: Request, path: str):
    return await proxy(request, AUTH_SERVICE_URL, f"/auth/{path}")

@app.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def user_proxy(request: Request, path: str):
    return await proxy(request, USER_SERVICE_URL, f"/users/{path}")

@app.api_route("/etl/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def etl_proxy(request: Request, path: str):
    return await proxy(request, ETL_SERVICE_URL, f"/etl/{path}")
