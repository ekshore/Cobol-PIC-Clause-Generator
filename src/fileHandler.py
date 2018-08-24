import csv
import os

class fileHandler:

  def __init__(self):
    self.lineGenerator = self.createGenerator()
    try:    
      self.inFile = open(self.getInfile(), 'r')
      self.outFile = open('../output/pictureClauses.txt', 'w')
    except:
      print ('Error opening file')
      exit()


  def getInfile(self):
    for file in os.listdir(os.getcwd() + '/../resources'):
      if file.endswith('.csv'):
        if input(file + ' : is this the correct file for the PCS Y/N?  ' ).upper() == 'Y':
          return '../resources/' + file


  def createGenerator(self):
    reader = csv.reader(self.inFile)
    rowNum  = 0 

    for row in reader:
      charCount = 0
      line = ''
      rowNum += 1
      if rowNum < 4: continue

      for column in row[1 : ]:
        charCount += 1

        if column != '':
          line += column
        else:
          line += ' '
        if charCount > 132 : break

      if line.isspace(): continue

      yield line


