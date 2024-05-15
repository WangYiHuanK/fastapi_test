import time
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request


def middleware_init(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
        allow_headers=['*']
    )

    @app.middleware('http')
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        time.sleep(1)
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['process_time'] = str(process_time)
        return response
