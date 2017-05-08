from __future__ import print_function
import pyglet
pyglet.options['debug_gl'] = False
pyglet.options['debug_gl_trace'] = False

import ratcave as rc
from natnetclient import NatClient
import random
import utils

ARENA_FILENAME = './assets/arena3uv.obj'
PROJECTOR_FILENAME = './calibration/p2.pickle'
SCREEN = 1
FULLSCREEN = True
VR_WALL_VISIBLE = True
VR_WALL_X_OFFSET = .0

window = utils.setup_window(screen=SCREEN, fullscreen=FULLSCREEN)
cube_fbo = utils.setup_cube_fbo()

motive = NatClient(read_rate=2000)

arena, arena_rb = utils.get_arena_with_rigidbody(arena_objfilename=ARENA_FILENAME, motive_client=motive, flat_shading=False)
arena.texture = cube_fbo.texture

beamer = rc.Camera.from_pickle(PROJECTOR_FILENAME)
beamer.projection.aspect = 1.7778
beamer.projection.fov_y = 41.5

scene = rc.Scene(meshes=[arena], camera=beamer, bgColor=(1., 0, 0))
scene.gl_states = scene.gl_states[:-1]
scene.light.position.xyz = beamer.position.xyz

shader = rc.Shader.from_file(*rc.resources.genShader)

fps_display = pyglet.window.FPSDisplay(window)


vr_meshes = []

if VR_WALL_VISIBLE:
    vr_wall = rc.WavefrontReader(rc.resources.obj_primitives).get_mesh('Plane')
    vr_wall.parent = arena
    vr_wall.scale.x = .5
    vr_wall.position.xyz = VR_WALL_X_OFFSET, 0, 0
    vr_wall.position.y += .35
    vr_wall.rotation.y = 98
    vr_wall.uniforms['diffuse'] = (1.,) * 3
    vr_wall.uniforms['specular'] = 0., 0., 0.
    vr_wall.texture = rc.Texture.from_image('./assets/uvgrid.png')
    vr_wall.uniforms['ambient'] = (1.,) * 3
    vr_meshes.append(vr_wall)


vr_arena = rc.WavefrontReader(ARENA_FILENAME).get_mesh('Arena')
vr_arena.uniforms['diffuse'] = 1., 1, 1
vr_arena.position.xyz = arena_rb.position
vr_arena.rotation.xyz = arena_rb.rotation
vr_arena.uniforms['flat_shading'] = False
vr_arena.texture = rc.Texture.from_image('./assets/uvgrid.png')
vr_meshes.append(vr_arena)

vr_scene = rc.Scene(meshes=vr_meshes, bgColor=(1., 1., 1.))
vr_scene.light.position.xyz = scene.light.position.xyz
# vr_scene.light.position.xyz = 0, 0, 0
vr_scene.gl_states = vr_scene.gl_states[:-1]
cube_camera = vr_scene.camera
cube_camera.projection.fov_y = 90
cube_camera.projection.aspect = 1.
cube_camera.projection.z_near = .004
cube_camera.projection.z_far = 1.5
rat_rb = motive.rigid_bodies['Rat']


@window.event
def on_draw():
    with shader:
        with cube_fbo as fbo:
            vr_scene.draw360_to_texture(fbo.texture)
        scene.draw()
    fps_display.draw()


def update(dt):
    arena.position.xyz = arena_rb.position
    arena.rotation.xyz = arena_rb.rotation
    vr_arena.position.xyz = arena_rb.position
    vr_arena.rotation.xyz = arena_rb.rotation
    cube_camera.position.xyz = rat_rb.position
    cube_camera.uniforms['playerPos'] = cube_camera.position.xyz
pyglet.clock.schedule(update)

pyglet.app.run()