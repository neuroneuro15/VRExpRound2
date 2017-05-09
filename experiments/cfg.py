import itertools as it

experiments = ['cliff', 'wall', 'object_exploration']
rats = ['Test'] + ['VR-{}{}'.format(cage, num) for cage, num in it.product(range(1, 6), 'AB')]

ARENA_FILENAME = './assets/arena3uv.obj'
PROJECTOR_FILENAME = './calibration/p2.pickle'
SCREEN = 1
FULLSCREEN = True

VR_WALL_VISIBLE = True
VR_WALL_X_OFFSET = .0

CLIFF_FILENAME = './assets/viscliff3.obj'
CLIFF_SIDE = 'R' # L or R

CIRCLE_SCALE = .07
POSITION_L = .225, -0.143, -.05
POSITION_R = -.205, -.14, .015
VR_OBJECTS_FILENAME = './assets/Eng_AllObjs1.obj'  #rc.resources.obj_primitives
VR_OBJECT_VISIBLE = True
VR_OBJECT_NAMES = ['Monkey']
VR_OBJECT_NAME = 'Monkey'
VR_OBJECT_SCALE = .01
VR_OBJECT_SIDE = 'R'