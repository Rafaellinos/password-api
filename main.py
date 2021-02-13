from fastapi import FastAPI

# app = FastAPI()

#
# @app.get("/")
# def root():
#     return {"message": "Hello World"}
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: str):
#     return {"item_id": item_id}
import uvicorn
from uvicorn.config import LOGGING_CONFIG
import configparser
import copy
config = configparser.ConfigParser(interpolation=None)

if __name__ == '__main__':
    new_config = copy.deepcopy(LOGGING_CONFIG)
    config.read(".config.init")
    new_config["formatters"]["access"]["fmt"] = config["logging_config"]["logging_format"]
    debug = config["server_config"].getboolean("debug")
    uvicorn.run(
        "sql_app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        debug=True,
        log_config=new_config,
    )
