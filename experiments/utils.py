import pyglet
import ratcave as rc
from collections import namedtuple
from pypixxlib import propixx


RenderCollection = namedtuple("RenderCollection", "shader fbo quad")

# Load up Meshes and Scene
def load_projected_scene(arena_file, projector_file, arena_name='Arena'):
    arena = rc.WavefrontReader(arena_file).get_mesh(arena_name)
    arena.uniforms['diffuse'] = .8, .8, .8
    projector = rc.Camera.from_pickle(projector_file)
    print(projector.projection.fov_y)
    projector.projection.aspect = 1.77
    print(projector.projection.aspect)
    scene = rc.Scene(meshes=[arena], camera=projector, bgColor=(.6, 0, 0))
    scene.light.position.xyz = projector.position.xyz
    return scene, arena


def setup_window(screen=1, fullscreen=True):
    """Return a pyglet Window on the screen desired."""
    display = pyglet.window.get_platform().get_default_display()
    screen = display.get_screens()[screen]
    window = pyglet.window.Window(fullscreen=fullscreen, screen=screen, vsync=False)
    return window


def setup_cube_fbo(width=4096):
    """Return a ratcave FBO instance, pre-loaded with a TextureCube of length 'width'."""
    return rc.FBO(texture=rc.TextureCube(width=4096, height=4096))


def get_arena_with_rigidbody(arena_objfilename, motive_client, flat_shading=False):
    arena = rc.WavefrontReader(arena_objfilename).get_mesh('Arena')
    arena.uniforms['diffuse'] = 1., 1, 1
    arena.rotation = arena.rotation.to_quaternion()
    arena_rb = motive.rigid_bodies['Arena']

    print('Original Arena Position: ', arena.position)
    arena.position.xyz = arena_rb.position
    arena.rotation.xyz = arena_rb.rotation
    arena.uniforms['flat_shading'] = False

def setup_deferred_rendering():
    """Return (Shader, FBO, QuadMesh) for deferred rendering."""
    fbo = rc.FBO(rc.Texture(width=4096, height=4096, mipmap=True))
    quad = rc.gen_fullscreen_quad("DeferredQuad")
    quad.texture = fbo.texture
    shader = rc.Shader.from_file(*rc.resources.deferredShader)
    return RenderCollection(shader=shader, fbo=fbo, quad=quad)


def setup_grey3x_rendering(update_projector=False):
    """
    Return (Shader, FBO, QuadMesh) for rendering in Propixx's 'GREY3X' mode. If desired, can
    also apply the settings to the beamer to set it to this mode (caution: won't change back afterward).
    """

    if update_projector:
        beamer = propixx.PROPixx()
        beamer.setDlpSequencerProgram('GREY3X')

    vert_shader = open(rc.resources.deferredShader.vert).read()
    frag_shader = """
    #version 400
    #extension GL_ARB_texture_rectangle : enable

    uniform sampler2D TextureMap;

    in vec2 texCoord;
    out vec3 color;

    void main( void ) {

        if (gl_FragCoord.x * 3 + 1 < 1920){
            color = vec3(texture2D(TextureMap, vec2(floor(gl_FragCoord.x * 3. + 0.0) / 1920.0, gl_FragCoord.y / 1080.0)).r,
                         texture2D(TextureMap, vec2(floor(gl_FragCoord.x * 3. + 1.0) / 1920.0, gl_FragCoord.y / 1080.0)).r,
                         texture2D(TextureMap, vec2(floor(gl_FragCoord.x * 3. + 2.0) / 1920.0, gl_FragCoord.y / 1080.0)).r
                         );

        } else {
            color = vec3(.2, 0., 0.);
        }
        return;
    }
    """

    shader = rc.Shader(vert=vert_shader, frag=frag_shader)
    quad = rc.gen_fullscreen_quad('Grey3xQuad')
    return RenderCollection(shader=shader, fbo=None, quad=quad)



