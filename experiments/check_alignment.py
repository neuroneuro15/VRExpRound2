from __future__ import print_function
import pyglet
pyglet.options['debug_gl'] = False
pyglet.options['debug_gl_trace'] = False

import ratcave as rc
from natnetclient import NatClient
import utils
import cfg

window = utils.setup_window(screen=cfg.SCREEN, fullscreen=cfg.FULLSCREEN)

motive = NatClient(read_rate=2000)


scene, arena, arena_rb = utils.load_projected_scene(arena_file=cfg.ARENA_FILENAME,
                                                    projector_file=cfg.PROJECTOR_FILENAME,
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