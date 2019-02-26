#!/usr/bin/python3
# Firebase imports
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db

import json
import time
import re
# from sklearn.feature_extraction.text import TfidfVectorizer
from unsplash.api import Api
from unsplash.auth import Auth


client_id = "b88a0c3cdaba27de042293268caffaa460a689d5c7bc115a8b4bbd59f7f5f177"
client_secret = "b3c11f61346871a40d2924658828aa3995129df46cf6c1ddac8bdab5792acfb0"
redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'


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
            urls.write('|')
            urls.write(res[0]['medium'])
            urls.write('|')
            urls.write(res[0]['small'])
            urls.write('|')
            urls.write(res[0]['name'])
            urls.write('\n')
            # print(ID)
            # print(res[0]['url'])
    f.close()
    urls.close()


def updateTags():
    pattern = re.compile('<div class=\\"entry-content\\">')
    newContent= open('newContent.json', 'w+')
    with open('data/newTags.json') as f:
        tags= json.load(f)
    urls= open('imgUrls.txt')
    hashd= dict()
    for line in urls:
        pts= line.split('|')
        hashd[pts[0]]= pts[1] + '|' + pts[2] + '|' + pts[3]
        # print(pts[0])
        # print(pts[1])
        # print(pts[2])
        # print(pts[3])

    for line in tags:
        pts= hashd[line].split('|')
        print(pts[0])
        print(pts[1])
        print(pts[2])

        tag= re.sub(pattern, '<div class=\"entry-content\"><img src="'+pts[0]+'">' + "<div>Photo from " + pts[2].rstrip() + " by Unsplash</div>", tags[line])
        hashd[line]= tag + '|' + pts[1]
        print(hashd[line])

    json.dump(hashd, newContent, ensure_ascii=False)
    newContent.close()
    f.close()

updateTags()
# auth = Auth(client_id, client_secret, redirect_uri)
# api = Api(auth)
# getImgUrls(api)
