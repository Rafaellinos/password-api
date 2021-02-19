import uvicorn
from app.main import app
from app.config.settings import get_settings

settings = get_settings()

uvicorn.run(
    app,
    host=settings.HOST,
    port=settings.PORT,
)
