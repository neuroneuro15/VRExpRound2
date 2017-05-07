from __future__ import print_function
import pyglet
pyglet.options['debug_gl'] = False
pyglet.options['debug_gl_trace'] = False

import ratcave as rc
from natnetclient import NatClient
import random

ARENA_FILENAME = 'arena3uv.obj'
PROJECTOR_FILENAME = 'p2.pickle'
SCREEN = 1
FULLSCREEN = True
CIRCLE_SCALE = .07
POSITION_L = .225, -0.243, -.05
POSITION_R = -.205, -.24, .015
VR_OBJECTS_FILENAME = '../assets/Eng_AllObjs1.obj'  #rc.resources.obj_primitives
VR_OBJECT_VISIBLE = True
VR_OBJECT_NAMES = ['Monkey']
VR_OBJECT_SCALE = .01
VR_OBJECT_SIDE = 'R'
VR_OBJECT_HEIGHT_OFFSET = .1

display = pyglet.window.get_platform().get_default_display()
screen = display.get_screens()[SCREEN]
window = pyglet.window.Window(fullscreen=FULLSCREEN, screen=screen, vsync=False)
cube_fbo = rc.FBO(texture=rc.TextureCube(width=2048, height=2048))

motive = NatClient(read_rate=2000)

arena = rc.WavefrontReader(ARENA_FILENAME).get_mesh('Arena')
arena.uniforms['diffuse'] = 1., 1, 1
arena.rotation = arena.rotation.to_quaternion()
arena_rb = motive.rigid_bodies['Arena']

print('Original Arena Position: ', arena.position)
arena.position.xyz = arena_rb.position
arena.rotation.xyz = arena_rb.rotation
arena.uniforms['flat_shading'] = False
# arena.texture = cube_fbo.texture

def get_sphere(position, scale=.05):
    primitive_reader = rc.WavefrontReader(rc.resources.obj_primitives)
    vr_mesh = primitive_reader.get_mesh('Sphere', scale=scale)
    vr_mesh.parent = arena
    vr_mesh.position.xyz = position
    vr_mesh.uniforms['diffuse'] = 0., 0., 0
    vr_mesh.uniforms['specular'] = 0., 0., 0.
    vr_mesh.uniforms['flat_shading'] = True
    return vr_mesh


circle1 = get_sphere(POSITION_L, scale=CIRCLE_SCALE)
circle2 = get_sphere(POSITION_R, scale=CIRCLE_SCALE + .0015)

circle1.parent = arena
circle2.parent = arena


beamer = rc.Camera.from_pickle(PROJECTOR_FILENAME)
beamer.projection.aspect = 1.7778
beamer.projection.fov_y = 41.5

scene = rc.Scene(meshes=[arena, circle1, circle2], camera=beamer, bgColor=(1., 0, 0))
scene.gl_states = scene.gl_states[:-1]
scene.light.position.xyz = beamer.position.xyz

shader = rc.Shader.from_file(*rc.resources.genShader)

fps_display = pyglet.window.FPSDisplay(window)


vr_meshes = []

if VR_OBJECT_VISIBLE:
    vr_obj_reader = rc.WavefrontReader(VR_OBJECTS_FILENAME)
    vr_obj_mesh = vr_obj_reader.get_mesh(random.choice(VR_OBJECT_NAMES))
    vr_obj_mesh.scale.x = VR_OBJECT_SCALE
    vr_obj_mesh.parent = arena
    vr_obj_mesh.position.xyz = POSITION_L if 'l' in VR_OBJECT_SIDE.lower() else POSITION_R
    vr_obj_mesh.position.y += VR_OBJECT_HEIGHT_OFFSET
    vr_obj_mesh.uniforms['diffuse'] = (.5,) * 3
    vr_obj_mesh.uniforms['specular'] = 0., 0., 0.
    vr_obj_mesh.uniforms['flat_shading'] = False
    vr_obj_mesh.uniforms['ambient'] = (1.,) * 3
    vr_meshes.append(vr_obj_mesh)


vr_arena = rc.WavefrontReader(ARENA_FILENAME).get_mesh('Arena')
vr_arena.rotation = vr_arena.rotation.to_quaternion()
vr_arena.uniforms['diffuse'] = 1., 1, 1
vr_arena.position.xyz = arena_rb.position
vr_arena.rotation.xyz = arena_rb.rotation
vr_arena.uniforms['flat_shading'] = False
vr_arena.texture = rc.Texture.from_image('uvgrid.png')
vr_meshes.append(vr_arena)

vr_scene = rc.Scene(meshes=vr_meshes, bgColor=(1., 1., 1.))
vr_scene.light.position.xyz = scene.light.position.xyz
# vr_scene.light.position.xyz = 0, 0, 0
vr_scene.gl_states = vr_scene.gl_states[:-1]
cube_camera = vr_scene.camera
cube_camera.rotation = cube_camera.rotation.to_quaternion()
cube_camera.projection.fov_y = 90
cube_camera.projection.aspect = 1.
cube_camera.projection.z_near = .004
cube_camera.projection.z_far = 1.5
rat_rb = motive.rigid_bodies['Rat']


@window.event
def on_draw():
    with shader:
        # with cube_fbo as fbo:
        #     vr_scene.draw360_to_texture(fbo.texture)
        scene.draw()
        # vr_scene.draw()
    fps_display.draw()


def update(dt):
    arena.position.xyz = arena_rb.position
    arena.rotation.xyzw = arena_rb.quaternion
    vr_arena.position.xyz = arena_rb.position
    vr_arena.rotation.xyzw = arena_rb.quaternion
    cube_camera.position.xyz = rat_rb.position
    cube_camera.rotation.xyzw = rat_rb.quaternion
    cube_camera.uniforms['playerPos'] = cube_camera.position.xyz
pyglet.clock.schedule(update)

pyglet.app.run()