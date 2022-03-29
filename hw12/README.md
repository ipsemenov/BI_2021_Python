# HW12 - Iterators and generators

This homework is about working with iterators and generators.
## Data: 
* **sequences.fa:** file with 10 nucleotide sequences in FASTA format
* **sequences_broken.fa:** the same file but without first record id (needed for validation)
* **sequences.faa:** file with 10 amino acid sequences in FASTA format

## Task 1
Write a generator which reads FASTA file and outputs record id (starting from '>' character) and sequence 

## Task 2
Write class for reading sequences from FASTA file and outputing them with some changes in infinite cycle.<br>
This class works with amino acid sequences as well as with nucleotide sequences.<br>
Following changes (mutations) per sequence are allowed:
* Substitution
* Insertion
* Deletion

Also it is possible to set for each type of mutation its probability of emergence.

## Task 3
Write generator ***iter_append(iterable, item)*** which appends ***item*** to the end of ***itearable*** object.<br>
So, during iterations we will, firstly, obtain data from ***iterable*** and only then from ***item***.<br>
It is not allowed to use any loops (for, while, etc.)

## Task 4
Write function unpacking elements of nested list into a new one (not nested).
