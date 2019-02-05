#!/usr/bin/python3

# This script crawls articles from the entrepreneurship and tech section. The first one
# has 9 pages and the latter has 23

# Firebase imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# Newtork imports
from urllib import request as req
# Parsing imports
from bs4 import BeautifulSoup as bs
import re
# Other imports
import time
import random
import datetime

# This function gets the links from a page given a url and the page number
def getLinks(url, pageNum):
    links= []
    url+= "/" + str(pageNum)
    rqst = req.Request(url)
    html = req.urlopen(rqst)
    txt = html.read().decode('utf-8')
    soup = bs(txt, 'html.parser')
    for header in soup.find_all('h2'):
        link = header.find('a', href=True)
        links.append(link['href'])
    return links

def crawl(url, iterations, arts, auths):
    
     # REGEX that substitute garbage content
    blogLinks = re.compile(r".*<a.*blog\.seccionamarilla\.com\.mx.*")
    eoa = re.compile(r".*<h3>También podría interesarte:</h3>.*")
    s_a_r = db.reference().child('Seccion_Amarilla')
    
    for i in range(1, (iterations+1)):
        links = getLinks(url, i)
        
        for link in links:
            print(link)
            time.sleep(random.randint(3, 7))
            linkReq = req.Request(link)
            linkRes = req.urlopen(linkReq)
            html = linkRes.read().decode('utf-8')
            article_soup = bs(html, 'html.parser')
            # Getting date info
            date = str(article_soup.find('span', 'date', 'updated').text)
            dParts= date.split(' ')
            day= int(dParts[0])
            mo= dParts[1]
            yr=int( dParts[2])
            if mo == "Ene": mo= 1
            elif mo== "Feb": mo= 2
            elif mo == "Mar": mo = 3
            elif mo== "Abr": mo = 4
            elif mo == "May": mo= 5
            elif mo == "Jun": mo = 6
            elif mo == "Jul": mo= 7
            elif mo == "Ago": mo= 8
            elif mo == "Sep": mo= 9
            elif mo == "Oct": mo = 10
            elif mo== "Nov": mo = 11
            elif mo == "Dic": mo = 12
            timestamp= int(datetime.datetime(yr, mo, day).timestamp())
            

            titleTag= article_soup.find('h1', 'entry-title')

            # Getting the tag where the article content is
            articleContent = article_soup.find("div", "entry-content")
            articleContent= re.sub(eoa, "", str(articleContent))
            articleContent= re.sub(blogLinks, "", str(articleContent))
            author = article_soup.find("div", "entry-author")
            innerHTML= str(titleTag) + articleContent
            title= str(titleTag.text)
            thumb= str(article_soup.find('div', 'thumb').find('img')['src'])
            # Getting the author's name
            author = str(article_soup.find('span', 'name').find('a').text)
            username= "@" + author
            username= username.replace(' ', '_')
            authID= ''
            if not username in auths:
                action= s_a_r.child("Authors").push({
                    'Emai': '',
                    'CoverImg': "https://firebasestorage.googleapis.com/v0/b/teclink-8e19c.appspot.com/o/User%20Images%2Fplaceholder.png?alt=media&token=7591c228-e4c5-40ee-bbc6-a0aab64476e5",
                    'Followers': 0,
                    'Following': 0,
                    'Name': author,
                    'ProfileImg': "https://firebasestorage.googleapis.com/v0/b/teclink-8e19c.appspot.com/o/User%20Images%2Fprofile_pic.jpg?alt=media&token=ebefced4-a054-4cd3-a806-c8e6b86a62b0",
                    'Skill': "",
                    'Tagline': '',
                    'UserName': username,
                })
                auths[username] = action.key
                authID= action.key
            else: authID= auths[username]
            if not articleContent in arts:
                s_a_r.child("Articles").push({
                    'InnerHTML': innerHTML,
                    'Title': title,
                    'Uploader': authID,
                    'CoverImg': thumb,
                    'Timestamp': timestamp,
                    'Category': 'Tech',
                    'Boosts': 0,
                    'InvBoosts': 0
                })
                arts[articleContent] = 1




cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://technauts-fcfa8.firebaseio.com' 
                })

""""
The page structure is described as follows:
    In the entry point, the articles' links are all wrapped in an h2 tag.
    Once the articles for that page end, one can easily request the next page using the nextPageTemplate.
    The HTML in each article has the author's name and a link to its profile in the plaftorm. Some
    authors also have a link to their social meda accounts.
"""


entrepreneurshipUrl='https://blog.seccionamarilla.com.mx/tag/emprendedores/page/'
TechUrl='https://blog.seccionamarilla.com.mx/tag/tecnologia/page/'

# Dict storing previously queried authors and articles
authors_dict= dict()
articles_dict= dict()

crawl(entrepreneurshipUrl, 9, articles_dict, authors_dict)
crawl(TechUrl, 23, articles_dict, authors_dict)
