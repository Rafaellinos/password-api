from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes.routes import router
from app.config.settings import get_settings


def get_application() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(
        router,
        prefix=settings.API_PREFIX,
    )
    return application


app = get_application()
