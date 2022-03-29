# HW10 - API for GENSCAN Online Version
[GENSCAN](http://hollywood.mit.edu/GENSCAN.html) identifies complete exon/intron structures of genes in genomic DNA.
Novel features of the program include the capacity to predict multiple genes in a sequence,
to deal with partial as well as complete genes, and to predict consistent sets of genes occurring on either or both DNA strands.
GENSCAN is shown to have substantially higher accuracy than existing methods when tested on standardized sets of human and vertebrate genes, with 75 to 80% of exons identified exactly. 
The program is also capable of indicating fairly accurately the reliability of each predicted exon.

**Task:** Here we have written API for GENSCAN Online Version.

## Data:
* `neurofibromin.fa` contains neurofibromin 1 nucleotide sequence.<br>
NF1 spans over 350-kb of genomic DNA and contains 62 exons.
* `insulin.fa` contains insulin gene nulceotide sequence.<br>
The human insulin gene (INS) is a small gene located on chromosome 11 and is composed of 3 exons separated by two introns.
* `nlrp3.fa` encodes a pyrin-like protein containing a pyrin domain, a nucleotide-binding site (NBS) domain, and a leucine-rich repeat (LRR) motif.
NLRP3 maps on chromosome 1 and consists of 3108 nucleotides.

## Functions:
`run_genscan` accepts parameters available on the web-site:
* **sequence:** DNA sequence (upper or lower case, spaces/numbers ignored), default = None
* **sequence_file:** path to DNA sequence file (default None)
* **organism:** type of organism from which DNA sequence was obtained (default "Vertebrate")
* **exon_cutoff:** allows to find less probable exons.  Available values: 1.00, 0.5, 0.25, 0.1, 0.05, 0.02, 0.01 (default 1.00)
* **sequence_name:** name of the target nucleotide sequence (default "")
* **print_options:** "Predicted peptides only" (default) or "Predicted CDS and peptides"

It returns an object from class `GenscanOutput` with the following attributes:
* **status:** status of response (200 - if it was successful)
* **intron_list:** list of introns coordinates (from the first table of results in browser version)
* **exon_list:** list of exons coordinates (from the first table of results in browser version)
* **cds_list:** list with predicted protein sequences after splicing (at the end of results in browser version)
* **resp:** response from the site (after implementation of requests.get() function)
