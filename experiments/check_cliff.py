from __future__ import print_function

import pyglet
pyglet.options['debug_gl'] = False
pyglet.options['debug_gl_trace'] = False

import ratcave as rc
from natnetclient import NatClient
import utils

ARENA_FILENAME = './assets/arena3uv.obj'
CLIFF_FILENAME = './assets/viscliff3.obj'
PROJECTOR_FILENAME = './calibration/p2.pickle'
SCREEN = 1
FULLSCREEN = True
CLIFF_SIDE = 'R' # L or R


window = utils.setup_window(screen=SCREEN, fullscreen=FULLSCREEN)
cube_fbo = utils.setup_cube_fbo()

motive = NatClient(read_rate=2000)


scene, arena, arena_rb = utils.load_projected_scene(arena_file=ARENA_FILENAME,
                                                    projector_file=PROJECTOR_FILENAME,
                                                    motive_client=motive)
arena.texture = cube_fbo.texture

shader = rc.Shader.from_file(*rc.resources.genShader)

arena_name = 'virArena' if 'l' in CLIFF_SIDE.lower() else 'virArena2'
vr_arena = utils.get_virtual_arena_mesh(arena_file=CLIFF_FILENAME, arena_mesh=arena, objname=arena_name,
                                        texture_filename='./assets/uvgrid.png')

vr_scene = utils.load_virtual_scene(active_scene=scene)
vr_scene.meshes = vr_arena

@window.event
def on_draw():
    with shader:
        with cube_fbo as fbo:
            vr_scene.draw360_to_texture(fbo.texture)
        scene.draw()


pyglet.clock.schedule(utils.update, arena, vr_scene.camera, motive)
pyglet.app.run()