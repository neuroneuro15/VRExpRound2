from __future__ import print_function

from app import motive, RatcaveApp
import ratcave as rc

ARENA_FILENAME = './assets/arena3uv.obj'
PROJECTOR_FILENAME = './calibration/p2.pickle'
SCREEN = 1
FULLSCREEN = True
VR_WALL_VISIBLE = True
VR_WALL_X_OFFSET = .0

vr_arena = rc.WavefrontReader(ARENA_FILENAME).get_mesh('Arena')
vr_arena.texture = './assets/uvgrid.png'

vr_wall = rc.WavefrontReader(rc.resources.obj_primitives).get_mesh('Plane')
vr_wall.scale.x = .5
vr_wall.position.xyz = VR_WALL_X_OFFSET, 0, 0
vr_wall.position.y += .35
vr_wall.rotation.y = 98
vr_wall.uniforms['diffuse'] = (1.,) * 3
vr_wall.uniforms['specular'] = 0., 0., 0.
vr_wall.texture = rc.Texture.from_image('./assets/uvgrid.png')
vr_wall.uniforms['ambient'] = (1.,) * 3

vr_scene = rc.Scene(meshes=[vr_arena, vr_wall], bgColor=(1., 1., 0.))

app = RatcaveApp(arena_objfile=ARENA_FILENAME, projector_file=PROJECTOR_FILENAME)
app.register_vr_scene(vr_scene)
app.run()