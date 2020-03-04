from itertools import islice
import os, sys, fileinput, string, time
from StringCases import find_cases


# global variables
lineCount = 0
newCall = True
filesEdited = 0
globalQuotationStack = []
frontQuotationCount = 0
rearQuotationCount = 0


# recursive file path iteration
def file_iterator(os_directory):
    for filename in os.listdir(os_directory):
        if filename.startswith('.'):
            continue
        elif filename.find("Controller") != -1:
            continue
        elif os.path.isdir(os_directory+'/'+filename):
            filename = os_directory+ '/' + filename
            file_iterator(filename)
        elif filename.endswith(".cs"):
            filename = os_directory+ '/' + filename
            file_editor(filename)
            continue
        else:
            continue


# string splice 
def insert_str(string, index):
    return string[:index] + ".ConfigureAwait(false)" + string[index:]


# find end of line for wrapped functions and construct
def eol_parenthesis_bool_check(tempLine, newCall, globalQuotationStack):

        startPosition = 0
        awaitable = tempLine.find('awaitable')
        configureAwait = tempLine.find('ConfigureAwait')
        awaitPosition = tempLine.find('await ')
        endOfMethodCall = tempLine.find(');')
        global frontQuotationCount 
        global rearQuotationCount

        if configureAwait != -1:
            stack = []
            return 0, False, stack
        if awaitable != -1:
            stack = []            
            return 0, False, stack

        if awaitPosition != -1 and newCall == True:
            startPosition = awaitPosition

        if awaitPosition == -1 and newCall == True:
            stack = []
            return 0, False, stack

        open = ["("]
        close = [")"]        
        
        if newCall == True:
            frontQuotationCount = 0
            rearQuotationCount = 0            
            #quotationStack = []            
            multipleLineEndPosition = 0
        else:
            startPosition = 0
            multipleLineEndPosition = 0
            
        for iterator in tempLine[startPosition: :1]:
            multipleLineEndPosition+=1
            if iterator in open:
                globalQuotationStack.append(iterator)
                frontQuotationCount+=1
                newCall = False
            elif iterator in close:
                rearQuotationCount+=1
                if len(globalQuotationStack) == 0:
                    if endOfMethodCall == -1:
                        eol_check = False
                        newCall = False
                    else:
                        eol_check = True
                        newCall = True
                        #multmultipleLineEndPosition = endOfMethodCall+1
                    return multipleLineEndPosition, eol_check, globalQuotationStack 
                else:
                    globalQuotationStack.pop()

            if newCall is False and len(globalQuotationStack) == 0:
                newCall = True
                eol_check = True
                if endOfMethodCall == -1:
                    eol_check = False
                    newCall = False
                else:
                    eol_check = True
                    newCall = True

        eol_check = False
        return multipleLineEndPosition, eol_check, globalQuotationStack


# find end of line
def find_eol(f_content, line):

    eol_check = True
    edit = True
    global lineCount 
    global newCall
    currentMethod = []
    global globalQuotationStack
    #startPositionHolder = lineCount - 1
    startPosition = lineCount - 1

    for i, tempLine in enumerate(islice(f_content, startPosition, None), startPosition):
        lineCount += 1
        if len(globalQuotationStack) == 0:
            endPosition, eol_check, stack = eol_parenthesis_bool_check(tempLine, True, globalQuotationStack)
            globalQuotationStack = stack
        else:
            endPosition, eol_check, stack = eol_parenthesis_bool_check(tempLine, False, globalQuotationStack)
            globalQuotationStack = stack
        if endPosition == 0 and stack == [] and eol_check == False:
            currentMethod.append(tempLine)
            edit = False
            return currentMethod, edit
        if eol_check is False:
            currentMethod.append(tempLine)
            continue
        else:
            editedLine = insert_str(tempLine, endPosition)
            currentMethod.append(editedLine)
            newCall = True
            break

    return currentMethod, edit

  
# find parenthesis within a single string
def find_parenthesis(line, endPosition):

    open = ["("]
    close = [")"]
    stackNull = False
    quotationStack = []
    global frontQuotationCount 
    global rearQuotationCount 

    for iterator in line[endPosition: :1]:
        endPosition+=1
        if iterator in open:
            quotationStack.append(iterator)
            stackNull = True
            frontQuotationCount+=1
        elif iterator in close:
            rearQuotationCount+=1
            stackNull = True
            if len(quotationStack) == 0:
                return endPosition
            else:
                quotationStack.pop()
        if stackNull and len(quotationStack) == 0:
            return endPosition-1


# single string construction
def string_construction(line, lineCount, startPosition):
    if line.find('.ConfigureAwait(false)') == -1:

        awaitable = line.find('awaitable')

        if awaitable != -1:
            return
        readAsByteArrayAsync = line.find('ReadAsByteArrayAsync')
        if readAsByteArrayAsync != -1:
            return
        readAsStringAsync = line.find('ReadAsStringAsync')
        if readAsStringAsync != -1:
            return

        global frontQuotationCount, rearQuotationCount
        newLine = None
        frontQuotationCount = 0
        rearQuotationCount = 0
        #toList = 0
        #whenAll = 0
        endPosition = startPosition + 6
        
        endPosition = find_parenthesis(line, endPosition)
        configureAwait = line.find('ConfigureAwait')
        if configureAwait != -1:
            return

        insertPosition = find_cases(line)
        if insertPosition != 999:
            endPosition = find_parenthesis(line, insertPosition)

        if(frontQuotationCount == rearQuotationCount):
            if(line.find(';') != -1):
                if line.find('ConfigureAwait(false)') == -1:
                    #toList = line.find('ToList')
                    #whenAll = line.find('WhenAll')

                    if(frontQuotationCount == 2 and rearQuotationCount == 2):
                        newLine = insert_str(line, endPosition+1)
                        return newLine
                    elif(frontQuotationCount == 1 and rearQuotationCount == 1):
                        newLine = insert_str(line, endPosition+1)
                        return newLine
                    elif(frontQuotationCount == rearQuotationCount):
                        if line.find('ConfigureAwait(false)') != -1:
                            return
                        #position = line.find(');')
                        positionSingle = line.find(';')
                        if endPosition is not None: 
                            newLine = insert_str(line, endPosition+1)
                        else:
                            newLine = insert_str(line, positionSingle)

                        return newLine
        return newLine


# parse through file lines 
def file_editor(filename):
    global lineCount
    global filesEdited 
    with open(filename, encoding="utf-8", errors='ignore') as f:

        linesContainingAwaitMethod = []
        f_content = f.readlines()
        newLine = None
        edited = False
        lineCount = 0

        for line in f_content:
            lineCount = lineCount + 1
            startPosition = line.find('await')
            if startPosition != -1:
                search = line.find('ConfigureAwait(false)')
                if search == -1:
                    sameLine = line.find(';')
                    if sameLine == -1:
                        linesContainingAwaitMethod, edit = find_eol(f_content, line)
                        if linesContainingAwaitMethod is not None:
                            methodLineCount = len(linesContainingAwaitMethod)
                            i = 2
                            if edit == True:
                                while i <= methodLineCount:                                
                                    f_content[lineCount-i] = linesContainingAwaitMethod.pop()
                                    edited = True
                                    i+=1                            
                                lineCount-=methodLineCount
                                linesContainingAwaitMethod.clear()
                                break
                            else:
                                lineCount-=methodLineCount
                                linesContainingAwaitMethod.clear()
                                continue
                    else:
                        newLine = string_construction(line, lineCount, startPosition)
                        if newLine is not None:
                            f_content[lineCount-1] = line = newLine
                            edited = True
                else:
                    continue

        if(edited):
            filesEdited+=1
            print("File Changed:")
            print(filename+"\n")
            with open(filename, "w", encoding='utf-8') as file:
                for line in f_content:
                    file.write(str(line))
            file.close
        f.close


# main 
input("Press any button to start ConfigureAwaitBuilder\n")
print("Program has Started --- Please Wait\n")
t0 = time.time()
directory = 'C:/Users/Richard Anderson/Storage/Documents/P97 Documents/integrations-sitesimulator'
file_iterator(directory)
print("\nTotal Number of Files Changed: " + str(filesEdited))
t1 = time.time()
total = t1-t0
print("\nTime Taken: " + str(round(total, 2)) + "seconds \n")
os.system("PAUSE")

