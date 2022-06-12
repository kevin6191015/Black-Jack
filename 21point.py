import random
def choosecard(cardlist):
    selectcard = random.randint(0,12)
    if card_list[selectcard] == 0:
        choosecard(cardlist)
    else:
        cardlist[selectcard] -= 1
        return selectcard
    
def calculate(PLAYER_IN_GAME,card_point,true):
    PLAYER__POINT = []
    if true == "fake":
        point = 0
        point = card_point[PLAYER_IN_GAME[0][0]]
        PLAYER__POINT.append(point)
        i = 1
    else:
        i = 0
    for num in range(i,len(PLAYER_IN_GAME)):
        point = 0
        for item in PLAYER_IN_GAME[num]:
            point += card_point[item]
        if PLAYER_IN_GAME[num].count(0) == 0:
            PLAYER__POINT.append(point)
        elif PLAYER_IN_GAME[num].count(0) == 1:
            if point > 21:
                point -= 10 #A from 10 to 1
            PLAYER__POINT.append(point)
        elif PLAYER_IN_GAME[num].count(0) == 2:
            if point >21:
                point -= 10
                if point >21:
                    point -= 10
                    PLAYER__POINT.append(point)
                else:
                     PLAYER__POINT.append(point)
            else:
                PLAYER__POINT.append(point)
    return PLAYER__POINT
    
def initialize(PLAYER_IN_GAME,PLAYER_NUM,PLAYER_BET,card_list,CURRENTBET_LIST):
    CURRENTBET_LIST = []
    card_list = [4,4,4,4,4,4,4,4,4,4,4,4,4]
    PLAYER_BET = [200,200,200]
    for x in range(0,PLAYER_NUM+1):
        PLAYER__POINT = []
        PLAYER__POINT.append(choosecard(card_list))
        PLAYER__POINT.append(choosecard(card_list))
        PLAYER_IN_GAME.append(PLAYER__POINT)

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
    
def add_card(PLAYER_IN_GAME,num,card_list,card_point,PLAYER__POINT):
    PLAYER_IN_GAME[num].append(choosecard(card_list))
    PLAYER__POINT = calculate(PLAYER_IN_GAME,card_point,"fake")
    return PLAYER__POINT

def wincheck(PLAYER__POINT):
    WIN_OR_NOT = []
    for x in range(1,len(PLAYER__POINT)):
        if PLAYER__POINT[0] >21:
            WIN_OR_NOT.append("win")
        elif PLAYER__POINT[x] <= 21 and PLAYER__POINT[x]>PLAYER__POINT[0]:
            WIN_OR_NOT.append("win")
        elif PLAYER__POINT[x] <= 21 and PLAYER__POINT[x]==PLAYER__POINT[0]:
            WIN_OR_NOT.append("tie")
        else:
            WIN_OR_NOT.append("loss")
    return WIN_OR_NOT

def count_bet(WIN_OR_NOT,PLAYER_BET,CURRENTBET_LIST):
    for x in range (0,len(WIN_OR_NOT)):
        if WIN_OR_NOT[x]  =='win':
            PLAYER_BET[x] += CURRENTBET_LIST[x]
        elif WIN_OR_NOT[x] == 'loss':
            PLAYER_BET[x] -= CURRENTBET_LIST[x]  
        else:
            PLAYER_BET[x] = PLAYER_BET[x]
    return PLAYER_BET

def status(PLAYER__POINT):
    player_satus = []
    for item in PLAYER__POINT:
        if item <= 21:
            player_satus.append("Sum:"+str(item))
        else:
            player_satus.append("Bust")
    return player_satus

def dealer_add_card(WIN_OR_NOT,PLAYER_IN_GAME,card_list,card_point,PLAYER__POINT):
    if (WIN_OR_NOT.count("win")/len(WIN_OR_NOT)) >= (2/3):
        PLAYER__POINT = add_card(PLAYER_IN_GAME,0,card_list,card_point,PLAYER__POINT)
        WIN_OR_NOT = wincheck(PLAYER__POINT)
        

    



card_show = ['A',2,3,4,5,6,7,8,9,10,'J','Q','K']
card_point = [11,2,3,4,5,6,7,8,9,10,10,10,10]
card_list = [4,4,4,4,4,4,4,4,4,4,4,4,4]

PLAYER_IN_GAME = []  #list list玩家手牌(包含莊家)
PLAYER_CARD = []  #玩家手牌(包含莊家)
PLAYER__POINT = [] #玩家點數(包含莊家)
PLAYER_BET = [200,200,200]   #玩家賭注(不包含莊家)
PLAYER_STATUS = [] #玩家狀態(包含莊家)
PLAYER_NUM = 3    #玩家人數(不包含莊家)
CURRENTBET_LIST = [] #當局賭注
WIN_OR_NOT = []


initialize(PLAYER_IN_GAME,PLAYER_NUM,PLAYER_BET,card_list,CURRENTBET_LIST)#初始
PLAYER__POINT = calculate(PLAYER_IN_GAME,card_point,"fake")#計算初始每人分數
PLAYER_CARD = show_card(PLAYER_IN_GAME,card_show,"fake")#牌面
PLAYER_STATUS = status(PLAYER__POINT)#分數狀態
#決定賭注

for num in range(1,PLAYER_NUM+1):
    askbet = "Player" + str(num) + ", This round bet  (>=10)?"
    bet = int(input(askbet))
    CURRENTBET_LIST.append(bet)
    
print(PLAYER_STATUS)
print (PLAYER_CARD)
print (PLAYER__POINT)

#是否加牌
for num in range(1,PLAYER_NUM+1):
    askadd = "Player" + str(num) + ",Deal([y]/[n])?"
    while 1:
        yes = str(input(askadd))
        if yes == "y":
            PLAYER__POINT = add_card(PLAYER_IN_GAME,num,card_list,card_point,PLAYER__POINT)
            PLAYER_CARD = show_card(PLAYER_IN_GAME,card_show,"fake")
            PLAYER_STATUS = status(PLAYER__POINT)
            print(PLAYER_STATUS)
            print (PLAYER_CARD)
            print (PLAYER__POINT)
            if PLAYER__POINT[num] >= 21:
                break;
        else:
            print(PLAYER_STATUS)
            print (PLAYER_CARD)
            print (PLAYER__POINT)
            break;
                
PLAYER__POINT = calculate(PLAYER_IN_GAME,card_point,"true")
PLAYER_CARD = show_card(PLAYER_IN_GAME,card_show,"true")
WIN_OR_NOT = wincheck(PLAYER__POINT)  

dealer_add_card(WIN_OR_NOT,PLAYER_IN_GAME,card_list,card_point,PLAYER__POINT)#自動加牌

PLAYER__POINT = calculate(PLAYER_IN_GAME,card_point,"true")
PLAYER_CARD = show_card(PLAYER_IN_GAME,card_show,"true")
WIN_OR_NOT = wincheck(PLAYER__POINT)  
print (PLAYER_CARD)
print (PLAYER__POINT)
print (WIN_OR_NOT)     

PLAYER_BET = count_bet(WIN_OR_NOT,PLAYER_BET,CURRENTBET_LIST)#計算BET結果

print (WIN_OR_NOT)
print (PLAYER_BET)
    
