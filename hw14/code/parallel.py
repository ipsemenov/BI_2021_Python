import argparse
import logging
from collections import Counter
from pathlib import Path
import sys

import multiprocessing
from Bio import SeqIO


class SeqCounter:

    def __init__(self, path_to_file, threads):
        '''
        Constructor

        :param path_to_file: str, path to FASTA file
        :param threads: int, number of processes to run in parallel
        '''

        self.path_to_file = path_to_file
        self.threads = threads

    def __str__(self):
        '''
        Represents the class objects as a string
        '''

        return "Path to the file: {}\nNumber of threads: {}".format(self.path_to_file, self.threads)

    def count_letters(self, id_, seq):
        '''
        Counts number of letters in a sequence and outputs these counts with sequence name

        :param id_: str, name of the FSTA sequence
        :param seq: FASTA sequence
        '''

        counts_dict = dict(Counter(seq))
        counts_list = [k + '=' + str(v) for k, v in counts_dict.items()]
        counts_str = ', '.join(counts_list)
        print(f'{id_}:', counts_str)

    def output_results(self):
        '''
        Reads FASTA file, counts letters in each sequence and outputs results
        '''

        processes = []
        records = SeqIO.parse(self.path_to_file, "fasta")
        for record in records:
            if len(processes) == self.threads:
                for process in processes:
                    process.start()
                for process in processes:
                    process.join()
                processes = []
            processes.append(multiprocessing.Process(target=self.count_letters, args=(record.id, record.seq)))
        if len(processes) > 0:
            for process in processes:
                process.start()
            for process in processes:
                process.join()


def SetLogger(logger_name):
    '''
    Create custom logger and set its configuration
    :param logger_name: name of created logger
    '''

    logger = logging.getLogger('argparse')
    logger.setLevel(logging.INFO)
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_format = logging.Formatter('%(levelname)s: %(message)s')
    c_handler.setFormatter(c_format)
    logger.addHandler(c_handler)


if __name__ == '__main__':

    # argparse main parameters
    parser = argparse.ArgumentParser(description='FASTA counter', epilog='Enjoy the program! :)',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input', type=str, help='Path to FASTA file', required=True, metavar='')
    parser.add_argument('-t', '--threads', type=int, help='number of processes to run in parallel',
                        required=True, metavar='')
    args = parser.parse_args()

    # create argparse logger
    SetLogger(logger_name='argparse')
    logger = logging.getLogger('argparse')

    # check whether input file exists
    if not Path(args.input).exists():
        logger.warning('File {} does not exist!'.format(args.input))
        logger.info('Abort calculations. Specify correct path to file.')
        sys.exit()

    seq_counter = SeqCounter(args.input, args.threads)
    logger.info(f'Start calculations for {args.input} with n_jobs = {args.threads}')
    seq_counter.output_results()
    logger.info('End calculations.')
