
# coding: utf-8

# In[95]:


import numpy as np
import xml.sax
import sys
import csv
import re
import string
import datetime
import Stemmer
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import *
    


# In[96]:


STOPWORDS = set(stopwords.words('english')) 
URL_STOP_WORDS = set(["http", "https", "web", "www", "ftp", "com", "net", "org", "archives", "pdf", "html", "png", "txt"])
UNWANTED_LINES= set(["redirect", "align", "realign", "valign", "nonalign", "malign", "unalign", "salign", "qalign", "halign", "font", "fontsiz", "fontcolor", "backgroundcolor", "background", "style", "center", "text"])
fields= ['t', 'i', 'c', 'b', 'r', 'l']
docId=1
Wiki_Dict= {}
Doc_Dict= {}

total_tokens =0


# In[97]:


def create_invertedIndex():
    global Wiki_Dict
    Wiki_Dict= sorted(Wiki_Dict.items(), key=lambda t: t[0])
    f = open("./{}InvertedIndex.txt".format(sys.argv[2]), "w")
    for key, value in Wiki_Dict:
        line= key +':'+ value +"\n"
        f.write(line)
    f.close()


# In[98]:


# class Page:
def ProcessPage(pageID, content, index):
    for word in content:
        if word not in Doc_Dict:
            value= np.zeros(6, dtype= int)
            Doc_Dict[word]= value
            Doc_Dict[word][index] =1
        else:
            Doc_Dict[word][index] +=1

    if(index ==5):
        for key, value in Doc_Dict.items():
            if key not in Wiki_Dict:                # pageID_totalcount:t1i2c3b4r5l6|pageID_totalcount:t1i2c3b4r5l6
                Wiki_Dict[key]= str(pageID)+ '-'
                for f in range (0, 6):
                    if(value[f] >0):
                        Wiki_Dict[key] += fields[f] + str(value[f])
            else:
                Wiki_Dict[key] += '|'+ str(pageID)+ '-'
                for f in range (0, 6):
                    if(value[f] >0):
                        Wiki_Dict[key] += fields[f] + str(value[f])
        Doc_Dict.clear()   

def extract_pageDetails(text):
    global total_tokens
    lines= text.split('\n')
    line =0
    body_flag= False
    infoBox, category, body, references, links= [], [], [], [], []

    while line <len(lines):
        if any(element in lines[line] for element in UNWANTED_LINES) ==True:
            total_tokens += len(lines[line].split())
            line +=1
        elif "{{infobox" in lines[line]:
            openBrackets, closedBrackets= 1,0
            line +=1
            while line< len(lines):
                if "{{" in lines[line]:
                    openBrackets +=1
                if "}}" in lines[line]:
                    closedBrackets +=1

                infoBox.extend(lines[line].split())
                if(openBrackets == closedBrackets):
                    break
                line +=1
        elif "[[category:" in lines[line]:
            body_flag= True
            try:
                category.extend((lines[line].split(':')[1].split(']]')[0]).split())
            except:
                category.extend((lines[line].split(':')[1]).split())

        elif "==external links==" in lines[line] or "== external links ==" in lines[line]:
            body_flag= True
            line +=1
            while line< len(lines):
                if "*[" in lines[line] or "* [" in lines[line]:
                    link= ""
                    while line< len(lines) and "]" not in lines[line]:
                        link += lines[line]
                        line+=1
                    link += lines[line]
                    link = link.split('[')
                    if(len(link)> 1):
                        link= link[1].split(']')[0]
                        links.extend(link.split())
                elif "[[category:" in lines[line]:
                    try:
                        category.extend((lines[line].split(':')[1].split(']]')[0]).split())
                    except:
                        category.extend((lines[line].split(':')[1]).split())
                line+=1


        elif "==references==" in lines[line] or "== references ==" in lines[line]:
            body_flag= True
            line +=1
            while line< len(lines):
                if "==" in lines[line] or "[[category:" in lines[line]:
                    line -=1
                    break
                elif "{{cite" in lines[line] or "{{vcite" in lines[line]:
                    cite_title= lines[line].split("title=")
                    if(len(cite_title) >1):
                        cite_title= cite_title[1].split("|")[0]
                        references.extend(cite_title.split())
                elif "{{" in lines[line] and "ref" not in lines[line]:
                    references.extend((lines[line].split("{{")[1].split("}}")[0]).split())
                line+=1

        elif body_flag== False:
            body.extend(lines[line].split())
        line +=1  

    total_tokens+= len(infoBox)+len(category)+len(body)+len(references)+len(links)

#     print (infoBox, category, body, references, links)
    return ' '.join(infoBox), ' '.join(category), ' '.join(body), ' '.join(references), ' '.join(links)


# In[99]:


class Data:
    def __init__(self):
        self.docId = 0
        self.title=""
        self.text = ""
        self.infoBox= ""
        self.category= ""
        self.body= ""
        self.references= ""
        self.links= ""
        self.stemmer= Stemmer.Stemmer("english")

    def set_data(self, docId, title, text):
        self.docId = docId
        self.title= title
        self.text = text

        self.infoBox, self.category, self.body, self.references, self.links = extract_pageDetails(self.text)
        
        global total_tokens
        total_tokens+= len(self.title.split())
        
        self.title, self.infoBox, self.category, self.body, self.references, self.links= self.cleanText(self.title), self.cleanText(self.infoBox), self.cleanText(self.category), self.cleanText(self.body), self.cleanText(self.references), self.cleanText(self.links)        
        
#         print (self.infoBox)
        
        ProcessPage(self.docId, self.title, 0)
        ProcessPage(self.docId, self.infoBox, 1)
        ProcessPage(self.docId, self.category, 2)
        ProcessPage(self.docId, self.body, 3)
        ProcessPage(self.docId, self.references, 4)
        ProcessPage(self.docId, self.links, 5)
    
    def cleanText(self, text):
#         text = re.sub(r'\\d+', '', text) #Remove numbers
        text = re.sub(r'<(.*?)>','',text) #Remove tags if any
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text, flags=re.MULTILINE) #Remove Url
        text = re.sub(r'{\|(.*?)\|}', '', text, flags=re.MULTILINE) #Remove CSS
        text = re.sub(r'\[\[file:(.*?)\]\]', '', text, flags=re.MULTILINE) #Remove File
        text = re.sub(r'[^\w\s]', '', text) #Remove Punctuations & Special Characters
        text = text.split()
        text = [x for x in text if x not in STOPWORDS and x not in URL_STOP_WORDS and (x.isdigit() and (len(x)<=2 or len(x)>=5)) ==False and bool(re.match('^(?=.*[a-zA-Z])(?=.*[0-9])', x)) ==False]
        text = [self.stemmer.stemWord(word) for word in text]
        return text


# In[100]:


class WikiHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.title = ""
        self.text = ""

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        # global docId
        # if tag == "page":
        #     print (docId, end= " ")

    # Call when an elements ends
    def endElement(self, tag):
        global docId
        if self.CurrentData == "text":
            page= Data()
            page.set_data(docId, self.title, self.text)
            docId +=1
        self.text= ""
        self.CurrentData = ""

    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == "title":
            self.title = content.lower()
        elif self.CurrentData == "text":
            self.text += content.lower()


# In[101]:


if ( __name__ == "__main__"):
    start = datetime.datetime.now()
    
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = WikiHandler()
    parser.setContentHandler(Handler)

    dump_data= sys.argv[1]
    parser.parse(dump_data)
    
    create_invertedIndex()
    
    end = datetime.datetime.now()
    secs  = (end-start).seconds
    hr = int(secs/(60*60))
    rm = int(secs%(60*60))
    mn = int(rm/60)
    rm=int(rm%60)
    secs = int(rm)
    
    # global Wiki_Dict
    # print ("\nTotal Tokens= ", total_tokens)
    # print ("\nStored Tokens= ", len(Wiki_Dict))
    print("\nIndexing Time : ",hr," hrs ",mn," mns",secs," secs")

    f= open(sys.argv[3], "w")
    f.write(str(total_tokens))
    f.write("\n")
    f.write(str(len(Wiki_Dict)))
    f.close()