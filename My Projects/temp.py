"""
Created on Sat 29 May 18:23 2021
Finished on
@author: Cpt.Ender
                                  """


# def dbl_linear(n):
#     u = [1, 3, 4, 7, 10]
#     i = 2
#     ii = 4
#     condition = True
#     while condition:
#         # print(u[i], u[i + 1])
#         y1 = 2 * u[i] + 1
#         z1 = 3 * u[i] + 1
#         y2 = 2 * u[i + 1] + 1
#         z2 = 3 * u[i + 1] + 1
#         temp = [y1, y2, z1, z2]
#         for num in temp:
#             inserted = False
#             j = -1
#             while not inserted:
#                 if num == u[j]:
#                     inserted = True
#                     ii -= 1
#                 if num > u[j]:
#                     if j != -1:
#                         # u.insert(j + 1, num)
#                         # u.append(0)
#                         u[j+1:] = [num]+u[j+1:]
#                     else:
#                         u.append(num)
#                     inserted = True
#                 j -= 1
#
#         if len(u) > n:
#             print(u[i], ii)
#             print(len(u), n)
#             condition = u[i] * 2 + 1 < u[n]
#         i += 2
#         ii += 4
#
#     return u
#
#
# n_ = 50
# ls = dbl_linear(n_)
# print(*ls)
# print(ls[n_])

# -------------------------------------------------------------------------------------------------
# def decodeBits(bits):
#
#     return
#
#
# def decodeMorse(morse_code):
#     CODE_reversed = {'..-.': 'F', '-..-': 'X',
#                      '.--.': 'P', '-': 'T', '..---': '2',
#                      '....-': '4', '-----': '0', '--...': '7',
#                      '...-': 'V', '-.-.': 'C', '.': 'E', '.---': 'J',
#                      '---': 'O', '-.-': 'K', '----.': '9', '..': 'I',
#                      '.-..': 'L', '.....': '5', '...--': '3', '-.--': 'Y',
#                      '-....': '6', '.--': 'W', '....': 'H', '-.': 'N', '.-.': 'R',
#                      '-...': 'B', '---..': '8', '--..': 'Z', '-..': 'D', '--.-': 'Q',
#                      '--.': 'G', '--': 'M', '..-': 'U', '.-': 'A', '...': 'S', '.----': '1',
#                      '...---...': 'SOS', '-.-.--': '!', '.-.-.-': '.'}
#     string = ''
#     words = morse_code.split('   ')
#
#     for word in words:
#         if word:
#             for s in word.split(' '):
#                 if s:
#                     string += CODE_reversed[s]
#             string += ' '
#     string = string[:-1]
#     return string
#
#
# a = decodeMorse(
#     '      ...---... -.-.--   - .... .   --.- ..- .. -.-. -.-   -... .-. --- .-- -.   ..-. --- -..-   .--- ..- -- .--. ...   --- ...- . .-.   - .... .   .-.. .- --.. -.--   -.. --- --. .-.-.- ')

# ------------------------------------------------------------------------------------------------
# def decompose(n, i=0):
#     ls = [n - 1]
#     temp = n ** 2
#     while temp > 1:
#         temp -= ls[-1] ** 2
#         if temp:
#             ls.append(int(temp ** (1 / 2)))
#         if len(ls) == i + 2 and ls[i] <= ls[i + 1]:
#             return None
#         if ls[-1] == ls[-2] and i != len(ls) - 2:
#             ls[i] -= 1
#             ls = ls[:i + 1]
#             temp = n ** 2 - sum([num ** 2 for num in ls[:-1]])
#     return None if len(ls) == 1 or ls[-1] == ls[-2] else ls[::-1]
#
#
# print(decompose(16))  #[11,10,5,3,1]
# for ii in range(1, 25):
#     print(decompose(ii), ii)
# ------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------
# Fluid height map
# def volume(fluidMap: list):
#     vol = 0
#     for row in fluidMap[1:len(fluidMap) - 1]:
#         pass
#     return vol
#
#
# ls = [[8, 8, 8, 8, 6, 6, 6, 6],
#       [8, 0, 0, 8, 6, 0, 0, 6],
#       [8, 0, 0, 8, 6, 0, 0, 6],
#       [8, 8, 8, 8, 6, 6, 6, 6],
#       ]
#
# # print(volume(ls))
# print(volume([[9, 9, 9, 9, 9],
#               [9, 0, 1, 2, 9],
#               [9, 7, 8, 3, 9],
#               [9, 6, 5, 4, 9],
#               [9, 9, 9, 9, 9]]))
# print(volume([[0, 10, 0, 20, 0],
#               [20, 0, 30, 0, 40],
#               [0, 40, 0, 50, 0],
#               [50, 0, 60, 0, 70],
#               [0, 60, 0, 70, 0]]))
# print(volume([[3, 3, 3, 3, 3],
#               [3, 0, 0, 0, 3],
#               [3, 3, 3, 0, 3],
#               [3, 0, 0, 0, 3],
#               [3, 0, 3, 3, 3],
#               [3, 0, 0, 0, 3],
#               [3, 3, 3, 1, 3]]))
# ------------------------------------------------------------------------------------------------
# Smallest Hamming Number

# def hamming2():
#     """\
#     This version is based on a snippet from:
#         https://web.archive.org/web/20081219014725/http://dobbscodetalk.com:80
#                          /index.php?option=com_content&task=view&id=913&Itemid=85
#         http://www.drdobbs.com/architecture-and-design/hamming-problem/228700538
#         Hamming problem
#         Written by Will Ness
#         December 07, 2008
#
#         When expressed in some imaginary pseudo-C with automatic
#         unlimited storage allocation and BIGNUM arithmetics, it can be
#         expressed as:
#             hamming = h where
#               array h;
#               n=0; h[0]=1; i=0; j=0; k=0;
#               x2=2*h[ i ]; x3=3*h[j]; x5=5*h[k];
#               repeat:
#                 h[++n] = min(x2,x3,x5);
#                 if (x2==h[n]) { x2=2*h[++i]; }
#                 if (x3==h[n]) { x3=3*h[++j]; }
#                 if (x5==h[n]) { x5=5*h[++k]; }
#     """
#     h = 1
#     _h = [h]  # memoized
#     multipliers = (2, 3, 5)
#     multindeces = [0 for i in multipliers]  # index into _h for multipliers
#     multvalues = [x * _h[i] for x, i in zip(multipliers, multindeces)]
#     yield h
#     while True:
#         h = min(multvalues)
#         _h.append(h)
#         for (n, (v, x, i)) in enumerate(zip(multvalues, multipliers, multindeces)):
#             if v == h:
#                 i += 1
#                 multindeces[n] = i
#                 multvalues[n] = x * _h[i]
#         # cap the memoization
#         mini = min(multindeces)
#         if mini >= 1000:
#             del _h[:mini]
#             multindeces = [i - mini for i in multindeces]
#         #
#         yield h
#
#
# for i, n in enumerate(hamming2()):
#     if i == 20:
#         print(n)
#         break


def next_smaller(n):
    digits = [int(i) for i in str(n)]

    for i in range(len(digits) - 1, -1, -1):
        if digits[i:] != sorted(digits[i:]):
            for j in range(len(digits) - 1, i, -1):
                if digits[j] < digits[i] and not (digits[j] == 0 and i == 0):
                    temp = digits[i]
                    digits[i] = digits[j]
                    digits[j] = temp
                    digits[i + 1:] = sorted(digits[i + 1:])[::-1]
                    return int(''.join([str(num) for num in digits]))
    return -1


print(next_smaller(907) == 790)
print(next_smaller(103166011366) == 103163666110)
print(next_smaller(1023456789) == -1)
