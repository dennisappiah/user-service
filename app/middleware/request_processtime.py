from datetime import datetime

from starlette.middleware.base import BaseHTTPMiddleware
import logging


class AccessMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        start_time = datetime.now()
        response = await call_next(request)
        process_time = datetime.now() - start_time
        logging.info(
            f"{response.status_code} {request.client.host} {request.method} {request.url} {process_time}"
        )
        return response
