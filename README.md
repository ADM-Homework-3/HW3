# HW3

The structure of the code is:

- **General Search Engine.ipynb**: All of the functions and usefull code is stored in this notebook
- **multi_processing_functions.py**: Functions which we have applied in parallel (using multi-processing package)
- **data**: In this folder is all the relevant data, i.e. parsed dataframe (final_tsv_files.tsv), pre-processed 
dataframe (clean_final.tsv) and the inverted indexes, vocabulary 
dictionary and tfidf dictionary (for the first two search 
engines, i.e. applied only over the Plot and for the third search 
engine, applied over more variables, PLot, BookTitle, BookAuthor, 
etc.) 

In order to run the search engine, nice visualization it is not necesarry to re-run the whole process (parsing, pre-processing, etc.). 
Please only run the cells which contain the comment: "# Run cell"
