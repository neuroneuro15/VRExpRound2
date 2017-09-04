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
              'VR_SPATIAL_NOVELTY_FIXED_POSITION': cfg.VR_SPATIAL_NOVELTY_FIXED_POSITION,
              'VR_SPATIAL_NOVELTY_OBJECT_TYPE': cfg.VR_SPATIAL_NOVELTY_OBJECT_TYPE,
              'FIRST_PERSON_MODE': cfg.FIRST_PERSON_MODE
              }

dlg = DlgFromDict(conditions, title='{} Experiment Settings'.format(cfg.VR_SPATIAL_NOVELTY_EXPERIMENT_NAME),
                  order=['RAT', 'VR_SPATIAL_NOVELTY_OBJECT_TYPE', 'VR_SPATIAL_NOVELTY_OBJECT_NAME',
                         'VR_SPATIAL_NOVELTY_FAMILIAR_POSITION', 'VR_SPATIAL_NOVELTY_NOVEL_POSITION', 'VR_SPATIAL_NOVELTY_FIXED_POSITION',
                         'EXPERIMENTER', 'PAPER_LOG_CODE', 'FIRST_PERSON_MODE'])
if dlg.OK:
    log_code = dlg.dictionary['PAPER_LOG_CODE']
    if not dlg.dictionary['RAT'].lower() in ['test', 'demo']:
        if len(log_code) != 7 or log_code[3] != '-':
            raise ValueError("Invalid PAPER_LOG_CODE.  Please try again.")

        subprocess.Popen(['holdtimer'])  # Launch the timer program

    dlg.dictionary['EXPERIMENT'] = cfg.VR_SPATIAL_NOVELTY_EXPERIMENT_NAME
    cfg.__dict__.update(dlg.dictionary)
    if cfg.VR_SPATIAL_NOVELTY_NOVEL_POSITION == cfg.VR_SPATIAL_NOVELTY_FAMILIAR_POSITION:
            raise ValueError("Familiar Position and Novel Position cannot be equal in this experiment.")
else:
    sys.exit()


projector.setSleepMode(not cfg.PROJECTOR_TURNED_ON)
projector.setLampLED(cfg.PROJECTOR_LED_ON)


if 'demo' in cfg.RAT.lower():
    proj_brightness = "100.0"
elif 'Real' in cfg.VR_SPATIAL_NOVELTY_OBJECT_TYPE:
    proj_brightness = "6.25"
else:
    proj_brightness = "6.25"

# proj_brightness = cfg.VR_SPATIAL_NOVELTY_PROJECTOR_LED_INTENSITY if not 'demo' in cfg.RAT.lower() else '100.0'
projector.setLedIntensity(proj_brightness)

# Configure Ratcave App
app = RatcaveApp(arena_objfile=cfg.ARENA_FILENAME, projector_file=cfg.PROJECTOR_FILENAME,
                 fullscreen=cfg.FULLSCREEN, screen=cfg.SCREEN, antialiasing=cfg.ANTIALIASING,
                 fps_mode=cfg.FIRST_PERSON_MODE)
app.set_mouse_visible(cfg.MOUSE_CURSOR_VISIBLE)
app.arena.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING

if cfg.VR_SPATIAL_COVER_RAT_WITH_UMBRELLA:
    umbrella = rc.WavefrontReader(rc.resources.obj_primitives).get_mesh('Cube')
    umbrella.scale.x = cfg.VR_SPATIAL_UMBRELLA_SCALE
    umbrella.uniforms['diffuse'] = 0., 0., 0.
    umbrella.uniforms['specular'] = 0., 0., 0.
    app.active_scene.meshes.append(umbrella)
    def cover_rat(dt):
        umbrella.position.xyz = app.rat_rb.position
    pyglet.clock.schedule(cover_rat)




# Create and Position Virtual Objects
vr_arena = rc.WavefrontReader(cfg.ARENA_FILENAME).get_mesh('Arena')
vr_arena.texture = cfg.ARENA_LIGHTING_TEXTURE
vr_arena.uniforms['diffuse'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_DIFFUSE
vr_arena.uniforms['specular'] = cfg.ARENA_LIGHTING_SPECULAR
vr_arena.uniforms['flat_shading'] = True #cfg.ARENA_LIGHTING_FLAT_SHADING

object_reader = rc.WavefrontReader(cfg.VR_SPATIAL_NOVELTY_OBJECT_FILENAME)
fixed_object = object_reader.get_mesh(cfg.VR_SPATIAL_NOVELTY_OBJECT_NAME, scale=cfg.VR_SPATIAL_NOVELTY_OBJECT_SCALE)
familiar_object = object_reader.get_mesh(cfg.VR_SPATIAL_NOVELTY_OBJECT_NAME, scale=cfg.VR_SPATIAL_NOVELTY_OBJECT_SCALE)
novel_object = object_reader.get_mesh(cfg.VR_SPATIAL_NOVELTY_OBJECT_NAME, scale=cfg.VR_SPATIAL_NOVELTY_OBJECT_SCALE)

for obj in [fixed_object, familiar_object, novel_object]:
    obj.parent = app.arena
    obj.uniforms['diffuse'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_DIFFUSE if '3D' in cfg.VR_SPATIAL_NOVELTY_OBJECT_TYPE else [el * 0 for el in cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_DIFFUSE]
    obj.uniforms['specular'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_SPECULAR
    obj.uniforms['spec_weight'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_SPEC_WEIGHT
    obj.uniforms['ambient'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_AMBIENT # if '2D' in cfg.VR_SPATIAL_NOVELTY_OBJECT_TYPE else (2.5,) * 3
    obj.uniforms['flat_shading'] = cfg.VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_FLAT_SHADING

fixed_object.position.xyz = cfg.VR_SPATIAL_FIXED_OBJECT_POSITIONS[cfg.VR_SPATIAL_NOVELTY_FIXED_POSITION - 1]
familiar_object.position.xyz = cfg.VR_SPATIAL_NOVELTY_OBJECT_POSITIONS[cfg.VR_SPATIAL_NOVELTY_FAMILIAR_POSITION - 1]
novel_object.position.xyz =  cfg.VR_SPATIAL_NOVELTY_OBJECT_POSITIONS[cfg.VR_SPATIAL_NOVELTY_NOVEL_POSITION - 1]


# Configure Scenes: Virtual scenes for '3D' Condition, and Active scenes for '2D' Condition
scene_without_object = rc.Scene(meshes=[vr_arena], name="Arena without Object")
scene_with_familiar_object = rc.Scene(meshes=[vr_arena, fixed_object, familiar_object], name="Arena with Fixed and Familiar Object")
scene_with_novel_object = rc.Scene(meshes=[vr_arena, fixed_object, novel_object], name="Arena with Fixed and Novel Object")

app.register_vr_scene(scene_without_object)
app.register_vr_scene(scene_with_familiar_object)
app.register_vr_scene(scene_with_novel_object)
app.current_vr_scene = scene_without_object

for scene in [scene_without_object, scene_with_familiar_object, scene_with_novel_object]:
    scene.camera.projection.z_near = cfg.VR_SPATIAL_CAMERA_Z_NEAR


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
    cfg.VR_SPATIAL_NOVELTY_PHASE_1_DURATION_SECS = 3.
    cfg.VR_SPATIAL_NOVELTY_PHASE_2_DURATION_SECS = 3.
    cfg.VR_SPATIAL_NOVELTY_PHASE_3_DURATION_SECS = 3.
    cfg.VR_SPATIAL_NOVELTY_PHASE_4_DURATION_SECS = 3.
else:
    cfg.VR_SPATIAL_NOVELTY_PHASE_1_DURATION_SECS = 1.
    cfg.VR_SPATIAL_NOVELTY_PHASE_2_DURATION_SECS = 50000.
    cfg.VR_SPATIAL_NOVELTY_PHASE_3_DURATION_SECS = 1.
    cfg.VR_SPATIAL_NOVELTY_PHASE_4_DURATION_SECS = 1.

change_virtual_scene = True #if cfg.VR_SPATIAL_NOVELTY_OBJECT_TYPE == '3D' else False

exp_seq = [
    events.wait_duration(cfg.VR_SPATIAL_NOVELTY_PHASE_1_DURATION_SECS),
    events.fade_to_black(meshes=meshes_to_fade, speed=cfg.VR_SPATIAL_NOVELTY_FADE_SPEED),
    events.set_scene_to(app, scene_with_familiar_object, virtual_scene=change_virtual_scene),
    events.fade_to_white(meshes=meshes_to_fade, speed=cfg.VR_SPATIAL_NOVELTY_FADE_SPEED),
    events.wait_duration(cfg.VR_SPATIAL_NOVELTY_PHASE_2_DURATION_SECS),
    events.fade_to_black(meshes=meshes_to_fade, speed=cfg.VR_SPATIAL_NOVELTY_FADE_SPEED),
    events.set_scene_to(app, scene_without_object, virtual_scene=change_virtual_scene),
    events.fade_to_white(meshes=meshes_to_fade, speed=cfg.VR_SPATIAL_NOVELTY_FADE_SPEED),
    events.wait_duration(cfg.VR_SPATIAL_NOVELTY_PHASE_3_DURATION_SECS),
    events.fade_to_black(meshes=meshes_to_fade, speed=cfg.VR_SPATIAL_NOVELTY_FADE_SPEED),
    events.set_scene_to(app, scene_with_novel_object, virtual_scene=change_virtual_scene),
    events.fade_to_white(meshes=meshes_to_fade, speed=cfg.VR_SPATIAL_NOVELTY_FADE_SPEED),
    events.wait_duration(cfg.VR_SPATIAL_NOVELTY_PHASE_4_DURATION_SECS),
    events.fade_to_black(meshes=meshes_to_fade, speed=cfg.VR_SPATIAL_NOVELTY_FADE_SPEED),
    events.close_app(app=app)
]
seq.extend(exp_seq)

# Make logfiles and set filenames
if cfg.RAT.lower() not in ['demo']:
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = '{expname}_{datetime}_{RAT}_{OBJECT_TYPE}_{FAMILIAR_POSITION}_{NOVEL_POSITION}_{FIXED_POSITION}_{object_name}_{person}_{log_code}'.format(
        expname=cfg.VR_SPATIAL_NOVELTY_EXPERIMENT_NAME, datetime=now, RAT=cfg.RAT,
        FAMILIAR_POSITION=cfg.VR_SPATIAL_NOVELTY_FAMILIAR_POSITION,
        NOVEL_POSITION=cfg.VR_SPATIAL_NOVELTY_NOVEL_POSITION,
        FIXED_POSITION=cfg.VR_SPATIAL_NOVELTY_FIXED_POSITION,
        OBJECT_TYPE=cfg.VR_SPATIAL_NOVELTY_OBJECT_TYPE,
        object_name=cfg.VR_SPATIAL_NOVELTY_OBJECT_NAME,
        person=cfg.EXPERIMENTER[0:3].upper(),
        log_code=cfg.PAPER_LOG_CODE)
    utils.create_and_configure_experiment_logs(filename=filename, motive_client=motive,
                                               exclude_subnames=['WALL', 'CLIFF', 'VR_OBJECT', 'ACUITY'])

exp = events.chain_events(seq, log=True, motive_client=motive)
exp.next()

# Schedule the event sequence and run the VR App!
pyglet.clock.schedule(exp.send)
app.run()
