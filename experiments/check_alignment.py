from __future__ import print_function
from app import RatcaveApp
import cfg

app = RatcaveApp(arena_objfile=cfg.ARENA_FILENAME, projector_file=cfg.PROJECTOR_FILENAME)
app.run()