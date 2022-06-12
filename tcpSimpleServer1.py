from socket import \
	SO_REUSEADDR, SOL_SOCKET, socket, AF_INET, SOCK_STREAM
import sys, select
import random
from time import sleep

card_show = ['A',2,3,4,5,6,7,8,9,10,'J','Q','K']
card_point = [11,2,3,4,5,6,7,8,9,10,10,10,10]
card_list = [4,4,4,4,4,4,4,4,4,4,4,4,4]

PLAYER_IN_GAME = []  #list list玩家手牌(包含莊家)
PLAYER_CARD = []  #玩家手牌(包含莊家)
PLAYER_POINT = [] #玩家點數(包含莊家)
PLAYER_BET = []   #玩家賭注(不包含莊家)
PLAYER_STATUS = [] #玩家狀態(包含莊家)
PLAYER_NUM = 3    #玩家人數(不包含莊家)
CURRENTBET_LIST = [] #當局賭注
WIN_OR_NOT = []




num = 0
bet_round = 0
game_round = 0
game_start = 0
player_num = 1
count = 0
total_player = 0


SOCKET_LIST = []
PLAYER_LIST = []

RECV_BUFFER = 4096

def calculate(PLAYER_IN_GAME,card_point,true):
    PLAYER_POINT = []
    if true == "fake":
        point = 0
        point = card_point[PLAYER_IN_GAME[0][0]]
        PLAYER_POINT.append(point)
        i = 1
    else:
        i = 0
    for num in range(i,len(PLAYER_IN_GAME)):
        point = 0
        for item in PLAYER_IN_GAME[num]:
            point += card_point[item]
        if PLAYER_IN_GAME[num].count(0) == 0:
            PLAYER_POINT.append(point)
        elif PLAYER_IN_GAME[num].count(0) == 1:
            if point > 21:
                point -= 10 #A from 10 to 1
            PLAYER_POINT.append(point)
        elif PLAYER_IN_GAME[num].count(0) == 2:
            if point >21:
                point -= 10
                if point >21:
                    point -= 10
                    PLAYER_POINT.append(point)
                else:
                     PLAYER_POINT.append(point)
            else:
                PLAYER_POINT.append(point)
    return PLAYER_POINT

def show_card(PLAYER_IN_GAME,card_show,true):
    PLAYER_CARD = []
    if true == "fake":
        card_color = ""
        card_color= str(card_show[PLAYER_IN_GAME[0][0]])
        card_color += "+ ?"
        PLAYER_CARD.append(card_color)
        i = 1
    else:
        i = 0
    for num in range(i,len(PLAYER_IN_GAME)):
        card_color = ""
        for x in range(0,len(PLAYER_IN_GAME[num])-1):
            card_color += str(card_show[PLAYER_IN_GAME[num][x]])
            card_color += "+"
        card_color += str(card_show[PLAYER_IN_GAME[num][len(PLAYER_IN_GAME[num])-1]])
        PLAYER_CARD.append(card_color)   
        
    return PLAYER_CARD

def add_card(PLAYER_IN_GAME,num,card_list,card_point,PLAYER_POINT):
    PLAYER_IN_GAME[num].append(choosecard(card_list))
    PLAYER_POINT = calculate(PLAYER_IN_GAME,card_point,"fake")
    return PLAYER_POINT

def add_card_deal(PLAYER_IN_GAME,num,card_list,card_point,PLAYER_POINT):
    PLAYER_IN_GAME[num].append(choosecard(card_list))
    PLAYER_POINT = calculate(PLAYER_IN_GAME,card_point,"true")
    return PLAYER_POINT

def wincheck(PLAYER_POINT):
    WIN_OR_NOT = []
    for x in range(1,len(PLAYER_POINT)):
        if PLAYER_POINT[0] >21 and PLAYER_POINT[x] <= 21:
            WIN_OR_NOT.append("win")
        elif PLAYER_POINT[x] <= 21 and PLAYER_POINT[x]>PLAYER_POINT[0]:
            WIN_OR_NOT.append("win")
        elif PLAYER_POINT[x] <= 21 and PLAYER_POINT[x]==PLAYER_POINT[0]:
            WIN_OR_NOT.append("tie")
        elif PLAYER_POINT[0] >21 and PLAYER_POINT[x] > 21:
            WIN_OR_NOT.append("tie")
        else:
            WIN_OR_NOT.append("loss")
    return WIN_OR_NOT

def status(PLAYER_POINT):
    player_satus = []
    for item in PLAYER_POINT:
        if item <= 21:
            player_satus.append("Sum:"+str(item))
        else:
            player_satus.append("Bust")
    return player_satus

def dealer_add_card(WIN_OR_NOT,PLAYER_IN_GAME,card_list,card_point,PLAYER_POINT):
    while (WIN_OR_NOT.count("win")/len(WIN_OR_NOT)) >= (2/3):
        if PLAYER_POINT[0] >= 21:
            break
        PLAYER_POINT = add_card_deal(PLAYER_IN_GAME,0,card_list,card_point,PLAYER_POINT)
        WIN_OR_NOT = wincheck(PLAYER_POINT)

def count_bet(WIN_OR_NOT,PLAYER_BET,CURRENTBET_LIST):
    for x in range (0,len(WIN_OR_NOT)):
        if WIN_OR_NOT[x]  =='win':
            PLAYER_BET[x] += int(CURRENTBET_LIST[x])
        elif WIN_OR_NOT[x] == 'loss':
            PLAYER_BET[x] -= int(CURRENTBET_LIST[x])  
        else:
            PLAYER_BET[x] = PLAYER_BET[x]
    return PLAYER_BET
    
def initialize(PLAYER_IN_GAME,PLAYER_NUM,PLAYER_BET,card_list,CURRENTBET_LIST):
    CURRENTBET_LIST = []
    card_list = [4,4,4,4,4,4,4,4,4,4,4,4,4]
    PLAYER_BET = [200,200,200]
    for x in range(0,PLAYER_NUM+1):
        PLAYER_POINT = []
        PLAYER_POINT.append(choosecard(card_list))
        PLAYER_POINT.append(choosecard(card_list))
        PLAYER_IN_GAME.append(PLAYER_POINT)

def printlist(wantprint):
    put = ""
    for item in wantprint:
        put += str(item) +"\t"+"|"
    return put

def initCURRENTBET_LIST(total_player):
    CURRENTBET_LIST = []
    for i in range (0 , total_player):
        CURRENTBET_LIST.append(0)
    return CURRENTBET_LIST

def initPLAYER_BET(total_player):
    PLAYER_BET = []
    for i in range (0 , total_player):
        PLAYER_BET.append(200)
    return PLAYER_BET


def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)



def playerDisplay (player_num,total_num):
    ouput = ""
    if player_num == 1:
        print ("Player 1(You) |" ,end="")
    else:
        print ("Player 1 |" ,end="")
    for i in range ( 2 , total_num + 1) :
        if i == player_num and i != total_num:
            ouput += " Player " + str(i) + "(YOU) |"
        elif i == player_num and i == total_num:
            ouput += " Player " + str(i) + "(YOU)"
        elif i == total_num and i != player_num:
            ouput += " Player " + str(i) 
        else :
            ouput += " Player " + str(i) + "|"
    print(ouput)

def playerdealerDisplay( player_num , total_num ):
    print("Dealer | ",end="")
    ouput = ""
    if player_num == 1:
        print ("Player 1(You) |" ,end="")
    else:
        print ("Player 1 |" ,end="")
    for i in range ( 2 , total_num + 1) :
        if i == player_num and i != total_num:
            ouput += " Player " + str(i) + "(YOU) |"
        elif i == player_num and i == total_num:
            ouput += " Player " + str(i) + "(YOU)"
        elif i == total_num and i != player_num:
            ouput += " Player " + str(i) 
        else :
            ouput += " Player " + str(i) + "|"
    print(ouput)

def betString(list) :
    output=""
    for i in list :
        output+="  "+str(i)+"  ";
    print(output)
    return output

def initialize(PLAYER_IN_GAME,PLAYER_NUM,PLAYER_BET,card_list,CURRENTBET_LIST):
    card_list = [4,4,4,4,4,4,4,4,4,4,4,4,4]
    CURRENTBET_LIST = []
    for x in range(0,PLAYER_NUM+1):
        PLAYER_POINT = []
        PLAYER_POINT.append(choosecard(card_list))
        PLAYER_POINT.append(choosecard(card_list))
        PLAYER_IN_GAME.append(PLAYER_POINT)

def choosecard(cardlist):
    selectcard = random.randint(0,12)
    if card_list[selectcard] == 0:
        choosecard(cardlist)
    else:
        cardlist[selectcard] -= 1
        return selectcard


print ('------------------------------------------------')
print ('Enter "begin" to create room or enter "quit" to leave')


while(1):
    choose = str(input())
    if choose=='begin':
        break
    elif choose=='quit':
        sys.exit()
    else :
        print ('please enter again')

port_num = random.randint(5000,6000)

print ('Room number:', port_num)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', port_num))
server_socket.listen(10)
PLAYER_LIST.append(server_socket.getsockname())
SOCKET_LIST.append(server_socket)
print ('wait for other players....')

while 1:
    ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
    for sock in ready_to_read:
        if sock == server_socket and game_start == 0 : 
            sockfd, addr = server_socket.accept()
            SOCKET_LIST.append(sockfd)
            PLAYER_LIST.append(addr)
            sockfd.send(str("givenum").encode())
            sleep(1)
            sockfd.send(str(len(PLAYER_LIST)).encode())
            sleep(1)
            broadcast(server_socket,sock,str("waitforplayer").encode())
            sleep(1)
            broadcast(server_socket,sock,str(len(PLAYER_LIST)).encode())
            total_player = len(PLAYER_LIST)
            print ('------------------------------------------------')
            playerDisplay(player_num,total_player)
            
            while(1):
                choose = str(input('Enter "start" to start the game , Enter "wait" to wait for other player\n'))
                if choose == 'start':
                    PLAYER_BET=initPLAYER_BET(total_player)
                    game_start = 1
                    bet_round = 1
                    broadcast(server_socket,sock,str("startgame").encode())
                    break
                elif choose == 'wait':
                    print ('wait for other players....')
                    break
                else:
                    print ('please enter again')
        elif game_start == 2 :
            for socket in ready_to_read :
                for j in SOCKET_LIST:
                    if socket == j :
                        data = socket.recv(1024).decode()
                        CURRENTBET_LIST[SOCKET_LIST.index(j)] = data
            if  CURRENTBET_LIST.count(0) == 0:
                game_start = 3
        elif game_start == 4 :
            for socket in ready_to_read :
                yes = socket.recv(1024).decode()
                if yes == "y":
                    PLAYER_POINT = add_card(PLAYER_IN_GAME,num,card_list,card_point,PLAYER_POINT)
                    PLAYER_CARD = show_card(PLAYER_IN_GAME,card_show,"fake")
                    PLAYER_STATUS = status(PLAYER_POINT)
                    print(str('------------------------------------------------'))
                    playerdealerDisplay(player_num , total_player)
                    broadcast(server_socket,server_socket,(str('------------------------------------------------')).encode())
                    sleep(1)
                    broadcast(server_socket,server_socket,str("printplayerdeal").encode())
                    data = str(printlist (PLAYER_CARD))
                    print(data)
                    sleep(1)
                    broadcast(server_socket,server_socket,data.encode())
                    data = printlist (PLAYER_STATUS)
                    print(data)
                    sleep(1)
                    broadcast(server_socket,server_socket,data.encode())
                    if PLAYER_POINT[num] < 21:
                        sleep(1)
                        broadcast(server_socket,server_socket,str("deal").encode())
                        sleep(1)
                        broadcast(server_socket,server_socket,str(num).encode())
                    else:
                        sleep(1)
                        broadcast(server_socket,server_socket,str("deal").encode())
                        sleep(1)
                        broadcast(server_socket,server_socket,str(num+1).encode())
                        num+=1
                else:
                    print(str('------------------------------------------------'))
                    broadcast(server_socket,server_socket,(str('------------------------------------------------')).encode())
                    sleep(1)
                    broadcast(server_socket,server_socket,str("printplayerdeal").encode())
                    data = str(printlist (PLAYER_CARD))
                    print(data)
                    broadcast(server_socket,server_socket,data.encode())
                    data = printlist (PLAYER_STATUS)
                    print(data)
                    broadcast(server_socket,server_socket,data.encode())
                    sleep(1)
                    broadcast(server_socket,server_socket,str("deal").encode())
                    sleep(1)
                    broadcast(server_socket,server_socket,str(num+1).encode())
                    num+=1
            if num == total_player+1:
                game_start=5
                    


    if game_start == 1 :
        CURRENTBET_LIST=initCURRENTBET_LIST(total_player)
        PLAYER_IN_GAME=[]
        initialize(PLAYER_IN_GAME,total_player,PLAYER_BET,card_list,CURRENTBET_LIST)
        game_round += 1
        num = 2
        PLAYER_POINT = calculate(PLAYER_IN_GAME,card_point,"fake")#計算初始每人分數
        PLAYER_CARD = show_card(PLAYER_IN_GAME,card_show,"fake")#牌面
        PLAYER_STATUS = status(PLAYER_POINT)#分數狀態
        print ('------------------------------------------------')
        playerDisplay( player_num , total_player )
        sleep(1)
        broadcast(server_socket,server_socket,(str('------------------------------------------------')).encode())
        sleep(1)
        broadcast(server_socket,server_socket,str("printplayer").encode())
        sleep(1)
        data = printlist (PLAYER_BET)
        print(data)
        sleep(1)
        broadcast(server_socket,server_socket,data.encode())
        print ('------------------------------------------------')
        print("Round "+str(game_round)+":")
        print("Current bet")
        print ('This round bet(>=10)?')
        CURRENTBET_LIST[0] = int(input())
        print ('------------------------------------------------')
        broadcast(server_socket,server_socket,str("initbet").encode())
        sleep(1)
        broadcast(server_socket,server_socket,(str('------------------------------------------------')).encode())
        sleep(1)
        broadcast(server_socket,server_socket,("Round "+str(game_round)+":").encode())
        sleep(1)
        broadcast(server_socket,server_socket,str("Current bet").encode())
        sleep(1)
        print ('------------------------------------------------')
        playerDisplay( player_num , total_player )
        data = printlist (PLAYER_BET)
        print(data)
        broadcast(server_socket,server_socket,data.encode())
        sleep(1)
        broadcast(server_socket,server_socket,str("getbet").encode())
        game_start=2
    if game_start == 3 :
        print ('------------------------------------------------')
        broadcast(server_socket,server_socket,str("printplayerdeal").encode())
        playerdealerDisplay( player_num , total_player )
        data = str(printlist (PLAYER_CARD))
        print(data)
        broadcast(server_socket,server_socket,data.encode())
        data = printlist (PLAYER_STATUS)
        print(data)
        broadcast(server_socket,server_socket,data.encode())
        askadd = "Player" + str(1) + ",Deal([y]/[n])?"
        while 1:
            yes = str(input(askadd))
            if yes == "y":
                PLAYER_POINT = add_card(PLAYER_IN_GAME,1,card_list,card_point,PLAYER_POINT)
                PLAYER_CARD = show_card(PLAYER_IN_GAME,card_show,"fake")
                PLAYER_STATUS = status(PLAYER_POINT)
                print(str('------------------------------------------------'))
                broadcast(server_socket,server_socket,(str('------------------------------------------------')).encode())
                sleep(1)
                broadcast(server_socket,server_socket,str("printplayerdeal").encode())
                playerdealerDisplay( player_num , total_player)
                data = str(printlist (PLAYER_CARD))
                print(data)
                broadcast(server_socket,server_socket,data.encode())
                data = printlist (PLAYER_STATUS)
                print(data)
                broadcast(server_socket,server_socket,data.encode())
                if PLAYER_POINT[1] >= 21:
                    break;
            else:
                print(str('------------------------------------------------'))
                playerdealerDisplay(player_num , total_player)
                broadcast(server_socket,server_socket,(str('------------------------------------------------')).encode())
                sleep(1)
                broadcast(server_socket,server_socket,str("printplayerdeal").encode())
                data = str(printlist (PLAYER_CARD))
                print(data)
                sleep(1)
                broadcast(server_socket,server_socket,data.encode())
                data = printlist (PLAYER_STATUS)
                print(data)
                sleep(1)
                broadcast(server_socket,server_socket,data.encode())
                break;
        sleep(1)
        broadcast(server_socket,server_socket,str("deal").encode())
        sleep(1)
        broadcast(server_socket,server_socket,str("2").encode())
        game_start = 4
    if game_start==5:
        PLAYER_POINT = calculate(PLAYER_IN_GAME,card_point,"true")
        PLAYER_CARD = show_card(PLAYER_IN_GAME,card_show,"true")
        WIN_OR_NOT = wincheck(PLAYER_POINT)  

        dealer_add_card(WIN_OR_NOT,PLAYER_IN_GAME,card_list,card_point,PLAYER_POINT)#自動加牌

        PLAYER_POINT = calculate(PLAYER_IN_GAME,card_point,"true")
        PLAYER_CARD = show_card(PLAYER_IN_GAME,card_show,"true")
        WIN_OR_NOT = wincheck(PLAYER_POINT)  
        print(str('------------------------------------------------'))
        playerdealerDisplay(player_num , total_player)
        broadcast(server_socket,server_socket,(str('------------------------------------------------')).encode())
        sleep(1)
        broadcast(server_socket,server_socket,str("printplayerdeal").encode())
        data = str(printlist (PLAYER_CARD))
        print(data)
        broadcast(server_socket,server_socket,data.encode())
        PLAYER_STATUS = status(PLAYER_POINT)
        data = printlist (PLAYER_STATUS)
        print(data)
        sleep(1)
        broadcast(server_socket,server_socket,data.encode())  

        PLAYER_BET = count_bet(WIN_OR_NOT,PLAYER_BET,CURRENTBET_LIST)#計算BET結果

        print(str('------------------------------------------------'))
        playerDisplay(player_num , total_player)
        broadcast(server_socket,server_socket,(str('------------------------------------------------')).encode())
        sleep(1)
        broadcast(server_socket,server_socket,str("printplayer").encode())
        data = str(printlist (WIN_OR_NOT))
        print(data)
        sleep(1)
        broadcast(server_socket,server_socket,data.encode())

        game_start=1
   


'''

initialize(PLAYER_IN_GAME,PLAYER_NUM,PLAYER_BET,card_list,CURRENTBET_LIST)#初始
PLAYER_POINT = calculate(PLAYER_IN_GAME,card_point,"fake")#計算初始每人分數
PLAYER_CARD = show_card(PLAYER_IN_GAME,card_show,"fake")#牌面
PLAYER_STATUS = status(PLAYER_POINT)#分數狀態


        else:
            try:
                data = sock.recv(RECV_BUFFER)
                if data:
                        # there is something in the socket
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data) 
                else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 
            except:
                broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                continue
    server_socket.close()
'''