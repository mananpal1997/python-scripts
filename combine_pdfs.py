import PyPDF2, os

# Get all the PDF filenames.
pdfFiles = []
for filename in os.listdir('C:\\Python34\\'):
    if filename.endswith('.pdf'):
        #command="cp "+filename+" temp.pdf; qpdf --password='' --decrypt temp.pdf "+filename
        #os.system(command)
        pdfFiles.append(filename)
pdfFiles.sort()

pdfWriter = PyPDF2.PdfFileWriter()

# Loop through all the PDF files.
for filename in pdfFiles:
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # Loop through all the pages (except the first) and add them.
    for pageNum in range(1, pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)
        pdfWriter.addPage(pageObj)

# Save the resulting PDF to a file.
pdfOutput = open('combined.pdf', 'wb')
pdfWriter.write(pdfOutput)
pdfOutput.close()
