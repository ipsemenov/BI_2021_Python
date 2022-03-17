import pandas as pd
import sqlite3
import warnings
from IPython.display import display
warnings.simplefilter('ignore')


# Look at our dataframes

df_metadata = pd.read_csv('../data/metadata.csv')
df_genstudio = pd.read_csv('../data/genstudio.csv')
print('metadata shape:', df_metadata.shape)
print('genstudio shape:', df_genstudio.shape)
display(df_metadata.head(), df_genstudio.head())

# Column `Sample ID` contains the same values as `dna_chip_id` => we will use them to connect two tables

all(df_genstudio['Sample ID'].isin(df_metadata['dna_chip_id']))

# Create two databases

df_metadata.info()
df_genstudio.info()
connection = sqlite3.connect('../data/my_database.db')
create_metadata = '''CREATE TABLE metadata(
                                Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                dna_chip_id TEXT,
                                breed TEXT,
                                sex TEXT)
                  '''

create_genstudio = '''CREATE TABLE genstudio(
                                        Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        SNP_name TEXT,
                                        SNP_index INTEGER,
                                        SNP_Aux INTEGER,
                                        dna_chip_id TEXT,
                                        SNP TEXT,
                                        Allele1_Top TEXT,
                                        Allele2_Top TEXT,
                                        Allele1_Forward TEXT,
                                        Allele2_Forward TEXT,
                                        Allele1_AB TEXT,
                                        Allele2_AB TEXT,
                                        Chr TEXT,
                                        Position TEXT,
                                        GC_Score NUMERIC,
                                        GT_Score NUMERIC,
                                        Theta NUMERIC,
                                        R NUMERIC,
                                        B_Allele_Freq NUMERIC,
                                        Log_R_Ration NUMERIC,
                                        FOREIGN KEY (dna_chip_id) REFERENCES metadata(dna_chip_id))
                     '''
connection.execute(create_metadata)
connection.execute(create_genstudio)


# Fill tables with values

insertion_metadata = '''INSERT INTO metadata(Id,
                                              dna_chip_id,
                                              breed,
                                              sex)
                                        VALUES(?,?,?,?)'''

insertion_genstudio = '''INSERT INTO genstudio(Id,
                                                SNP_name,
                                                SNP_index,
                                                SNP_Aux,
                                                dna_chip_id,
                                                SNP,
                                                Allele1_Top,
                                                Allele2_Top,
                                                Allele1_Forward,
                                                Allele2_Forward,
                                                Allele1_AB,
                                                Allele2_AB,
                                                Chr,
                                                Position,
                                                GC_Score,
                                                GT_Score,
                                                Theta,
                                                R,
                                                B_Allele_Freq,
                                                Log_R_Ration)
                                        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''


connection.executemany(insertion_metadata, df_metadata.values)
connection.executemany(insertion_genstudio, df_genstudio.values)
connection.commit()
connection.close()


# Test some commands

connection = sqlite3.connect('../data/my_database.db')

query = '''SELECT Id, dna_chip_id, SNP_name, SNP FROM genstudio
            WHERE genstudio.GC_score > 0.5'''
rows = connection.execute(query).fetchmany(15)
for row in rows:
    print(row)

query = '''SELECT metadata.Id, metadata.dna_chip_id,
                  metadata.breed, metadata.sex,
                  genstudio.SNP_name, genstudio.SNP,
                  genstudio.Chr
          FROM metadata, genstudio
          WHERE metadata.dna_chip_id = genstudio.dna_chip_id
        '''

rows = connection.execute(query).fetchmany(20)
for row in rows:
    print(row)
