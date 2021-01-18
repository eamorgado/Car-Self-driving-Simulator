import carla
import pygame
from pygame.locals import KMOD_CTRL
from pygame.locals import KMOD_SHIFT
from pygame.locals import K_0
from pygame.locals import K_9
from pygame.locals import K_BACKQUOTE
from pygame.locals import K_BACKSPACE
from pygame.locals import K_COMMA
from pygame.locals import K_DOWN
from pygame.locals import K_ESCAPE
from pygame.locals import K_F1
from pygame.locals import K_LEFT
from pygame.locals import K_PERIOD
from pygame.locals import K_RIGHT
from pygame.locals import K_SLASH
from pygame.locals import K_SPACE
from pygame.locals import K_TAB
from pygame.locals import K_UP
from pygame.locals import K_a
from pygame.locals import K_c
from pygame.locals import K_d
from pygame.locals import K_h
from pygame.locals import K_m
from pygame.locals import K_p
from pygame.locals import K_q
from pygame.locals import K_r
from pygame.locals import K_s
from pygame.locals import K_w
from pygame.locals import K_l
from pygame.locals import K_MINUS
from pygame.locals import K_EQUALS
from pygame.locals import K_PLUS

import statistics
from server import core


import numpy as np


class KeyboardControl(object):
    def __init__(self, world, start_in_autopilot):
        self._autopilot_enabled = start_in_autopilot
        if isinstance(world.player, carla.Vehicle):
            self._control = carla.VehicleControl()
            world.player.set_autopilot(self._autopilot_enabled)
        elif isinstance(world.player, carla.Walker):
            self._control = carla.WalkerControl()
            self._autopilot_enabled = False
            self._rotation = world.player.get_transform().rotation
        else:
            raise NotImplementedError("Actor type not supported")
        self._steer_cache = 0.0
        world.hud.notification("Press 'H' or '?' for help.", seconds=4.0)

    def parse_events(self, client, world, clock):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYUP:
                if self._is_quit_shortcut(event.key):
                    return True
                elif event.key == K_BACKSPACE:
                    world.restart()
                elif event.key == K_F1:
                    world.hud.toggle_info()
                elif event.key == K_h or (event.key == K_SLASH and pygame.key.get_mods() & KMOD_SHIFT):
                    world.hud.help.toggle()
                elif event.key == K_TAB:
                    world.camera_manager.toggle_camera()
                elif event.key == K_c and pygame.key.get_mods() & KMOD_SHIFT:
                    world.next_weather(reverse=True)
                elif event.key == K_c:
                    world.next_weather()
                elif event.key == K_BACKQUOTE:
                    world.camera_manager.next_sensor()
                elif event.key > K_0 and event.key <= K_9:
                    world.camera_manager.set_sensor(event.key - 1 - K_0)
                elif event.key == K_r and not (pygame.key.get_mods() & KMOD_CTRL):
                    world.camera_manager.toggle_recording()
                elif event.key == K_r and (pygame.key.get_mods() & KMOD_CTRL):
                    if (world.recording_enabled):
                        client.stop_recorder()
                        world.recording_enabled = False
                        world.hud.notification("Recorder is OFF")
                    else:
                        client.start_recorder("manual_recording.rec")
                        world.recording_enabled = True
                        world.hud.notification("Recorder is ON")
                elif event.key == K_p and (pygame.key.get_mods() & KMOD_CTRL):
                    # stop recorder
                    client.stop_recorder()
                    world.recording_enabled = False
                    # work around to fix camera at start of replaying
                    currentIndex = world.camera_manager.index
                    world.destroy_sensors()
                    # disable autopilot
                    self._autopilot_enabled = False
                    world.player.set_autopilot(self._autopilot_enabled)
                    world.hud.notification("Replaying file 'manual_recording.rec'")
                    # replayer
                    client.replay_file("manual_recording.rec", world.recording_start, 0, 0)
                    world.camera_manager.set_sensor(currentIndex)
                elif event.key == K_MINUS and (pygame.key.get_mods() & KMOD_CTRL):
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        world.recording_start -= 10
                    else:
                        world.recording_start -= 1
                    world.hud.notification("Recording start time is %d" % (world.recording_start))
                elif event.key == K_EQUALS and (pygame.key.get_mods() & KMOD_CTRL):
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        world.recording_start += 10
                    else:
                        world.recording_start += 1
                    world.hud.notification("Recording start time is %d" % (world.recording_start))
                
                #Activate Lane Detection
                elif event.key == K_l and (pygame.key.get_mods() & KMOD_CTRL):
                    core.app['DETECTION_LANE'] = not core.app['DETECTION_LANE']
                    if not core.app['DETECTION_LANE']:
                        core.app['LANE_STEERING'] = False

                #Activate lane steering
                elif event.key == K_l:
                    if core.app['DETECTION_LANE']:
                        core.app['LANE_STEERING'] = not core.app['LANE_STEERING']
                        if not core.app['LANE_STEERING']:
                            core.app['LANE_STEERING_ANGLE'] = [0.0]
                        world.hud.notification(str('Lane Auto Steering Toggle' + str(core.app['LANE_STEERING'])))
                
                #Increase - decrease lane params:
                    """
                    elif event.key == K_PLUS:
                        if core.app['DETECTION_LANE']:
                            h = 'Lane Detection Config:\n1) Max Lane Steering Angles\n2)Max Lane growth\nq)Quit\n'
                            flag = True
                            while flag:
                                print(h)
                                v = str(input('Input: '))
                                if v == '1':
                                    flag_angles = True
                                    while flag_angles:
                                        h_angles = 'Max Lane Steering Angles: ' + str(core.app['MAX_LANE_STEERING_ANGLES']) + '\n+) Increase (+10)\n-) Decrease (-10)\nq) Back\n'
                                        print(h_angles)
                                        v_angles = str(input('Input: '))
                                        if v_angles == '+':
                                            core.app['MAX_LANE_STEERING_ANGLES'] += 10
                                        elif v_angles == '-':
                                            core.app['MAX_LANE_STEERING_ANGLES'] -= 10
                                        elif v_angles == 'q':
                                            flag_angles = False
                                elif v == '2':
                                    flag_angles = True
                                    while flag_angles:
                                        h_angles = 'Max Lane Growth:  ' + str(core.app['MAX_LANE_STEERING_ANGLE_GROWTH']) + '\n+) Increase (+10)\n-) Decrease (-10)\nq) Back\n'
                                        print(h_angles)
                                        v_angles = str(input('Input: '))
                                        if v_angles == '+':
                                            core.app['MAX_LANE_STEERING_ANGLE_GROWTH'] = min(1.0, (core.app['MAX_LANE_STEERING_ANGLE_GROWTH'] + 0.01))
                                            core.app['MAX_LANE_STEERING_ANGLE_GROWTH'] = abs(core.app['MAX_LANE_STEERING_ANGLE_GROWTH'])
                                        elif v_angles == '-':
                                            core.app['MAX_LANE_STEERING_ANGLE_GROWTH'] = max(0.0, (core.app['MAX_LANE_STEERING_ANGLE_GROWTH'] - 0.01))
                                            core.app['MAX_LANE_STEERING_ANGLE_GROWTH'] = abs(core.app['MAX_LANE_STEERING_ANGLE_GROWTH'])
                                        elif v_angles == 'q':
                                            flag_angles = False
                                elif v == 'q':
                                    flag = False
                    """

                #Activate Signal Detection
                elif event.key == K_s and (pygame.key.get_mods() & KMOD_CTRL):
                    core.app['DETECTION_SIGNAL'] = not core.app['DETECTION_SIGNAL']
                    if core.app['DETECTION_SIGNAL']:
                        from server.signal_detection.detection import init
                        init()
                    else:
                        core.app['SIGNAL_RCNN_MODEL'] = None
                        core.app['SIGNAL_RCNN_MAP'] = None

                if isinstance(self._control, carla.VehicleControl):
                    if event.key == K_q:
                        self._control.gear = 1 if self._control.reverse else -1
                    elif event.key == K_m:
                        self._control.manual_gear_shift = not self._control.manual_gear_shift
                        self._control.gear = world.player.get_control().gear
                        world.hud.notification('%s Transmission' %
                                               ('Manual' if self._control.manual_gear_shift else 'Automatic'))
                    elif self._control.manual_gear_shift and event.key == K_COMMA:
                        self._control.gear = max(-1, self._control.gear - 1)
                    elif self._control.manual_gear_shift and event.key == K_PERIOD:
                        self._control.gear = self._control.gear + 1
                    elif event.key == K_p and not (pygame.key.get_mods() & KMOD_CTRL):
                        self._autopilot_enabled = not self._autopilot_enabled
                        world.player.set_autopilot(self._autopilot_enabled)
                        world.hud.notification('Autopilot %s' % ('On' if self._autopilot_enabled else 'Off'))
        if not self._autopilot_enabled:
            if isinstance(self._control, carla.VehicleControl):
                self._parse_vehicle_keys(pygame.key.get_pressed(), clock.get_time())
                self._control.reverse = self._control.gear < 0
            elif isinstance(self._control, carla.WalkerControl):
                self._parse_walker_keys(pygame.key.get_pressed(), clock.get_time())
            world.player.apply_control(self._control)
    
    def _parse_vehicle_keys(self, keys, milliseconds):
        self._control.throttle = 1.0 if keys[K_UP] or keys[K_w] else 0.0
        steer_increment = 5e-4 * milliseconds
        if keys[K_LEFT] or keys[K_a]:
            self._steer_cache -= steer_increment
        elif keys[K_RIGHT] or keys[K_d]:
            self._steer_cache += steer_increment
        else:
            self._steer_cache = 0.0

        if core.app['LANE_STEERING']:
            angle = core.app['LANE_STEERING_ANGLE']
            #arr = np.array(core.app['LANE_STEERING_ANGLE'])
            #norm = np.linalg.norm(arr)
            #normal_array = arr/norm
            #angle = normal_array[-1]
            #new_angle = core.app['LANE_STEERING_ANGLE'][-1]
            #before = core.app['LANE_STEERING_ANGLE'][:-1]
            #angle = sum(before)/len(before)
            #angle = statistics.median(core.app['LANE_STEERING_ANGLE'])
            
            """if new_angle > (abs(angle) + core.app['MAX_LANE_STEERING_ANGLE_GROWTH']):
                new_angle = abs(angle) + core.app['MAX_LANE_STEERING_ANGLE_GROWTH']
                core.app['LANE_STEERING_ANGLE'][-1] = new_angle
                #angle = new_angle
                print('YES')
            elif new_angle < (abs(angle)*-1 - core.app['MAX_LANE_STEERING_ANGLE_GROWTH']):
                new_angle = abs(angle)*-1 - core.app['MAX_LANE_STEERING_ANGLE_GROWTH']
                core.app['LANE_STEERING_ANGLE'][-1] = new_angle
                #angle = new_angle
                print('YES')
            """
            #angle = sum(core.app['LANE_STEERING_ANGLE'])/len(core.app['LANE_STEERING_ANGLE'])
            #print(angle)
            #dev = statistics.stdev(core.app['LANE_STEERING_ANGLE'])
            #print('Size: ',len(core.app['LANE_STEERING_ANGLE']))
            #print('STDV: ',dev)
            #if len(core.app['LANE_STEERING_ANGLE']) > core.app['MAX_LANE_STEERING_ANGLES']:
            #    core.app['LANE_STEERING_ANGLE'] = [angle]
            self._steer_cache = angle

        self._steer_cache = min(0.5, max(-0.5, self._steer_cache))
        

        self._control.steer = round(self._steer_cache, 1)
        self._control.brake = 1.0 if keys[K_DOWN] or keys[K_s] else 0.0
        self._control.hand_brake = keys[K_SPACE]


    def _parse_walker_keys(self, keys, milliseconds):
        self._control.speed = 0.0
        if keys[K_DOWN] or keys[K_s]:
            self._control.speed = 0.0
        if keys[K_LEFT] or keys[K_a]:
            self._control.speed = .01
            self._rotation.yaw -= 0.08 * milliseconds
        if keys[K_RIGHT] or keys[K_d]:
            self._control.speed = .01
            self._rotation.yaw += 0.08 * milliseconds
        if keys[K_UP] or keys[K_w]:
            self._control.speed = 5.556 if pygame.key.get_mods() & KMOD_SHIFT else 2.778
        self._control.jump = keys[K_SPACE]
        self._rotation.yaw = round(self._rotation.yaw, 1)
        self._control.direction = self._rotation.get_forward_vector()

    @staticmethod
    def _is_quit_shortcut(key):
        return (key == K_ESCAPE) or (key == K_q and pygame.key.get_mods() & KMOD_CTRL)