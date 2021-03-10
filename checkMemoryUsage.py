# coding=utf8

import re
import sys

def get(filename=None, endAddress="0x1fff0"):
    # Switching type
    endAddress = int(endAddress,16)
    # Exception
    if filename is None:
        print("Error when calling checkMemoryUsage.get")
        print("Usage: checkMemoryUsage.get([filename])")
        return

    # Set parameters for parsing
    regex = "^Address: ([0-9a-fA-Fx]+) +, Function: [\w$]+ +, description: ([0-9a-fA-Fx\-]+) +"
    test_str = ""
    try:
        with open(filename,"r") as f:
            for letters in f:
                test_str += letters
    except:
        print(filename+" does not exist.")
        return

    # Parsing
    matches = re.finditer(regex, test_str, re.MULTILINE)

    '''
    # For Debug
    for m in matches:
        print(m.group(1), m.group(2))
    '''

    # Searching last function
    lastMatch = None
    for each in matches:
        if lastMatch == None: # Initial lastMatch
            lastMatch = each
        elif not int(each.group(1),16) == endAddress:
            lastMatch = each
        else:
            break

    # Calculate remain buffer
    funcStartAddress = int(lastMatch.group(1),16)
    if lastMatch.group(2)=="--":
        funcLength = 0
    else:
        funcLength = int(lastMatch.group(2),16)
    remainBuffer = endAddress - funcStartAddress - funcLength

    # Introduce the result
    with open("checkMemoryUsage.txt","a") as outputFile:
        outputFile.write(str(filename)+"\t"+str(remainBuffer)+"\n")

# Debug main function
def debug_main():
    get("Core0Boot1.txt",0x1fff0)
    get("Core0Boot2.txt",0x1fff0)
    get("Core0Isp.txt",0x1fff0)

# Executing
if len(sys.argv)<3:
    print("usage: checkMemoryUsage [filename] [limit address]")
else:
    get(sys.argv[1],sys.argv[2])

