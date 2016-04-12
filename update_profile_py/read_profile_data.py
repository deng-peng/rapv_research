# -*- encoding: utf-8 -*
import codecs
import json
import random
f = codecs.open('profile_data.txt', 'r', encoding='utf-8')
peoples = []
for line in f.readlines():
    jObj = json.loads(line)
    peoples.append(jObj)

people = random.choice(peoples)
print people['family_name']