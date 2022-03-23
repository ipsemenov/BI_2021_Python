import numpy as np


# Task 1
def fasta_reader(path_to_file):
    '''
    Generator which reads FASTA file and outputs record id (starting from '>' character) and sequence
    :param path_to_file: str, path to FASTA file
    :return id, seq: record id and sequence
    '''

    # some check for valid format
    with open(path_to_file, 'r') as handle:
        for line in handle:
            if line[0] != '>':
                raise ValueError("Expected FASTA record starting with '>' character")
            break

    # generator
    with open(path_to_file, 'r') as handle:
        title, lines = None, []
        for line in handle:
            if line[0] == '>' and title is None:
                title = line[1:].rstrip()
            elif line[0] == '>':
                yield title, ''.join(lines)
                title, lines = line[1:].rstrip(), []
            else:
                lines.append(line.rstrip())
        yield title, ''.join(lines)


# Task 2
class FastaReader:
    '''
    Class for reading sequences from FASTA file and outputing them
    with some changes in infinite cycle
    '''

    alphabet_nt = ['A', 'T', 'C', 'G']

    alphabet_aa = ['A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I',
                   'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']

    def __init__(self, path_to_file, seq_type, probs, seq_size=None):
        '''
        Constructor

        :param path_to_file: str, path to FASTA file
        :param seq_type: str, type of input data ('nt' or 'aa') for nucleotide
                              and amino acid sequences respectively
        :param probs: list, probabilities for substitution, insertion and deletion
        :param seq_size: int, number of first letters of initial sequnece to work with
        '''

        self.path_to_file = path_to_file
        self.probs = probs
        self.seq_size = seq_size
        if seq_type == 'aa':
            self.alphabet = self.alphabet_aa
        elif seq_type == 'nt':
            self.alphabet = self.alphabet_nt

    def fasta_reader(self):
        '''
        Generator which reads FASTA file and outputs record id
        (starting from '>' character) and sequence
        '''

        # some check for valid format
        with open(self.path_to_file, 'r') as handle:
            for line in handle:
                if line[0] != '>':
                    raise ValueError("Expected FASTA record starting with '>' character")
                break

        # generator
        with open(self.path_to_file, 'r') as handle:
            title, lines = None, []
            for line in handle:
                if line[0] == '>' and title is None:
                    title = line[1:].rstrip()
                elif line[0] == '>':
                    yield title, ''.join(lines)
                    title, lines = line[1:].rstrip(), []
                else:
                    lines.append(line.rstrip())
            yield title, ''.join(lines)

    def change_seq(self, seq):
        '''
        Change input sequence, introducing substitution, insertion
        or deletion into random position
        '''

        mutation = np.random.choice(['substitution', 'insertion', 'deletion'], p=self.probs)
        index = np.random.choice(range(len(seq)))
        if mutation == 'substitution':
            letter_to_change = seq[index]
            available_letters = list(set(self.alphabet)-set(letter_to_change))
            change = np.random.choice(available_letters)
        elif mutation == 'insertion':
            change = np.random.choice(self.alphabet)
        elif mutation == 'deletion':
            change = ''
        seq_changed = seq[:index] + change + seq[index+1:]

        return seq_changed

    def display_changed_seq(self):
        '''
        Iterate through FASTA file and output record id
        (starting from '>' character) and changed sequence
        '''

        while True:
            reader = self.fasta_reader()
            for id_, seq in reader:
                if self.seq_size is None:
                    seq_changed = self.change_seq(seq=seq)
                else:
                    seq_changed = self.change_seq(seq=seq[:self.seq_size])
                print(id_, seq_changed, sep='\t')
            print()

    def __repr__(self):
        message = f'''
                Class {self.__class__.__name__}

                Change sequences with following probabilities:
                substitution = {self.probs[0]},
                insertion = {self.probs[1]},
                deletion = {self.probs[2]}
                '''
        return message


# Task 3
def iter_append(iterable, item):
    '''
    Append item to the end of itearble object.
    So, during iterations we will, firstly, obtain data from iterable and only then form item

    :param iterable: some iterable object
    :param item: object to append to iterable
    :return: generator
    '''

    iterable = list(iterable)
    if iterable:
        yield iterable.pop(0)
        yield from iter_append(iterable, item)
    else:
        yield item


# Task 4
def my_generator(iterable):
    '''
    Unpack elements of nested list and return them.

    :param iterable: nested list to unpack
    :return: generator
    '''

    if iterable:
        if isinstance(iterable[0], list):
            yield from my_generator(iterable[0])
        else:
            yield iterable[0]
        yield from my_generator(iterable[1:])


def nested_list_unpacker(iterable):
    '''
    Unpack elements of nested list into a new one

    :param iterable: nested list to unpack
    :return: unpacked list
    '''

    generator = my_generator(iterable=iterable)
    return [i for i in generator]
