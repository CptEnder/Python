"""
Created on Mon 19 Jul 20:32 2021
Finished on Mon 19 Jul 20:35 2021
@author: Cpt.Ender

TapFive (aka prisoners' code) encryption and decryption
                                                          """

encryptArray = {'A': 11, 'B': 12, 'C': 13, 'D': 14, 'E': 15,
                'F': 21, 'G': 22, 'H': 23, 'I': 24, 'J': 25,
                'L': 31, 'M': 32, 'N': 33, 'O': 34, 'P': 35,
                'Q': 41, 'R': 42, 'S': 43, 'T': 44, 'U': 45,
                'V': 51, 'W': 52, 'X': 53, 'Y': 54, 'Z': 55}

decryptArray = dict()
for c in encryptArray.items():
    decryptArray[c[1]] = c[0]


def encrypt(string):
    string = list(string.upper())

    encryption = ''
    for s in string:
        if s == 'K':
            s = 'C'
        encryption += str(encryptArray[s])

    return encryption


def decrypt(string):
    decryption = ''

    for i in range(len(string)):
        if not i % 2:
            decryption += decryptArray[int(string[i:i + 2])]

    return decryption


print(encrypt("JAWBREAKERS"))
print(decrypt("2511521242151113154243"))
