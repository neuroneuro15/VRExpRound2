from __future__ import print_function

import itertools
from app import motive, RatcaveApp
import ratcave as rc
import cfg
import pyglet
import events
import subprocess
from psychopy.gui import DlgFromDict
import sys
from datetime import datetime
import utils
from pypixxlib import propixx

projector = propixx.PROPixx()

# Show User-Defined Experiment Settings
conditions = {'RAT': cfg.RAT,
              'EXPERIMENTER': cfg.EXPERIMENTER,
              'PAPER_LOG_CODE': cfg.PAPER_LOG_CODE,
              'VR_SPATIAL_NOVELTY_OBJECT_NAME': cfg.VR_SPATIAL_NOVELTY_OBJECT_NAME,
              'VR_SPATIAL_NOVELTY_FAMILIAR_POSITION': cfg.VR_SPATIAL_NOVELTY_FAMILIAR_POSITION,
              'VR_SPATIAL_NOVELTY_NOVEL_POSITION': cfg.VR_SPATIAL_NOVELTY_NOVEL_POSITION,
              'VR_SPATIAL_NOVELTY_OBJECT_TYPE': cfg.VR_SPATIAL_NOVELTY_OBJECT_TYPE,
              }

dlg = DlgFromDict(conditions, title='{} Experiment Settings'.format(cfg.VR_SPATIAL_NOVELTY_EXPERIMENT_NAME),
                  order=['RAT', 'VR_SPATIAL_NOVELTY_OBJECT_TYPE', 'VR_SPATIAL_NOVELTY_OBJECT_NAME',
                         'VR_SPATIAL_NOVELTY_FAMILIAR_POSITION', 'VR_SPATIAL_NOVELTY_NOVEL_POSITION',
                         'EXPERIMENTER', 'PAPER_LOG_CODE'])
if dlg.OK:
    log_code = dlg.dictionary['PAPER_LOG_CODE']
    if not dlg.dictionary['RAT'].lower() in ['test', 'demo']:
        if len(log_code) != 7 or log_code[3] != '-':
            raise ValueError("Invalid PAPER_LOG_CODE.  Please try again.")
        subprocess.Popen(['holdtimer'])  # Launch the timer program

    dlg.dictionary['EXPERIMENT'] = cfg.VR_SPATIAL_NOVELTY_EXPERIMENT_NAME
    cfg.__dict__.update(dlg.dictionary)
else:
    sys.exit()


projector.setSleepMode(not cfg.PROJECTOR_TURNED_ON)
projector.setLampLED(cfg.PROJECTOR_LED_ON)
proj_brightness = cfg.VR_SPATIAL_NOVELTY_PROJECTOR_LED_INTENSITY if not 'demo' in cfg.RAT.lower() else '100.0'
projector.setLedIntensity(proj_brightness)

# Create Virtual Scenes
vr_arena = rc.WavefrontReader(cfg.ARENA_FILENAME).get_mesh('Arena')
vr_arena.texture = cfg.ARENA_LIGHTING_TEXTURE
vr_arena.uniforms['diffuse'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_DIFFUSE
vr_arena.uniforms['specular'] = cfg.ARENA_LIGHTING_SPECULAR
vr_arena.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING

object_reader = rc.WavefrontReader(cfg.VR_SPATIAL_NOVELTY_OBJECT_FILENAME)
fixed_object = object_reader.get_mesh(cfg.VR_SPATIAL_NOVELTY_OBJECT_NAME, scale=cfg.VR_SPATIAL_NOVELTY_OBJECT_SCALE)
fixed_object.position.xyz = cfg.VR_SPATIAL_FIXED_OBJECT_POSITION
fixed_object.uniforms['diffuse'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_DIFFUSE
fixed_object.uniforms['specular'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_SPECULAR
fixed_object.uniforms['spec_weight'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_SPEC_WEIGHT
fixed_object.uniforms['ambient'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_AMBIENT
fixed_object.uniforms['flat_shading'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_FLAT_SHADING

familiar_object = object_reader.get_mesh(cfg.VR_SPATIAL_NOVELTY_OBJECT_NAME, scale=cfg.VR_SPATIAL_NOVELTY_OBJECT_SCALE)
familiar_object.position.xyz = cfg.VR_SPATIAL_NOVELTY_OBJECT_POSITIONS[cfg.VR_SPATIAL_NOVELTY_FAMILIAR_POSITION - 1]
familiar_object.uniforms['diffuse'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_DIFFUSE
familiar_object.uniforms['specular'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_SPECULAR
familiar_object.uniforms['spec_weight'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_SPEC_WEIGHT
familiar_object.uniforms['ambient'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_AMBIENT
familiar_object.uniforms['flat_shading'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_FLAT_SHADING

novel_object = object_reader.get_mesh(cfg.VR_SPATIAL_NOVELTY_OBJECT_NAME, scale=cfg.VR_SPATIAL_NOVELTY_OBJECT_SCALE)
novel_object.position.xyz =  cfg.VR_SPATIAL_NOVELTY_OBJECT_POSITIONS[cfg.VR_SPATIAL_NOVELTY_NOVEL_POSITION - 1]
novel_object.uniforms['diffuse'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_DIFFUSE
novel_object.uniforms['specular'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_SPECULAR
novel_object.uniforms['spec_weight'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_SPEC_WEIGHT
novel_object.uniforms['ambient'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_AMBIENT
novel_object.uniforms['flat_shading'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_FLAT_SHADING



vr_scene_without_object = rc.Scene(meshes=[vr_arena], name="Arena without Object")
vr_scene_with_familiar_object = rc.Scene(meshes=[vr_arena, fixed_object, familiar_object], name="Arena with Fixed and Familiar Object")
vr_scene_with_novel_object = rc.Scene(meshes=[vr_arena, fixed_object, novel_object], name="Arena with Fixed and Novel Object")


# Configure Ratcave App and register the virtual Scenes.
app = RatcaveApp(arena_objfile=cfg.ARENA_FILENAME, projector_file=cfg.PROJECTOR_FILENAME,
                 fullscreen=cfg.FULLSCREEN, screen=cfg.SCREEN, antialiasing=cfg.ANTIALIASING,
                 fps_mode=cfg.FIRST_PERSON_MODE)
app.set_mouse_visible(cfg.MOUSE_CURSOR_VISIBLE)
app.arena.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING

app.register_vr_scene(vr_scene_without_object)
app.register_vr_scene(vr_scene_with_familiar_object)
app.register_vr_scene(vr_scene_with_novel_object)

app.current_vr_scene = vr_scene_without_object

meshes_to_fade = [app.arena]


# Build experiment event sequence
seq = []
if cfg.RAT.lower() not in ['test', 'demo']:
    motive_seq = [
        events.change_scene_background_color(scene=app.active_scene, color=(0., 0., 1.)),
        events.wait_for_recording(motive_client=motive),
        events.change_scene_background_color(scene=app.active_scene, color=(1., 0., 0.)),
    ]
    seq.extend(motive_seq)
elif cfg.RAT.lower() in 'test':
    cfg.VR_SPATIAL_NOVELTY_PHASE_1_DURATION_SECS = 1.
    cfg.VR_SPATIAL_NOVELTY_PHASE_2_DURATION_SECS = 1.
    cfg.VR_SPATIAL_NOVELTY_PHASE_3_DURATION_SECS = 5.
    cfg.VR_SPATIAL_NOVELTY_PHASE_4_DURATION_SECS = 1.
else:
    cfg.VR_SPATIAL_NOVELTY_PHASE_1_DURATION_SECS = 1.
    cfg.VR_SPATIAL_NOVELTY_PHASE_2_DURATION_SECS = 50000.
    cfg.VR_SPATIAL_NOVELTY_PHASE_3_DURATION_SECS = 1.
    cfg.VR_SPATIAL_NOVELTY_PHASE_4_DURATION_SECS = 1.

exp_seq = [
    events.wait_duration(cfg.VR_SPATIAL_NOVELTY_PHASE_1_DURATION_SECS),
    events.fade_to_black(meshes=meshes_to_fade, speed=cfg.VR_SPATIAL_NOVELTY_FADE_SPEED),
    events.set_scene_to(app, vr_scene_with_familiar_object),
    events.fade_to_white(meshes=meshes_to_fade, speed=cfg.VR_SPATIAL_NOVELTY_FADE_SPEED),
    events.wait_duration(cfg.VR_SPATIAL_NOVELTY_PHASE_2_DURATION_SECS),
    events.fade_to_black(meshes=meshes_to_fade, speed=cfg.VR_SPATIAL_NOVELTY_FADE_SPEED),
    events.set_scene_to(app, vr_scene_without_object),
    events.fade_to_white(meshes=meshes_to_fade, speed=cfg.VR_SPATIAL_NOVELTY_FADE_SPEED),
    events.wait_duration(cfg.VR_SPATIAL_NOVELTY_PHASE_3_DURATION_SECS),
    events.fade_to_black(meshes=meshes_to_fade, speed=cfg.VR_SPATIAL_NOVELTY_FADE_SPEED),
    events.set_scene_to(app, vr_scene_with_novel_object),
    events.fade_to_white(meshes=meshes_to_fade, speed=cfg.VR_SPATIAL_NOVELTY_FADE_SPEED),
    events.wait_duration(cfg.VR_SPATIAL_NOVELTY_PHASE_4_DURATION_SECS),
    events.fade_to_black(meshes=meshes_to_fade, speed=cfg.VR_SPATIAL_NOVELTY_FADE_SPEED),
    events.close_app(app=app)
]
seq.extend(exp_seq)

# Make logfiles and set filenames
if cfg.RAT.lower() not in ['demo']:
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = '{expname}_{datetime}_{RAT}_{OBJECT_TYPE}_{FAMILIAR_POSITION}_{NOVEL_POSITION}_{object_name}_{person}_{log_code}'.format(
        expname=cfg.VR_SPATIAL_NOVELTY_EXPERIMENT_NAME, datetime=now, RAT=cfg.RAT,
        FAMILIAR_POSITION=cfg.VR_SPATIAL_NOVELTY_FAMILIAR_POSITION,
        NOVEL_POSITION=cfg.VR_SPATIAL_NOVELTY_NOVEL_POSITION,
        OBJECT_TYPE=cfg.VR_SPATIAL_NOVELTY_OBJECT_TYPE,
        object_name=cfg.VR_SPATIAL_NOVELTY_OBJECT_NAME,
        person=cfg.EXPERIMENTER[0:3].upper(),
        log_code=cfg.PAPER_LOG_CODE)
    utils.create_and_configure_experiment_logs(filename=filename, motive_client=motive,
                                               exclude_subnames=['WALL', 'CLIFF', 'OBJECT', 'ACUITY'])

exp = events.chain_events(seq, log=True, motive_client=motive)
exp.next()

# Schedule the event sequence and run the VR App!
pyglet.clock.schedule(exp.send)
app.run()
