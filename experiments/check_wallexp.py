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

vr_arena = utils.get_virtual_arena_mesh(arena_file=ARENA_FILENAME, arena_mesh=arena, objname='Arena', texture_filename='./assets/uvgrid.png')
vr_meshes.append(vr_arena)

vr_scene = utils.load_virtual_scene(active_scene=scene)
vr_scene.meshes = vr_meshes


@window.event
def on_draw():
    with shader:
        with cube_fbo as fbo:
            vr_scene.draw360_to_texture(fbo.texture)


pyglet.clock.schedule(utils.update, arena, vr_scene.camera, motive)

pyglet.app.run()