import os

DEBUG = False

current_dir = os.path.dirname(os.path.realpath(__file__))
LOG_DIR = current_dir + '/../../data/logs/'

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
        'precise': {
            'format': '%(asctime)s %(name)-15s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'precise',
            'filename': LOG_DIR + 'app.log',
            'maxBytes': 1024,
            'backupCount': 3,
            'mode': 'w'
        }
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    }
}