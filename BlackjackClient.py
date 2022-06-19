from base64 import decode
from socket import \
socket, AF_INET, SOCK_STREAM
import sys
from tkinter import Place
s = socket(AF_INET, SOCK_STREAM)
player_number = 0
total_player = 0

bonbon = ""


def bonboncal(total_player):
    temp=""
    for i in range ( 0 , total_player):
        temp+="----------------"
    return temp

def playerDisplay (player_num,total_num):
    ouput = ""
    if player_num == 1:
        temp = ("Player 1(You)").ljust(15, ' ')+"|"
        print (temp ,end="")
    else:
        temp = ("Player 1").ljust(15, ' ')+"|"
        print (temp ,end="")
    for i in range ( 2 , total_num + 1) :
        if i == player_num and i != total_num:
            ouput += ("Player" + str(i) + "(YOU)").ljust(15, ' ')+"|"
        elif i == player_num and i == total_num:
            ouput += ("Player" + str(i)+"(YOU)").ljust(15, ' ')+"|"
        else :
            ouput += ("Player" + str(i)).ljust(15, ' ') + "|"
    print(ouput)

def playerdealerDisplay( player_num , total_num ):
    temp = ("Dealer").ljust(15, ' ')+"|"
    print(temp,end="")
    ouput = ""
    if player_num == 1:
        temp = ("Player 1(You)").ljust(15, ' ')+"|"
        print (temp ,end="")
    else:
        temp = ("Player 1").ljust(15, ' ')+"|"
        print (temp ,end="")
    for i in range ( 2 , total_num + 1) :
        if i == player_num and i != total_num:
            ouput += ("Player" + str(i) + "(YOU)").ljust(15, ' ')+"|"
        elif i == player_num and i == total_num:
            ouput += ("Player" + str(i)+"(YOU)").ljust(15, ' ')+"|"
        else :
            ouput += ("Player" + str(i)).ljust(15, ' ')+ "|"
    print(ouput)


print ('------------------------------------------------')
print ('Enter room number to enter the game or enter "quit" to leave')
server_ip = input("Please input server ip : ")
number = int(input("Please input room number : "))
s.connect((server_ip, number))
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
        print (bonboncal(total_player+1))     
        while 1:
            if Bet >= 10:
                s.send(str(Bet).encode())
                break
            else:
                print ("Please enter again")
                Bet = int(input('This round bet(>=10)?'))  
    elif data == 'startgame':
        bonbon=bonboncal(total_player)
        print (bonbon)
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