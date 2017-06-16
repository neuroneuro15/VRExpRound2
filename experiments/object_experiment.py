from __future__ import print_function

import itertools
from app import motive, RatcaveApp
import ratcave as rc
import cfg
import pyglet
from serial import Serial
import events
import subprocess
from psychopy.gui import DlgFromDict
import sys
from datetime import datetime
import utils
from pypixxlib import propixx
import warnings

projector = propixx.PROPixx()

robo_arm = Serial(cfg.VR_OBJECT_ARDUINO_PORT, timeout=0.5)

# print('Current RoboArm rotation: ', motive.rigid_bodies['RoboArm'].rotation )
if motive.rigid_bodies['RoboArm'].rotation[2] > -15:
    warnings.warn("RoboArm seems to be raised currently. It should be lowered first.")
    robo_arm.write('D')


# Show User-Defined Experiment Settings
conditions = {'RAT': cfg.RAT,
              'EXPERIMENTER': cfg.EXPERIMENTER,
              'PAPER_LOG_CODE': cfg.PAPER_LOG_CODE,
              'VR_OBJECT_NAME': cfg.VR_OBJECT_NAME,
              'VR_OBJECT_SIDE': cfg.VR_OBJECT_SIDE,
              'VR_OBJECT_TYPE': cfg.VR_OBJECT_TYPE,
              }
dlg = DlgFromDict(conditions, title='{} Experiment Settings'.format(cfg.VR_OBJECT_EXPERIMENT_NAME),
                  order=['RAT', 'VR_OBJECT_TYPE', 'VR_OBJECT_SIDE', 'VR_OBJECT_NAME', 'EXPERIMENTER', 'PAPER_LOG_CODE'])
if dlg.OK:
    log_code = dlg.dictionary['PAPER_LOG_CODE']
    if not dlg.dictionary['RAT'].lower() in ['test', 'demo']:
        if len(log_code) != 7 or log_code[3] != '-':
            raise ValueError("Invalid PAPER_LOG_CODE.  Please try again.")
        subprocess.Popen(['holdtimer'])  # Launch the timer program

    dlg.dictionary['EXPERIMENT'] = cfg.VR_OBJECT_EXPERIMENT_NAME
    cfg.__dict__.update(dlg.dictionary)
else:
    sys.exit()


projector.setSleepMode(not cfg.PROJECTOR_TURNED_ON)
projector.setLampLED(cfg.PROJECTOR_LED_ON)
proj_brightness = cfg.VR_OBJECT_PROJECTOR_LED_INTENSITY if not 'demo' in cfg.RAT.lower() else '100.0'
projector.setLedIntensity(proj_brightness)

# Create Virtual Scenes
vr_arena = rc.WavefrontReader(cfg.ARENA_FILENAME).get_mesh('Arena')
vr_arena.texture = cfg.ARENA_LIGHTING_TEXTURE
vr_arena.uniforms['diffuse'] = cfg.VR_OBJECT_VRARENA_LIGHTING_DIFFUSE
vr_arena.uniforms['specular'] = cfg.ARENA_LIGHTING_SPECULAR
vr_arena.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING

vr_object = rc.WavefrontReader(cfg.VR_OBJECT_FILENAME).get_mesh(cfg.VR_OBJECT_NAME, scale=cfg.VR_OBJECT_SCALE)
vr_object.position.xyz = cfg.VR_OBJECT_POSITION_L if 'l' in cfg.VR_OBJECT_SIDE.lower() else cfg.VR_OBJECT_POSITION_R
vr_object.position.y += cfg.VR_OBJECT_Y_OFFSET
vr_object.uniforms['diffuse'] = cfg.VR_OBJECT_LIGHTING_DIFFUSE
vr_object.uniforms['specular'] = cfg.VR_OBJECT_LIGHTING_SPECULAR
vr_object.uniforms['spec_weight'] = cfg.VR_OBJECT_LIGHTING_SPEC_WEIGHT
vr_object.uniforms['ambient'] = cfg.VR_OBJECT_LIGHTING_AMBIENT
vr_object.uniforms['flat_shading'] = cfg.VR_OBJECT_LIGHTING_FLAT_SHADING
if 'real' in cfg.VR_OBJECT_TYPE.lower():
    vr_object.visible = False

if cfg.VR_OBJECT_LIGHTING_TEXTURE:
    vr_object.texture = cfg.VR_OBJECT_LIGHTING_TEXTURE

vr_scene_without_object = rc.Scene(meshes=[vr_arena], name="Arena without Object")
vr_scene_with_object = rc.Scene(meshes=[vr_arena, vr_object], name="Arena with Object")


# Configure Ratcave App and register the virtual Scenes.
app = RatcaveApp(arena_objfile=cfg.ARENA_FILENAME, projector_file=cfg.PROJECTOR_FILENAME,
                 fullscreen=cfg.FULLSCREEN, screen=cfg.SCREEN, antialiasing=cfg.ANTIALIASING,
                 fps_mode=cfg.FIRST_PERSON_MODE)
app.set_mouse_visible(cfg.MOUSE_CURSOR_VISIBLE)
app.arena.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING

app.register_vr_scene(vr_scene_with_object)
app.register_vr_scene(vr_scene_without_object)

app.current_vr_scene = None

meshes_to_fade = [app.arena]
# Highlight positions of Real Objects with circles, so squares aren't drawn on them.
circles = []
if 'real' in cfg.VR_OBJECT_TYPE.lower():
    primitive_reader = rc.WavefrontReader(rc.resources.obj_primitives)
    for position in [cfg.VR_OBJECT_POSITION_L, cfg.VR_OBJECT_POSITION_R]:
        circle = primitive_reader.get_mesh('Circle')
        circle.position.xyz = position
        circle.position.y += cfg.VR_OBJECT_CIRCLE_Y_OFFSET
        circle.rotation.x = 90
        circle.parent = app.arena
        circle.scale.x = cfg.VR_OBJECT_CIRCLE_SCALE
        circle.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING
        circle.uniforms['diffuse'] = cfg.VR_OBJECT_VRARENA_LIGHTING_DIFFUSE
        app.active_scene.meshes.append(circle)
        circles.append(circle)
        meshes_to_fade.append(circle)


# Build experiment event sequence
seq = []
if cfg.RAT.lower() not in ['test', 'demo']:
    motive_seq = [
        events.change_scene_background_color(scene=app.active_scene, color=(0., 0., 1.)),
        events.wait_for_recording(motive_client=motive),
        events.change_scene_background_color(scene=app.active_scene, color=(0., 1., 0.)),
        # events.wait_for_distance_under(rb1=app.arena_rb, rb2=motive.rigid_bodies['TransportBox'], distance=0.5),
        # events.wait_for_distance_exceeded(rb1=app.rat_rb, rb2=motive.rigid_bodies['TransportBox'], distance=0.4),
        events.change_scene_background_color(scene=app.active_scene, color=(1., 0., 0.)),
    ]
    seq.extend(motive_seq)
elif cfg.RAT.lower() in 'test':
    cfg.VR_OBJECT_PHASE_1_DURATION_SECS = 1.
    cfg.VR_OBJECT_PHASE_2_DURATION_SECS = 1.
    cfg.VR_OBJECT_PHASE_3_DURATION_SECS = 5.
    cfg.VR_OBJECT_PHASE_4_DURATION_SECS = 1.
else:
    cfg.VR_OBJECT_PHASE_1_DURATION_SECS = 1.
    cfg.VR_OBJECT_PHASE_2_DURATION_SECS = 1.
    cfg.VR_OBJECT_PHASE_3_DURATION_SECS = 50000.
    cfg.VR_OBJECT_PHASE_4_DURATION_SECS = 1.

exp_seq = [
    events.wait_duration(cfg.VR_OBJECT_PHASE_1_DURATION_SECS),
    events.fade_to_black(meshes=meshes_to_fade, speed=cfg.VR_OBJECT_FADE_SPEED),
    events.set_scene_to(app, vr_scene_without_object),
    events.fade_to_white(meshes=meshes_to_fade, speed=cfg.VR_OBJECT_FADE_SPEED),
    events.wait_duration(cfg.VR_OBJECT_PHASE_2_DURATION_SECS),
    events.fade_to_black(meshes=meshes_to_fade, speed=cfg.VR_OBJECT_FADE_SPEED),
    events.send_robo_command(robo_arm, cfg.VR_OBJECT_ROBO_COMMAND_UP),
    events.wait_duration(cfg.VR_OBJECT_ROBO_ARM_WAIT_DURATION_SECS),
    events.set_scene_to(app, vr_scene_with_object),
    events.fade_to_white(meshes=meshes_to_fade, speed=cfg.VR_OBJECT_FADE_SPEED),
    events.wait_duration(cfg.VR_OBJECT_PHASE_3_DURATION_SECS),
    events.fade_to_black(meshes=meshes_to_fade, speed=cfg.VR_OBJECT_FADE_SPEED),
    events.send_robo_command(robo_arm, cfg.VR_OBJECT_ROBO_COMMAND_DOWN),
    events.wait_duration(cfg.VR_OBJECT_ROBO_ARM_WAIT_DURATION_SECS),
    events.set_scene_to(app, vr_scene_without_object),
    events.fade_to_white(meshes=meshes_to_fade, speed=cfg.VR_OBJECT_FADE_SPEED),
    events.wait_duration(cfg.VR_OBJECT_PHASE_4_DURATION_SECS),
    events.fade_to_black(meshes=meshes_to_fade, speed=cfg.VR_OBJECT_FADE_SPEED),
    events.close_app(app=app)
]
seq.extend(exp_seq)

# Make logfiles and set filenames
if cfg.RAT.lower() not in ['demo']:
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = '{expname}_{datetime}_{RAT}_{VR_OBJECT_SIDE}_{object_name}_{person}_{log_code}'.format(
        expname=cfg.VR_OBJECT_EXPERIMENT_NAME, datetime=now, RAT=cfg.RAT,
        VR_OBJECT_SIDE=cfg.VR_OBJECT_SIDE, object_name=cfg.VR_OBJECT_NAME, person=cfg.EXPERIMENTER[0].upper(),
        log_code=cfg.PAPER_LOG_CODE)
    utils.create_and_configure_experiment_logs(filename=filename, motive_client=motive,
                                               exclude_subnames=['WALL', 'CLIFF', 'SPATIAL_NOVELTY', 'ACUITY'])

exp = events.chain_events(seq, log=True, motive_client=motive)
exp.next()

# Schedule the event sequence and run the VR App!
pyglet.clock.schedule(exp.send)
app.run()
