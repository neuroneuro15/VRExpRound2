from __future__ import print_function
import pyglet
pyglet.options['debug_gl'] = False
pyglet.options['debug_gl_trace'] = False

import ratcave as rc
from natnetclient import NatClient
import utils

ARENA_FILENAME = './assets/arena3uv.obj'
PROJECTOR_FILENAME = './calibration/p2.pickle'
SCREEN = 1
FULLSCREEN = True


window = utils.setup_window(screen=SCREEN, fullscreen=FULLSCREEN)

motive = NatClient(read_rate=2000)


scene, arena, arena_rb = utils.load_projected_scene(arena_file=ARENA_FILENAME,
                                                    projector_file=PROJECTOR_FILENAME,
                                                    motive_client=motive)
beamer = scene.camera

shader = rc.Shader.from_file(*rc.resources.genShader)

fps_display = pyglet.window.FPSDisplay(window)

@window.event
def on_draw():
    with shader:
        scene.draw()
    fps_display.draw()


def update(dt):
    arena.position.xyz = arena_rb.position
    arena.rotation.xyzw = arena_rb.quaternion
pyglet.clock.schedule(update)

print('Projector: ', beamer.position, beamer.orientation)
print('Fov_y: ', beamer.projection.fov_y)
print('Aspect: ', beamer.projection.aspect)
print('Arena: ', arena.position, arena.rotation)

pyglet.app.run()