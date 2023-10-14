"""
Created on Mon Feb 25 19:02:00 2019

@author: plabc
"""
import random
print('Welcome to a game of Rock Paper Scissors')
print("It's you against the computer")

list = ['rock', 'paper', 'scissors']
inp_cmd = input("Choose 'wisely' :")
# inp_cmd = list[random.randint(0, 2)]
wins2 = 0
wins1 = 0
draws = 0
while inp_cmd == list[0] or inp_cmd == list[1] or inp_cmd == list[2]:
    pc_cmd = random.randint(0, 2)
    print('Your choice was:', inp_cmd, '''
            Computer's choice was:''', list[pc_cmd])
    if inp_cmd == list[0] and pc_cmd == 1 or inp_cmd == list[1] and pc_cmd == 2 or inp_cmd == list[2] and pc_cmd == 0:
        print('The computer wins!')
        wins2 += 1
    elif inp_cmd == list[pc_cmd]:
        print("It's a draw")
        draws += 1
    else:
        print('You win!!!!')
        wins1 += 1
    print('Your wins:', wins1, 'Computer wins:', wins2, 'Draws:', draws)
    inp_cmd = input("Choose 'wisely' :")
    # inp_cmd = list[random.randint(0, 2)]