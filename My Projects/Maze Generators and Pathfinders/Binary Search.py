"""
Created on Sat 08 May 00:57 2021
Finished on Sat 08 May 01:20 2021
@author: Cpt.Ender

Implementation of binary search algorithm
                                         """
numbers = [89, 419, 398, 278, 105, 86, 463, 65, 182, 94, 204, 88, 363, 471, 29, 129, 157, 335, 258, 58, 419, 491, 93,
           289, 38, 434, 225, 122, 486, 321, 250, 268, 346, 231, 228, 240, 422, 306, 231, 178, 83, 198, 228, 379, 333,
           485, 110, 298, 319, 330, 244, 361, 110, 203, 344, 12, 260, 156, 391, 186, 20, 117, 427, 179, 46, 206, 286,
           411, 333, 173, 473, 322, 405, 481, 413, 410, 394, 126, 214, 303, 119, 181, 205, 301, 261, 251, 239, 428, 32,
           102, 192, 364, 45, 312, 348, 437, 184, 429, 330, 144]
numbers.sort()


def binarySearch(numbersList: list, number: int, index=0):
    if not numbersList:
        return -1

    mid = len(numbersList) // 2
    if numbersList[mid] == number:
        return index + mid
    else:
        if number < numbersList[mid]:
            return binarySearch(numbersList[:mid], number, index)
        else:
            return binarySearch(numbersList[mid + 1:], number, index + mid + 1)


for i in range(500):
    print(binarySearch(numbers, i), i)
