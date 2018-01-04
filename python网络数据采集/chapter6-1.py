from urllib.request import urlopen
from io import StringIO
import csv

data = urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv")\
    .read().decode("utf-8", 'ignore')
dataFile = StringIO(data)
dictReader = csv.DictReader(dataFile)

print(dictReader.fieldnames)
print("----------------")

for row in dictReader:
    print(row['Name'] + "--书写日期--：" + row['Year'])
