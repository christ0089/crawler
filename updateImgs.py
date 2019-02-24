#!/usr/bin/python3
# Firebase imports
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db

import json
import time
import re
# from sklearn.feature_extraction.text import TfidfVectorizer
# from unsplash.api import Api
# from unsplash.auth import Auth


# client_id = "b88a0c3cdaba27de042293268caffaa460a689d5c7bc115a8b4bbd59f7f5f177"
# client_secret = "b3c11f61346871a40d2924658828aa3995129df46cf6c1ddac8bdab5792acfb0"
# redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'


def getImgUrls(API):
    with open('missingKw.json') as f:
        keywords= json.load(f)
    urls= open('imgUrls.txt', 'a')
    for ID in keywords:
        # time.sleep(6)
        res= API.search.getPhotosWithUrlAndId(keywords[ID])
        if not len(res) >= 1: 
            print('could not get image for', keywords[ID])
            print(ID)
        else: 
            urls.write(ID)
            urls.write(':')
            urls.write(res[0]['url'])
            urls.write('\n')
            # print(ID)
            # print(res[0]['url'])
    f.close()
    urls.close()

def updateImgs():
    urlFile= open('imgUrls.txt')
    for line in urlFile:
        pts= line.split('|')
        ID= pts[0]
        url= pts[1]

        # db.reference('/AllArticles/'+ID).update({
        #    'CoverImg':url 
        # })

# auth = Auth(client_id, client_secret, redirect_uri)
# api = Api(auth)
# updateImgs()
pattern = re.compile('<div class=\\"entry-content\\">')
newContent= open('newContent.json', 'w+')
with open('data/newTags.json') as f:
    tags= json.load(f)
urls= open('imgUrls.txt')
hashd= dict()
for line in urls:
    pts= line.split('|')
    hashd[pts[0]]= pts[1]
for line in tags:
    tag= re.sub(pattern, '<div class=\"entry-content\"><img src="'+hashd[line]+'">', tags[line])
    hashd[line]= hashd[line] + '|' + tag

json.dump(hashd, newContent, ensure_ascii=False)
# getImgUrls(api)
