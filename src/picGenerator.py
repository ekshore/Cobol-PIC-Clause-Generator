#!/usr/bin/python
# Written by Caleb Ekstrand
# 2/7/2017
# Version 2.0
# This script is to take in a printer spacing chart in comma demlimited format.
# And ouput the nessary picture clauses in COBOL code.

#fileName = input('Please enter file name of the Printer Spacing Chart: ')

from fileHandler import fileHandler

fHandler = fileHandler()

def main():
  for line in fHandler.lineGenerator:
    print(line)
    if input("Do you wish to process this line Y/N?  ").upper() == 'Y':
      dataProcessing(line)
      fHandler.outFile.write('\n\n')


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
    fHandler.outFile.write('\n' + printLine[ : 72])
    fHandler.outFile.write('\n' + exPrintLine)
    print(ran)
  else:
    fHandler.outFile.write('\n' + printLine)
    print(printLine)

main()
