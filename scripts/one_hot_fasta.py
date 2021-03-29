#! /usr/bin/env python

# takes a fasta as input and saves a pickle file of sparse matricies
# corresponding to the one hot encoding of the values. 
# N values are encoded as 0
import argparse
from sklearn.preprocessing import OneHotEncoder
import pickle
import numpy as np
import sys

def parse_and_encode_fasta(file, dense, padzeroes):
    """
    input:
        file - fasta file to be converted into one hot encoding of sequence
    returns:
        names - a list of strings where each string is the location of the
            sequence
        seqs - a list of strings where each string is the sequence 
            of a line in a given fasta
        encoder - a OneHotEncoder object which translates sequences to 
            one hot encoding values
    """

    encoder = OneHotEncoder(categories='auto',
                            sparse=not dense, # declares if sparse or not
                            handle_unknown='ignore' # converts not ATCG bases to zeros
                           )
    encoder.fit(np.array(["A", "T", "C", "G"]).reshape(-1, 1))
    
    if (padzeroes):
        import os
        stream = os.popen('wc -L {}'.format(file))
        output = stream.read()
        max_len = int(output.split(' ')[0])
        with open(file, 'r', encoding='utf-8') as f:
            count = 0
            names = []
            seqs = []

            for line in f:
                line = line.strip('\n')
                if count % 2 == 0:
                    names.append(line)
                else:
                    # zero padding is done by adding an unrecognized char via
                    # ljust the encoder will conver these into zeros on the end of
                    # the sequence
                    use = np.array(list(line.upper().ljust(max_len, 'x'))).reshape(-1, 1)
                    seqs.append(encoder.transform(use).T)
                count+=1
            return names, seqs, encoder
    else:
        with open(file, 'r', encoding='utf-8') as f:
            count = 0
            names = []
            seqs = []

            for line in f:
                line = line.strip('\n')
                if count % 2 == 0:
                    names.append(line)
                else:
                    use = np.array(list(line.upper())).reshape(-1, 1)
                    seqs.append(encoder.transform(use).T)
                count+=1
            return names, seqs, encoder
    
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

    
def create_parser():
    parser = MyParser(description=\
                        ("generates one hot encoded sequences from a fasta"
                        "and saves them as a pickled dictionary"
                        ))
    parser.add_argument('-i', '--input',
                        required=True, 
                        help="a fasta file of sequences to one hot encode")
    parser.add_argument('-o', '--output',
                        required=True,
                       help="an output file to save pickled results")
    parser.add_argument('-p', '--padzeroes',
                        required=False,
                        action='store_true',
                       help='''wether to normalize length by zero
                       padding the one hot encoded sequence''')
    parser.add_argument('-d', '--dense',
                        required=False,
                        action='store_true',
             help="option saves dense rather than sparse arrays of one hot encoded variables")
    
    return parser


if __name__ == '__main__':
    
    parser = create_parser()
    args = parser.parse_args()
    
    names, seqs, encoder = parse_and_encode_fasta(args.input,
                                                  args.dense,
                                                  args.padzeroes)
    
    to_pickle = {'sequence_name' : names,
                 'sparse_one_hot' : seqs,
                 'one_hot_encoder': encoder}
    
    pickle.dump(to_pickle, open(args.output, 'wb'),
                protocol=pickle.HIGHEST_PROTOCOL)