import time
from serial import Serial


arm = Serial('COM7', timeout=.2)
print('Successfully connected.')
arm.write(b'D')
print('Lowering Arm...')

time.sleep(6.)