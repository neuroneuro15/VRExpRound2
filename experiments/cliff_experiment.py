from __future__ import print_function

from app import RatcaveApp, motive
import ratcave as rc

ARENA_FILENAME = './assets/arena3uv.obj'
CLIFF_FILENAME = './assets/viscliff3.obj'
PROJECTOR_FILENAME = './calibration/p2.pickle'
SCREEN = 1
FULLSCREEN = True
CLIFF_SIDE = 'R' # L or R


arena_name = 'virArena' if 'l' in CLIFF_SIDE.lower() else 'virArena2'
vr_arena = rc.WavefrontReader(CLIFF_FILENAME).get_mesh(arena_name)
vr_arena.texture = './assets/uvgrid.png'
vr_scene = rc.Scene(meshes=[vr_arena])

app = RatcaveApp(arena_objfile=ARENA_FILENAME, projector_file=PROJECTOR_FILENAME)
app.register_vr_scene(vr_scene)
app.run()