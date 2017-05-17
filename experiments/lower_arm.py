from serial import Serial

arm = Serial('COM7', timeout=.2)
print('Successfully connected.')
arm.write('D')
print('Lowering Arm...')