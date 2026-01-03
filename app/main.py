import sys
import os
import uvicorn
import argparse
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from v1 import router as api_router
from v2 import router as api_v2_router
from v3 import router as api_v3_router
from config.init_db import init_db
from config.session import engine_embed, engine_postgres


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db(engine_embed)
    init_db(engine_postgres)
    yield

def create_app():
    app = FastAPI(title="Suno Prompt Generator API", version="1.0", lifespan=lifespan)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(api_router, prefix="/api/v1")
    app.include_router(api_v2_router, prefix="/api/v2")
    app.include_router(api_v3_router, prefix="/api/v3")

    return app

app = create_app()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Suno Data Fetcher and API Server')
    parser.add_argument('--start-server', action='store_true', help='Start the API server after fetching data')
    parser.add_argument('--host', default='127.0.0.1', help='Host for the API server')
    parser.add_argument('--port', default=8000, type=int, help='Port for the API server')
    
    args = parser.parse_args()
    
    if args.start_server:
        uvicorn.run(app, host=args.host, port=args.port)
