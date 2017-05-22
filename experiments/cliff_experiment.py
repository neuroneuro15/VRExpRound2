from __future__ import print_function

from app import RatcaveApp, motive
import cfg
import ratcave as rc
from pypixxlib import propixx
import pyglet

projector = propixx.PROPixx()
projector.setSleepMode(not cfg.PROJECTOR_TURNED_ON)
projector.setLampLED(cfg.PROJECTOR_LED_ON)
projector.setLedIntensity(cfg.CLIFF_PROJECTOR_LED_INTENSITY)


# Set up VR Scenes
cliff_names = {'real': {'l': 'realArena2', 'r': 'realArena2'},
               'vr': {'l': 'virArena', 'r': 'virArena2'},
               'static': {'l': 'virArena', 'r': 'virArena2'}}
arena_name = cliff_names[cfg.CLIFF_TYPE.lower()][cfg.CLIFF_SIDE.lower()]


vr_arena = rc.WavefrontReader(cfg.CLIFF_FILENAME).get_mesh(arena_name)
vr_arena.texture = cfg.CLIFF_ARENA_LIGHTING_TEXTURE
vr_arena.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING
vr_arena.uniforms['diffuse'] = cfg.ARENA_LIGHTING_DIFFUSE
vr_arena.uniforms['specular'] = cfg.ARENA_LIGHTING_SPECULAR
vr_scene = rc.Scene(meshes=vr_arena)

# Configure App
app = RatcaveApp(arena_objfile=cfg.ARENA_FILENAME, projector_file=cfg.PROJECTOR_FILENAME,
                 fullscreen=cfg.FULLSCREEN, screen=cfg.SCREEN, antialiasing=cfg.ANTIALIASING)
app.set_mouse_visible(cfg.MOUSE_CURSOR_VISIBLE)

app.arena.texture = cfg.ARENA_LIGHTING_TEXTURE
app.arena.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING
app.arena.uniforms['diffuse'] = cfg.CLIFF_REALARENA_LIGHTING_DIFFUSE
app.arena.uniforms['specular'] = cfg.ARENA_LIGHTING_SPECULAR

app.register_vr_scene(vr_scene)


# Alter App Behavior for Static and Real conditions
if cfg.CLIFF_TYPE.lower() in ['static', 'real']:
    pyglet.clock.unschedule(app.update)
    app.update(.016)  # Just one single call, to get things adjusted.
    view_pos = app.arena.position.xyz if 'static' in cfg.CLIFF_TYPE.lower() else app.active_scene.camera.position.xyz
    app.current_vr_scene.camera.position.xyz = view_pos
    app.current_vr_scene.camera.uniforms['playerPos'] = view_pos
    app.current_vr_scene.camera.projection.z_far = 4.

app.run()