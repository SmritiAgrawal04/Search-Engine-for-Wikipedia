# Search-Engine-for-Wikipedia
It is an Information Retrieval system designed to help find information stored on a computer system. It is a Text-based Search Engine which provides users an interface to query about an item of interest and have the engine find the matching items.
### Technologies used
1) Python3 & its libraries for Natural Language Processing(NLP)
2) Jupyter- Notebook
### Launch
How to run the project? 
The various steps involved in building a search engine are as follows- 
CRAWAL- First step is to download all the Wiki dump from dataurls.txt and rename them to *.xml. 
INDEX- Next before performing a search our index should be ready and to prep that run all the cells of index.ipynb notebook after setting the path of the xml files in the main(). Also, create a new folder named "inverted_index" in current directory to hold you index files.
(Note that this step might take 12-15 HOURS to complete depending on your sytem configs.)
SEARCH- Now, we're ready to perform a search on multiple queries of your choice. (One may refer the sample_queries.txt file)
### Characterstics of the SE
1) Fast & Accurate.
2) Uses Ranking Mechanisms to rank the documents.
3) Uses tf idf scores to sort k-relevant results.
4) The index size is 1/4th the size of corpus.
