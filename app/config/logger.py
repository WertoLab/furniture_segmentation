import logging.config
from app.config.config import config


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/healthz") == -1


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': config.logger.CONSOLE_LOG_LEVEL,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': config.logger.FILE_LOG_LEVEL,
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'myapp.log',
            'mode': 'w',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'cmdstanpy': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False
        },
        'prophet': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False
        },
        'sqlalchemy.engine.Engine': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False
        },
        'uvicorn': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        }
    }
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
    logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
