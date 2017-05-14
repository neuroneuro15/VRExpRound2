#
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


def chain_events(events):
    events = list(events[::-1])
    for event in events:
        event.next()
    while True:
        dt = yield
        try:
            events[-1].send(dt)
        except StopIteration:
            events.pop()
        except IndexError:
            raise StopIteration


# def log_item(filename, )