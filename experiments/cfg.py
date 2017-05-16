RAT = ['Demo', 'Test', 'VR-1A', 'VR-1B', 'VR-2A', 'VR-2B', 'VR-3A', 'VR-3B', 'VR-4A', 'VR-4B', 'VR-5A', 'VR-5B']
EXPERIMENTER = ['Nicholas A. Del Grosso', 'Eduardo Blanco-Hernandez']
# General settings
ARENA_FILENAME = './assets/arena3uv.obj'
ARENA_LIGHTING_DIFFUSE = 1., 1., 1.
ARENA_LIGHTING_SPECULAR = 0., 0., 0.
ARENA_LIGHTING_TEXTURE = './assets/uvgrid_bw.png'
ARENA_LIGHTING_FLAT_SHADING = True
PROJECTOR_FILENAME = './calibration/p2.pickle'
SCREEN = 1
FULLSCREEN = True
MOUSE_CURSOR_VISIBLE = False
PAPER_LOG_CODE = ''

# Cliff experiment settings
CLIFF_FILENAME = './assets/viscliff3b.obj'
CLIFF_TYPE = 'VR'  # Real, or VR, or Static
CLIFF_SIDE = 'R' # L or R
CLIFF_OBJECT_L = 'virArena'
CLIFF_OBJECT_R = 'virArena2'
CLIFF_OBJECT_REAL = 'RealArena'

# Wall experiment settings
VR_WALL_EXPERIMENT_NAME = 'VRWallExp'
VR_WALL_VISIBLE = True
VR_WALL_X_OFFSET = [-.3, -.1, .1, .3]
VR_WALL_Y_OFFSET = .28
VR_WALL_SCALE = .6
VR_WALL_Y_ROTATION = 98.
VR_WALL_LIGHTING_DIFFUSE = 1., 1., 1.
VR_WALL_LIGHTING_SPECULAR = 0., 0., 0.
VR_WALL_LIGHTING_AMBIENT = 0., 0., 0.  #1., 1., 1.
VR_WALL_LIGHTING_TEXTURE = ARENA_LIGHTING_TEXTURE
VR_WALL_LIGHTING_FLAT_SHADING = True
VR_WALL_PHASE_1_DURATION_SECS = 60.
VR_WALL_PHASE_2_DURATION_SECS = 240.
VR_WALL_PHASE_3_DURATION_SECS = 240.
VR_WALL_PHASE_4_DURATION_SECS = 240.

# Object experiment settings
VR_OBJECT_EXPERIMENT_NAME = 'VRObjectExp'
VR_OBJECT_TYPE = ['VR', 'Real']
VR_OBJECT_POSITION_L = .230, -0.133, -.06
VR_OBJECT_POSITION_R = -.195, -.13, .015#-.205, -.14, .015
VR_OBJECT_FILENAME = './assets/Eng_AllObjs1.obj'
VR_OBJECT_NAME = ['Snake', 'Torus', 'Monkey', 'Masher', 'Moon', 'Pyramid', 'Mine']
VR_OBJECT_SCALE = .01
VR_OBJECT_SIDE = ['L', 'R']
VR_OBJECT_LIGHTING_DIFFUSE = (.85,) * 3
VR_OBJECT_LIGHTING_SPECULAR = (1.0,) * 3  #ARENA_LIGHTING_SPECULAR
VR_OBJECT_LIGHTING_SPEC_WEIGHT = 50.
VR_OBJECT_LIGHTING_AMBIENT = 0.3, 0.3, 0.3# 1., 1., 1.
VR_OBJECT_LIGHTING_FLAT_SHADING = False
VR_OBJECT_LIGHTING_TEXTURE = None
VR_OBJECT_VRARENA_LIGHTING_DIFFUSE = (.7,) * 3
VR_OBJECT_PHASE_1_DURATION_SECS = VR_WALL_PHASE_1_DURATION_SECS
VR_OBJECT_PHASE_2_DURATION_SECS = VR_WALL_PHASE_2_DURATION_SECS
VR_OBJECT_PHASE_3_DURATION_SECS = VR_WALL_PHASE_3_DURATION_SECS
VR_OBJECT_PHASE_4_DURATION_SECS = VR_WALL_PHASE_4_DURATION_SECS
VR_OBJECT_ROBO_ARM_WAIT_DURATION_SECS = 4.
VR_OBJECT_ARDUINO_PORT = 'COM7'
VR_OBJECT_ROBO_COMMAND_UP = b'U'
VR_OBJECT_ROBO_COMMAND_DOWN = b'D'