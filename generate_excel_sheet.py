import xlsxwriter
import time
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--name",  required=True)
parser.add_argument("-a", "--account",  required=True)
parser.add_argument("-t", "--text", required=True)
parser.add_argument("-f", "--file", required=True)

args = parser.parse_args()

workbook = xlsxwriter.Workbook('refusjon.xlsx')
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': True,'font_size':18})
worksheet.write('A1', args.text, bold)

bold_small = workbook.add_format({'bold': True,'font_size':12,})
normal = workbook.add_format({'font_size':12})
worksheet.write('A3', 'Navn', bold_small)
worksheet.write('A4', 'Konto', bold_small)
worksheet.write('B3', args.name, normal)
worksheet.write('B4', args.account, normal)

n = workbook.add_format({'font_size':10,'border':1});
worksheet.write('A6','Vedlegg',n);
worksheet.write('B6','Dato',n);
worksheet.write('C6','Beskrivelse',n);
worksheet.write('D6','Beløp',n);
worksheet.write('E6','Sum kategori',n);
worksheet.write('F6',' Selskap ',n);
worksheet.write('G6',' Prosjekt ',n);

n = workbook.add_format({'font_size':10,'left':1,'right':1});

currentRow = 6
acc = 0
with open(args.file,'r') as f:
    reader = csv.reader(f)
    for row in reader:
        for c, col in enumerate(row):
            worksheet.write(currentRow, c, col,n)
            if c == 3:
                try:
                    val = float(col)
                    acc = acc + float(col)
                except:
                    pass
        currentRow = currentRow+1

n = workbook.add_format({'font_size':10,'left':1,'right':1,'top':1,'bottom':1});

for c in range(7):
    worksheet.write(currentRow,c,'',n)
worksheet.write(currentRow,3,acc,n)
currentRow = currentRow+2

col = ["Dato","Sign.","Attestert"]

for c,v in enumerate(col):
    worksheet.write(currentRow,c,v,n)

date = time.strftime("%d.%m.%Y")
col = [date,"",""]

currentRow = currentRow+1

for c,v in enumerate(col):
    worksheet.write(currentRow,c,v,n)

worksheet.set_column(0, 0, 10)
worksheet.set_column(1, 2, 20)
worksheet.set_column(4, 4, 10)
worksheet.set_row(12, 30)

workbook.close()
