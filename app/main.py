from fastapi import FastAPI
import uvicorn

from routes.routes import router
from config.settings import get_settings


settings = get_settings()
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
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

