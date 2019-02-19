import argparse
import math
import time
import os

# TODO figure out performance and correctness

def get_token_weight(token):
    return W[token]

def get_line_weight(line_weight_entry):
    return line_weight_entry[0]

def eqo(r,s,t):
    return ((t / (1+t))*(r + s))

# WATCH OUT: M contains the position of s in R. Lookup in R returns
# required list.
# There is no actual lookup, just a get from array, so O(1)

def verify(r_index, M, t_j):

    # res = []
    res = 0
    # Key = list as a String, value = overlap
    # for key, olap in M.items():
    for key in M.keys():
        olap = M[key]
        # Initialize ret
        ret = False
        # Get list from stored String value
        # s = R[key]
        s_index = key
        s_w = line_to_weight[s_index]

        piI_s = math.ceil(s_w - math.ceil(eqo(s_w,s_w,t_j)) + 1)
        # w_r - last token of r-prefix
        w_r = R[r_index][l_p - 1]
        # w_s - last token of s-prefix
        w_s = R[s_index][piI_s - 1]
        t = eqo(line_to_weight[r_index], line_to_weight[s_index], t_j)
        # Check which last token is larger
        # TODO pi_r + 1, olap + 1?

        if w_r < w_s:
            ret = ssjoin_verify(r_index, s_index, t, olap, l_p, olap)
        else:
            # TODO verify this change
            ret = ssjoin_verify(r_index, s_index, t, olap, l_p, piI_s)
        if ret:
            # TODO union
            # We only need an integer value and not the actual sets
            # res = r.union(s)
            # print("THERE IS A CORRECT MATCH HERE!!!!")
            res += 1
    return res


def ssjoin_verify(r_index, s_index, t, olap, p_r, p_s):

    # max_r - max potential r-overlap
    # max-s - max potential s-overlap
    max_r = line_to_weight[r_index] - p_r + olap
    max_s = line_to_weight[s_index] - p_s + olap
    r = R[r_index]
    s = R[s_index]

    while max_r >= t and max_s >= t and olap < t:
        # If there is a match, increase overlap and move to next token
        if r[p_r] == s[p_s]:
            p_r += 1
            p_s += 1
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
    parser.add_argument('weight_file', default='bms-pos.txt')
    parser.add_argument('jaccard_threshold', default=0.5, type=float)
    args = parser.parse_args()

    # required since lists cannot be dictionary keys. M defined as dictionary
    # integer -> counter.
    # Use in verify: get integer from M -> get list from R
    # -> use list normally.
    res = []
    output_size = 0
    max_number = 0
    R = []

    with open(args.input_file,'r') as input_file:
        full_file = input_file.readlines()

        # Represents the input of the full file as a list of lists
        # R[x] is the x-th line of the file
        # R[x][y] is the y-th number on the x-th line
        # Starting on 0 obviously


        # Copy each line of the full file, split it into a list(that is actually an array)
        # The emphasis is on COPY. If we have a memory problem, this is where to look at
        for line in full_file:
            r = []
            for x in line.rstrip(os.linesep).split():
                r.append(int(x))
                if int(x) > max_number:
                    max_number = int(x)
            R.append(list(r))

    # map tokens to their weight. All not specified in weight
    # file have weight 1.0
    W = [1.0 for _ in range(max_number + 1)]

    # Define line-weights array : Array of 2 element tuples mapping a line's
    # total weight to its position in R
    line_weights = []

    with open(args.weight_file,'r') as weight_file:
        full_file = weight_file.readlines()

        for line in full_file:
            split_line = line.rstrip(os.linesep).split(':')
            W[int(split_line[0])] = float(split_line[1])

    ### Compare tokens by weight. Lines are sorted descendingly by token weight
    ### + create line-weight -> linenumber mapping on the fly.
    for i in range(len(R)):
        R[i] = sorted(R[i], key=get_token_weight, reverse=True)
        weight_sum = 0
        for token in R[i]:
            weight_sum += W[token]
        line_weights.append((float(weight_sum), i))

    ### sort line-weights array ascendingly by weight in each tuple.
    line_weights = sorted(line_weights, key=get_line_weight, reverse=False)

    # Define array mapping lines in R to their total weight
    line_to_weight = [0 for _ in range(len(R))]
    for weight_line_entry in line_weights:
        line_to_weight[weight_line_entry[1]] = weight_line_entry[0]


    ### PREPROCESSING END

    reading_time = time.process_time()

    # I implemented as array in which entries are tuples containing an integer (counter)
    # and a list of integers (positions of s in R)

    # Initialize array of tuples where every tuple contains a counter and a list for s
    # The list of s is actually a list of the positions in S(=R)
    I = [[0, []] for _ in range(max_number + 1)]
    # -1 instead of 0 for the counter, to signal that it is empty
    # I = [[-1, []] for _ in range(max_number)]

    # The position of r in R
    r_index_in_R = 0

    t_in = args.jaccard_threshold

    for weight_line_entry in line_weights:
        r_index_in_R = weight_line_entry[1]
        r = R[r_index_in_R]

        # Key: candidate as position in R=S, Value: number of intersecting tokens found so far
        M = {}

        # lb_r = t * |r|
        lb_r = t_in * weight_line_entry[0]
        # l_p (page 17 in paper)
        temp_weight_sum = 0
        l_p = 0
        for position in range(len(r)):
            temp_weight_sum += W[r[position]]
            if((weight_line_entry[0] - temp_weight_sum) /
                weight_line_entry[0] < t_in):

                l_p = position + 1
                break


        # l_i (page 17 in paper)
        temp_weight_sum = 0
        l_i = 0
        for position in range(len(r)):
            temp_weight_sum += W[r[position]]
            if((weight_line_entry[0] - temp_weight_sum) /
               (weight_line_entry[0] + temp_weight_sum) < t_in):

                l_i = position + 1
                break


        for p in range(l_p):
            r_p = r[p]
            #print(str(I[r_p][0]) +"     "+ str(len(I[r_p][1])))
            for pos_s in range(I[r_p][0], len(I[r_p][1])):
                # r_p: p-th entry in r. I[r_p]: tuple in array for entry
                # I[r_p][1]: list of integers in index
                # I[r_p][1][pos]: integer at position pos. (position of s in R)
                # s_index_in_S is the index of s in R(=S)
                s_index_in_S = I[r_p][1][pos_s]
                # print(s)
                # print(len(s))
                # print(line_to_weight[s_index_in_S - 1])
                # print("\n")
                #print(line_to_weight[s_index_in_S - 1])
                if line_to_weight[s_index_in_S] < lb_r:
                    # remove index entry with s from I_r[p]
                    # Just add 1 to counter. Next lookup starts at counter
                    I[r_p][0] += 1
                # else:
                else:
                    # if s is not in M
                    if s_index_in_S not in M:
                        # M_dict[s] = 0
                        M[s_index_in_S] = 0
                    # M_dict[s] = M_dict[s] + 1
                    M[s_index_in_S] += 1

        for p in range(l_i):
            # I_r[p] = I_r[p] o r # Add set r to index
            I[r[p]][1].append(r_index_in_R)

        #print(str(c) + "####" + str(d))
        if len(M) > 0:
            # print("Length of M = " + str(len(M)))
            # res = res U  Verify(r,M,t_J)
            output_size += verify(r_index_in_R, M, t_in)

        # print("----------------- r_" + str(r_index_in_R + 1 ) + "-------------------")
        # numkey = 1
        # print("######### Contents of M ##############")
        # for key in M.keys():
        #     print("numKey = " + str(numkey))
        #     print("key = " + str(key))

        #     print("olap = " + str(M[key]))
        #     numkey += 1

        # indexEntry = 0
        # print("========= Contents of I ==============")
        # for x in I:
        #     print("indexEntry  = " + str(indexEntry))
        #     print("count = " + str(x[0]))
        #     for y in x[1]:
        #         print("Entries = " + str(y))
        #     indexEntry += 1

    join_time_in_seconds = time.process_time() - reading_time
    print(output_size)
    print(join_time_in_seconds)
