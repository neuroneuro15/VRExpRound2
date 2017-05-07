import pyglet
import ratcave as rc
from pypixxlib import propixx

beamer = propixx.PROPixx()
beamer.setDlpSequencerProgram('GREY3X')

shader_gen = rc.Shader.from_file(*rc.resources.genShader)

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

shader_rescale = rc.Shader(vert=vert_shader, frag=frag_shader)


reader = rc.WavefrontReader(rc.resources.obj_primitives)
monkey = reader.get_mesh('Monkey', position=(0, 0, -1), scale = .3)
monkey.uniforms['diffuse'] = 1., 1., 1.

scene = rc.Scene(meshes=[monkey], bgColor=(0., 0., 0.))


quad_texture = rc.Texture(width=1920, height=1080)
fbo = rc.FBO(texture=quad_texture)
quad = rc.gen_fullscreen_quad('SceneQuad')
quad.texture = fbo.texture


display = pyglet.window.get_platform().get_default_display()
screen = display.get_screens()[1]
window = pyglet.window.Window(fullscreen=True, screen=screen)

fps_display = pyglet.clock.ClockDisplay()

@window.event
def on_draw():
    with fbo:
        with shader_gen:
            scene.draw()
        fps_display.draw()

    with shader_rescale:
        quad.draw()


def update(dt):
    monkey.rotation.z += 45 * dt
pyglet.clock.schedule(update)

if __name__ == '__main__':
    pyglet.app.run()
