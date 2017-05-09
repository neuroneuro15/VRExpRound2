from __future__ import print_function

from app import motive, RatcaveApp
import ratcave as rc
import cfg

vr_arena = rc.WavefrontReader(cfg.ARENA_FILENAME).get_mesh('Arena')
vr_arena.texture = './assets/uvgrid.png'

vr_object = rc.WavefrontReader(cfg.VR_OBJECTS_FILENAME).get_mesh(cfg.VR_OBJECT_NAME, scale=cfg.VR_OBJECT_SCALE)
vr_object.position.xyz = cfg.POSITION_L if 'l' in cfg.VR_OBJECT_SIDE.lower() else cfg.POSITION_R
vr_object.uniforms['diffuse'] = (.5,) * 3
vr_object.uniforms['specular'] = 0., 0., 0.
vr_object.uniforms['flat_shading'] = False
vr_object.uniforms['ambient'] = (1.,) * 3
vr_object.texture = './assets/uvgrid.png'

vr_scene_without_object = rc.Scene(meshes=[vr_arena])
vr_scene_with_object = rc.Scene(meshes=[vr_arena, vr_object])

app = RatcaveApp(arena_objfile=cfg.ARENA_FILENAME, projector_file=cfg.PROJECTOR_FILENAME)
app.register_vr_scene(vr_scene_with_object)
app.register_vr_scene(vr_scene_without_object)

app.current_vr_scene = vr_scene_with_object

app.run()