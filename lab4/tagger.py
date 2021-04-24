# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
import numpy as np
import time

def transitions(t2, t1, train_set):
    tags = []
    for pair in train_set:
        tags.append(pair[1])
    
    count_t1 = 0
    for t in tags:
        if t == t1:
            count_t1 += 1
    count_t2_t1 = 0
  
    for index in range(len(tags)-1):
        if tags[index]==t1 and tags[index+1] == t2:
            count_t2_t1 += 1
    return (count_t2_t1, count_t1)

def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    #
    # YOUR IMPLEMENTATION GOES HERE
    #

    # STEP 1: load up all the sentence and training vocab
    pairs = []
    test = []
    start = time.time()
    # load the tagged tuples
    for training_file in training_list:
        with open(training_file) as f: 
            contents = f.read()
            contents = contents.split("\n")
            
            for i in contents:
                if i != '':
                    pairs.append(i.split(" : "))
    
    with open(test_file) as f: 
        contents = f.read()
        contents = contents.split("\n")
        
        for i in contents:
            if i != '':
                test.append(i.split(" : "))

    # STEP 2: create a probability (emission, and transition) tables
    print("===============================================================")
    # obtain the total possible tags in the training set
    tags = []
    words = []
    for tuplee in pairs:

        tag = tuplee[1]
        word = tuplee[0]
        if tag not in tags: 
            tags.append(tag)
        if word not in words: 
            words.append(word)

    emissions = {}
    for word in words:
        for tag in tags:
            pair = (word, tag)
            emissions[pair] = 0
            # print(pair)
            # print(emissions[pair]) 

    # keep a tally of occurances
    count = 0
    for pair in pairs: 
        nonList = (pair[0], pair[1])
        emissions[nonList] += 1
        count += 1

    totals = {}
    for tag in tags:
        totals[tag] = 0
    for pair in pairs: 
        totals[pair[1]] += 1
    
    # ---- create emission probabilities ----
    for tag in tags:
        for word in words:
            tuplee = (word, tag)
            emissions[tuplee] = emissions[tuplee] / totals[tag]

    # ---- create transition probabilities ---- 
    tags_matrix = {}
    for _, t1 in enumerate(list(tags)):
        for _, t2 in enumerate(list(tags)):
            # print("t1={}, t2={}".format(x1, x2))
            # print("trans={} total={}".format(transitions(t2, t1, pairs)[0],transitions(t2, t1, pairs)[1]))
            tags_matrix[(t1, t2)] = transitions(t2, t1, pairs)[0]/transitions(t2, t1, pairs)[1] # gets the probability of getting x2 after x1
   
    # print(tags_matrix)
    # STEP 3: develop a trellis forward pass algorithm for the nodes and path
    word_seq = []
    state = []
    tagged = []

    for word in test:
        word_seq.append(word[0])
   
    for key, word in enumerate(word_seq):
        # print("{} {}".format(key,word))
        p = [] # will store the probabilities of each tag
        for tag in tags:
            if key == 0:
                tran_p = 1 # no transition to the first word
            else: 
                tran_p = tags_matrix[(state[key - 1], tag)] # otherwise, from prev max state to current state (tag)
            
            if (word,tag) in emissions.keys():
                emit_p = emissions[(word, tag)]
            else: 
                emit_p = 1

            state_p = emit_p * tran_p
            p.append(state_p)

        max_p = max(p) # find the probability that gives the max value
        max_state = tags[p.index(max_p)] # find the tag that contains this probability
        state.append(max_state) # remember this max state
    
    end = time.time()
    # STEP 4: develop a backtracking algorithm which goes back, and restores all the labels
    fileOut = open(output_file, 'w')
    for key, word in enumerate(word_seq):
        s = word + " : " + state[key] + "\n"
        fileOut.write(s)
        tagged.append((word, state[key]))

    print("time taken (s):", (end - start))
    matches = 0
    # total = len(pairs)

    # for key, pair in enumerate(pairs):
    #     print("{} vs {}".format(pair[1], state[key]))
    #     if pair[1] == state[key]:
    #         matches += 1

    # acc = matches / total
    # print("accuracy: ", acc * 100)
if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    print("Training files: " + str(training_list))
    print("Test file: " + test_file)
    print("Ouptut file: " + output_file)

    # Start the training and tagging operation.
    tag (training_list, test_file, output_file)