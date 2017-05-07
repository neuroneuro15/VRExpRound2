import itertools as it

experiments = ['cliff', 'wall', 'object_exploration']
rats = ['Test'] + ['VR-{}{}'.format(cage, num) for cage, num in it.product(range(1, 6), 'AB')]
