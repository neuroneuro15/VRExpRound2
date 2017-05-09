from __future__ import print_function

from app import RatcaveApp, motive
import cfg
import ratcave as rc

arena_name = 'virArena' if 'l' in cfg.CLIFF_SIDE.lower() else 'virArena2'
vr_arena = rc.WavefrontReader(cfg.CLIFF_FILENAME).get_mesh(arena_name)
vr_arena.texture = './assets/uvgrid.png'
vr_scene = rc.Scene(meshes=[vr_arena])

app = RatcaveApp(arena_objfile=cfg.ARENA_FILENAME, projector_file=cfg.PROJECTOR_FILENAME)
app.register_vr_scene(vr_scene)
app.run()