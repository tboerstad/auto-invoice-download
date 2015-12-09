import requests
from bs4 import BeautifulSoup
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="User name", required=True)
parser.add_argument("-p", "--password", help="Password",  required=True)

args = parser.parse_args()

data = {'username' : args.username,
        'password' : args.password}

s    = requests.session();
resp = s.post('https://www.onecall.no/login',data=data)
resp = s.get('https://www.onecall.no/minesider/forbruk')
soup = BeautifulSoup(resp.content)

invoicetable  = soup.find("table",{"id":"lastinvoices"})
rows          = invoicetable.findAll('tr')
newestInvoice = rows[1].findAll('td')

newestInvoicePdf = newestInvoice[-1].contents[0]['href']
pdfLink = 'https://www.onecall.no'+newestInvoicePdf

with open('onecall.pdf', 'wb') as handle:
     response = s.get(pdfLink, stream=True)
     for block in response.iter_content(1024):
         handle.write(block)

bill = []
for j in range(3):
    bill.append(newestInvoice[j].text.strip().replace(',','.'))

with open('onecall.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(bill)
