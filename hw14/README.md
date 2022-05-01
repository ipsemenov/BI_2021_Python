# HW14 - Parallel Programming

This homework is about parallel programming. 
Here I realize a console utility which allows to read large FASTA files (500МB+) and count number of letters in each sequence. 
This utility can be run in parallel to reduce time of program execution.

## Data: 
* Initial data (human genome) can be downloaded via [link](https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh38_latest/refseq_identifiers/GRCh38_latest_genomic.fna.gz).
* Downloaded file should be uncompressed and moved into working directory:
                
                $ gunzip GRCh38_latest_genomic.fna.gz

## Installation and Usage:
1. Install necessary libraries

                $ pip install -r requirements.txt

2. To show information about program usage execute the following command:
                
                $ python parallel.py --help

![image](https://user-images.githubusercontent.com/56733786/166161475-dbf0d745-26a4-4376-9806-23a3cf03d6f9.png)

3. Run calculations and measure time in terminal:
  
                $ time python parallel.py --input INPUT --threads THREADS

4. The same program can be launched in jupyter notebook - file parallel.ipynb

## Results:
Program was launched with different number of cores and the following results were obtained:

* 1 core:

![image](https://user-images.githubusercontent.com/56733786/166161751-04f71ca4-e818-4be1-9d9f-bdd3c1ed936f.png)

* 2 cores:

![image](https://user-images.githubusercontent.com/56733786/166161767-72f67a58-218d-41af-8966-dbc440403740.png)

* 4 cores:

![image](https://user-images.githubusercontent.com/56733786/166161778-895b7fcb-cd00-49fb-9e53-af19992c5fd0.png)


* 8 cores:

![image](https://user-images.githubusercontent.com/56733786/166161798-b7133afd-9960-4550-816e-36d5352ae535.png)

Also time measurements can be found in parallel.ipynb



