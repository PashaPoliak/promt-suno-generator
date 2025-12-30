#!/usr/bin/env python3
"""
Application startup script with environment handling
"""
import os
import sys
import argparse
import uvicorn
from config.settings import settings


def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(description='Suno Data Fetcher and API Server')
    parser.add_argument('--start-server', action='store_true', help='Start the API server after fetching data')
    parser.add_argument('--host', default='0.0.0.0', help='Host for the API server')
    parser.add_argument('--port', type=int, help='Port for the API server')
    
    args = parser.parse_args()
    
    # Use provided port or default to environment variable or 8000
    port = args.port or int(os.getenv('PORT', 8000))
    
    if args.start_server or os.getenv('START_SERVER', '').lower() == 'true':
        from main import create_app
        app = create_app()
        
        print(f"Starting server on {args.host}:{port}")
        print(f"Environment: {settings.environment}")
        print(f"Debug mode: {settings.debug}")
        
        uvicorn.run(
            app, 
            host=args.host, 
            port=port,
            reload=settings.debug,
            log_level=settings.log_level.lower()
        )
    else:
        print("Server not started. Use --start-server to start the server.")
        print(f"Environment: {settings.environment}")
        print(f"Database URL: {settings.database_url}")


if __name__ == "__main__":
    main()