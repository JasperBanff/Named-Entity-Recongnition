# -*- coding: utf-8 -*-

# Relation Extraction Skeleton
# ==========================================
#
# Author: Jianbin Qin <jqin@cse.unsw.edu.au>

from relation import Relation

candidates = ['son','daughter','parent','child','children','grow','raised','adopted','mother','father']

bad_relation = ['sister','brother','sibling','grandfather','grandmother']


def iob_2_ner_span_parent(ioblist):

   # process the annotation, and only extract the tokens where its annotation
   # is PERSON,O, where O is contains the key relation such as born, to, and ....
   # return a list of words with its annotation.


    result = []
    last_type =""
    last_property=""
    for e in ioblist:
        if e[2] == 'B-PERSON':
            result.append([e[0],e[1],'PERSON'])
            last_type = 'PERSON'
        if e[2] == 'I-PERSON' and last_type == 'PERSON':
            result[-1][0] = result[-1][0] + " " + e[0]
            last_property = 'PERSON'
        if e[2] == 'O' and e[0] == 'born':
            result.append([e[0],e[1],'BORN'])
            last_type = 'BORN'
        if e[0] == 'to':
            result.append([e[0],e[1],'TO'])
            last_property = 'TO'
        if e[0] in candidates:
            result.append([e[0],e[1],'RELATION'])
            last_type = 'RELATION'
        if e[0] in bad_relation:
            result.append([e[0],e[1],'BAD-RELATION'])
            last_type = 'RELATION'
        if e[0] == 'of' and last_type == 'RELATION':
            result[-1][0] = result[-1][0] + " " + e[0]
            last_type = 'of'
        if e[0] == 'and':
            result.append([e[0],e[1],'AND'])
            last_type = 'AND'

        if e[0] in ['Mr.','Mrs.']:
            result.append([e[0],e[1],'Mr'])
            last_type = 'Mr'

    return [(x[0],x[2]) for x in result]   
     

def iob_2_ner_span(ioblist): 

   # process the annotation, and only extract the tokens where its annotation
   # is PERSON, DATE, O, where O is contains the key relation such as born.
   # return a list of words with its annotation.

    result = []
    last_type =""
    for e in ioblist:
        if e[2] == 'B-PERSON':
            result.append([e[0],e[1],'PERSON'])
            last_type = 'PERSON'
        if e[2] == 'I-PERSON' and last_type == 'PERSON':
            result[-1][0] = result[-1][0] + " " + e[0]
        if e[2] == 'O':
            if last_type != 'O' and (e[1] == 'VBD' or e[1] =='VBN') :
                result.append([e[0],e[1],'O'])
                last_type = 'O'
            elif last_type == 'O' and (e[1] == 'VBD' or e[1] =='VBN') :
                result[-1][0] = result[-1][0] + " " + e[0]
        if e[2] == 'B-DATE':
            result.append([e[0],e[1],'DATE'])
            last_type = 'DATE'
        if e[2] == 'I-DATE' and last_type == 'DATE':
            result[-1][0] = result[-1][0] + " " + e[0]


    return [(x[0],x[2]) for x in result]



def extract_date_of_birth(sentence):
    #extract the date of birth relation from the sentence
 
    results = []
    person =[]
    date = []
    predicate = "DateOfBirth"
    annotation = sentence["annotation"]
    text = sentence["text"]
    ner = iob_2_ner_span(ioblist=[[x[1],x[3],x[4]] for x in annotation])

 

    for i in range(len(ner)):
        if ner[i][1] == 'O' and 'born' in ner[i][0] or 'Born' in ner[i][0]:
            for n in range(len(ner)):
                if ner[n][1] == 'PERSON':
                    person.append([ner[n][0],n])
                    
            for m in range(len(ner)):
                if ner[m][1] == 'DATE':
                    date.append([ner[m][0],m])

    if len(date) == 1:
        if date[0][1] > person[0][1]:
            rel = Relation(person[0][0], predicate, date[0][0])
            results.append(rel)
        elif date[0][1] < person[0][1]:
            rel = Relation(person[0][0], predicate, date[0][0])
            results.append(rel)

    if len(date) >= 2: 
        if person[0][1] > date[0][1]:       
            rel = Relation(person[0][0], predicate, date[0][0])
            results.append(rel)
        elif person[0][1] < date[0][1]:
            rel = Relation(person[0][0], predicate, date[0][0])
            results.append(rel)

    return results

def extract_has_parent(sentence):
#extract the has parent relation from sentence.

    out = []
    predicate = "HasParent"
    annotation = sentence["annotation"]
    text = sentence["text"]
    words = iob_2_ner_span_parent(ioblist=[[x[1], x[3],x[4]] for x in annotation])

    parents = []

    son = ''
    
    find_born = False

    for i in range(len(words)):
        if words[i][1] == 'PERSON':
            if son == '':
                son = words[i][0]
            else:
                if i > 0 and (words[i-1][1] == 'TO' or words[i-1][1] == 'RELATION'):
                    if words[i-1][1] == 'RELATION':
                        parents.append(words[i][0])

                    else:
                        for j in range(i-1):
                            if words[j][1] == 'BORN':
                                find_born = True
                                break
                        if find_born:
                            parents.append(words[i][0])
                            find_born = False


                elif i > 0 and words[i-1][1] == 'AND' and len(parents) != 0:
                    parents.append(words[i][0])
                elif i > 2 and words[i-2][1] == 'AND' and words[i-1][1] == 'Mr':
                    parents.append(words[i][0])
                elif i > 2 and words[i-2][1] == 'TO' and words[i-1][1] == 'Mr':
                    parents.append(words[i][0])
                elif i > 2 and words[i-2][1] == 'RELATION' and words[i-1][1] != 'PERSON':
                    parents.append(words[i][0])
    if len(parents) != 0:
        for p in parents:
            rel = Relation(son, predicate, p)
            out.append(rel)
    return out

   