# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
import numpy as np

def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    #
    # YOUR IMPLEMENTATION GOES HERE
    #

    # STEP 1: load up all the sentence and training vocab
    lines = []
    with open('training1.txt') as f:
        lines = f.readlines()

    count = 0
    for line in lines:
        count += 1
        print(f'line {count}: {line}')  
    # STEP 2: create a probability table of all adjacent vocabulary based on the training files

    # STEP 3: develop a trellis forward pass algorithm for the nodes and path

    # STEP 4: develop a backtracking algorithm which determines the tag of each word/punctuation

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