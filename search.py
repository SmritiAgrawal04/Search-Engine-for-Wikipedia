
# coding: utf-8

# In[37]:


import string, sys
import nltk
import Stemmer
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import *

STOPWORDS = set(stopwords.words('english')) 
URL_STOP_WORDS = set(["http", "https", "www", "ftp", "com", "net", "org", "archives", "pdf", "html", "png", "txt", "redirect", "align", "realign", "valign", "nonalign", "malign", "unalign", "salign", "qalign", "halign", "font", "fontsiz", "fontcolor", "backgroundcolor", "background", "style", "center", "text"])
fields= ['t:', 'i:', 'c:', 'b:', 'r:', 'l:']


# In[38]:


def readIndex():
    f= open("{}InvertedIndex.txt".format(sys.argv[1]), "r")
    Index= {}

    lines= f.readlines()
    line =0

    while line< len(lines):
        text = lines[line].split(":")
        word= text[0]
        frequency= text[1]
        line +=1
        while line< len(lines) and ":" not in lines[line]:
            frequency += lines[line]
            line +=1
        Index[word]= frequency

    f.close()
    return Index


# In[39]:


def cleanQuery(query):
    stemmer= Stemmer.Stemmer("english")
    query = re.sub(r'\\d+', '', query) #Remove numbers
    query = re.sub(r'<(.*?)>','',query) #Remove tags if any
    query = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', query, flags=re.MULTILINE) #Remove Url
    query = re.sub(r'{\|(.*?)\|}', '', query, flags=re.MULTILINE) #Remove CSS
    query = re.sub(r'\[\[file:(.*?)\]\]', '', query, flags=re.MULTILINE) #Remove File
    query = re.sub(r'[^\w\s]', '', query) 
    query = query.split()
    query = [x for x in query if x not in STOPWORDS and x not in URL_STOP_WORDS]
    query = [stemmer.stemWord(word) for word in query]
#     print ("Query in Processing: {}".format(query))
    
    return query


# In[40]:


def search_fieldQuery(documents, field_type):
    fieldDocs= []
    documents= documents.split("|")
    for doc in documents:
        if field_type in doc:
            fieldDocs.append(doc)
    return fieldDocs


# In[41]:


def process_fieldQuery(query):
    fieldInfo= {}
    
    for f in fields:
        field= query.find(f)
        if field !=-1:
            fieldInfo[field]= f
    
    fieldInfo= sorted(fieldInfo.items())
    fieldInfo.append((1234567890, ""))
#     print(fieldInfo)
    i=0
    while i+1 <len(fieldInfo):
        fieldQuery = (query[fieldInfo[i][0]+2 : fieldInfo[i+1][0]]).lower()
#         print (fieldQuery)
        fieldQuery = cleanQuery(fieldQuery)
#         print (fieldQuery)
        for word in fieldQuery:
            if word not in Index:
                print (word, " : ", [])
            else:
                value= Index[word]
                print(word, " : ", search_fieldQuery(value, fieldInfo[i][1][:1]))
            print()
        i +=1
    


# In[42]:


Index= readIndex()

query= sys.argv[2]
# print ("Query in Python: ", query)

if "t:" in query or "i:" in query or "c:" in query or "b:"in query or "r:" in query or "l:" in query:    
    process_fieldQuery(query)
else:
    query = cleanQuery(query)
    for word in query:
        if word.lower() in Index:
            print (word, " : ", Index[word.lower()])
        else:
            print (word, " : ", [])

