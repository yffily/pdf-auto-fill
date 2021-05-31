#! /usr/bin/env python3
import sys
import io
from reportlab.pdfgen import canvas
import reportlab.lib as rll
from PyPDF4 import PdfFileWriter, PdfFileReader, PdfFileMerger
import datetime
from PIL import Image


for i in range(1,13):
	date  = datetime.date(2021,i,1)

	# Load the empty pdf template.
	page = PdfFileReader(open('template.pdf','rb')).getPage(0)

	# Create a second pdf page in ReportLab.
	packet = io.BytesIO()
	can    = canvas.Canvas(packet, pagesize=rll.pagesizes.letter)
	can.setFont("Helvetica",10.5)
	unit   = rll.units.inch
	
	# Add text. Input the coordinates of the text (measured from the bottom 
	# left corner, in inches) and the text to write.
	x,y,txt = 6.5,9.12,'Yes'
	can.drawString(x*unit, y*unit, txt)
	x,y,txt = 1.5,8.55,date.strftime("%m/%d/%Y")
	can.drawString(x*unit, y*unit, txt)
	
	# Add signature. Input the coordinates and size of the signature.
	x,y,size = 1.8,7.9,0.5
	img = Image.open('signature.png')
	a   = img.height/img.width
	can.drawImage('signature.png', x*unit, y*unit, 
	               size*unit, size*a*unit, mask='auto')
	
	# Save and load into pypdf.
	can.save()
	page2  = PdfFileReader(packet).getPage(0)

	# Merge the two pages.
	page.mergePage(page2)

	# Write the result to a pdf file.
	output = PdfFileWriter()
	output.addPage(page)
	fn = f'output/{date.month}-{date.strftime("%B")}.pdf'
	output.write(open(fn,'wb'))
