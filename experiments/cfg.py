import itertools as it

experiments = ['cliff', 'wall', 'object_exploration']
rats = ['Test'] + ['VR-{}{}'.format(cage, num) for cage, num in it.product(range(1, 6), 'AB')]

# General settings
ARENA_FILENAME = './assets/arena3uv.obj'
ARENA_LIGHTING_TEXTURE = './assets/uvgrid.png'
PROJECTOR_FILENAME = './calibration/p2.pickle'
SCREEN = 1
FULLSCREEN = True

# Cliff experiment settings
CLIFF_FILENAME = './assets/viscliff3.obj'
CLIFF_SIDE = 'R' # L or R
CLIFF_OBJECT_L = 'virArena',
CLIFF_OBJECT_R = 'virArena2'

# Wall experiment settings
VR_WALL_VISIBLE = True
VR_WALL_X_OFFSET = .0
VR_WALL_Y_OFFSET = .35
VR_WALL_SCALE = .5
VR_WALL_Y_ROTATION = 98.
VR_WALL_LIGHTING_DIFFUSE = 1., 1., 1.
VR_WALL_LIGHTING_SPECULAR = 0., 0., 0.
VR_WALL_LIGHTING_AMBIENT = 1., 1., 1.
VR_WALL_LIGHTING_TEXTURE = './assets/uvgrid.png'

# Object experiment settings
CIRCLE_SCALE = .07
POSITION_L = .225, -0.143, -.05
POSITION_R = -.205, -.14, .015
VR_OBJECTS_FILENAME = './assets/Eng_AllObjs1.obj'  #rc.resources.obj_primitives
VR_OBJECT_VISIBLE = True
VR_OBJECT_NAMES = ['Monkey']
VR_OBJECT_NAME = 'Monkey'
VR_OBJECT_SCALE = .01
VR_OBJECT_SIDE = 'R'
VR_OBJECT_LIGHTING_DIFFUSE = 0.5, 0.5, 0.5
VR_OBJECT_LIGHTING_SPECULAR = 0., 0., 0.
VR_OBJECT_LIGHTING_AMBIENT = 1., 1., 1.
VR_OBJECT_LIGHTING_FLAT_SHADING = False
VR_OBJECT_LIGHTING_TEXTURE = './assets/uvgrid.png'