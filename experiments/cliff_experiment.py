from __future__ import print_function

from app import RatcaveApp, motive
import cfg
import ratcave as rc

if not cfg.CLIFF_SIDE.lower() in 'lr':
    raise ValueError("CLIFF_SIDE must be 'L' or 'R'.")

if 'real' in cfg.CLIFF_TYPE.lower():
    arena_name = cfg.CLIFF_OBJECT_REAL
elif 'l' in cfg.CLIFF_SIDE.lower():
    arena_name = cfg.CLIFF_OBJECT_L
elif 'r' in cfg.CLIFF_SIDE.lower():
    arena_name = cfg.CLIFF_OBJECT_R

# arena_name = cfg.CLIFF_OBJECT_L if 'l' in cfg.CLIFF_SIDE.lower() else cfg.CLIFF_OBJECT_R
vr_arena = rc.WavefrontReader(cfg.CLIFF_FILENAME).get_mesh(arena_name)
vr_arena.texture = cfg.ARENA_LIGHTING_TEXTURE
vr_arena.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING
vr_arena.uniforms['diffuse'] = cfg.ARENA_LIGHTING_DIFFUSE
vr_arena.uniforms['specular'] = cfg.ARENA_LIGHTING_SPECULAR
vr_scene = rc.Scene(meshes=[vr_arena])

app = RatcaveApp(arena_objfile=cfg.ARENA_FILENAME, projector_file=cfg.PROJECTOR_FILENAME,
                 fullscreen=cfg.FULLSCREEN, screen=cfg.SCREEN)
app.set_mouse_visible(cfg.MOUSE_CURSOR_VISIBLE)

app.arena.texture = cfg.ARENA_LIGHTING_TEXTURE
app.arena.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING
app.arena.uniforms['diffuse'] = cfg.ARENA_LIGHTING_DIFFUSE
app.arena.uniforms['specular'] = cfg.ARENA_LIGHTING_SPECULAR

app.register_vr_scene(vr_scene)

app.run()