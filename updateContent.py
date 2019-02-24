#!/usr/bin/python3
import json
import io   
# Firebase imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate('techLinkCredentials.json')
techLinkRef = firebase_admin.initialize_app(cred,{
    'databaseURL': "https://teclinx-8e19c.firebaseio.com"
})
db.reference()
with open('newContent.json') as f:
    content= json.load(f)

    for ID in content:
        print(ID)
        pts= content[ID].split('|')
        imgUrl= pts[0]
        html= pts[1]
        print(imgUrl)
        print(html)
