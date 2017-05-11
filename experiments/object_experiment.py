from __future__ import print_function

from app import motive, RatcaveApp
import ratcave as rc
import cfg
import pyglet

vr_arena = rc.WavefrontReader(cfg.ARENA_FILENAME).get_mesh('Arena')
vr_arena.texture = cfg.ARENA_LIGHTING_TEXTURE
vr_arena.uniforms['diffuse'] = cfg.ARENA_LIGHTING_DIFFUSE
vr_arena.uniforms['specular'] = cfg.ARENA_LIGHTING_SPECULAR
# vr_object.uniforms['ambient'] = cfg.VR_OBJECT_LIGHTING_AMBIENT
vr_arena.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING


vr_object = rc.WavefrontReader(cfg.VR_OBJECTS_FILENAME).get_mesh(cfg.VR_OBJECT_NAME, scale=cfg.VR_OBJECT_SCALE)
vr_object.position.xyz = cfg.POSITION_L if 'l' in cfg.VR_OBJECT_SIDE.lower() else cfg.POSITION_R
vr_object.uniforms['diffuse'] = cfg.VR_OBJECT_LIGHTING_DIFFUSE
vr_object.uniforms['specular'] = cfg.VR_OBJECT_LIGHTING_SPECULAR
vr_object.uniforms['ambient'] = cfg.VR_OBJECT_LIGHTING_AMBIENT
vr_object.uniforms['flat_shading'] = cfg.VR_OBJECT_LIGHTING_FLAT_SHADING
if cfg.VR_OBJECT_LIGHTING_TEXTURE:
    vr_object.texture = cfg.VR_OBJECT_LIGHTING_TEXTURE

vr_scene_without_object = rc.Scene(meshes=[vr_arena])
vr_scene_with_object = rc.Scene(meshes=[vr_arena, vr_object])

app = RatcaveApp(arena_objfile=cfg.ARENA_FILENAME, projector_file=cfg.PROJECTOR_FILENAME)
app.arena.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING
# app.arena.texture = cfg.ARENA_LIGHTING_TEXTURE

app.register_vr_scene(vr_scene_with_object)
app.register_vr_scene(vr_scene_without_object)

app.current_vr_scene = None


app.time = 0.
def update_phase(dt):
    app.time += dt

    if app.time < cfg.VR_OBJECT_PHASE_1_DURATION_SECS:
        app.current_vr_scene = None
    elif app.time < cfg.VR_OBJECT_PHASE_1_DURATION_SECS + cfg.VR_OBJECT_PHASE_2_DURATION_SECS:
        app.current_vr_scene = vr_scene_without_object
    elif app.time < cfg.VR_OBJECT_PHASE_1_DURATION_SECS + cfg.VR_OBJECT_PHASE_2_DURATION_SECS + cfg.VR_OBJECT_PHASE_3_DURATION_SECS:
        app.current_vr_scene = vr_scene_with_object
    elif app.time < cfg.VR_OBJECT_PHASE_1_DURATION_SECS + cfg.VR_OBJECT_PHASE_2_DURATION_SECS + cfg.VR_OBJECT_PHASE_3_DURATION_SECS + cfg.VR_OBJECT_PHASE_4_DURATION_SECS:
        app.current_vr_scene = vr_scene_without_object
    else:
        app.close()
pyglet.clock.schedule(update_phase)

app.run()