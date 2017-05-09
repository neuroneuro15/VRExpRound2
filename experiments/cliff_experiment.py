from __future__ import print_function

from app import RatcaveApp, motive
import cfg
import ratcave as rc

if not cfg.CLIFF_SIDE.lower() in 'lr':
    raise ValueError("CLIFF_SIDE must be 'L' or 'R'.")
arena_name = cfg.CLIFF_OBJECT_L if 'l' in cfg.CLIFF_SIDE.lower() else cfg.CLIFF_OBJECT_R
vr_arena = rc.WavefrontReader(cfg.CLIFF_FILENAME).get_mesh(arena_name)
vr_arena.texture = cfg.ARENA_LIGHTING_TEXTURE
vr_scene = rc.Scene(meshes=[vr_arena])

app = RatcaveApp(arena_objfile=cfg.ARENA_FILENAME, projector_file=cfg.PROJECTOR_FILENAME)
app.register_vr_scene(vr_scene)
app.run()