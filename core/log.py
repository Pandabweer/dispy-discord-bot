import logging
import coloredlogs

log_level = logging.DEBUG

# Log format
log_format = '%(asctime)s [%(levelname)s] - [%(filename)s > %(funcName)s() > %(lineno)s]: %(message)s'
log_date_format = '%m/%d/%Y|%I:%M:%S %p'

# Info color/format logger
fieldstyle = {
    'asctime': {'color': 'green'},
    'levelname': {
        'bold': True,
        'color': 'black'
    },
    'filename': {'color': 'cyan'},
    'funcName': {'color': 'blue'}
}

# Message color/format logger
levelstyles = {
    'critical': {
        'bold': True,
        'color': 'red'
    },
    'debug': {'color': 'green'},
    'error': {'color': 'red'},
    'info': {'color': 'magenta'},
    'warning': {'color': 'yellow'}
}

# Creating logger
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# File handler
file = logging.FileHandler("bot.log")
fileformat = logging.Formatter(log_format, datefmt=log_date_format)
file.setLevel(log_level)
file.setFormatter(fileformat)

# Adding handlers to logger
logger.addHandler(file)

coloredlogs.install(
    level=log_level,
    logger=logger,
    fmt=log_format,
    datefmt=log_date_format,
    field_styles=fieldstyle,
    level_styles=levelstyles
)

# Some demo codes
# logger.debug("debug")
# logger.info("info")
# logger.warning("warn")
# logger.critical("critical")
# logging.exception(raise ValueError)
# logger.error("error")
