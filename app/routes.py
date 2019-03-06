from app import app
from flask import request
import json

import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet
import re
from dateutil.parser import parse

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
final_result={}

#-------------------------------------------------------------------------------------------------------------------------
                                                #APIS
#-------------------------------------------------------------------------------------------------------------------------

@app.route('/')
def index():    return "Hello, World!"# -*- coding: utf-8 -*-

@app.route('/postJson', methods=['POST'])
def post():
    content = request.get_json()
    print(content['value'])
    startAnalyzing(content['value'])
    final_result['date'] = content['timeStamp']
    return 'JSON POSTED SUCCESSFULLY ...'

@app.route('/getJSON', methods=['GET'])
def get():
    return json.dumps(final_result)


#-------------------------------------------------------------------------------------------------------------------------
                                                #Functions
#-------------------------------------------------------------------------------------------------------------------------


def startAnalyzing(data):
    final_result.clear()
    sentences = sent_tokenize(data)
    for s in sentences:
        words=[]
        temp = word_tokenize(s)
        for w in temp:
            if w not in stop_words:
                words.append(lemmatizer.lemmatize(w))
        parseInformation(words)
        parseSuggestions(words)
        parseNextScheduleMeeting(words)
    return

def getSynonyms(word):
    syns = wordnet.synsets(word)
    temp=set()
    words=[]
    for s in syns:
        for l in s.lemmas():
            if l.name() not in temp:
                temp.add(l.name())
                words.append(l.name())
    return words

def parseSuggestions(words):
    suggestions=[]
    suggest_synonyms = getSynonyms("suggest")
    if any(x in suggest_synonyms for x in words):
        postTag = nltk.pos_tag(words)
        for p in postTag:
            if p[1][0] == 'N':
                suggestions.append(p[0])
        final_result['suggestions'] = suggestions
    else:
        return
    return

def parseNextScheduleMeeting(words):
    schedule_synonyms = getSynonyms("scheduling")
    if any(z in schedule_synonyms for z in words):
        try:
            date_token = parse(' '.join(words), fuzzy_with_tokens=True)
            temp = date_token[0]
            final_result['next schedule'] = temp.__str__()
        except TypeError:
            return
    return

def parseSymptoms(words):
    return

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

def parseInformation(words):
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