# -*- encoding: utf-8 -*
import codecs
import json
import random


class Profile(object):
    family_name = ''
    given_name = ''
    industry = ''
    organization = ''
    start_year = 0
    start_month = ''
    title = ''
    description = ''


class ProfileMaker(object):
    def __init__(self):
        self.profile = Profile()
        self.profile.start_year = random.choice([2008, 2009, 2010, 2011, 2012, 2013, 2014])
        self.profile.start_month = random.choice(
            ['January', 'February', 'March', 'April', 'May', 'June', 'Juny', 'August', 'September', 'October',
             'November', 'December'])

    def make(self):
        f = codecs.open('profile_data.txt', 'r', encoding='utf-8')
        peoples = []
        for line in f.readlines():
            jObj = json.loads(line)
            peoples.append(jObj)

        people = random.choice(peoples)
        self.profile.family_name = people['family_name']

        people = random.choice(peoples)
        self.profile.given_name = people['given_name']

        people = random.choice(peoples)
        self.profile.industry = people['industry']

        exp = None
        while exp is None:
            people = random.choice(peoples)
            if 'experience' in people and len(people['experience']) > 0:
                exp1 = people['experience'][0]
                if 'description' in exp1:
                    exp = exp1

        self.profile.organization = exp['organization'][0]['name']
        self.profile.title = exp['title']
        self.profile.description = exp['description']

        print self.pretty_obj(self.profile)
        return self.profile

    @staticmethod
    def pretty_obj(obj):
        return '\r\n'.join(['%s:%s' % item for item in obj.__dict__.items()])
