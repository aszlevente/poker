import random
import pygame
import time
import sys

# ♠♥♦♣
#vals = [2,3,4,5,6,7,8,9,10,'Jack','Queen','King','Ace']
#symbols = ['Spades','Hearts','Diamonds','Clubs']

vals = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
symbols = ['♠','♥','♦','♣']

#print(random.choice(vals),"of",random.choice(symbols))

pygame.init()
screen = pygame.display.set_mode((600,600))

width = screen.get_width()
height = screen.get_height()

checkA = callA = raiseA = foldA = True

def printCard(val, sym, pos) :
    if sym in ('♠','♣') : color = (0,0,0)
    else : color = (255,0,0)

    font = pygame.font.SysFont('Arial',35)
    text = font.render(str(val)+sym, True, color)
    print(str(val)+sym)
    textRect = text.get_rect()
    textRect.center = pos
    
    screen.blit(text, textRect)

def printText(amount, pos, money) :
    font = pygame.font.SysFont('Arial',35)
    if money : text = font.render(f'{amount}$', True, (0,0,0)) # hibaforrás
    else: text = font.render(amount, True, (0,0,0)) # hibaforrás
    textRect = text.get_rect()
    textRect.center = pos

    screen.blit(text, textRect)

def clearAll() :
    screen.fill((100,255,100))
    printCard(holes[0][0][0],holes[0][0][1], (width/2-30,520))
    printCard(holes[0][1][0],holes[0][1][1], (width/2+30,520))
    printText(money[0], (width-50, height-50),True)
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

money = [100,100,100,100]
dealer = 0
blind = 2

while True : #1 iteráció = egy kör a játékban

    holes = [[],[],[],[]]
    for hole in holes :
        for i in range(2) :
            test = True
            while test :
                test = False
                card = (random.choice(vals),random.choice(symbols))
                for l in holes :
                    for m in l :
                        if m == card : test = True

            hole.append(card)
            
    river = []
    for i in range(5) :
        test = True
        while test :
            test = False
            card = (random.choice(vals),random.choice(symbols))
            if card in river : continue
            for l in holes :
                for m in l :
                    if m == card : test = True

        river.append(card)

    screen.fill((100,255,100))
    pygame.display.flip()
    
    #1. kör
    clearAll()

    for kor in range(3) :
        screen.fill((100,255,100))
        if kor == 0 :
            printCard(river[0][0],river[0][1], (width/2-60,height/2))
            printCard(river[1][0],river[1][1], (width/2,height/2))
            printCard(river[2][0],river[2][1], (width/2+60,height/2))
        elif kor == 1 :
            printCard(river[0][0],river[0][1], (width/2-90,height/2))
            printCard(river[1][0],river[1][1], (width/2-30,height/2))
            printCard(river[2][0],river[2][1], (width/2+30,height/2))
            printCard(river[3][0],river[3][1], (width/2+90,height/2))
        else :
            printCard(river[0][0],river[0][1], (width/2-120,height/2))
            printCard(river[1][0],river[1][1], (width/2-60,height/2))
            printCard(river[2][0],river[2][1], (width/2,height/2))
            printCard(river[3][0],river[3][1], (width/2+60,height/2))
            printCard(river[4][0],river[4][1], (width/2+120,height/2))

        printCard(holes[0][0][0],holes[0][0][1], (width/2-30,520))
        printCard(holes[0][1][0],holes[0][1][1], (width/2+30,520))
        printText(money[0], (width-50, height-50), True)
        #Buttons
        drawButtons()

        pygame.display.flip()

        while True :
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if checkA and width-100 <= x <= width-20 and height-200 <= y <= height-150 :
                        pygame.quit()
                        
                        break
                    elif callA and width-100 <= x <= width-20 and height-275 <= y <= height-225 :
                        pygame.quit()
                    elif width-100 <= x <= width-20 and height-350 <= y <= height-300 :
                        clearAll()
                        pygame.draw.rect(screen,(200,200,200),(width-150,height-350,130,50))
                        pygame.display.flip()
                        checkA = callA = raiseA = foldA = False
                    elif foldA and width-100 <= x <= width-20 and height-425 <= y <= height-375 :
                        pygame.quit()
                        

        

        time.sleep(2)
    



    #következő lépés: pénz, handek, actionök implementálása
    break
