from serial import Serial
import time

arm = Serial('COM7', timeout=.5)
print('Successfully connected.')
arm.write(b'U')
print('Raising arm...')

time.sleep(1.)