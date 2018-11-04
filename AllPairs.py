import argparse
import math
import time

def eqo(r,s,t):
    return ((t /(1+t))*(len(r.split()) + len(s.split())))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get filename and threshold input.')
    parser.add_argument('input_file', default='bms-pos.txt')
    parser.add_argument('jaccard_threshold', default=0.5, type=float)
    args = parser.parse_args()

    with open(args.input_file,'r') as input_file:  
        full_file = input_file.readlines()
        reading_time = time.process_time()
        stuff = 0
        # I implemented as array with tuple and integer
        for line in full_file:
            # M_dict = {} # Key: candidate, Value: number of intersecting tokens found so far
            # length_r = |r|
            length_r = len(line.split())

            # lb_r = t * |r|
            lb_r = args.jaccard_threshold * length_r

            # pi_r = |r| - roof(lb_r) + 1
            pi_r = length_r - math.ceil(lb_r) + 1 

            # piI_r = |r| - roof(eqo(r,r)) + 1
            piI_r = length_r - math.ceil(eqo(line,line,args.jaccard_threshold)) + 1

            for p in range(pi_r - 1):
                stuff += 1
                # for s in I_r[p]:
                    # if len(s) < lb_r:
                        # remove index entry with s from I_r[p]
                    # else:
                        # if s is not in M 
                            # M_dict[s] = 0
                        # M_dict[s] = M_dict[s] + 1
            for p in range(piI_r - 1):
                # I_r[p] = I_r[p] o r # Add set r to index
                stuff += 1 

        
            # Verify
            # res = res U  Verify(r,M,t_J)

    join_time_in_seconds = time.process_time() - reading_time
    output_size = 1
    print(output_size)
    print(join_time_in_seconds)

