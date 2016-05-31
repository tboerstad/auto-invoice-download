import requests
from bs4 import BeautifulSoup
import csv
import argparse
import re
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="User name", required=True)
parser.add_argument("-p", "--password", help="Password",  required=True)

args = parser.parse_args()

data = {'userId'   : args.username,
        'password' : args.password}

s    = requests.session()
resp = s.post('https://telia.no/min-side-login?p_p_id=auth_WAR_authportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_auth_WAR_authportlet_javax.portlet.action=login', data=data)

BASE_URL = 'https://min-side.telia.no/'
resp = s.get(BASE_URL+'/invoices')


soup = BeautifulSoup(resp.content)
invoiceTable = soup.find("tbody")

rows = invoiceTable.findAll("tr")
newestInvoice = rows[0].findAll("td")

pdfLink = newestInvoice[1].contents[1]['href']

with open('telia.pdf', 'wb') as handle:
    response = s.get(BASE_URL+'/'+pdfLink, stream=True)
    for block in response.iter_content(1024):
        handle.write(block)

v = [s.text.strip().replace(',', '.') for s in newestInvoice]

dates = re.findall("\d\d\.\d\d\.\d\d\d\d", v[0])
amount = re.findall("\d+\.\d+",v[2])

description = 'mobilregning ( fra ' + dates[0] + ' til ' + dates[1] + ') '
bill = ['1', v[3], description, amount ,'','','']

with open('invoices.csv', 'a+') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(bill)
