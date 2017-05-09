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
CIRCLE_SCALE = .07
POSITION_L = .225, -0.143, -.05
POSITION_R = -.205, -.14, .015
VR_OBJECTS_FILENAME = './assets/Eng_AllObjs1.obj'  #rc.resources.obj_primitives
VR_OBJECT_VISIBLE = True
VR_OBJECT_NAMES = ['Monkey']
VR_OBJECT_NAME = 'Monkey'
VR_OBJECT_SCALE = .01
VR_OBJECT_SIDE = 'R'


window = utils.setup_window(screen=SCREEN, fullscreen=FULLSCREEN)
cube_fbo = utils.setup_cube_fbo()

motive = NatClient(read_rate=2000)

scene, arena, arena_rb = utils.load_projected_scene(arena_file=ARENA_FILENAME, projector_file=PROJECTOR_FILENAME, motive_client=motive)
arena.texture = cube_fbo.texture

shader = rc.Shader.from_file(*rc.resources.genShader)

fps_display = pyglet.window.FPSDisplay(window)


def load_vr_obj_mesh(obj_filename, mesh_name, arena, position, scale=VR_OBJECT_SCALE):
    vr_obj_reader = rc.WavefrontReader(obj_filename)
    mesh = vr_obj_reader.get_mesh(mesh_name, scale=scale, position=position)
    mesh.parent = arena
    mesh.uniforms['diffuse'] = (.5,) * 3
    mesh.uniforms['specular'] = 0., 0., 0.
    mesh.uniforms['flat_shading'] = False
    mesh.uniforms['ambient'] = (1.,) * 3
    return mesh

mesh_local_pos = POSITION_L if 'l' in VR_OBJECT_SIDE.lower() else POSITION_R

if VR_OBJECT_VISIBLE:
    vr_meshes = [load_vr_obj_mesh(obj_filename=VR_OBJECTS_FILENAME,
                                 arena=arena,
                                 position=mesh_local_pos,
                                 mesh_name=VR_OBJECT_NAME)]
else:
    vr_meshes = []


vr_arena = utils.get_virtual_arena_mesh(arena_file=ARENA_FILENAME, arena_mesh=arena, objname='Arena', texture_filename='./assets/uvgrid.png')
vr_meshes.append(vr_arena)

vr_scene = utils.load_virtual_scene(active_scene=scene)
vr_scene.meshes = vr_meshes


@window.event
def on_draw():
    with shader:
        with cube_fbo as fbo:
            vr_scene.draw360_to_texture(fbo.texture)
        scene.draw()
        # vr_scene.draw()
    fps_display.draw()


pyglet.clock.schedule(utils.update, arena, vr_scene.camera, motive)
pyglet.app.run()