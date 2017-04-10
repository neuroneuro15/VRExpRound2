import pyglet
pyglet.options['debug_gl'] = False
import ratcave as rc

from . import cfg, utils


cliff_cfg = cfg['viscliff']

real_scene = utils.load_projected_scene(arena_file='calibration/arena.obj',
                                        projector_file='calibration/projector.pickle')


def load_vr_scene(objfile):
    """Loads meshes from the viscliff scene and returns the ratcave Scene object."""
    reader = rc.WavefrontReader(cliff_cfg['objfile'])
    arena_vr = reader.get_mesh('Arena')
    cliff = reader.get_mesh('Cliff')
    safe1 = reader.get_mesh('Safe1')
    safe2 = reader.get_mesh('Safe2')
    player = rc.Camera(projection=rc.PerspectiveProjection(fov_y=90, aspect=1., z_near=.005, z_far=2.0))
    scene = rc.Scene(meshes=[arena_vr, cliff, safe1, safe2],
                     camera=player)
    return scene

vr_scene = load_vr_scene('assets/viscliff.obj')
vr_scene.light = real_scene.light
rat = vr_scene.camera

window = utils.setup_window(sceneID=1, fullscreen=True)

deferred = utils.setup_deferred_rendering()

shader3d = rc.Shader.from_file(*rc.resources.genShader)


@window.event
def on_draw():
    with shader3d:
        real_scene.draw()

pyglet.app.run()

