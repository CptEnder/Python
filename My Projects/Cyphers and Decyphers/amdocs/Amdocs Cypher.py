"""
Created on Sun 17 Jul 22:25 2022
Finished on
@author: Cpt.Ender
                                  """


def encrypt(string: str):
    counter = True
    new = ''
    for c in string:
        if counter:
            new += '1' * ord(c)
            counter = not counter
        else:
            new += '0' * ord(c)
            counter = not counter
    return new


def decrypt(string: str):
    start = 0
    new = ''
    for i in range(len(string) - 1):
        if string[i + 1] != string[i]:
            new += chr(i + 1 - start)
            start = i + 1
    new += chr(len(string) - start)
    return new


# print(decrypt(encrypt('183273asdas')))
codes1 = ['KyAn', 'GeoA', 'Deme', 'An19', 'StavZ', 'geoMe', 'ChrH', 'hadK', 'GiorM', 'g!or', 'MichA', 'PhiG', 'Aliv',
          'SpiS', 'ArDeM', 'Chr&1', 'Con!', 'Ppie', 'Para#', 'KyrK', 'GiorV']
codes2 = [
    '1960', 'ga?19', 'raf19', '5991', 'ACH1', 'n195', 'Ad%1', 'y?19', 'N@!19', '!L19', 'A196',
    '1959', '!&19', 'k*19', 'e$19', '9599', 'Gio19', 'r#*19', '19601', 'yp&&1', 'eN!!1']

for i, code in enumerate(codes1):
    print(code, encrypt(code))
    f = open(f"Cyphers and Decyphers/amdocs/{i + 1}.txt", 'w')
    f.write(encrypt(code))
    f.close()
    f = open(f"Cyphers and Decyphers/amdocs/{i + 1}.txt", 'r')
    print(decrypt(f.read()))
    f.close()
