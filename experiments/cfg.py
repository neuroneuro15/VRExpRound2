RAT = ['Demo', 'Test', 'VR-1A', 'VR-1B', 'VR-2A', 'VR-2B', 'VR-3A', 'VR-3B', 'VR-4A', 'VR-4B', 'VR-5A', 'VR-5B']
EXPERIMENTER = ['Eduardo Blanco-Hernandez', 'Nicholas A. Del Grosso']
# General settings
ARENA_FILENAME = './assets/arena3uv2.obj'
ARENA_LIGHTING_DIFFUSE = 1., 1., 1.
ARENA_LIGHTING_SPECULAR = 0., 0., 0.
ARENA_LIGHTING_TEXTURE = './assets/uvgrid_bw2.png'
ARENA_LIGHTING_FLAT_SHADING = True
PROJECTOR_FILENAME = './calibration/p2.pickle'
SCREEN = 1
FULLSCREEN = True
ANTIALIASING = True
MOUSE_CURSOR_VISIBLE = False
PAPER_LOG_CODE = ''
FIRST_PERSON_MODE = False
PROJECTOR_TURNED_ON = True
PROJECTOR_LED_ON = True


# Cliff experiment settings
CLIFF_EXPERIMENT_NAME = 'VRCliffExp'
CLIFF_FILENAME = './assets/viscliff4.obj'
CLIFF_VRARENA_LIGHTING_TEXTURE = './assets/uvgrid_bw2_cliffvers.png'
CLIFF_REALARENA_LIGHTING_TEXTURE = './assets/uvgrid_bw2_cliffvers_recolored.png'
CLIFF_REALARENA_LIGHTING_DIFFUSE = (1.5,) * 3
CLIFF_TYPE = ['VR', 'Static', 'Real']
CLIFF_SIDE = ['L', 'R']
CLIFF_OBJECT_L = 'virArena'
CLIFF_OBJECT_R = 'virArena2'
CLIFF_OBJECT_REAL = 'RealArena'
CLIFF_PROJECTOR_LED_INTENSITY = "12.5"  # Requires exact string: "100.0", "50.0", "25.0", "12.5", "6.25"
CLIFF_COVER_RAT_WITH_UMBRELLA = True
CLIFF_UMBRELLA_SCALE = .03
CLIFF_SHOW_BOARD = True

# Wall experiment settings
VR_WALL_EXPERIMENT_NAME = 'VRWallExp'
VR_WALL_FILENAME = './assets/vr_wall.obj'
VR_WALL_MESHNAME = 'VR_Wall'
VR_WALL_VISIBLE = True
VR_WALL_X_OFFSET = [-.3, -.1, .1, .3]
VR_WALL_Y_OFFSET = 0.067
VR_WALL_LIGHTING_DIFFUSE = 1., 1., 1.
VR_WALL_LIGHTING_SPECULAR = 0., 0., 0.
VR_WALL_LIGHTING_AMBIENT = 0., 0., 0.  #1., 1., 1.
VR_WALL_LIGHTING_TEXTURE = ARENA_LIGHTING_TEXTURE
VR_WALL_LIGHTING_FLAT_SHADING = True
VR_WALL_PHASE_1_DURATION_SECS = 90.
VR_WALL_PHASE_2_DURATION_SECS = 240.
VR_WALL_PHASE_3_DURATION_SECS = 240.
VR_WALL_PHASE_4_DURATION_SECS = 240.
VR_WALL_PROJECTOR_LED_INTENSITY = "6.25"  # Requires exact string: "100.0", "50.0", "25.0", "12.5", "6.25"
VR_WALL_FADE_SPEED = 0.125

# Object experiment settings
VR_OBJECT_EXPERIMENT_NAME = 'VRObjectExp'
VR_OBJECT_TYPE = ['VR', 'Real']
VR_OBJECT_POSITION_R = .225, -0.133, -.05
VR_OBJECT_POSITION_L = -.20, -.13, .015#-.205, -.14, .015
VR_OBJECT_Y_OFFSET = .0
VR_OBJECT_FILENAME = './assets/Eng_AllObjs1.obj'
VR_OBJECT_NAME = ['Snake', 'Torus', 'Monkey', 'Masher', 'Moon', 'Pyramid', 'Mine']
VR_OBJECT_SCALE = .01
VR_OBJECT_SIDE = ['L', 'R']
VR_OBJECT_LIGHTING_DIFFUSE = (.85,) * 3
VR_OBJECT_LIGHTING_SPECULAR = (1.0,) * 3  #ARENA_LIGHTING_SPECULAR
VR_OBJECT_LIGHTING_SPEC_WEIGHT = 50.
VR_OBJECT_LIGHTING_AMBIENT = 0.5, 0.5, 0.5# 1., 1., 1.
VR_OBJECT_LIGHTING_FLAT_SHADING = False
VR_OBJECT_LIGHTING_TEXTURE = None
VR_OBJECT_VRARENA_LIGHTING_DIFFUSE = (.7,) * 3
VR_OBJECT_CIRCLE_SCALE = .05
VR_OBJECT_CIRCLE_Y_OFFSET = -.08
VR_OBJECT_PHASE_1_DURATION_SECS = VR_WALL_PHASE_1_DURATION_SECS
VR_OBJECT_PHASE_2_DURATION_SECS = VR_WALL_PHASE_2_DURATION_SECS
VR_OBJECT_PHASE_3_DURATION_SECS = VR_WALL_PHASE_3_DURATION_SECS
VR_OBJECT_PHASE_4_DURATION_SECS = VR_WALL_PHASE_4_DURATION_SECS
VR_OBJECT_ROBO_ARM_WAIT_DURATION_SECS = 4.
VR_OBJECT_ARDUINO_PORT = 'COM7'
VR_OBJECT_ROBO_COMMAND_UP = b'U'
VR_OBJECT_ROBO_COMMAND_DOWN = b'D'
VR_OBJECT_PROJECTOR_LED_INTENSITY = "12.5"  # Requires exact string: "100.0", "50.0", "25.0", "12.5", "6.25"
VR_OBJECT_FADE_SPEED = VR_WALL_FADE_SPEED

# Spatial novelty experiment settings
VR_SPATIAL_NOVELTY_EXPERIMENT_NAME = 'VRSpatNovelExp_BlackBackg'
VR_SPATIAL_NOVELTY_OBJECT_NAME = ['Snake', 'Torus', 'Monkey', 'Masher', 'Moon', 'Pyramid', 'Mine']
VR_SPATIAL_NOVELTY_FAMILIAR_POSITION = [1, 2, 3, 4]
VR_SPATIAL_NOVELTY_NOVEL_POSITION = [1, 2, 3, 4]
VR_SPATIAL_NOVELTY_FIXED_POSITION = [1, 2, 3]
VR_SPATIAL_NOVELTY_OBJECT_TYPE = ['Real', '3D']
VR_SPATIAL_NOVELTY_PROJECTOR_LED_INTENSITY = "6.25"  # Requires exact string: "100.0", "50.0", "25.0", "12.5", "6.25"
VR_SPATIAL_NOVELTY_LIGHTING_DIFFUSE = (.1,) * 3
VR_SPATIAL_NOVELTY_OBJECT_FILENAME = VR_OBJECT_FILENAME
VR_SPATIAL_NOVELTY_OBJECT_SCALE = .008
VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_DIFFUSE = (0.7, 0.7, 0.7)
VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_SPECULAR = (0., 0., 0.)
VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_SPEC_WEIGHT = 1.
VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_AMBIENT = (1.5,) * 3
VR_SPATIAL_NOVELTY_LIGHTING_OBJECT_FLAT_SHADING = False
VR_SPATIAL_NOVELTY_PHASE_1_DURATION_SECS = 240.
VR_SPATIAL_NOVELTY_PHASE_2_DURATION_SECS = 180.
VR_SPATIAL_NOVELTY_PHASE_3_DURATION_SECS = 60.
VR_SPATIAL_NOVELTY_PHASE_4_DURATION_SECS = 180.
VR_SPATIAL_NOVELTY_FADE_SPEED = 0.125 #VR_OBJECT_FADE_SPEED
VR_SPATIAL_NOVELTY_OBJECT_POSITIONS = [(.32, -.155, .001), (.295, -.155, -.11), (-.29, -.155, .085), (-.300, -.155, -.019),]
VR_SPATIAL_FIXED_OBJECT_POSITIONS =  [(.09, -.155, -.025),(.008, -.155, -.01), (-.08, -.155, .00)]
VR_SPATIAL_CAMERA_Z_NEAR = .025
VR_SPATIAL_CIRCLE_SCALE = .05
VR_SPATIAL_CIRCLE_Y_OFFSET = -.05
VR_SPATIAL_COVER_RAT_WITH_UMBRELLA = True
VR_SPATIAL_UMBRELLA_SCALE = VR_SPATIAL_CAMERA_Z_NEAR




# Visual acuity experiment settings
VR_ACUITY_EXPERIMENT_NAME = 'VRAcuityExp'
VR_ACUITY_PROJECTOR_LED_INTENSITY = "12.5"  # Requires exact string: "100.0", "50.0", "25.0", "12.5", "6.25"
VR_ACUITY_LIGHTING_DIFFUSE =(300., 300., 300.)# VR_WALL_LIGHTING_DIFFUSE
VR_ACUITY_LIGHTING_SPECULAR = (0., 0., 0.)
VR_ACUITY_LIGHTING_SPEC_WEIGHT = 1.
VR_ACUITY_LIGHTING_AMBIENT = VR_WALL_LIGHTING_AMBIENT
VR_ACUITY_LIGHTING_FLAT_SHADING = True #VR_WALL_LIGHTING_FLAT_SHADING
VR_ACUITY_CYLINDER_POSITION = 0., 0., 0.
VR_ACUITY_PHASE_DURATION_SECS = 30.
VR_ACUITY_CYLINDER_TEXTURE = './assets/uvgrid_bw.png'
VR_ACUITY_CYLINDER_SPEEDS = 0., 7., 14., 28.
VR_ACUITY_ISI_DURATION_SECS = 10.
