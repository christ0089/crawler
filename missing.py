#!/usr/bin/python3

import json

with open('data/keywords.json') as f:
    cac= json.load(f)

hash= dict()

for line in cac:
    hash[line]= 1

cac2= open('imgUrls.txt')

for po in cac2:
    ls= po.split(':')[0]
    if ls in hash: hash[ls]+= hash[ls] + 1

for k, v in hash.items():
    if v == 1: print(k)

f.close()
cac2.close()