import os
from itertools import islice
import argparse


def bound_modify(func):
    '''
    Wrapper around bound_value parameter.
    :param func: function for wrapping around
    :return: func with modified parameter
    '''
    def a_wrapper_accepting_arguments(nt_seq, bound_value=None):
        if not bound_value:
            return func(nt_seq)
        elif isinstance(bound_value, tuple):
            return func(nt_seq, *bound_value[::-1])
        elif isinstance(bound_value, (int, float)):
            return func(nt_seq, bound_value)
    return a_wrapper_accepting_arguments


@bound_modify
def is_in_gc_bounds(nt_seq, upper_bound=100, lower_bound=0):
    '''
    Check if GC content of nucleotide sequence is in available range of values
    :param nt_seq: read nucleotide sequence
    :param upper_bound: upper bound of the range of available GC content values
    :param upper_bound: upper bound of the range of available GC content values
    :return: bool value (True/False)
    '''
    gc_content = (nt_seq.upper().count('C') + nt_seq.upper().count('G')) / len(nt_seq) * 100
    return lower_bound <= gc_content <= upper_bound


@bound_modify
def is_in_length_bounds(nt_seq, upper_bound=2**32, lower_bound=0):
    '''
    Check if read length is in available range of values
    :param nt_seq: read nucleotide sequence
    :param upper_bound: upper bound of the range of available read length values
    :param upper_bound: upper bound of the range of available read length values
    :return: bool value (True/False)
    '''
    read_length = len(nt_seq)
    return lower_bound <= read_length <= upper_bound


@bound_modify
def is_in_quality_bounds(ascii_seq, quality_threshold=0):
    '''
    Check if average read quality score is higher than some threshold
    :param ascii_seq: quality score per nucleotide of a read in ascii format
    :quality_threshold: average read quality threshold
    :return: bool value (True/False)
    '''
    phred_seq = [ord(symb)-33 for symb in ascii_seq]
    phred_mean = sum(phred_seq)/len(phred_seq)
    return phred_mean >= quality_threshold


def check_all_conditions(nt_seq, ascii_seq, gc_bounds=None, length_bounds=None, quality_threshold=None):
    '''
    Check if GC content, read length and quality score are in available range of values
    :param nt_seq: read nucleotide sequence
    :param ascii_seq: quality score per nucleotide of a read in ascii format
    :param gc_bounds: range of available GC content values
    :param length_bounds: range of available read length values
    :param quality_threshold: average read quality threshold
    :return: bool value (True/False)
    '''
    is_proper_gc = is_in_gc_bounds(nt_seq, bound_value=gc_bounds)
    is_proper_length = is_in_length_bounds(nt_seq, bound_value=length_bounds)
    is_proper_quality = is_in_quality_bounds(ascii_seq, bound_value=quality_threshold)
    return (is_proper_gc and is_proper_length and is_proper_quality)


def check_reads(next_n_lines, gc_bounds=None, length_bounds=None, quality_threshold=None):
    '''
    Check if read in a fastq file passes filtration process
    :param next_n_lines: 4 lines in fastq file per read
    :param gc_bounds: range of available GC content values
    :param length_bounds: range of available read length values
    :param quality_threshold: average read quality threshold
    :return: bool value (True/False)
    '''
    lines_stripped = [line.strip() for line in next_n_lines]
    nt_seq, ascii_seq = lines_stripped[1], lines_stripped[3]
    is_proper_all = check_all_conditions(nt_seq=nt_seq, ascii_seq=ascii_seq,
                                         gc_bounds=gc_bounds, length_bounds=length_bounds,
                                         quality_threshold=quality_threshold)
    return is_proper_all


def main(input_fastq, output_file_prefix, gc_bounds=None, length_bounds=None,
         quality_threshold=None, save_filtered=False):
    '''
    Filtrate reads and save them in separate files
    :param input_fastq: path to fastq file
    :param output_file_prefix: prefix of output fastq file
    :param gc_bounds: range of available GC content values
    :param length_bounds: range of available read length values
    :param quality_threshold: average read quality threshold
    :param save_filtered: bool value which shows if failed reads should be saved in a file or not
    '''
    output_fastq_passed = output_file_prefix + '_passed.fastq'
    output_fastq_failed = output_file_prefix + '_failed.fastq'
    with open(input_fastq, 'r') as f_inp:
        with open(output_fastq_passed, 'w') as f_passed, open(output_fastq_failed, 'w') as f_failed:
            while True:
                next_n_lines = list(islice(f_inp, 4))
                if not next_n_lines:
                    break
                is_proper_all = check_reads(next_n_lines=next_n_lines,
                                            gc_bounds=gc_bounds,
                                            length_bounds=length_bounds,
                                            quality_threshold=quality_threshold)
                if is_proper_all:
                    f_passed.write(''.join(next_n_lines))
                else:
                    if save_filtered:
                        f_failed.write(''.join(next_n_lines))
        if not save_filtered:
            os.remove(output_fastq_failed)


if __name__ == '__main__':
    # argparse main parameters
    parser = argparse.ArgumentParser(description='fastq filtrator', epilog='Enjoy the program! :)',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--input_fq', type=str, help='Path to fastq file', required=True, metavar='')
    parser.add_argument('--output_pref', type=str, help='Prefix of output fastq file', required=True, metavar='')
    parser.add_argument('--gc', type=str, metavar='',
                        help='Range of available GC content values (separate values with comma). Default: 0,100')
    parser.add_argument('--len', type=str, metavar='',
                        help='Range of available read length values (separate values with comma). Default: 0,2^32')
    parser.add_argument('--quality', type=int, metavar='',
                        help='Average read quality threshold. Default: 0')
    parser.add_argument('--save', type=int, metavar='',
                        help='Failed reads should be saved in a file (1) or not (0). Default: 0')
    args = parser.parse_args()
    if args.gc:
        gc_bounds = tuple([int(val) for val in args.gc.split(',')])
    else:
        gc_bounds = None
    if args.len:
        length_bounds = tuple([int(val) for val in args.len.split(',')])
    else:
        length_bounds = None
    print('Start fastq filtration...')
    main(input_fastq=args.input_fq, output_file_prefix=args.output_pref,
         gc_bounds=gc_bounds, length_bounds=length_bounds,
         quality_threshold=args.quality, save_filtered=args.save)
    print('End fastq filtration')
