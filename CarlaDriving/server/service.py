import carla
import pygame
import cv2 as cv
from server import core
from server.carla.world import World
from server.carla.hud_screen import HUD
from server.carla.keyboard_control import KeyboardControl

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
        def initPoints():
            p1_r = (0,0)
            p2_r = (0,0)
            p_avg_r = (0,0)
            count_pos_r = 0

            p1_l = (0,0)
            p2_l = (0,0)
            p_avg_l = (0,0)
            count_pos_l = 0

            return p1_r,p2_r,p_avg_r,count_pos_r,  p1_r,p2_r,p_avg_l,count_pos_r

        while True:
            self.clock.tick_busy_loop(60)
            if self.controller.parse_events(self.client, self.world, self.clock):
                self.stop()
                return
            
            self.world.tick(self.clock)
            self.world.render(self.display)
            pygame.display.flip()

            p1_r,p2_r,p_avg_r,count_pos_r,  p1_r,p2_r,p_avg_l,count_pos_r = initPoints()

            img = cv.cvtColor(core.app['CAMERA_IMAGE'],cv.COLOR_BGR2RGB)

            #Resize image to defined res
            img = cv.resize(img,(self.screen_width,self.screen_height))

            #ROI coordinates
            img = img[240:480, 108:532]
            img = cv.resize(img, (424,240))

            #Gaussian filter 5x5
            img = cv.bilateralFilter(img,d=-1,sigmaColor=5, sigmaSpace=5)

            #Canny edge detector with Sobel filter
            img = cv.Canny(img,50,100)
            cv.imshow('',img)


