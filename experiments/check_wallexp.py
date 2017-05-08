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
VR_WALL_VISIBLE = True
VR_WALL_X_OFFSET = .0

window = utils.setup_window(screen=SCREEN, fullscreen=FULLSCREEN)
cube_fbo = utils.setup_cube_fbo()

motive = NatClient(read_rate=2000)
scene, arena, arena_rb = utils.load_projected_scene(arena_file=ARENA_FILENAME, projector_file=PROJECTOR_FILENAME, motive_client=motive)
arena.texture = cube_fbo.texture


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
vr_arena.parent = arena
vr_arena.uniforms['flat_shading'] = False
vr_arena.texture = rc.Texture.from_image('./assets/uvgrid.png')
vr_meshes.append(vr_arena)

vr_scene = rc.Scene(meshes=vr_meshes, bgColor=(1., 1., 1.))
vr_scene.light.position.xyz = scene.light.position.xyz
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


pyglet.clock.schedule(utils.update, arena, cube_camera, motive)

pyglet.app.run()