"""
Created on Sun 31 May 12:51 2020
Finished on
@author: Cpt.Ender
                                  """


def encrypt(k: list, text='Onoma'):
    i = 0
    encrypted_text = ''

    for t in text:
        Chr = ord(t) + k[i]
        encrypted_text += chr(Chr)
        i += 1
        if i == len(k):
            i = 0

    print(encrypted_text)


kleida = [14, 25, 20, 19, 5]
Frasi = input("Input text: ")

if Frasi:
    encrypt(kleida, Frasi)
else:
    encrypt(kleida)