#seq_tools

My toolkit for working with genomic sequences.

#Current scripts:
##one_hot_fasta.py:
usage: one_hot_fasta.py [-h] -i INPUT -o OUTPUT [-p] [-d]

generates one hot encoded sequences from a fastaand saves them as a pickled
dictionary

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        a fasta file of sequences to one hot encode
  -o OUTPUT, --output OUTPUT
                        an output file to save pickled results
  -p, --padzeroes       wether to normalize length by zero padding the one hot
                        encoded sequence
  -d, --dense           option saves dense rather than sparse arrays of one
                        hot encoded variables
