"""打开pdf格式或者word"""

from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open


def read_pdf(pdf_file):
    """转换pdf格式的文件为txt"""
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdf_file)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content


pdf_file = urlopen("http://pythonscraping.com/pages/warandpeace/chapter1.pdf")
outputString = read_pdf(pdf_file)
print(outputString)
pdf_file.close()
