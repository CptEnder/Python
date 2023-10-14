from random import *
import os
import sys


def deleteDirs(path):
    os.system("sudo rm -rf " + path + "start")


print("Initiating Annihilation Program\n")

users = ""
with open(os.path.join(sys.path[0], "wrkstn1Users.txt"), "r") as f:
    users = f.read().split("\n")

for u in users:
    temp = u.split(":")
    print("\nUser:", temp[0])
    deleteDirs("../../" + temp[0] + "/")
    print("\tClear")

print("\nDone")
