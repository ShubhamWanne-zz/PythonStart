import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
import re

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
final_result={}


def startAnalyzing(data):
    final_result.clear()
    sentences = sent_tokenize(data)
    for s in sentences:
        words=[]
        temp = word_tokenize(s)
        for w in temp:
            if w not in stop_words:
                words.append(lemmatizer.lemmatize(w))
        parseSentence(words)

def getName(words):
    pos = nltk.pos_tag(words)
    sentt = nltk.ne_chunk(pos, binary = False)
    person = []
    person_list=[]
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1:
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
    if(len(person_list)!=0):
        return person_list[0]
    else:
        return

def getNumericValue(words):
    sentence = ' '.join(words)
    temp = re.findall('[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?',sentence)
    if(len(temp) == 1):
        return temp[0]
    else:
        return -1

def parseSentence(words):
    if('temperature' in words):
        final_result['temperature'] = float(getNumericValue(words))
        return
    if('pulse' in words):
        final_result['pulse'] = float(getNumericValue(words))
        return
    if(set(['blood','pressure']).issubset(set(words))):
        final_result['blood pressure'] = float(getNumericValue(words))
        return        
    if(set(['patient','id']).issubset(set(words))):
        final_result['patient id'] = int(getNumericValue(words))
        return
    if('name' in words):
        if('?' in words):
            return
        final_result['name'] = getName(words)
            
    else:
        return