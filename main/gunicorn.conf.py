import os

# Gunicorn configuration for FastAPI
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
workers = int(os.environ.get('WEB_CONCURRENCY', '1'))
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# Additional configuration for proper ASGI support
worker_connections = 1000
max_requests = 0  # Disable max requests to avoid restarts