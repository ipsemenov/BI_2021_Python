available_commands = {'exit', 'transcribe', 'reverse', 'complement', 'reverse complement'}
complement_dict_dna = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'a': 't', 't': 'a', 'g': 'c', 'c': 'g'}
complement_dict_rna = {'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G', 'a': 'u', 'u': 'a', 'g': 'c', 'c': 'g'}
while True:
    command = input('Enter command: ')
    if command not in available_commands:
        print('Invalid command. Try again!')
        continue
    if command == 'exit':
        print('Good luck!')
        break
    elif command == 'transcribe':
        seq = input('Enter sequence: ')
        while not all([nt in {'A', 'G', 'C', 'T'} for nt in seq.upper()]):
            print('Invalid DNA alphabet. Try again!')
            seq = input('Enter sequence: ')
        seq_tr = seq.replace('t', 'u').replace('T', 'U')
        print(seq_tr)
    else:
        seq = input('Enter sequence: ')
        is_dna = all([nt in {'A', 'G', 'C', 'T'} for nt in seq.upper()])
        is_rna = all([nt in {'A', 'G', 'C', 'U'} for nt in seq.upper()])
        while not (is_dna or is_rna):
            print('Invalid alphabet. Try again!')
            seq = input('Enter sequence: ')
            is_dna = all([nt in {'A', 'G', 'C', 'T'} for nt in seq.upper()])
            is_rna = all([nt in {'A', 'G', 'C', 'U'} for nt in seq.upper()])

        if command == 'reverse':
            seq_rev = seq[::-1]
            print(seq_rev)
        elif command == 'complement':
            if is_dna:
                seq_rev = ''.join([complement_dict_dna[nt] for nt in seq])
            else:
                seq_rev = ''.join([complement_dict_rna[nt] for nt in seq])
            print(seq_rev)
        elif command == 'reverse complement':
            if is_dna:
                seq_rev_compl = ''.join([complement_dict_dna[nt] for nt in seq])[::-1]
            else:
                seq_rev_compl = ''.join([complement_dict_rna[nt] for nt in seq])[::-1]
            print(seq_rev_compl)
