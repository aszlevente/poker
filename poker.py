import random
import pygame
import time
import sys

# ♠♥♦♣
#vals = [2,3,4,5,6,7,8,9,10,'Jack','Queen','King','Ace']
#suits = ['Spades','Hearts','Diamonds','Clubs']

vals = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
suits = ['♠','♥','♦','♣']
dealer = 0

pygame.init()
screen = pygame.display.set_mode((600,600))

width = screen.get_width()
height = screen.get_height()

checkA = callA = raiseA = foldA = True # TODO raiseA egyenlőre teljesen fölösleges, töröld ha a végén is az

def printCard(val, sym, pos, size=35, spac=0) :
    if sym in ('♠','♣') : color = (0,0,0)
    else : color = (255,0,0)

    font = pygame.font.SysFont('Arial',size)
    text = font.render(str(val)+sym, True, color)
    textRect = text.get_rect()
    textRect.center = (10 + pos[0] + spac + (text.get_width()/2),pos[1]) if spac else pos
    #makes two cards have a certain distance from each other if "spac" argument is given
    screen.blit(text, textRect)
    return text.get_width()

def printText(amount, pos, dollar=False, size=35) :
    font = pygame.font.SysFont('Arial',size)
    if dollar : text = font.render(f'{amount}$', True, (0,0,0)) # hibaforrás
    else: text = font.render(amount, True, (0,0,0)) # hibaforrás
    textRect = text.get_rect()
    textRect.center = pos

    screen.blit(text, textRect)

def clearAll(kor,reveal=False) :
    screen.fill((100,255,100))
    printCard(holes[0][0][0],holes[0][0][1], (width/2-30,520))
    printCard(holes[0][1][0],holes[0][1][1], (width/2+30,520))
    printText(money[0], (width-50, height-50),True)
    if kor == 1 :
        printCard(river[0][0],river[0][1], (width/2-60,height/2))
        printCard(river[1][0],river[1][1], (width/2,height/2))
        printCard(river[2][0],river[2][1], (width/2+60,height/2))
    elif kor == 2 :
        printCard(river[0][0],river[0][1], (width/2-90,height/2))
        printCard(river[1][0],river[1][1], (width/2-30,height/2))
        printCard(river[2][0],river[2][1], (width/2+30,height/2))
        printCard(river[3][0],river[3][1], (width/2+90,height/2))
    elif kor == 3 :
        printCard(river[0][0],river[0][1], (width/2-120,height/2))
        printCard(river[1][0],river[1][1], (width/2-60,height/2))
        printCard(river[2][0],river[2][1], (width/2,height/2))
        printCard(river[3][0],river[3][1], (width/2+60,height/2))
        printCard(river[4][0],river[4][1], (width/2+120,height/2))
    for i in range(3): #többi játékosok adatainak mutatása
        printText(f'Player {i+1}', (80,40+i*60), size=30)
        printText(money[i+1], (180,40+i*60), True, size=25)
        if actions[i+1] != None : 
            printText(actions[i+1], (260,40+i*60), size=25)
        if reveal:
            firstCardWidth = printCard(holes[i+1][0][0], holes[i+1][0][1], (90,70+i*60), 20)
            printCard(holes[i+1][1][0], holes[i+1][1][1], (90,70+i*60), 20, spac=firstCardWidth/2)
    pygame.display.flip()

def drawButtons() :
    pygame.draw.rect(screen,(200,200,200),(width-150,height-200,130,50))
    printText('Check',(width-85,height-175),False)

    pygame.draw.rect(screen,(200,200,200),(width-150,height-275,130,50))
    printText('Call',(width-85,height-250),False)

    pygame.draw.rect(screen,(200,200,200),(width-150,height-350,130,50))
    printText('Raise',(width-85,height-325),False)

    pygame.draw.rect(screen,(200,200,200),(width-150,height-425,130,50))
    printText('Fold',(width-85,height-400),False)
    
def handRecognition(cards) : #Hand értékének számítása
    #high card, pair, two pair, three of a kind, straight, flush, full house, four of a kind, straight flush, royal flush
    cards = [((2,3,4,5,6,7,8,9,10,11,12,13,14)[vals.index(i[0])], i[1]) for i in cards]
    #straight = cards.copy() talán szügség lesz rá
    cards.sort(key=lambda x: x[0])
    straight = [i[0] for i in cards]
    flush = [i[1] for i in cards]
    highestStraight = 0
    highestStraightFlush = 0
    for i in range(3):
        if straight[i:i+5] in [[n,n+1,n+2,n+3,n+4,n+5] for n in range(2,11)]:
            if straight[i] > highestStraightFlush and [k[1] for k in cards[i:i+5]] in (['♠']*5,['♥']*5,['♦']*5,['♣']*5) :
                highestStraightFlush = straight[i]
                
            if straight[i] > highestStraight :
                highestStraight = straight[i]
                
    ofAKind = [0,0] #[what kind, what value]
    ofAKind[0] = max([straight.count(k) for k in range(2,15)])
    ofAKind[1] = max([k for k in range(2,15) if straight.count(k) == ofAKind[0]])
    
    fullHouse = [0,0] #[three of a kind, pair]
    if 2 in [straight.count(k) for k in range(2,15)] and 3 in [straight.count(k) for k in range(2,15)] :
        fullHouse[0] = max([k for k in range(2,15) if straight.count(k) >= 3])
        fullHouse[1] = max([k for k in range(2,15) if straight.count(k) >= 2])
                
    row = straight
    
    row.sort(reverse=True)
    
    if highestStraightFlush == 10 : 
        return [0, row]
        
    elif highestStraightFlush > 0 :
        for i in range(1,6): row.pop(row.find(i))
        return [1, [highestStraightFlush] + row]
        
    elif ofAKind[0] == 4 :
        for i in range(ofAKind[0]): row.pop(row.find(ofAKind[1]))
        return [2, [ofAKind[1]] + row]
        
    elif sum(fullHouse) >= 2 :
        for i in range(3): row.pop(row.find(fullHouse[0]))
        for i in range(2): row.pop(row.find(fullHouse[1]))
        return [3, fullHouse + row]
        
    elif flush.count('♠') == 5 or flush.count('♥') == 5 or flush.count('♦') == 5 or flush.count('♣') == 5 :
        cards.sort(reverse=True, key=lambda x: x[0])
        for i in suits :
            if [k[1] for k in cards].count(i) >= 5 : winningSuit = i
            
        for i in cards :
            if i[1] != winningSuit : cards.pop(cards.find(i))
            
        return [4, [i[0] for i in cards][0:6]]
        
    elif highestStraight > 0 :
        for i in range(1,6): row.pop(row.find(i))
        return [5, [highestStraight] + row]
        
    elif ofAKind[0] == 3 :
        for i in range(ofAKind[0]): row.pop(row.find(ofAKind[1]))
        return [6, [ofAKind[1]] + row]
        
    elif len([k for k in range(2,15) if straight.count(k) >= 2]) >= 2 :
        pairs = [k for k in range(2,15) if straight.count(k) >= 2]
        pairs.sort()
        for i in range(2): row.pop(row.find(pairs[0]))
        for i in range(2): row.pop(row.find(pairs[1]))
        return [7, pairs[0:2] + row]
        
    elif ofAKind[0] == 2 :
        for i in range(ofAKind[0]): row.pop(row.find(ofAKind[1]))
        return [8, [ofAKind[1]] + row]
        
    else : return [9, row]
        
def playerResponse(kor) :
    global checkA, callA, raiseA, foldA
    active = False
    bet = '0'
    while True :
        
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if checkA and width-100 <= x <= width-20 and height-200 <= y <= height-150 :
                    return 0
                elif callA and width-100 <= x <= width-20 and height-275 <= y <= height-225 :
                    if max(bets)-bets[0] <= money[0]: return max(bets)-bets[0]

                # raise összeg megadása
                elif width-100 <= x <= width-20 and height-350 <= y <= height-300 :
                    active = not active
                    clearAll(kor)
                    if active :
                        pygame.draw.rect(screen,(200,200,200),(width-150,height-350,130,50))
                        printText(bet,(width-85,height-325),True)
                    else :
                        drawButtons()
                        bet = '0'
                    pygame.display.flip()
                    checkA = callA = raiseA = foldA = not active
                    
                    
                elif foldA and width-100 <= x <= width-20 and height-425 <= y <= height-375 :
                    return -1

                elif active :# no idea miért itt van de működik
                    active = False
                    clearAll(kor)
                    drawButtons()
                    pygame.display.flip()
                    checkA = callA = raiseA = foldA = True

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and max(bets)-bets[0] < int(bet) <= money[0]:
                        print(f'{bet}$')
                        active = False
                        clearAll(kor)
                        drawButtons()
                        pygame.display.flip()
                        checkA = callA = raiseA = foldA = True
                        return int(bet)
                    elif event.key == pygame.K_BACKSPACE:
                        bet = '0' if len(bet) == 1 else bet[:-1]
                        
                    elif event.unicode in '0123456789':
                        if bet == '0': bet = ''
                        bet += event.unicode

                    pygame.draw.rect(screen,(200,200,200),(width-150,height-350,130,50))
                    printText(bet,(width-85,height-325),True)
                    pygame.display.flip()

money = [100,100,100,100]
actions = [None]*4
dealer = 0
blind = 2

while True : #1 iteráció = egy kör a játékban
    holes = [[],[],[],[]] # az első az élő játékos
    for hole in holes :
        for i in range(2) :
            test = True
            while test :
                test = False
                card = (str(random.choice(vals)),random.choice(suits))
                for l in holes :
                    for m in l :
                        if m == card : test = True

            hole.append(card)
            
    river = []
    for i in range(5) :
        test = True
        while test :
            test = False
            card = (str(random.choice(vals)),random.choice(suits))
            if card in river : continue
            for l in holes :
                for m in l :
                    if m == card : test = True

        river.append(card)

    pot = 0
    winner = -1
    
    clearAll(-1, True)
    drawButtons()
    pygame.display.flip()

    for kor in range(4) :

        global bets
        bets = [0,0,0,0]
        folded = [False]*4
        checked = [False]*4
        
        if kor == 0:
            money[dealer+1 if dealer+1 < 4 else dealer-3]  -= int(blind/2)
            bets[dealer+1 if dealer+1 < 4 else dealer-3] += int(blind/2)
            
            money[dealer+2 if dealer+2 < 4 else dealer-2]  -= int(blind)
            bets[dealer+2 if dealer+2 < 4 else dealer-2] += int(blind)
        
        activePlayer = dealer+3 if kor == 0 else dealer+1
        if activePlayer > 3: activePlayer -= 4
        while True :
            
            if folded.count(True) == 3:
                winner = folded.index(False)
                break
            
            if activePlayer == 0 and folded[0] == False:
                
                resp = playerResponse(kor)
                if resp == -1:
                    folded[0] = True
                else:
                    money[0] -= resp
                    bets[0] += resp
                    
            elif folded[activePlayer] == False:
                # computer-controled-player action
                if bets[activePlayer] < max(bets):
                    #raise, call or fold
                    act = random.random()
                    if act < 0.8:
                        #call
                        money[activePlayer] -= max(bets)-bets[activePlayer]
                        bets[activePlayer] += max(bets)-bets[activePlayer]
                        actions[activePlayer] = 'Call'
                    elif act < 0.95:
                        #raise
                        raiseAmount = random.randint(1+(max(bets)-bets[activePlayer]),money[activePlayer])
                        money[activePlayer] -= raiseAmount
                        bets[activePlayer] += raiseAmount
                        actions[activePlayer] = 'Raise'
                    else :
                        #fold
                        folded[activePlayer] = True #rakd be: folded játékosok actualy essenek ki
                        actions[activePlayer] = 'Fold'
                elif bets[activePlayer] == max(bets):
                    #check or raise
                    act = random.random()
                    if act < 0.8:
                        checked[activePlayer] = True
                        actions[activePlayer] = 'Check'
                    else:
                        # raising
                        raiseAmount = random.randint(1,money[activePlayer])
                        money[activePlayer] -= raiseAmount
                        bets[activePlayer] += raiseAmount
                        actions[activePlayer] = 'Raise'
                        
            clearAll(kor, True)
            drawButtons()
            pygame.display.flip()

            if not folded[activePlayer]: time.sleep(2)
            activePlayer = 0 if activePlayer == 3 else activePlayer+1
            
            aliveBets = [bets[i] for i in range(4) if not folded[i]]

            if bets == ([aliveBets[0]]*len(aliveBets) and aliveBets != [0]*len(aliveBets)) or (aliveBets == [0]*len(aliveBets) and checked == [True]*len(aliveBets)):
                actions = [None]*4
                print('betting kör vége')
                break # betting kör vége

        pot += sum(bets)
        
        if kor == 3 or winner >= 0:
            
            playerHands = [handRecognition(holes[i]) if not folded[i] else [10] for i in range(4)]
            
            handTypes = ['Royal Flush', 'Straight Flush', 'Four Of A Kind', 'Full House', 'Flush', 'Straight', 'Three Of A Kind', 'Two Pair', 'Pair', 'High Card', 'Folded']
            
            #kártyavillantás, handek kiírása
            for i in range(4) :
                pass
            
            money[winner] += pot
            break
        
        #if folded[0]: break
    

    dealer = 0 if dealer == 3 else dealer+1
    break
