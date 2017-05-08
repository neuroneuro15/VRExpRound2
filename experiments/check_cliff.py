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
CLIFF_SIDE = 'L' # L or R


window = utils.setup_window(screen=SCREEN, fullscreen=FULLSCREEN)
cube_fbo = utils.setup_cube_fbo()

motive = NatClient(read_rate=2000)

arena, arena_rb = utils.get_arena_with_rigidbody(arena_objfilename=ARENA_FILENAME, motive_client=motive, flat_shading=False)
arena.texture = cube_fbo.texture

beamer = utils.get_beamer_camera(PROJECTOR_FILENAME)

scene = rc.Scene(meshes=[arena], camera=beamer, bgColor=(1., 0, 0))
scene.gl_states = scene.gl_states[:-1]
scene.light.position.xyz = beamer.position.xyz

shader = rc.Shader.from_file(*rc.resources.genShader)

fps_display = pyglet.window.FPSDisplay(window)


vr_meshes = []

arena_name = 'virArena' if 'l' in CLIFF_SIDE.lower() else 'virArena2'
vr_arena = rc.WavefrontReader(CLIFF_FILENAME).get_mesh(arena_name)
vr_arena.uniforms['diffuse'] = 1., 1, 1
vr_arena.parent = arena
vr_arena.position.y -= 0
# vr_arena.rotation.y = 180 if 'r' in CLIFF_SIDE.lower() else 0
vr_arena.uniforms['flat_shading'] = False
vr_arena.texture = rc.Texture.from_image('./assets/uvgrid.png')
vr_meshes.append(vr_arena)

vr_scene = rc.Scene(meshes=vr_meshes, bgColor=(1., 1., 1.))
vr_scene.light.position.xyz = scene.light.position.xyz
# vr_scene.light.position.xyz = 0, 0, 0

vr_scene.gl_states = vr_scene.gl_states[:-1]
cube_camera = utils.get_cubecamera()
vr_scene.camera = cube_camera
rat_rb = motive.rigid_bodies['Rat']


@window.event
def on_draw():
    with shader:
        with cube_fbo as fbo:
            vr_scene.draw360_to_texture(fbo.texture)
        scene.draw()
    fps_display.draw()


pyglet.clock.schedule(utils.update, [arena], cube_camera, motive)
pyglet.app.run()