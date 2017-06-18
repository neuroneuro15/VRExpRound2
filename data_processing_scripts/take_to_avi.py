import argparse
from motivebatch import Take

# Get Script Inputs
parser = argparse.ArgumentParser(description='Convert Motive Take File to CSV Format.')
parser.add_argument('i', type=str, help='Take Filename')
parser.add_argument('o', type=str, help='CSV Filename')

args = parser.parse_args()


take = Take(args.i)
take.to_avi(args.o)