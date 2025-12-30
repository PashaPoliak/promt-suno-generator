import sys
import os
import argparse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from routes.v1 import router as api_router
from routes.v2 import router as api_v2_router
from routes.v3 import clips_router as v3_clips_router, playlists_router as v3_playlists_router, profiles_router as v3_profiles_router
from database.mongo_connection import mongodb


def create_app():
    app = FastAPI(title="Suno Prompt Generator API", version="1.0.0")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(api_router, prefix="/api/v1")
    app.include_router(api_v2_router, prefix="/api/v2")
    app.include_router(v3_clips_router, prefix="/api/v3/clips")
    app.include_router(v3_playlists_router, prefix="/api/v3/playlists")
    app.include_router(v3_profiles_router, prefix="/api/v3/profiles")

    return app

app = create_app()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Suno Data Fetcher and API Server')
    parser.add_argument('--start-server', action='store_true', help='Start the API server after fetching data')
    parser.add_argument('--host', default='127.0.0.1', help='Host for the API server')
    parser.add_argument('--port', default=8000, type=int, help='Port for the API server')
    
    args = parser.parse_args()
    
    if args.start_server:
        import uvicorn
        app = create_app()
        uvicorn.run(app, host=args.host, port=args.port)
