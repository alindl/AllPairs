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

    string_to_list = {}

    with open(args.input_file,'r') as input_file:
        full_file = input_file.readlines()
        reading_time = time.process_time()
        stuff = 0
        # I implemented as array with tuple and integer
        max_number = 5000  #determine while reading file

        # initilise array of tuples where every tuple contains a counter and a list for s
        I = [[0, []] for _ in range(max_number)]

        for line in full_file:
            # M_dict = {} # Key: candidate, Value: number of intersecting tokens found so far
            M = {}

            # text line to array
            r = [int(x) for x in line.split()]
            string_to_list[line] = r

            # length_r = |r|
            length_r = len(r)

            # lb_r = t * |r|
            lb_r = args.jaccard_threshold * length_r

            # pi_r = |r| - roof(lb_r) + 1
            pi_r = length_r - math.ceil(lb_r) + 1

            # piI_r = |r| - roof(eqo(r,r)) + 1
            piI_r = length_r - math.ceil(eqo(line,line,args.jaccard_threshold)) + 1

            for p in range(pi_r - 1):
                r_p = r[p]
                # for s in I_r[p]:
                #print(I[r_p][0])
                for pos_s in range(I[r_p][0], len(I[r_p][1])):
                    # r_p: p-th entry in r. I[r_p]: tuple in array for entry
                    # I[r_p][1]: list of arrays in index
                    # I[r_p][1][pos]: array at position pos. Actual s
                    s = I[r_p][1][pos_s]
                    # if len(s) < lb_r:
                    if len(s) < lb_r:
                        # remove index entry with s from I_r[p]
                        # Just add 1 to counter. Next lookup starts at counter
                        I[r_p][0] += 1
                    # else:
                    else:
                        # create string to add to string_to_list
                        # M indexed by s as string (list as key not possible)
                        s_str = ' '.join(str(e) for e in s)
                        # if s is not in M
                        if s_str not in M:
                            # M_dict[s] = 0
                            M[s_str] = 0
                        # M_dict[s] = M_dict[s] + 1
                        M[s_str] = M[s_str] + 1
            for p in range(piI_r - 1):
                # I_r[p] = I_r[p] o r # Add set r to index
                I[r[p]][1].append(r)

            print(len(M))
            # Verify
            # WATCH OUT: M contains s as string. Lookup in string_to_list returns
            # required list
            # res = res U  Verify(r,M,t_J)

    join_time_in_seconds = time.process_time() - reading_time
    output_size = 1
    print(output_size)
    print(join_time_in_seconds)
