import numpy as np
from server import core

def create_app(width,height,debug):
    # Get services
    from server.carla.carla import init as carla_init

    #Load carla module
    core.init()
    carla_init()
    core.app['CAMERA_IMAGE'] = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    core.app['DEBUG'] = debug

def init(configs):
    from server.service import Service

    core.app['SERVICE'] = Service(configs)

def loop():
    core.app['SERVICE'].loop()

def stop():
    if core.app['SERVICE'] is not None:
        core.app['SERVICE'].stop()
    core.app['SERVICE'] = None
