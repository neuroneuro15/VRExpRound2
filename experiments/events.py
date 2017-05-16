from __future__ import print_function

import logging
from collections import deque

def fade_to_black(mesh, speed=1.):
    vel = -speed
    while mesh.uniforms['diffuse'][0] > 0.:
        dt = yield
        mesh.uniforms['diffuse'] = [dif + (vel  * dt) for dif in mesh.uniforms['diffuse']]

def fade_to_white(mesh, speed=1.):
    vel = speed
    while mesh.uniforms['diffuse'][0] <= 1.:
        dt = yield
        mesh.uniforms['diffuse'] = [dif + (vel  * dt) for dif in mesh.uniforms['diffuse']]

def wait_duration(duration):
    total_time = duration
    curr_time = 0.
    while curr_time < total_time:
        dt = yield
        curr_time += dt

def set_scene_to(app, new_scene):
    dt = yield
    app.current_vr_scene = new_scene


def send_robo_command(device, msg):
    dt = yield
    device.write(msg)


def chain_events(events, log=True, motive_client=None):
    def init_next_event():
        event = events.popleft()
        event.next()
        if log and motive_client:
            event_data = event.gi_frame.f_locals
            args = {var: event.gi_frame.f_locals[var]  for var in event.gi_code.co_varnames[:event.gi_code.co_argcount]}
            print(event_data, args)

            logging.warn('{mot_time}, {fun_name}, {args}'.format(mot_time=motive_client.timestamp_recording, fun_name=event.__name__,
                                                                   args=args))
        return event

    events = deque(events)
    event = init_next_event()
    while True:
        dt = yield
        try:
            event.send(dt)
        except StopIteration:
            event = init_next_event()
        except IndexError:
            raise StopIteration



