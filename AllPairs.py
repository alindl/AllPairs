import argparse
import time

parser = argparse.ArgumentParser(description='Get filename and threshold input.')
parser.add_argument('input_file', default='bms-pos.txt')
parser.add_argument('jaccard_threshold', default=0.5, type=float)
args = parser.parse_args()

# print(args.input_file)
# print(args.jaccard_threshold)




sum_results = 1
print(sum_results)
print(time.process_time())
