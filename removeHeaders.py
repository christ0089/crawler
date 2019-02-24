#!/usr/bin/python3
# Firebase imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from bs4 import BeautifulSoup as bs
import json
import io
import re

cred = credentials.Certificate('techLinkCredentials.json')
techLinkRef = firebase_admin.initialize_app(cred,  {
    'databaseURL': "https://teclink-8e19c.firebaseio.com"
},)

def changeHeaders():
    keys= open('articleKeys.txt')
    articles= db.reference('/Articles/AllArticles')
    arts= articles.get()
    pattern= re.compile('<h1.*class.*=.*".*entry-title.*">.*</h1>')
    tagMap= dict()
    newTags= open('newTags.json', 'w+')

    for key in keys:
        key= key.rstrip()
        html= arts[key]['InnerHTML']
        # print(html)
        h= re.sub(pattern, '', html)
        tagMap[key]= h
        
    json.dump(tagMap, newTags, ensure_ascii=False)


def writeNewHeaders():
    with open('newTags.json') as f:
        tags= json.load(f)
    for key in tags:
        newHtml= tags[key]
        article = db.reference('/Articles/AllArticles/'+key)
        article.update({
            "InnerHTML": newHtml
        })


# writeNewHeaders()
