from __future__ import print_function

from app import motive, RatcaveApp
import ratcave as rc
import cfg
import pyglet
import events
import subprocess
import logging
from psychopy.gui import DlgFromDict
import sys
from datetime import datetime
import json

# Check that environment is set up.


if not motive.rigid_bodies:
    raise IOError("Not Detecting Rigid Bodies.  Turn RigidBody Streaming On in the Motive Streaming Pane.")

if not motive.rigid_bodies['Arena'].position:
    raise IOError("Not Detecitng Arena Position.  Turn RigidBody Streaming on in the Motive Streaming Pane.")



# Show User-Defined Experiment Settings
conditions = {'RAT': cfg.RAT, 'VR_WALL_X_OFFSET': cfg.VR_WALL_X_OFFSET,
              'EXPERIMENTER': cfg.EXPERIMENTER, 'PAPER_LOG_CODE': cfg.PAPER_LOG_CODE}

dlg = DlgFromDict(conditions, title='Virtual Wall Experiment')
if dlg.OK:
    log_code = dlg.dictionary['PAPER_LOG_CODE']
    if not 'test' in dlg.dictionary['RAT'].lower():
        if len(log_code) != 7 or log_code[3] != '-':
            raise ValueError("Invalid PAPER_LOG_CODE.  Please try again.")
        subprocess.Popen(['holdtimer'])  # Launch the timer program

    dlg.dictionary['EXPERIMENT'] = 'wall'
    cfg.__dict__.update(dlg.dictionary)
else:
    sys.exit()


# Create Virtual Scenes
vr_lighting = {
    'diffuse': cfg.VR_WALL_LIGHTING_DIFFUSE,
    'specular': cfg.VR_WALL_LIGHTING_SPECULAR,
    'ambient': cfg.VR_WALL_LIGHTING_AMBIENT,
    'flat_shading': cfg.VR_WALL_LIGHTING_FLAT_SHADING,
}

vr_arena = rc.WavefrontReader(cfg.ARENA_FILENAME).get_mesh('Arena')
vr_arena.texture = cfg.ARENA_LIGHTING_TEXTURE
for key, value in vr_lighting.iteritems():
    vr_arena.uniforms[key] = value #.update(vr_lighting)

vr_wall = rc.WavefrontReader(rc.resources.obj_primitives).get_mesh('Plane')
vr_wall.arrays[2][:] /= 1.7
vr_wall.scale.x = cfg.VR_WALL_SCALE
vr_wall.position.xyz = cfg.VR_WALL_X_OFFSET, cfg.VR_WALL_Y_OFFSET, 0
vr_wall.rotation.y = cfg.VR_WALL_Y_ROTATION
for key, value in vr_lighting.iteritems():
    vr_wall.uniforms[key] = value
vr_wall.texture = cfg.VR_WALL_LIGHTING_TEXTURE

vr_scene_with_wall = rc.Scene(meshes=[vr_arena, vr_wall], name="Arena without Wall")
vr_scene_without_wall = rc.Scene(meshes=[vr_arena], name="Arena with Wall")


# Configure Ratcave App and register the virtual Scenes.
app = RatcaveApp(arena_objfile=cfg.ARENA_FILENAME, projector_file=cfg.PROJECTOR_FILENAME,
                 fullscreen=cfg.FULLSCREEN, screen=cfg.SCREEN)
app.set_mouse_visible(cfg.MOUSE_CURSOR_VISIBLE)
app.arena.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING

app.register_vr_scene(vr_scene_with_wall)
app.register_vr_scene(vr_scene_without_wall)

app.current_vr_scene = None #vr_scene_with_wall


# Make logfiles and set filenames
now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
filename = '{expname}_{datetime}_{RAT}_{VR_WALL_X_OFFSET}_{person}'.format(
    expname='VRWallExp', datetime=now, RAT=cfg.RAT,
    VR_WALL_X_OFFSET=cfg.VR_WALL_X_OFFSET, person=cfg.EXPERIMENTER[0].upper())

filename_settings = 'logs/settings_logs/' + filename + '.json'
with open(filename_settings, 'w') as f:
    json.dump({var: cfg.__dict__[var] for var in dir(cfg) if not '_' in var[0] and not 'OBJECT' in var and not 'CLIFF' in var}, f, sort_keys=True, indent=4)

filename_log = 'logs/event_logs/' + filename + '.csv'
with open(filename_log, 'a') as f:
    f.write('DateTime; MotiveExpTimeSecs; Event; EventArguments\n')
logging.basicConfig(filename=filename_log,
                    level=logging.INFO, format='%(asctime)s; %(message)s')

motive.set_take_file_name(file_name=filename)


# Build experiment event sequence
seq = []
if not 'test' in cfg.RAT.lower():
    motive_seq = [
        events.change_scene_background_color(scene=app.active_scene, color=(0., 0., 1.)),
        events.wait_for_recording(motive_client=motive),
        events.change_scene_background_color(scene=app.active_scene, color=(0., 1., 0.)),
        events.wait_for_distance_under(rb1=app.arena_rb, rb2=motive.rigid_bodies['TransportBox'], distance=0.5),
        events.wait_for_distance_exceeded(rb1=app.rat_rb, rb2=motive.rigid_bodies['TransportBox'], distance=0.4),
        events.change_scene_background_color(scene=app.active_scene, color=(1., 0., 0.)),
    ]
    seq.extend(motive_seq)
else:
    cfg.VR_WALL_PHASE_1_DURATION_SECS = 1.
    cfg.VR_WALL_PHASE_2_DURATION_SECS = 1.
    cfg.VR_WALL_PHASE_3_DURATION_SECS = 50000.

exp_seq = [
    events.wait_duration(cfg.VR_WALL_PHASE_1_DURATION_SECS),
    events.fade_to_black(app.arena),
    events.set_scene_to(app, vr_scene_without_wall),
    events.fade_to_white(app.arena),
    events.wait_duration(cfg.VR_WALL_PHASE_2_DURATION_SECS),
    events.fade_to_black(app.arena),
    events.set_scene_to(app, vr_scene_with_wall),
    events.fade_to_white(app.arena),
    events.wait_duration(cfg.VR_WALL_PHASE_3_DURATION_SECS),
    events.fade_to_black(app.arena),
    events.set_scene_to(app, vr_scene_without_wall),
    events.fade_to_white(app.arena),
    events.wait_duration(cfg.VR_WALL_PHASE_4_DURATION_SECS)
]
seq.extend(exp_seq)
exp = events.chain_events(seq, log=True, motive_client=motive)
exp.next()

def update_phase(dt):
    try:
        exp.send(dt)
    except StopIteration:
        app.close()
pyglet.clock.schedule(update_phase)





# Run the VR App!
app.run()