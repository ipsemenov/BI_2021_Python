import re
import requests


class GenscanOutput:

    def __init__(self, status, cds_list, intron_list, exon_list, resp):
        self.status = status
        self.intron_list = intron_list
        self.exon_list = exon_list
        self.cds_list = cds_list
        self.resp = resp


def run_genscan(sequence=None,
                sequence_file=None,
                organism="Vertebrate",
                exon_cutoff=1.00,
                sequence_name="",
                print_options='Predicted peptides only'):
    '''
    API for GENSCAN Online Version.
    It identifies complete exon/intron structures of genes in genomic DNA.
    Allows to analyze sequences up to 1 million base pairs (1 Mbp) in length.

    :param sequence: str, DNA sequence (upper or lower case, spaces/numbers ignored)
    :param sequence_file: str, path to DNA sequence file
    :param organism: str, type of organism from which DNA sequence was obtained
    :param exon_cutoff: float, allows to find less probable exons.
                        Available values: 1.00, 0.5, 0.25, 0.1, 0.05, 0.02, 0.01 (default 1.00)
    :param sequence_name: name of the target nucleotide sequence
    :param print_options: str, 'Predicted peptides only' (default) or 'Predicted CDS and peptides'
    '''

    genscan_url = 'http://hollywood.mit.edu/cgi-bin/genscanw_py.cgi'
    payload = {'-o': organism,
               '-e': exon_cutoff,
               '-n': sequence_name,
               '-p': print_options}

    # make request and get info from browser
    if sequence_file is None:
        payload['-s'] = sequence
        resp = requests.post(genscan_url, data=payload)
    else:
        with open(sequence_file, 'rb') as fasta_file:
            files = {'-u': fasta_file}
            resp = requests.post(genscan_url, data=payload, files=files)

    # find list of coding sequences
    pattern_1 = re.compile(r'Predicted peptide sequence\(s\):[\d\D]+')
    pattern_2 = re.compile(r'>.+\n{2}([ARNDCEQGHILKMFPSTWYV\n]+)')
    pattern_3 = re.compile(r'([ARNDCEQGHILKMFPSTWYV]+)')
    results = pattern_2.findall(pattern_1.findall(resp.text)[0])
    cds_list = []
    for result in results:
        cds_list.append(''.join(pattern_3.findall(result)))

    # find exons and introns
    exon_list = []
    intron_list = []
    for element in re.compile(r'\d\.\d{2}\s+([A-z]+)\s+[\-\+]\s+(\d+)\s+(\d+)').findall(resp.text):
        if element[0] in ['Init', 'Intr', 'Term', 'Sngl']:
            exon_list.append(element[1:])
        else:
            intron_list.append(element[1:])

    genscan_output = GenscanOutput(status=resp.status_code,
                                   cds_list=cds_list,
                                   intron_list=intron_list,
                                   exon_list=exon_list,
                                   resp=resp)

    return genscan_output


if __name__ == '__main__':

    genscan_output_nlrp3 = run_genscan(sequence=None,
                                       sequence_file='../data/nlrp3.fa',
                                       organism="Vertebrate",
                                       exon_cutoff=1.00,
                                       sequence_name="NLRP3",
                                       print_options='Predicted peptides only')

    print('\n')
    print('Status code:', genscan_output_nlrp3.status)
    print('\n')

    print('Coding sequences:')
    print('-----------------------------------------------')
    print(*genscan_output_nlrp3.cds_list, sep='\n\n')
    print('\n\n')

    print('Intron coordinates:')
    print('-----------------------------------------------')
    print(*genscan_output_nlrp3.intron_list, sep='\n\n')
    print('\n\n')

    print('Exon coordinates:')
    print('-----------------------------------------------')
    print(*genscan_output_nlrp3.exon_list, sep='\n\n')
    print('\n\n')
