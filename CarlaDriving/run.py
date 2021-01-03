import os
import argparse
import sys
from flask import request
from server import create_app, init,loop,stop
from server.logging.log import show_traceback

if __name__ == '__main__':
    print('Run python run.py --help to get info about running config\n')
    try:

        helps = """
        """

        parser = argparse.ArgumentParser(description=''.join(helps))
        parser.add_argument('--serverport', dest='serverport', type=int,
                            default=2001, help='Port to run server')
        parser.add_argument('--carlaport', dest='carlaport', type=int,
                            default=2000, help='TCP Port to listen to')
        parser.add_argument('--servername', dest='servername', type=str,
                            help='IP of carla server', default="127.0.0.1", required=False)
        parser.add_argument('--debug', dest='debug', action='store_true')
        parser.add_argument('--autopilot', dest='autopilot', action='store_true')
        parser.add_argument('--resolution',dest='resolution',metavar='WxH', default='940x720',help='Window resolution')
        parser.add_argument('--car-type',dest='car_type',default='vehicle.tesla.model3',help='Actor vehicle type')
        parser.add_argument('--car-name',dest='car_name',default='hero')
        parser.add_argument('--world',dest='world',default='Town04',help='Carla world: Town04, Town06 highway, Town07 country')


        parser.set_defaults(debug=False,autopilot=False)

        args = parser.parse_args()
        serverport, debug = args.serverport, args.debug

        carlaport, servername = args.carlaport, args.servername

        autopilot = bool(args.autopilot)
        width,height = [int(x) for x in args.resolution.split('x')]
        car_type = args.car_type
        car_name = args.car_name
        world = args.world


        configs = {
            'SCREEN_WIDTH': width,
            'SCREEN_HEIGHT': height,
            'CARLA_HOST': servername,
            'CARLA_PORT': carlaport,
            'AUTO_PILOT': autopilot,
            'ROLENAME': car_name,
            'FILTER': car_type,
            'WORLD_NAME': world
        }

        
        create_app(width,height,debug)

        init(configs)
        loop()
        stop()

        print("Service started")
    except Exception as e:
        show_traceback(override=True)
        print("Service failed: " + str(e))
