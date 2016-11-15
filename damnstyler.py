# -*- coding: utf-8 -*-

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
# ========== СДЕЛАТЬ ===========
# 0 - встречая комментарий игнорируем его содержимое то соотв разделителя
# 1 - вставка строки с копирайтом +
# 2 - замена табуляций на пробелы ----- заменяем на calcTabsConst пробелов +
# 3 - изменение констант включения ---- такие строки переписываем сами +
# 4 - вставка пробела после цикла ----- переписываем строку +
# 5 - сдвиг откр фигурных скобок ------ если строка начинается с фигурн откр
# --- то тогда мы вставляем её с пробелом на последнее значащее место +
# 6 - 
# 7 - один пробел перед public +
# 8 - написать функцию поиска парной скобки
# 9*- дописать до опционального настраиваемого скрипта 
# 
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


import math
import os
import string
import sys

def strInsert(strArg, strTemp, position):
  if(type(strArg) != str or  type(strTemp) != str or type(position) != int):
     pass
  else:
     return strArg[0 : position] + strTemp + strArg[position :]

def strShift(strArg, position, count):
  if(type(strArg) != str or type(position) != int or type(count) != int):
     pass
  else:
     return strArg[0 : position] + strArg[(position + count) :]

def genIncludeConst(nameOfFile):
  incName = "INCLUDE_"
  for z in nameOfFile.split("."):
    incName = incName + z.upper() + "_"
  return incName

def reverse(strArg):
  if(type(strArg) != str):
    pass
  else:
    res = ""
    for i in range(len(strArg)):
      res = res + strArg[-i-1]
    return res

def findLast(strArg, ch):
  if(type(strArg) != str or len(ch) > 1 or type(ch) != str):
    pass  
  else:
    return (len(strArg) - reverse(strArg).find(ch)-1)

def findLastNonSpacePosBefore(strArg, before):
  if(type(strArg) != str or type(before) != str):
    pass  
  else:
    lastWord = strArg[:strArg.find(before)].strip().split()[-1]
    return len(lastWord) + strArg[:strArg.find(before)].rstrip().rfind(lastWord)

calcTabsConst = 2
namesOfCicles = ["for", "while", "if", "else if"]
typeOfPrivacy = ["private:", "public:", "protected:"]
blankStrFlag = 0

stdLibNames = [" ostream",  "istream", " fstream"," cout ", " cin ", " ofstream", "ifstream", " fstream", " endl", "queue<", "stack<", "vector<" ]

# --главная_первый_проход-- {
for i in range(1, len(sys.argv)):
  print("Parsing file " + (sys.argv[i]).upper() + " ... ")
  inFile = open(sys.argv[i],"rb")
  stringList = (str(inFile.read())).splitlines() # .decode("WINDOWS-1251").encode("UTF-8")
  inFile.close()
  for k in range(len(stringList)):
    if(stringList[k].startswith("//")):
      print(str(k) + ": COMMENT " + stringList[k])

    if(stringList[k].startswith("#include")):
      continue

    if(stringList[k].startswith("#") and 
          len(stringList[k].split()) == 2):
      stringList[k] = stringList[k].split()[0] + " " + genIncludeConst(sys.argv[i])
      continue
      print(str(k) + ": DEFINES " + stringList[k])
    elif(stringList[k].startswith("#endif")):
      stringList[k] = stringList[k].split()[0] + "  // " + genIncludeConst(sys.argv[i])
      print(str(k) + ": ENDDEFS " + stringList[k])

    while(stringList[k].startswith("\t")):
      stringList[k] = stringList[k].expandtabs(calcTabsConst)
      print(str(k) + ": TABULAT " + stringList[k])
    
    for cicleName in namesOfCicles:
      if(stringList[k].find(cicleName) >= 0 and stringList[k][stringList[k].find(cicleName)+len(cicleName)] != " "):
        stringList[k] = strInsert(stringList[k], " ", stringList[k].find(cicleName) + len(cicleName)) 
        print(str(k) + ": CONDSTATE " + stringList[k])  
    
    for privacyName in typeOfPrivacy:
      if(stringList[k].lstrip().startswith(privacyName)):
        stringList[k] = " " + privacyName + stringList[k].lstrip()[len(privacyName):]
        print(str(k) + ": PRIVACY " + stringList[k])
        if(blankStrFlag == 0): 
          stringList[k] = "\n" + stringList[k]
        else:
          stringList[k-1] = stringList[k-1][:len(stringList[k])-1] 
    
    if(stringList[k-1].lstrip().startswith("class ")):
      blankStrFlag = 1
    else:
      blankStrFlag = 0 
    #####################################################
    if((stringList[k].lstrip()).startswith("{") and
          not (stringList[k].lstrip()).endswith("}")):
      stringList[k] = stringList[k].lstrip();
      stringList[k] = strShift(stringList[k], 0, 1)
      if(stringList[k-1].find("//") > 0):
        insPos = findLastNonSpacePosBefore(stringList[k-1], "//")
      	stringList[k-1] = stringList[k-1][:insPos] + " {" + stringList[k-1][insPos:]  
      else:
        stringList[k-1] = stringList[k-1].rstrip() + " {"
      print(str(k) + ": BRACES " + stringList[k-1])		
    ########################################################
	

    if(stringList[k].find("{") > 0 and stringList[k][stringList[k].find("{")-1] != " "):
      stringList[k] = strInsert(stringList[k], " ", stringList[k].find("{"))
#linepartition
    if(stringList[k].lstrip().find("//") > 0):
      stringList[k] = (stringList[k][:stringList[k].find("//")]).rstrip() + "  // " + (stringList[k][(stringList[k].find("//")+2):]).lstrip()
    elif(stringList[k].lstrip().find("//") == 0):
      stringList[k] = "// " + stringList[k].lstrip()[2:].lstrip()

    if(len(stringList[k].rstrip()) > 80):
      print(str(k) + ": NEEDLINEPARTITION WAS" + stringList[k])
      listHalfLen = len(stringList[k].split()) // 2
      stringFormattingSymb = " "
      if(stringList[k].find("//") > 0):
        if(k > 0):
          stringList[k] = stringList[k][:stringList[k].find("//")].rstrip() + "\n" + " " * stringList[k-1].find(stringList[k-1].lstrip())+ stringList[k][stringList[k].find("//"):].rstrip()
          print(str(k) + ": WANTED TO INSERT SPACES")
        else:
          stringList[k] = stringList[k][:stringList[k].find("//")].rstrip() + "\n" + stringList[k][stringList[k].find("//"):].rstrip()
      elif(stringList[k].find("//") == 0): 
        stringList[k] = strInsert(stringList[k], "\n// ", len(stringList[k]) // 2 + stringList[k][:len(stringList[k]) // 2].find(" ")).rstrip()
        stringList[k] = stringList[k][:stringList[k].find("\n")].rstrip() + stringList[k][stringList[k].find("\n"):].lstrip()
      elif(stringList[k].find('"') < stringList[k].find(stringList[k].split()[listHalfLen]) and
          (stringList[k].find(stringList[k].split()[listHalfLen])+len(stringList[k].split()[listHalfLen]) < stringList[k][:stringList[k].find("//")].rfind('"'))):
        stringList[k] = " " * stringList[k].find(stringList[k].strip()) + stringFormattingSymb.join(stringList[k].split()[:listHalfLen]) + '"\n' + " " * stringList[k].find('"') + '"' + stringFormattingSymb.join(stringList[k].split()[listHalfLen:])
      else:
        stringList[k] = " " * stringList[k].find(stringList[k].strip()) + stringFormattingSymb.join(stringList[k].split()[:listHalfLen]) + "\n" + stringFormattingSymb.join(stringList[k].split()[listHalfLen:])
      print(str(k) + ": NEEDLINEPARTITION " + stringList[k])

    

    ##if(stringList[k].lstrip().startswith("}")):
    ##  stringList[k] = stringList[k] + "\n\n"
    # --главная_первый_проход-- }
    # --главная_второй_проход-- {
    
    if(stringList[k].lstrip().startswith("using namespace std;")):
      stringList[k] = stringList[k].lstrip()[len("using namespace std;"):]
      for z in range(len(stringList)):
        if(stringList[z].strip().startswith("#include")):
          continue
        for m in range(len(stdLibNames)):
          if(stringList[z].find(stdLibNames[m].strip()) >= 0):
            stringList[k] = "using std::" + stdLibNames[m].split("<")[0].strip() + ";\n" + stringList[k] 
            print("USING STD::" + stdLibNames[m])
            stdLibNames[m] = "*&*&\-92-02" + stdLibNames[m]
    # --главная_второй_проход-- }
    
      
  outFile = open(sys.argv[i] + "~", "wb")
  if(not stringList[0].startswith("// Copyright")):
    outFile.write(("// Copyright 2016 AuthorName. All rights reserved.\n").decode("cp1251").encode("cp1251"))
  

  for k in stringList:
    if(len(k.strip()) > 0):
      outFile.write((k.rstrip() + "\n").decode("utf-8").encode("utf-8"))
  outFile.close()
  print("Parsing of " + sys.argv[i].upper() + " DONE.......")

