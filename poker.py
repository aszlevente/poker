import random
import pygame
import time

# ♠♡♢♣
#vals = [2,3,4,5,6,7,8,9,10,'Jack','Queen','King','Ace']
#symbols = ['Spades','Hearts','Diamonds','Clubs']

vals = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
symbols = ['♠','♡','♢','♣']

#print(random.choice(vals),"of",random.choice(symbols))

pygame.init()
screen = pygame.display.set_mode((600,600))

def printCard(val, sym) :
    if sym in ('♠','♣') : color = (0,0,0)
    else : color = (255,0,0)

    font = pygame.font.SysFont('Corbel',35)
    text = font.render(str(val)+sym, True, color)
    print(str(val)+sym)
    return text

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
                    for m in holes :
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
                for m in holes :
                    if m == card : test = True

        river.append(card)

    screen.fill((100,255,100))
    screen.blit(printCard(holes[0][0][0],holes[0][0][1]), (400,400))
    pygame.display.flip()
    #for i in range(4) :
        
    
    #következő lépés: pénz, handek, actionök implementálása
