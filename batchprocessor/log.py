import logging

from .config import Config

logging.basicConfig (
    format="%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %z",
    )

def getLogger(appName):
    logger = logging.getLogger(appName)
    logger.setLevel(Config.LOG_LEVEL)
    return logger