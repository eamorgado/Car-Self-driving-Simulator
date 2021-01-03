"""Summary of module
Logging module, generates log file for app
"""
import traceback
import logging
from server import core

logging.basicConfig(filename='./service.log',
                     filemode='a',
                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                     datefmt='%H:%M:%S',
                     level=logging.INFO)

def log_error(str):
    logging.error(str)
    pass

def log_info(str):
    logging.info(str)
    pass

def show_traceback(override=False):
    if override:
        print(traceback.print_exc())
        return

    if bool(core.app['DEBUG']):
        print(traceback.print_exc())
