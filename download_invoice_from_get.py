import requests
from bs4 import BeautifulSoup
import argparse

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="User name", required=True)
parser.add_argument("-p", "--password", help="Password",  required=True)

args = parser.parse_args()

s    = requests.Session()
resp = s.get('https://login.get.no/login')
soup = BeautifulSoup(resp.content)

data = {'password':args.password,
        'username':args.username}

for item in soup("input"):
    if item.has_attr('name') and item.has_attr('value'):
        if item['name'] not in data:
            data[item['name']] = item['value']

a = s.post('https://login.get.no/login',data=data)
a = s.get('https://www.get.no/logincontroller?returnPage=http%3A%2F%2Fwww.get.no%2Fv3%2Fmin-get%2Ffaktura')
a = s.get('https://login.get.no/?service=https%3A%2F%2Fwww.get.no%2Fportalbackend%2Fj_spring_cas_security_check')
a = s.get('https://www.get.no/logincontroller?loginState=2')

soup = BeautifulSoup(a.content)
il   = soup.find('ul',{'class':'invoice-list'})
rows = il.findAll('li');
cols = rows[0].findAll('div')

pdfLink = cols[1].contents[0]['href']
a       = s.get(pdfLink)

with open('get.pdf', 'wb') as handle:
     response = s.get(pdfLink, stream=True)
     for block in response.iter_content(1024):
         handle.write(block)
