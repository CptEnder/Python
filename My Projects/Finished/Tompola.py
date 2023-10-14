"""
Created on Fri 01 Jan 01:33 2021
Finished on Fri 01 Jan 02:00 2021
@author: Cpt.Ender
                                  """
import random

lst = list(range(1, 91))
random.shuffle(lst)
newList = []

for n in lst:
    print("Epomenos arithmos:", n)
    newList.append(n)
    iN = input()
    if iN != "":
        temp = [int(_) for _ in input("Dwse noumera: ").split()]
        if [item in temp for item in newList].count(True) == len(temp):
            if len(temp) == 5:
                print("Ekleise grammi. \nMpraaaaavo")
            elif len(temp) == 15:
                print("Tompola !!!")
            else:
                print("Wrong number of numbers")
        else:
            print("Re ma peripaizeis mas re?")
