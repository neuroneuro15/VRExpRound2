from __future__ import print_function

from app import motive, RatcaveApp
import ratcave as rc
import cfg
import pyglet

vr_arena = rc.WavefrontReader(cfg.ARENA_FILENAME).get_mesh('Arena')
vr_arena.texture = cfg.ARENA_LIGHTING_TEXTURE
vr_arena.uniforms['flat_shading'] = cfg.VR_WALL_LIGHTING_FLAT_SHADING
vr_arena.uniforms['diffuse'] = cfg.VR_WALL_LIGHTING_DIFFUSE
vr_arena.uniforms['specular'] = cfg.VR_WALL_LIGHTING_SPECULAR
vr_arena.uniforms['ambient'] = cfg.VR_WALL_LIGHTING_AMBIENT

vr_wall = rc.WavefrontReader(rc.resources.obj_primitives).get_mesh('Plane')
vr_wall.arrays[2][:] /= 1.7
vr_wall.scale.x = cfg.VR_WALL_SCALE
vr_wall.position.xyz = cfg.VR_WALL_X_OFFSET, cfg.VR_WALL_Y_OFFSET, 0
vr_wall.rotation.y = cfg.VR_WALL_Y_ROTATION
vr_wall.uniforms['diffuse'] = cfg.VR_WALL_LIGHTING_DIFFUSE
vr_wall.uniforms['specular'] = cfg.VR_WALL_LIGHTING_SPECULAR
vr_wall.uniforms['ambient'] = cfg.VR_WALL_LIGHTING_AMBIENT
vr_wall.uniforms['flat_shading'] = cfg.VR_WALL_LIGHTING_FLAT_SHADING
vr_wall.texture = cfg.VR_WALL_LIGHTING_TEXTURE

vr_scene_with_wall = rc.Scene(meshes=[vr_arena, vr_wall])
vr_scene_without_wall = rc.Scene(meshes=[vr_arena])

app = RatcaveApp(arena_objfile=cfg.ARENA_FILENAME, projector_file=cfg.PROJECTOR_FILENAME)
app.arena.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING
app.register_vr_scene(vr_scene_with_wall)
app.register_vr_scene(vr_scene_without_wall)

app.current_vr_scene = None #vr_scene_with_wall


app.time = 0.
def update_phase(dt):
    app.time += dt

    if app.time < cfg.VR_WALL_PHASE_1_DURATION_SECS:
        app.current_vr_scene = None
    elif app.time < cfg.VR_WALL_PHASE_1_DURATION_SECS + cfg.VR_WALL_PHASE_2_DURATION_SECS:
        app.current_vr_scene = vr_scene_without_wall
    elif app.time < cfg.VR_WALL_PHASE_1_DURATION_SECS + cfg.VR_WALL_PHASE_2_DURATION_SECS + cfg.VR_WALL_PHASE_3_DURATION_SECS:
        app.current_vr_scene = vr_scene_with_wall
    elif app.time < cfg.VR_WALL_PHASE_1_DURATION_SECS + cfg.VR_WALL_PHASE_2_DURATION_SECS + cfg.VR_WALL_PHASE_3_DURATION_SECS + cfg.VR_WALL_PHASE_4_DURATION_SECS:
        app.current_vr_scene = vr_scene_without_wall
    else:
        app.close()
pyglet.clock.schedule(update_phase)

app.run()
print('All Done!')