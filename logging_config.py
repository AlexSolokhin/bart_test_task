dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': '%(levelname)s | %(name)s | %(asctime)s | %(message)s'
        }
    },
    'handlers': {
        'time_rotating_bot_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'base',
            'filename': 'bot_logs.log',
            'when': 'h',
            'interval': 24,
            'backupCount': 7,
        },
        'time_rotating_parser_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'base',
            'filename': 'parser_logs.log',
            'when': 'h',
            'interval': 24,
            'backupCount': 7,
        }
    },
    'loggers': {
        'bot_logger': {
            'level': 'INFO',
            'handlers': ['time_rotating_bot_handler'],
        },
        'parser_logger': {
            'level': 'ERROR',
            'handlers': ['time_rotating_parser_handler']
        },
    }
}
