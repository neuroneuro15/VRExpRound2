from __future__ import print_function

from app import motive, RatcaveApp
import ratcave as rc
import cfg



vr_arena = rc.WavefrontReader(cfg.ARENA_FILENAME).get_mesh('Arena')
vr_arena.texture = './assets/uvgrid.png'

vr_wall = rc.WavefrontReader(rc.resources.obj_primitives).get_mesh('Plane')
vr_wall.scale.x = .5
vr_wall.position.xyz = cfg.VR_WALL_X_OFFSET, 0, 0
vr_wall.position.y += .35
vr_wall.rotation.y = 98
vr_wall.uniforms['diffuse'] = (1.,) * 3
vr_wall.uniforms['specular'] = 0., 0., 0.
vr_wall.texture = rc.Texture.from_image('./assets/uvgrid.png')
vr_wall.uniforms['ambient'] = (1.,) * 3

vr_scene_with_wall = rc.Scene(meshes=[vr_arena, vr_wall])
vr_scene_without_wall = rc.Scene(meshes=[vr_arena])

app = RatcaveApp(arena_objfile=cfg.ARENA_FILENAME, projector_file=cfg.PROJECTOR_FILENAME)
app.register_vr_scene(vr_scene_with_wall)
app.register_vr_scene(vr_scene_without_wall)

app.current_vr_scene = vr_scene_with_wall

app.run()