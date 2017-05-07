import pyglet
pyglet.options['debug_gl'] = False
import ratcave as rc
# from natnetclient import NatClient
import motive

#from . import cfg, utils
import utils

# cliff_cfg = cfg['viscliff']

real_scene, arena = utils.load_projected_scene(arena_file='calibration/arena.obj',
                                        projector_file='calibration/projector.pickle')
print(real_scene.camera.position)


def load_vr_scene(objfile):
    """Loads meshes from the viscliff scene and returns the ratcave Scene object."""
    reader = rc.WavefrontReader('viscliff.obj')#cliff_cfg['objfile'])
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

window = utils.setup_window(screen=1, fullscreen=True)

deferred = utils.setup_deferred_rendering()

shader3d = rc.Shader.from_file(*rc.resources.genShader)



motive.initialize()
motive.load_project('calibration/exp.ttp')
for el in range(3):
    motive.update()

arena_rb = motive.get_rigid_bodies()['Arena']
print("Motive arena position: {}".format(arena_rb.location))
arena.position.xyz = arena_rb.location
# arena.rotation.xyz = arena_rb.rotation
print(arena.position)

print("Projector FOV_Y: {}".format(real_scene.camera.projection.fov_y))

@window.event
def on_draw():
    with shader3d:
        real_scene.draw()

# def update(dt):
#     arena.rotation.y += 10. * dt
# pyglet.clock.schedule(update)

pyglet.app.run()

