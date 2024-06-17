import time
from collections import defaultdict
from typing import Dict
import asyncio
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
import logging


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limit: float = 1.0):
        super().__init__(app)
        self.rate_limit_records: Dict[str, float] = defaultdict(float)
        self.rate_limit = rate_limit
        self.lock = asyncio.Lock()

    async def log_message(self, message: str):
        logging.info(message)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        client_ip_address = request.client.host
        current_time = time.time()

        async with self.lock:
            last_request_time = self.rate_limit_records[client_ip_address]

            # 1 request per second
            if current_time - last_request_time < self.rate_limit:
                return Response(content="Rate limit exceeded", status_code=429)

            self.rate_limit_records[client_ip_address] = current_time

        path = request.url.path
        await self.log_message(f"Request to {path}")

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        response.headers["X-Process-time"] = str(process_time)

        await self.log_message(f"Response for {path} took {process_time:.4f} seconds")

        return response
