"""Custom logger configuration."""
from sys import stdout

from loguru import logger as custom_logger


def formatter(log):
    """Format log colors based on level."""
    if log["level"].name == "SUCCESS":
        return (
            "<fg #aad1f7>{time:MM-DD-YYYY HH:mm:ss}</fg #aad1f7> | "
            "<light-green>{level}</light-green>: "
            "<light-white>{message}</light-white> \n"
        )
    if log["level"].name == "WARNING":
        return (
            "<fg #aad1f7>{time:MM-DD-YYYY HH:mm:ss}</fg #aad1f7> | "
            "<light-yellow>{level}</light-yellow>: "
            "<light-white>{message}</light-white> \n"
        )
    elif log["level"].name == "ERROR":
        return (
            "<fg #aad1f7>{time:MM-DD-YYYY HH:mm:ss}</fg #aad1f7> | "
            "<light-red>{level}</light-red>: "
            "<light-white>{message}</light-white> \n"
        )
    else:
        return (
            "<fg #aad1f7>{time:MM-DD-YYYY HH:mm:ss}</fg #aad1f7> | "
            "<fg #67c9c4>{level}</fg #67c9c4>: "
            "<light-white>{message}</light-white> \n"
        )


def create_logger():
    """Create custom logger."""
    custom_logger.remove()
    custom_logger.add(stdout, colorize=True, format=formatter)
    return custom_logger


LOGGER = create_logger()
