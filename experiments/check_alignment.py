from __future__ import print_function
from app import RatcaveApp
import cfg

app = RatcaveApp(arena_objfile=cfg.ARENA_FILENAME, projector_file=cfg.PROJECTOR_FILENAME)
app.arena.texture = cfg.ARENA_LIGHTING_TEXTURE
app.arena.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING
app.run()