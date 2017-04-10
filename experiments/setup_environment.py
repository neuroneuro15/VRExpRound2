import sys
from datetime import datetime

# Load Config file
import yaml
with open('config.yaml') as cfgfile:
    cfg  = yaml.load(cfgfile)


# Turn off OpenGL debugging, to speed up program
import pyglet
pyglet.options['debug_gl'] = cfg['opengl']['debug_mode']
pyglet.options['debug_gl_trace'] = cfg['opengl']['debug_mode']

# Confirm beamer has correct settings
from pypixxlib import propixx
beamer = propixx.PROPixx()
beamer.setSleepMode(False)  # Turns on beamer (just in case)
#beamer.setCeilingMountMode(True)
#beamer.setRearProjectionMode(True)
#beamer.setLedIntensity('100.0')
beamer.setDlpSequencerProgram(cfg['beamer']['sequence'])

# Confirm that Motive is broadcasting network data
import socket
import natnetclient
try:
    motive_client =  natnetclient.NatClient(client_ip=cfg['motive']['ip'],
                                        data_port=cfg['motive']['dataport'],
                                        comm_port=cfg['motive']['commport'])
except socket.error:
    err_msg = """
    Motive not broadcasting data.
    To fix, Make sure 'Broadcast Frame Data' is turned on under the 'Data Streaming' pane in the Motive GUI.
    Client IP Address: {ip}
    Data Port: {dport}
    Comm Port: {cport}
    """.format(ip=cfg['motive']['ip'], dport=cfg['motive']['dataport'], cport=cfg['motive']['commport'])
    raise IOError(err_msg)



# Startup Experiment Selector and have it select which options they want
from psychopy import gui
options = {'Experiment': cfg['experiments'],
           'Rat': cfg['rats'],
           }
dialogue = gui.DlgFromDict(options, title='Select Experiment and Rat')

if dialogue.OK:
    print(options)
else:
    print('User Cancelled. Exiting...')
    sys.exit()


# Lookup which conditions and parameters are needed for the next
import sqlite3
con = sqlite3.connect('vr_sessions.sqlite3')
cursor = con.cursor()
cursor.execute("INSERT INTO sessions VALUES (?, ?)", [options['Experiment'], options['Rat']])
con.commit()
sessions = cursor.execute('SELECT * FROM sessions WHERE rat == ? AND experiment == ?',
                          [options['Rat'], options['Experiment']]).fetchall()


# Present the User with Suggested Conditions for the Experiment, so they set up the recording setup.
expDlg = gui.Dlg(title="Experiment Conditions: Suggested Parameters")
expDlg.addField(label='Experiment', initial=options['Experiment'], enabled=False)
expDlg.addField(label='Rat', initial=options['Rat'], enabled=False)

now = datetime.now()
expDlg.addField('Time', now.date().strftime('%d-%m-%Y'))
expDlg.addField('Date', now.time().strftime('%H:%M'))
if options['Experiment'] == 'Visual Cliff':
    expDlg.addField('Cliff Type', choices=cfg['viscliff']['conditions'], enabled=True)
    expDlg.addField('Cliff Side', choices=cfg['viscliff']['cliffsides'], enabled=True)
if options['Experiment'] == 'Object Exploration':
    expDlg.addField('Object Type', choices=cfg['objexp']['conditions'], enabled=True)
    expDlg.addField('Object Side', choices=cfg['objexp']['objsides'], enabled=True)
if options['Experiment'] == 'Wall Exploration':
    expDlg.addField('Wall Position', choices=cfg['wallexp']['wallpositions'], enabled=True)
expDlg.show()


# Start The Selected Experiment, passigng the selected parameters to that experiment script
sys.exit()

