from fastapi import FastAPI
import uvicorn

from routes.routes import router
from config.settings import get_settings
from starlette.middleware.cors import CORSMiddleware


settings = get_settings()
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router,
    prefix=settings.API_PREFIX,
)

if __name__ == '__main__':
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG,
    )

