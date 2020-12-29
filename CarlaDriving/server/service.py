import carla
import pygame
import cv2 as cv
from server import core
from server.carla.world import World
from server.carla.hud_screen import HUD
from server.carla.keyboard_control import KeyboardControl

from server.lane_detection.detection import detection as lane_detection

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
        self.client.set_timeout(2.0)

        self.display = pygame.display.set_mode(
            (self.screen_width,self.screen_height),
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )

        self.hud = HUD(self.screen_width,self.screen_height)

        self.world = World(self.client.load_world(world_name),self.hud,filter,rolename)

        self.controller = KeyboardControl(self.world,enable_autopilot)

        self.clock = pygame.time.Clock()

    def stop(self):
        if self.world and self.world.recording_enabled:
            self.client.stop_recorder()
        
        if self.world is not None:
            self.world.destroy()
        
        pygame.quit()

    
    def loop(self):
        while True:
            self.clock.tick_busy_loop(60)
            if self.controller.parse_events(self.client, self.world, self.clock):
                self.stop()
                return
            
            self.world.tick(self.clock)
            self.world.render(self.display)
            pygame.display.flip()

            lane_detection(core.app['CAMERA_IMAGE'],self,show_canny=True,show_hough=True)

            


