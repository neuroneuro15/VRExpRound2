from __future__ import print_function
from app import RatcaveApp
import cfg

from pypixxlib import propixx

projector = propixx.PROPixx()
projector.setSleepMode(not cfg.PROJECTOR_TURNED_ON)
projector.setLampLED(cfg.PROJECTOR_LED_ON)
projector.setLedIntensity("6.25")

app = RatcaveApp(arena_objfile=cfg.ARENA_FILENAME, projector_file=cfg.PROJECTOR_FILENAME)
app.arena.texture = cfg.ARENA_LIGHTING_TEXTURE
app.arena.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING
app.run()