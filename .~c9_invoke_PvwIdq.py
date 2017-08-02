# get a token - works python3
'''
urllib has been split up in Python 3. The urllib.urlencode() function is
now urllib.parse.urlencode(), and the urllib.urlopen() function is now
urllib.request.urlopen().
'''
import urllib
import urllib.parse
import urllib.request
import urllib.error
import re
import string
import json
import dpath.util
from pprint import pprint

import nltk
# from nltk.corpus import reuters
# categories = reuters.categories()
# print("Number of Categories:",len(categories))
# print(categories[0:9],categories[-10:])
# words = reuters.words()
# print("number of words", len(words) )
# print("first 10 words:", words[0:9])

def get_token():
    url = 'https://api.healthgraphic.com/v1/login.json'
    values = {'email' : 'om','password' : 'zoo987BUG'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    '''
In HTTP there are two ways to POST data: application/x-www-form-urlencoded
and multipart/form-data (MIME types): send a list of name/value pairs to the
server. Depending on the type and amount of data being transmitted, one
of the methods will be more efficient than the other. To understand why,
you have to look at what each is doing under the covers. For
application/x-www-form-urlencoded, the body of the HTTP message sent to
the server is essentially one giant query string -- name/value pairs are
names are separated from values by the  equals symbol (=). See below.
names are separated from values by the  equals symbol (=). See below.

nb non-alphanumeric (binary) data is sent as multipart/form data

req (see below) is an object made using a class. This class used is an abstraction of a URL request.
class urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None
NB  should be a string containing a valid URL.
NB data must be an object specifying additional data to send to the server, or None if no such data is needed. 
Currently HTTP requests are the only ones that use data. This here is an HTTP POST method that uses 
the application/x-www-form-urlencoded format mentioned above'''

    data = urllib.parse.urlencode(values) # "email=paddy10tellys@gmail.com&password=zoo987BUG"
    data = data.encode('ascii')
    req = urllib.request.Request(url, data, headers)  #  nb the Request object
    try:
        with urllib.request.urlopen(req) as response:
            response_body = response.read()
            response_body = response_body.translate(None, b'\r\n') # None indicates deletion, b indicates is binary 
            response_body = response_body.decode()  # bytes to ascii
            response_body = re.sub('['+string.punctuation+']', '', response_body)  # remove all the punctuation
            token = response_body[-31:]  # the last 31 chars
            print('Server reached...\nFufilling request...')
        return token
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        else:
            print('wtf is going on?')
    
''' The .translate line above removes carriage returns & new lines but is actually extremely complicated. Read
https://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python/3939381#3939381
'''

def get_conditionSx():
    datalink = 'https://api.healthgraphic.com/v1/conditions/acute_sinusitis/symptoms?page=1&per_page=10'

    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'token': get_token()
      }

    try:
        url = datalink
        req = urllib.parse.urlencode(headers)
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        respData = resp.read()
        encoding = resp.info().get_content_charset('utf-8')
        respData = json.loads(respData.decode(encoding))  # <class 'dict'>
        pprint(respData)
        print('+++++++ end of pretty print ++++++++++++++++')

        print(respData['response']['symptoms']['response'][0]['name'])
        print('******')

        for item in respData['response']['symptoms']['response']:
            print(item['name'])
        print('******')

        query = dpath.util.get(respData, 'response/symptoms/response/0/name')
        print(query)  # see https://github.com/akesterson/dpath-python


        # resp_dict = {
        #     "a": {
        #         "b": {
        #         "3": 2,
        #         "43": 30,
        #         "c": [],
        #         "d": ['red', 'buggy', 'bumpers'],
        #         }
        #     }
        # }

        #query = dpath.util.get(resp_dict, 'a/b/43')



    except Exception as e:
        print(str(e))


get_conditionSx()










