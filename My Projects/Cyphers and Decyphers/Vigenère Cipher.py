"""
Created on Tue 26 Oct 15:05 2021
Finished on Tue 26 Oct 15:40 2021
@author: Cpt.Ender

Vigenere cipher encryption and decryption
                                  """

encryptArray = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5,
                'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10,
                'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15,
                'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20,
                'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}

decryptArray = dict()
for c in encryptArray.items():
    decryptArray[c[1]] = c[0]


def encrypt(string: str, key: str):
    if len(string) > len(key):
        key = (len(string) // len(key)) * key + key[:(len(string) - len(key))]
    else:
        key = (len(string) - len(key)) * key + key[:len(string)]
    encryption = ''
    for i, s in enumerate(string):
        encryption += decryptArray[(encryptArray[s] + encryptArray[key[i]]) % 26]

    return encryption


def decrypt(string: str, key: str):
    if len(string) > len(key):
        key = (len(string) - len(key)) * key + key[:-(len(string) - len(key))]
    else:
        key = (len(string) - len(key)) * key + key[len(string)]

    decryption = ''
    for i, s in enumerate(string):
        decryption += decryptArray[(encryptArray[s] - encryptArray[key[i]]) % 26]

    return decryption


print(encrypt("HELLOWORLD", "ABCXYZ"))
print(decrypt("HFNIMVOSNA", "ABCXYZ"))
