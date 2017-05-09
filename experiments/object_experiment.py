from __future__ import print_function

from app import motive, RatcaveApp
import ratcave as rc

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

vr_arena = rc.WavefrontReader(ARENA_FILENAME).get_mesh('Arena')
vr_arena.texture = './assets/uvgrid.png'

vr_object = rc.WavefrontReader(VR_OBJECTS_FILENAME).get_mesh(VR_OBJECT_NAME, scale=VR_OBJECT_SCALE)
vr_object.position.xyz = POSITION_L if 'l' in VR_OBJECT_SIDE.lower() else POSITION_R
vr_object.uniforms['diffuse'] = (.5,) * 3
vr_object.uniforms['specular'] = 0., 0., 0.
vr_object.uniforms['flat_shading'] = False
vr_object.uniforms['ambient'] = (1.,) * 3
vr_object.texture = './assets/uvgrid.png'

vr_scene = rc.Scene(meshes=[vr_arena, vr_object])

app = RatcaveApp(arena_objfile=ARENA_FILENAME, projector_file=PROJECTOR_FILENAME)
app.register_vr_scene(vr_scene)
app.run()