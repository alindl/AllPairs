import argparse
import time

parser = argparse.ArgumentParser(description='Get filename and threshold input.')
parser.add_argument('input_file', default='bms-pos.txt')
parser.add_argument('jaccard_threshold', default=0.5, type=float)
args = parser.parse_args()

with open(args.input_file) as input_file:  
    full_file = input_file.read()
    reading_time = time.process_time()
    sum_results = 0
    # I implemented as array with tuple and integer
    for line in full_file:
        M_dict = {} # Key: candidate, Value: number of intersecting tokens found so far
        sum_results += 1 
        
    

        # Verify

# print(args.input_file)
# print(args.jaccard_threshold)



join_time_in_seconds = time.process_time() - reading_time
output_size = 1
print(sum_results)
print(join_time_in_seconds)

