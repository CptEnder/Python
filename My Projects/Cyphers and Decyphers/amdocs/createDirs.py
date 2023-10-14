from random import *
import random
import string
import os
import sys


def createDirs(path, digit: int):
    os.system("sudo mkdir " + path + "start/")
    print("|", end="")
    rand = randint(500, 750)
    percent = 0
    fileDirIndex = randint(1, rand - 1)
    fileDir = ''
    imageDirIndex = randint(1, rand - 1)
    imageDir = ''
    loreDirIndex = randint(1, rand - 1)
    loreDir = ''
    for i in range(rand):
        name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        os.system("sudo mkdir " + path + "start/" + name)
        if percent == ((i * 100) // rand):
            print("-", end="")
            percent += 1
        if i == fileDirIndex:
            fileDir += path + "start/" + name
            os.system('sudo cp ' + str(digit) + '.txt ' + fileDir + '/.johnCena.txt')
            os.system('sudo chmod 500 ' + fileDir + '/.johnCena.txt')
            print(fileDir)
        if i == imageDirIndex:
            imageDir += path + "start/" + name
            os.system('sudo cp ' + str(digit) + '.png ' + imageDir + '/scpMe.txt')
            os.system('sudo chmod 500 ' + fileDir + '/scpMe.txt')
            print(imageDir)
        if i == loreDirIndex:
            loreDir += path + "start/" + name
            os.system('sudo cp ' + str(digit) + str(digit) + '.txt ' + loreDir + '/giorkos.txt')
            os.system('sudo chmod 500 ' + fileDir + '/giorkos.txt')
            print(loreDir)
    print("|\n", i, "folders added")
    return [fileDir, imageDir, loreDir]


print("Initiating Annihilation Program\n")

users = ""
file = "wrkstn1Users.txt"
workStationNum = ''
for m in file:
    if m.isdigit():
        workStationNum += m
workStationNum = int(workStationNum)

with open(os.path.join(sys.path[0], file), "r") as f:
    users = f.read().split("\n")

dirs = []
f1 = open("export.txt", "w")
for i, u in enumerate(users):
    temp = u.split(":")
    print("\nUser:", temp[0])
    dirs = createDirs("../../" + temp[0] + "/", (workStationNum - 1) * len(users) + 1 + (i + 1) % len(users))
    os.system('sudo chown ' + temp[0] + " ../../" + temp[0] + "/start/")
    os.system('sudo chmod 500 ' + temp[0] + " ../../" + temp[0] + "/start/")
    for d in dirs:
        f1.write('User:' + temp[0] + ' -' + d + '\n')
f1.close()

print("\nDone")
