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

def getLinks(url, pageNum):
    links= []
    url+= "/" + str(pageNum)
    rqst = req.Request(url)
    html = req.urlopen(rqst)
    txt = html.read().decode('utf-8')
    soup = bs(txt, 'html.parser')
    for header in soup.find_all('h2'):
        link = header.find('a', href=True)
        #file.write(link)
        links.insert(0, link['href'])
    return links

def crawl(url, iterations, arts, auths):
    
     # REGEX that substitute garbage content
    blogLinks = re.compile(r".*<a.*blog\.seccionamarilla\.com\.mx.*")
    eoa = re.compile(r".*<h3>También podría interesarte:</h3>.*")
    s_a_r = db.reference().child('Seccion_Amarilla')
    
    for i in range(1, (iterations+1)):
        links = getLinks(url, i)
        
        for link in links:
            time.sleep(random.randint(1, 4))
            linkReq = req.Request(link)
            linkRes = req.urlopen(linkReq)
            html = linkRes.read().decode('utf-8')
            article_soup = bs(html, 'html.parser')
            # String that will hold the author's social media info
            socs = ''
            articleContent
            author
            author_link
            # Getting the tag where the article content is
            for articleContent in article_soup.find_all("div", "entry-content"):
                # Substituting unuseful tags
                articleContent += re.sub(eoa, "", str(articleContent))
                articleContent += re.sub(blogLinks, "", articleContent)
            for auth in article_soup.find_all("div", "entry-author"):
                # Getting the author's name and link to its blog profile
                author = str(auth.find('span').find('a').text)
                author_link = str(auth.find('span').find('a')['href'])
                # Checking if author has links to its social networks
                socials = []
                socialSpan = article_soup.find('span', 'saboxplugin-socials')
                if socialSpan:
                    for soc in socialSpan.find_all('a'):
                        socials.append(soc)
                if len(socials) != 0:
                    socs = '||'.join(soc for soc in socs)
                else:
                    socs = "None"
            if not articleContent in arts:
                s_a_r.child("Articles").push({
                    'author': author,
                    'content': articleContent
                })
                arts[articleContent] = 1
            if not author_link in auths:
                s_a_r.child("Authors").push({
                    'name': author,
                    'link': author_link,
                    'contact': socs
                })
                auths[author_link] = 1




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
