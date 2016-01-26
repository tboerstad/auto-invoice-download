import requests
from bs4 import BeautifulSoup
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="User name", required=True)
parser.add_argument("-p", "--password", help="Password",  required=True)

args = parser.parse_args()

data = {'userId'   : args.username,
        'password' : args.password}

s    = requests.session()
resp = s.post('https://netcom.no/min-side-login?p_p_id=auth_WAR_authportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_auth_WAR_authportlet_javax.portlet.action=login', data=data)
resp = s.get('https://min-side.netcom.no/invoices')


soup = BeautifulSoup(resp.content)
invoiceTable = soup.find("tbody")
rows = invoiceTable.findAll("tr")
newestInvoice = rows[0].findAll("td")
pdfLink = newestInvoice[8].contents[1]['href']

with open('netcom.pdf', 'wb') as handle:
    response = s.get(pdfLink, stream=True)
    for block in response.iter_content(1024):
        handle.write(block)

v = [s.text.strip().replace(',', '.') for s in newestInvoice]

bill = ['1', v[4], 'mobilregning (' + v[2] + ')', v[6].split(' ')[0] ,'','','']

with open('invoices.csv', 'a+') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(bill)
