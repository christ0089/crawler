#!/usr/bin/python3
# Firebase imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pickle
import json
import io



def downloadArticles(refDb):
    articles = refDb.child('Articles')
    arts = articles.get()
    articlesFile = io.open("articles.json", 'w+', encoding='utf8')
    articlesFile.write('[')
    for article in arts:
        art = arts[article]
        # print(article)
        art["Subtitle"] = art["Title"]
        json.dump(art, articlesFile, ensure_ascii=False)
        articlesFile.write('\n')
        articlesFile.write(',')
        # print(art)
    articlesFile.write(']')

def downloadAuthors(refDb):
    authorsFile= io.open('authors.json', 'w+', encoding='utf8')
    # authorsFile.write('[')

    authors= refDb.child('Authors')
    auths= authors.get()
    json.dump(auths, authorsFile, ensure_ascii=False)
    # for auth in auths:
    #     print(auth)
    #     print('----------------------')
    #     print(auths[auth])
    #     print('======================')

cred = credentials.Certificate('techNautsCredentials.json')
firebase_admin.initialize_app(cred,  {
    'databaseURL': 'https://technauts-fcfa8.firebaseio.com'
})

s_a_r = db.reference().child('Seccion_Amarilla3')

downloadAuthors(s_a_r)

# for art in arts:
#     print(arts.get(art))



# for key, val in arts.items():
#     imgs+= 1
#     val["Subtitle"]= val["Title"]
#     # print('KEY\n\n\n\n {0}: {1}'.format(key, val["Subtitle"]))

# print(imgs, "total images")

    # print(a["CoverImg"])
#     for key, val in arts.items():
#         print('KEY\n\n\n\n {0}: {1}'.format(key, val["CoverImg"]))
#         # for k, v in val.items():
#         #     if k == "CoverImg":
#         #         print(v['CoverImg'])
#             # print('KKK\n\n\n\n {0}: {1}'.format(k, v))
#     print('---------')

