import csv

text=[]
with open('get.txt','r',encoding='utf-8') as f:
        text=f.read()
        a=text.split

a = text.split('\n')
b = [x for x in a if x]

i = b.index('TOTALT $ BETALE')
price = b[i-1].replace(',','.')
i = b.index('Betalingsfrist')
date = b[i+1]
i = b.index('PERIODE')
period = "bredbaand ({0})".format(b[i+2])

bill = ['',date,period,price,'','','']


with open('invoices.csv','a+') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(bill)        
