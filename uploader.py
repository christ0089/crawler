#!/usr/bin/python3
# Firebase imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import io

cred = credentials.Certificate('techLinkCredentials.json')
techLinkRef= firebase_admin.initialize_app(cred,  {
    'databaseURL': "https://teclink-8e19c.firebaseio.com"
},)



# Code for uploading authors
# authsRef= db.reference().child('UserNode').child('Users')
# with open('authors.json') as ff:
#     authors= json.load(ff)
# keys= open('newAuthorsIds.txt', 'w+')
# mapFile= io.open('keyMap.json', 'w+', encoding='utf8')
# keyMap= dict()

# for auth in authors:
#     id= authsRef.push(authors[auth]).key
#     keys.write(auth)
#     keys.write(':')
#     keys.write(id)
#     keys.write('\n')
#     keyMap[auth]= id

# json.dump(keyMap, mapFile, ensure_ascii=False)

# Code for uploading articles
# with open('keyMap.json') as fff:
#     keyMap= json.load(fff)
# artsRef= db.reference().child('Articles').child('AllArticles')
# articleKeys= open('articleKeys.txt', 'w+')
# with open('articles.json') as f:
#     articles = json.load(f)
# for article in articles:
#     article['Uploader'] =  keyMap[article['Uploader']].rstrip()
#     article["Status"]= 'Received'
#     article['CoverImg'] = 'https://scontent.fmfe1-1.fna.fbcdn.net/v/t1.0-9/46520239_1099313216906413_5088531725923909632_n.png?_nc_cat=108&_nc_ht=scontent.fmfe1-1.fna&oh=75848731aad10eb6973ab3127fca9104&oe=5CF90EAF'
#     # print(article)
#     id= artsRef.push(article).key
#     articleKeys.write(id)
#     articleKeys.write('\n')

