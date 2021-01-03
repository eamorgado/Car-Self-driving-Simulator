"""Summary of module
This is the main module for carla connection
It will import the carla egg from the downloaded carla engine (PythonAPI/carla/dist), we will plage the egg withing the files 
"""

import os
import sys
import glob

from server.logging.log import log_info, log_error, show_traceback

def init():
    try:
        log_info('CARLA-INIT: Loading egg')

        sys.path.append(glob.glob('server/carla/carla_data/carla-*%d.%d-%s.egg' % (
            sys.version_info.major,
            sys.version_info.minor,
            'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])

        log_info('CARLA-INIT: Loaded egg')
    except IndexError as e:
        show_traceback()
        log_error('CARLA-INIT: Failed loading egg: ' + str(e))
        pass
