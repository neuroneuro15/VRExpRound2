from serial import Serial
import time

arm = Serial('COM7', timeout=.2)
print('Successfully connected.')
arm.write('U')
print('Raising arm...')