"""
Created on Tue 03 Aug 16:07 2021
Finished on Tue 03 Aug 17:20 2021
@author: Cpt.Ender

Rail Fence encryption and decryption
                                      """


def createIndexes(ln, rails: int):
    ls = [[] for r in range(rails)]
    for rail in range(rails):
        n = rail
        count = 0
        while n < ln:
            ls[rail].append(n)
            if rail == 0 or rail == rails - 1:
                n += 1 + 2 * (rails - 2) + 1
            else:
                if not count % 2:
                    n += 2 * (rails - rail - 1 - 1) + 2
                else:
                    n += 2 * (rail - 1) + 2
                count += 1
    return [index for ls_ in ls for index in ls_]


def encrypt(string: str, rails: int):
    ls = createIndexes(len(string), rails)
    return ''.join([string[index] for index in ls])


def decrypt(string: str, rails: int):
    ls = createIndexes(len(string), rails)
    new_ls = ['0'] * len(string)
    for i, index in enumerate(ls):
        new_ls[index] = string[i]
    return ''.join(new_ls)


print(encrypt('WEAREDISCOVEREDFLEEATONCE', 3) == 'WECRLTEERDSOEEFEAOCAIVDEN')
print(decrypt('WECRLTEERDSOEEFEAOCAIVDEN', 3))
print(encrypt('WEAREDISCOVEREDFLEEATONCE', 4))
