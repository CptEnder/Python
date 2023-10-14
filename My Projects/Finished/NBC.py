def countWords(text, counts):           #function for counting words in a string
    textWords = text.split(" ")
    for word in textWords:
        if word not in counts:
            counts[word] = 0
        counts[word] += 1
    return counts

spam1 = "FREE online !!!"
spam2 = "FREE online results FREE !!!"
spam3 = "!!! registration FREE !!!"
safe1 = "results repository online"
safe2 = "conference online registration conference"
safe3 = "conference results repository rsults"
smoothing = "FREE online !!! results repository registration conference rsults"
test1 = "FREE online conference !!!"
test2 = "conference registration results conference online"

print("Choose text:")
print("1: test1 (FREE online conference !!!)")
print("2: test2 (conference registration results conference online)")
print("3: User Input")

option = int(input()) 

if option == 1:
    currentTest = test1                   
if option == 2:
    currentTest = test2
if option == 3:
    print("Enter Text:")
    currentTest = input()   

spams = [spam1, spam2, spam3, smoothing]
safes = [safe1, safe2, safe3, smoothing]

spamCounts = {}                        #create dictionary for spam           
safeCounts = {}                        #create dictionary for safe

for spam in spams:
    countWords(spam, spamCounts)       #spam frequency for each word (includes smoothing)

for safe in safes:
    countWords(safe, safeCounts)       #safe frequency for each word (includes smoothing)

allSpams = sum(spamCounts.values())    # 20
allSafes = sum(safeCounts.values())    # 19
all = allSpams + allSafes              # 39
Pspam = allSpams / all
Psafe = allSafes / all
PwordsInSpam = sum([spamCounts[w] for w in currentTest.split(" ") if w in spamCounts]) 
PwordsInSafe = sum([safeCounts[w] for w in currentTest.split(" ") if w in safeCounts])
Pwords = PwordsInSafe + PwordsInSpam

if Pwords == 0:
    print("Not enough information (NBC wasn't trained with these words)")
    exit()

chanceOfSpam = ((PwordsInSpam / allSpams)*Pspam)/(Pwords / all)
chanceOfSafe = ((PwordsInSafe / allSafes)*Psafe)/(Pwords / all)

SpamPercentage = "%.0f%%" % (100 * chanceOfSpam)
SafePercentage = "%.0f%%" % (100 * chanceOfSafe)

print("Text has a " + SpamPercentage + " of being spam.")
print("Text has a " + SafePercentage + " of being safe.")

if chanceOfSpam > chanceOfSafe:
    print("Text is propably spam")
else:
    print("Text is propably safe")


