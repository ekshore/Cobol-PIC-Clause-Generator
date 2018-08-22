#!/usr/bin/python
# Written by Caleb Ekstrand
# 2/7/2017
# Version 2
# This script is to take in a printer spacing chart in comma demlimited format.
# And ouput the nessary picture clauses in COBOL code.

#fileName = input('Please enter file name of the Printer Spacing Chart: ')

import os

for file in os.listdir(os.getcwd()):
  if file.endswith('.csv'):
    if input(file + '   :is the is the correct file for the PCS Y/N?  ').upper() == 'Y':
      fileName = file
      break
    else:continue
try:
  inFile = open(fileName, 'r')
except:
  print ('file failed')
outfile = open('pictureClauses.txt', 'w')


def main():
  record = ''
  n = 0
  for line in inFile:
    n += 1
    if n < 4: continue
    processInput(line)
#    if n > 11: break



#This function sorts through all the commas in the .csv file for the usable data..
def processInput(line):
  charCount, skip = 0, 0
  processedInput, previous, prevValue = '', '', ''

  start = line.find(',')
  for char in line[start: ]:

    if skip > 0:
      skip -= 1
      continue
    if char.isspace(): continue
    if char != ',':
      #This part looks for commas in an edit masks. commas are represented by ",".
      #This if looks for a '"' and then adds a comma to the edit mask and tells the loop to
      #skip the next two iteration character in the string.
      if char == '"':
        processedInput = processedInput + ','
        skip = 2
        previous = char
        charCount += 1
        continue
      if char != '-':
        prevValue = char
      processedInput = processedInput + prevValue
      charCount += 1
    else:
      if previous == ',':
        nextChar = ' '
        processedInput = processedInput + ' '
        charCount += 1

    previous = char
    if charCount > 132: break
  processedInput = processedInput + ' '
  print (processedInput)
  if processedInput.isspace(): return
  if not input("Do you wish to process this line Y/N?  ").upper() == 'Y': return
  dataProcessing(processedInput)
  outfile.write('\n\n')


#This funcion takes the data given by the processInput funcion and processes
#out the data that is needed to generate a Picture clause.
def dataProcessing(line):
  name, dataType, numChars, value, editMask = '', '', 0, '', False
  prev = ''
  currentField = ''
  totChar = 0

  for char in line:
    if char != prev:
      if char.isspace():

        #new field processing
        print(currentField)
        name = input('What would you like the name of the next field to be: ')
        if currentField.isnumeric():
          dataType = '9'
          value = ''
          editMask = False
        else:
          if '.99' in currentField or 'Z9' in currentField:
            editMask = True
            value = currentField
            dataType = ''
          else:
            if prev == 'Y':
              dataType = '9'
              value = ''
            else:
              editMask = False
              value = '"' + currentField + '"'
              dataType = 'X'

        numChars = len(currentField)
        if currentField.count('X') >= numChars:
          value = ""
        picClauseGen(name.upper(), dataType, numChars, value, editMask)
        currentField = ''
        totChar = totChar + numChars

      if prev.isspace():
        name = 'FILLER'
        dataType = 'X'
        numChars = len(currentField)
        value = 'SPACE'
        editMask = False
        picClauseGen(name.upper(), dataType, numChars, value, editMask)
        currentField = ''
        totChar = totChar + numChars

      if prev == '/':
        name = 'FILLER'
        dataType = '9'
        numChars = len(currentField)
        if currentField.count('X') < numChars: value = '"' + currentField + '"'
        picClauseGen(name.upper(), dataType, numChars, value, editMask)
        currentField = ''
        totChar = totChar + numChars

      if char == '/':
        print(currentField)
        name = input('What would you like the name of the next field to be: ')
        dataType = '9'
        numChars = len(currentField)
        value = ''
#        if currentField.count('X') < numChars: value = '"' + currentField + '"'
        picClauseGen(name.upper(), dataType, numChars, value, editMask)
        currentField = ''
        totChar = totChar + numChars

    currentField = currentField + char
    prev = char

  numChars = 132 - totChar
  picClauseGen('FILLER', 'X', numChars, 'SPACE', False)


#This function takes the data that it is given by the processing function and generates a PICTURE clause.
"""@name - name of the field
  @type - value type
  @chars - number of characters
  @value - literal starting value
  @edit mask - boolean
  """
def picClauseGen(name, type, chars, value, editMask):
  printLine, exPrintLine = '', ''
  while len(printLine) < 12:
    printLine = printLine + ' '

  printLine = printLine + '05 {}'.format(name)

  while len(printLine) < 36:
    printLine = printLine + ' '

  if editMask:
    printLine = printLine + 'PIC {}.'.format(value)
  else:
    printLine = printLine + 'PIC {}({})'.format(type, chars)
    if len(value) > 1:
      while len(printLine) < 48:
        printLine = printLine + ' '
      printLine = printLine + "VALUE   {}.".format(value)
    else:
      printLine = printLine + '.'

  if len(printLine) > 72:
    exPrintLine = '      -                            {}'.format(printLine[73: ])
    outfile.write('\n' + printLine[ : 72])
    outfile.write('\n' + exPrintLine)
    print(ran)
  else:
    outfile.write('\n' + printLine)
    print(printLine)

main()
