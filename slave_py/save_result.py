import requests
import json

results = {
    u'Price.Buford@yahoo.com': {u'errorCode': 0, u'status': 403,
                                u'message': u"[invalid.profile.access]. You don't have access to the profile"},
    u'yHarvey@yahoo.com': {u'errorCode': 0, u'status': 404, u'message': u"Couldn't find member"},
    u'Douglas.Michaela@Stracke.com': {u'distance': 3, u'publicProfileUrl': u'https://www.linkedin.com/in/xxx'}
}
payload = json.dumps(results)

r = requests.post('http://localhost:8000/result', data={'result': payload})
print r.text
