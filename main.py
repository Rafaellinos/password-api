import uvicorn
from uvicorn.config import LOGGING_CONFIG
import configparser
import copy


config = configparser.ConfigParser(interpolation=None)
config.read(".config")

DEBUG = config["server_config"].getboolean("debug")


if __name__ == '__main__':
    new_config = copy.deepcopy(LOGGING_CONFIG)
    new_config["formatters"]["access"]["fmt"] = config["logging_config"]["logging_format"]
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        debug=DEBUG,
        log_config=new_config,
    )
