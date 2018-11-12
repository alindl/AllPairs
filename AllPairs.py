import argparse
import math
import time
import os

def eqo(r,s,t):
    return ((t /(1+t))*(len(r) + len(s)))

# WATCH OUT: M contains s as string. Lookup in string_to_list returns
# required list
# We don't do that, just look up s in R(=S)
# There is no actual lookup, just a get from array, so O(1)
def verify(r, M, t_j):

    # res = []
    res = 0
    # Key = list as a String, value = overlap
    for key, olap in M.items():
        # Initialize ret
        ret = None
        # Get list from stored String value
        s = string_to_list.get(key)
        # Or don't
        s = R[key]
        pi_s = len(s) - math.ceil(lb_r) + 1
        # w_r - last token of r-prefix
        w_r = r[pi_r - 1]
        # w_s - last token of s-prefix
        w_s = s[pi_s - 1]
        t = eqo(r, s, t_j)
        # Check which last token is larger
        # TODO pi_r + 1, olap + 1?
        # NO, we don't need + 1 because 0 indexing (I think)
        # He said something like that, but I didn't wrote down a note that proofs that :(
        if w_r < w_s:
            ret = ssjoin_verify(r, s, t, olap, pi_r + 1, olap + 1)
        else:
            ret = ssjoin_verify(r, s, t, olap, olap + 1, pi_s + 1)
        if ret:
            # TODO union
            # We only need an integer value and not the actual sets
            # res = r.union(s)
            res += 1
    return res


def ssjoin_verify(r, s, t, olap, p_r, p_s):

    # max_r - max potential r-overlap
    # max-s - max potential s-overlap
    max_r = len(r) - p_r + olap
    max_s = len(s) - p_s + olap

    while max_r >= t and max_s >= t and olap < t:
        # If there is a match, increase overlap and move to next token
        if r[p_r] == s[p_s]:
            r += 1
            s += 1
            olap += 1
        # Decrease max possible overlap for r, go to next r-token
        elif r[p_r] < s[p_s]:
            p_r += 1
            max_r -= 1
        # Decrease max possible overlap for s, go to next s-token
        else:
            p_s += 1
            max_s -= 1
    return olap >= t


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get filename and threshold input.')
    parser.add_argument('input_file', default='bms-pos.txt')
    parser.add_argument('jaccard_threshold', default=0.5, type=float)
    args = parser.parse_args()

    # required since lists cannot be dictionary keys. M defined as dictionary
    # string -> counter.
    # string_to_list maps the Strings to lists.
    # Use in verify: get String from M -> get list from string_to_list
    # -> use list normally.
    string_to_list = {}
    res = []
    output_size = 0

    with open(args.input_file,'r') as input_file:
        full_file = input_file.readlines()

        # Represents the input of the full file as a list of lists
        # R[x] is the x-th line of the file
        # R[x][y] is the y-th number on the x-th line
        # Starting on 0 obviously
        R = []        

        max_number = 0

        # Copy each line of the full file, split it into a list(that is actually an array)
        # The emphasis is on COPY. If we have a memory problem, this is where to look at
        for line in full_file:
            r = []
            for x in line.rstrip(os.linesep).split():
                r.append(int(x))
                if int(x) > max_number:
                    max_number = int(x)
            R.append(list(r))

        reading_time = time.process_time()

        # I implemented as array with tuple and integer
        # max_number = 5000  #determine while reading file

        # Initialize array of tuples where every tuple contains a counter and a list for s
        # The list of s is actually a list of the positions in S(=R)
        I = [[0, []] for _ in range(max_number)]
        # -1 instead of 0 for the counter, to signal that it is empty
        # I = [[-1, []] for _ in range(max_number)]

        # The position of r in R
        r_index_in_R = 0

        for r in R:

            # Key: candidate as position in R=S, Value: number of intersecting tokens found so far
            M = {}

            # text line to array
            # TODO: read before algorithm starts
            # r = [int(x) for x in line.rstrip(os.linesep).split()]
            
            # string_to_list[line] = r

            # length_r = |r|
            length_r = len(r)

            # lb_r = t * |r|
            lb_r = args.jaccard_threshold * length_r

            # pi_r = |r| - roof(lb_r) + 1
            pi_r = length_r - math.ceil(lb_r) + 1

            # piI_r = |r| - roof(eqo(r,r)) + 1
            piI_r = length_r - math.ceil(eqo(r,r,args.jaccard_threshold)) + 1

            for p in range(pi_r - 1):
                r_p = r[p]
                # for s in I_r[p]:
                for pos_s in range(I[r_p][0], len(I[r_p][1])):
                    # r_p: p-th entry in r. I[r_p]: tuple in array for entry
                    # I[r_p][1]: list of arrays in index
                    # I[r_p][1][pos]: array at position pos. Actual s
                    # s = I[r_p][1][pos_s]
                    s = R[I[r_p][1][pos_s]]
                    # s_index_in_S is the index of s in R(=S)
                    s_index_in_S = I[r_p][1][pos_s]
                    # if len(s) < lb_r:
                    if len(s) < lb_r:
                        # remove index entry with s from I_r[p]
                        # Just add 1 to counter. Next lookup starts at counter
                        I[r_p][0] += 1
                    # else:
                    else:
                        # create string to add to string_to_list
                        # M indexed by s as string (list as key not possible)
                        # s_str = ' '.join(str(e) for e in s)
                        # if s is not in M
                        # if s_str not in M:
                        if s_index_in_S not in M:
                            # M_dict[s] = 0
                            M[s_index_in_S] = 0
                        # M_dict[s] = M_dict[s] + 1
                        M[s_index_in_S] += M[s_index_in_S]
            for p in range(piI_r - 1):
                # I_r[p] = I_r[p] o r # Add set r to index
                I[r[p]][1].append(r_index_in_R)
                if I[r_p][0] is -1:
                    I[r_p][0] = 0



            if len(M) > 0:
                # res = res U  Verify(r,M,t_J)
                output_size += verify(r, M, args.jaccard_threshold)

        r_index_in_R += 1

    join_time_in_seconds = time.process_time() - reading_time
    print(output_size)
    print(join_time_in_seconds)
