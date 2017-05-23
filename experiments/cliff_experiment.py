from __future__ import print_function

from app import RatcaveApp, motive
import cfg
import ratcave as rc
from psychopy.gui import DlgFromDict
from pypixxlib import propixx
import pyglet
import sys
from datetime import datetime
import utils


# Show User-Defined Experiment Settings
conditions = {'RAT': cfg.RAT,
              'EXPERIMENTER': cfg.EXPERIMENTER,
              'PAPER_LOG_CODE': cfg.PAPER_LOG_CODE,
              'CLIFF_TYPE': cfg.CLIFF_TYPE,
              'CLIFF_SIDE': cfg.CLIFF_SIDE,
              }

dlg = DlgFromDict(conditions, title='{} Experiment Settings'.format(cfg.CLIFF_EXPERIMENT_NAME))
if dlg.OK:
    log_code = dlg.dictionary['PAPER_LOG_CODE']
    if not dlg.dictionary['RAT'].lower() in ['test', 'demo']:
        if len(log_code) != 7 or log_code[3] != '-':
            raise ValueError("Invalid PAPER_LOG_CODE.  Please try again.")
        dlg.dictionary['PAPER_LOG_CODE'] = log_code.upper()

    dlg.dictionary['EXPERIMENT'] = cfg.CLIFF_EXPERIMENT_NAME
    cfg.__dict__.update(dlg.dictionary)
else:
    sys.exit()


projector = propixx.PROPixx()
projector.setSleepMode(not cfg.PROJECTOR_TURNED_ON)
projector.setLampLED(cfg.PROJECTOR_LED_ON)
projector.setLedIntensity("50.0" if 'real' in cfg.CLIFF_TYPE.lower() else "12.5")

# Set up VR Scenes
cliff_names = {'real': {'l': 'realArena2', 'r': 'realArena2'},
               'vr': {'l': 'virArena', 'r': 'virArena2'},
               'static': {'l': 'virArena', 'r': 'virArena2'}}
arena_name = cliff_names[cfg.CLIFF_TYPE.lower()][cfg.CLIFF_SIDE.lower()]


vr_arena = rc.WavefrontReader(cfg.CLIFF_FILENAME).get_mesh(arena_name)
vr_arena.texture = cfg.CLIFF_REALARENA_LIGHTING_TEXTURE if 'real' in cfg.CLIFF_TYPE.lower() else cfg.CLIFF_VRARENA_LIGHTING_TEXTURE
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


# Set Motive Filename
if cfg.RAT.lower() not in ['demo']:
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = '{expname}_{datetime}_{RAT}_{CLIFF_TYPE}_{CLIFF_SIDE}_{person}_{log_code}'.format(
        expname=cfg.CLIFF_EXPERIMENT_NAME, datetime=now, RAT=cfg.RAT,
        CLIFF_TYPE=cfg.CLIFF_TYPE, CLIFF_SIDE=cfg.CLIFF_SIDE, person=cfg.EXPERIMENTER[0].upper(),
        log_code=cfg.PAPER_LOG_CODE)
    utils.create_and_configure_experiment_logs(filename=filename, motive_client=motive,
                                               exclude_subnames=['OBJECT', 'WALL'])

app.run()