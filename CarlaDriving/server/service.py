import math
import carla
import pygame
import cv2 as cv
from server import core
from server.carla.world import World
from server.carla.hud_screen import HUD
from server.carla.keyboard_control import KeyboardControl

from server.lane_detection.detection import detection as lane_detection
from server.signal_detection.detection import detection as signal_detection

class Service():
    def __init__(self,configs):
        pygame.init()
        pygame.font.init()

        self.screen_width = configs['SCREEN_WIDTH']
        self.screen_height = configs['SCREEN_HEIGHT']

        carla_host = configs['CARLA_HOST']
        carla_port = configs['CARLA_PORT']

        enable_autopilot = configs['AUTO_PILOT']
        rolename = configs['ROLENAME']
        filter = configs['FILTER']
        world_name = configs['WORLD_NAME']

        self.client = carla.Client(carla_host,carla_port)
        self.client.set_timeout(5.0)

        self.display = pygame.display.set_mode(
            (self.screen_width,self.screen_height),
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )

        self.hud = HUD(self.screen_width,self.screen_height)

        self.world = World(self.client.load_world(world_name),self.hud,filter,rolename)

        self.controller = KeyboardControl(self.world,enable_autopilot)

        self.clock = pygame.time.Clock()

        self.setParams(configs)

    def setParams(self,configs):
        #Set RCNN model paths
        keys = [
            'RCNN_MODEL_PATH','RCNN_MAP_PATH',
            'RCNN_NET_DIM','RCNN_MAX_PROPOSALS',
            'RCNN_POSITIVE_CLASS','RCNN_THRESHOLD',
        ]
        for k in keys:
            core.app[k] = configs[k]

        core.app['DETECTION_SIGNAL'] = False
        core.app['SIGNAL_RCNN_MODEL'] = None
        core.app['SIGNAL_RCNN_MAP'] = None


        #Set Lane Params
        core.app['DETECTION_LANE'] = False
        core.app['LANE_STEERING'] = False
        core.app['LANE_STEERING_ANGLE'] = 0.0

    def stop(self):
        if self.world and self.world.recording_enabled:
            self.client.stop_recorder()
        
        if self.world is not None:
            self.world.destroy()
        
        pygame.quit()

    
    def loop(self):
        #Lane params
        #Memory of controller
        core.app['MAX_LANE_STEERING_ANGLES'] = 100
        core.app['MAX_LANE_STEERING_ANGLE_GROWTH'] = 0.3
        lane_steering_angle = 90
        #-----------------
        while True:
            self.clock.tick_busy_loop(60)
            if self.controller.parse_events(self.client, self.world, self.clock):
                self.stop()
                return
            
            self.world.tick(self.clock)
            self.world.render(self.display)
            pygame.display.flip()

            camera_image = core.app['CAMERA_IMAGE']
            lane_image = None
            if core.app['DETECTION_LANE']:
                new_steering_angle,lane_image = lane_detection(camera_image,self,lane_steering_angle,show_canny=True,show_hough=True)

                if new_steering_angle is not None and new_steering_angle >= 0:
                    lane_steering_angle = new_steering_angle
                    if lane_steering_angle > 0 and lane_steering_angle < 89:
                        t = "Turn Left"
                    elif lane_steering_angle >= 89 and lane_steering_angle <= 91:
                        t = "Straight forward"
                    else:
                        t = "Turn right"
                    
                    #Steering Angle [-1.0,...,0.0,...,1.0]
                    #Degrees:       [0º,...,90º,...,180º]
                    #Function: -cos(x)
                    converted_angle = math.radians(lane_steering_angle)
                    converted_angle = math.cos(converted_angle) * -1
                    
                    #print(t + '\t' + str(converted_angle))
                    core.app['LANE_STEERING_ANGLE'].append(converted_angle)

                    self.hud.notification(t)


            if core.app['DETECTION_SIGNAL']:
                rcnn_image = signal_detection(camera_image,self)


            


