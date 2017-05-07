# Turn off OpenGL debugging (should be very first thing you do), to speed up program
import pyglet
pyglet.options['debug_gl'] = False
pyglet.options['debug_gl_trace'] = False


# Confirm beamer has correct settings
from pypixxlib import propixx
beamer = propixx.PROPixx()
beamer.setSleepMode(False)  # Turns on beamer (just in case)
#beamer.setCeilingMountMode(True)
#beamer.setRearProjectionMode(True)
#beamer.setLedIntensity('100.0')
beamer.setDlpSequencerProgram('RGB')#cfg['beamer']['sequence'])

# Confirm that Motive is broadcasting network data
import socket
import natnetclient
try:
    motive =  natnetclient.NatClient()
except socket.error:
    err_msg = """
    Motive not broadcasting data.
    To fix, Make sure 'Broadcast Frame Data' is turned on under the 'Data Streaming' pane in the Motive GUI.
    Client IP Address: {ip}
    Command Port: {cport}
    Data Port: {dport}

    """.format(ip='localloop', dport=1511, cport=1510)
    raise IOError(err_msg)

if not motive.rigid_bodies:
    raise IOError("Not Detecting Rigid Bodies.  Turn RigidBody Streaming On in the Motive Streaming Pane.")

if not motive.rigid_bodies['Arena'].position:
    raise IOError("Not Detecitng Arena Position.  Turn RigidBody Streaming on in the Motive Streaming Pane.")


print('Everything is working!  Have fun!')