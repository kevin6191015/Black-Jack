from base64 import decode
from socket import \
socket, AF_INET, SOCK_STREAM
import sys
from tkinter import Place
s = socket(AF_INET, SOCK_STREAM)
player_number = 0
total_player = 0

def playerDisplay (player_num,total_num):
    output = ""
    if player_num == 1:
        print ("Player 1(You) |" ,end="")
    else:
        print ("Player 1 |" ,end="")
    for i in range ( 2 , total_num + 1) :
        if i == player_num and i != total_num:
            output += " Player " + str(i) + "(YOU) |"
        elif i == player_num and i == total_num:
            output += " Player " + str(i) + "(YOU)"
        elif i == total_num and i != player_num:
            output += " Player " + str(i) 
        else :
            output += " Player " + str(i) + "|"
    print(output)

def playerdealerDisplay (player_num,total_num):
    output = ""
    print("Dealer | ",end="")
    if player_num == 1:
        print ("Player 1(You) |" ,end="")
    else:
        print ("Player 1 |" ,end="")
    for i in range ( 2 , total_num + 1) :
        if i == player_num and i != total_num:
            output += " Player " + str(i) + "(YOU) |"
        elif i == player_num and i == total_num:
            output += " Player " + str(i) + "(YOU)"
        elif i == total_num and i != player_num:
            output += " Player " + str(i) 
        else :
            output += " Player " + str(i) + "|"
    print(output)


print ('------------------------------------------------')
print ('Enter room number to enter the game or enter "quit" to leave')
number = int(input())
s.connect(('127.0.0.1', number))
print ('------------------------------------------------')

while 1:
    data = s.recv(1024).decode()
    data = str(data)
    if data == 'deal':
        if int(s.recv(1024).decode()) == player_number:
            print ('Deal([y]/[n])?')
            DEAL = str(input())
            s.send(DEAL.encode())
        else:
            print ('waiting for other player')
    elif data == 'wait':
        data = s.recv(1024).decode()
        print ('Waiting for Player')
    elif data == 'getbet':
        print ('This round bet(>=10)?')
        Bet = int(input())
        print ('------------------------------------------------')     
        while 1:
            if Bet >= 10:
                s.send(str(Bet).encode())
                break
            else:
                print ("Please enter again")
                Bet = int(input('This round bet(>=10)?'))  
    elif data == 'startgame':
        print ('------------------------------------------------')
        print ('Game Start')
    elif data == 'initbet':
        data = s.recv(1024).decode()
        print (data)
        data = s.recv(1024).decode()
        print (data)

        data = s.recv(1024).decode()
        print (data)
        print ('')
        playerDisplay (player_number, total_player)
    elif data == 'waitforplayer':
        data = s.recv(1024).decode()
        total_player = int(data)
        playerDisplay (player_number, total_player)
        print ('Waiting for Player')
    elif data == 'givenum':
        data = s.recv(1024).decode() 
        player_number = int(data)
    elif data == 'printplayer':
        playerDisplay (player_number, total_player)
    elif data == 'printplayerdeal':
        playerdealerDisplay (player_number, total_player)
    elif not data :
        print("server close");
        sys.exit()
    else :
        print (data)
        


s.close()