"""
Created on Sat 01 Jul 11:45 2023
Finished on Sun 02 Jul 13:00 2023
@author: Cpt.Ender

Bifid's cipher encryption and decryption
https://en.wikipedia.org/wiki/Bifid_cipher
                                          """


def polySquare(key: str, polyS25: bool):
    polybiusSquare = {}
    inversePolySquare = {}
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    i = 0
    size = 6
    if polyS25:
        size = 5
        alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    for c in ''.join(key.upper().split(' ')) + alphabet:
        if c not in polybiusSquare.keys() and c in alphabet:
            polybiusSquare[c] = str((i // size + 1) * 10 + i % size + 1)
            inversePolySquare[str((i // size + 1) * 10 + i % size + 1)] = c
            i += 1
    return polybiusSquare, inversePolySquare


def encrypt(text: str, key: str, period=1000, polyS25=False):
    text = ''.join(text.upper().split(' '))
    if polyS25:
        text = text.replace('J', 'I')

    polybiusSquare, inversePolySquare = polySquare(key, polyS25)
    text = [text[i:i + period] for i in range(0, len(text), period)]
    encryption = ''
    for chunk in text:
        digitsLine = ''
        for l in chunk:
            digitsLine += polybiusSquare[l]
        digitsLine = digitsLine[0::2] + digitsLine[1::2]
        encryption += ''.join([inversePolySquare[digitsLine[i:i + 2]] for i in range(0, len(digitsLine), 2)])
    return encryption


def decrypt(text: str, key: str, period=1000, polyS25=False):
    text = ''.join(text.upper().split(' '))
    if polyS25:
        text = text.replace('J', 'I')

    polybiusSquare, inversePolySquare = polySquare(key, polyS25)
    text = [text[i:i + period] for i in range(0, len(text), period)]
    decryption = ''
    for chunk in text:
        digitsLine = ''
        for l in chunk:
            digitsLine += polybiusSquare[l]
        digitsLine = ''.join(
            [digitsLine[i] + digitsLine[len(digitsLine) // 2 + i] for i in range(len(digitsLine) // 2)])
        decryption += ''.join([inversePolySquare[digitsLine[i:i + 2]] for i in range(0, len(digitsLine), 2)])
    return decryption


# encrypt('hello world', key='secret keyword', polyS25=True)
# decrypt('ANYKLUYMND', key='secret keyword', polyS25=True)
en = encrypt('this is a test of the new bifid component of cryptool 2', period=5, key='secret keyword1')
de = decrypt(en, period=5, key='secret keyword1')
