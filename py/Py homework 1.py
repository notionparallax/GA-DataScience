# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

#  1. Create some code that will create any MUTABLE data structure.
#  1. Perform an operation on all the elements of object you created
#  1. Subset an object using a control flow operation and create at least 2 new objects
#  1. Create a new function that will accept inputs and perform an operation on those inputs.
#  1. Create a function that will prompt the user to enter their Name, age, weight and height then return a well formatted sentence to the user on the screen showing them their BMI index.
#  1. Install sci-kit learn as homework so that you can use it next session

# <rawcell>

# Create some code that will create any MUTABLE data structure.

# <codecell>

text = "If you drink much from a bottle marked 'poison' it is certain to disagree with you sooner or later."
wordList = text.split(" ")
print wordList

# <rawcell>

# Perform an operation on all the elements of object you created

# <codecell>

wordList[6] = "eat"
wordList[6] = "sandwich"
wordList[8] = "'knuckle'"
print wordList

# <rawcell>

# Subset an object using a control flow operation and create at least 2 new objects

# <codecell>

for i in range(len(wordList)):
    if wordList[i] == "If":
        wordList[i] = "When"
        print wordList
    elif len(wordList[i]) > 3:
        wordList[i] = {"status":"redacted", "reason":"teaspooon", "secret":wordList[i]}

# <codecell>

print wordList

# <rawcell>

# Create a new function that will accept inputs and perform an operation on those inputs.

# <codecell>

def unRedactWord(redactedWord):
    r = redactedWord
    if type(r) is dict:
        return r["secret"]
    else:
        return r

def unRedactPhrase(listOfWords):
    phrase = []
    for word in listOfWords:
        phrase.append(unRedactWord(word))
    return phrase

# <codecell>

print unRedactPhrase(wordList)

# <rawcell>

# Create a function that will prompt the user to enter their Name, age, weight 
# and height then return a well formatted sentence to the user on the screen
# showing them their BMI index.

# <codecell>

def bmi(height, weight):
    return weight/(height ** 2)
def calcBMIforUser():
    name = raw_input("what's your name : ")    
    age = float(raw_input("what's your age : "))
    height = float(raw_input("what's your height (in m) : "))
    weight = float(raw_input("what do you weight (in kg) : "))
    sex    = raw_input("Are you male or female (type m or f) : ")
    
    BMI = bmi(height, weight)
    print "| {0} | {1} | {2} |".format(name,age,sex)
    print "Your BMI is {0}".format(BMI)
    
calcBMIforUser()