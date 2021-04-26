#!/usr/bin/env python
#Cardgame

import random
import copy
from random import shuffle, randint as rng
import time
import pygame
pygame.init()

import cardmaker
from picturedump import *


#Basic variables
shutdown=False  #if True shuts game down
playerlist=list()
playerhealth=25
endgame=False
turnnumber=0
discoverlist=list()
deck1, deck2 = '',''

allcarddict=dict()
for card in cardmaker.cardlist:
    allcarddict[card.__name__] = card(2,[])

spelldictnull={               
               'target':0, #Target number

               #Target type
               'target_hp':0,
               'target_healminion':0,
               'target_atk':0,
               'target_kill':0,
               'target_freeze':0,
               'target_hand_hp':0,
               'target_hand_atk':0,
               'target_hand_manacost':0,
               'target_hand_discard':0,
               'target_face':0,
               'target_barrier':0,
               'target_lifesteal':0,
               'target_rush':0, 
               'target_silence':0,
               'target_recall': 0,

               #AOE part
               'ally_hand_manacost_aoe':0,
               'ally_hand_discard_aoe':0,
               'ally_deck_manacost_aoe':0,
               'enemy_deck_discard_aoe':0,
               'ally_freeze_aoe':0,
               'enemy_freeze_aoe':0,
               'ally_kill_aoe':0,
               'enemy_kill_aoe':0,
               'ally_atk_aoe':0,
               'enemy_atk_aoe':0,
               'ally_hp_aoe':0,
               'enemy_hp_aoe':0,
               'ally_healminion_aoe':0,
               'enemy_healminion_aoe':0,
               'ally_face':0,
               'enemy_face':0,
               'ally_current_mana':0,
               'enemy_current_mana':0,
               'ally_max_mana':0,
               'enemy_max_mana':0,
               'ally_armour':0,
               'enemy_armour':0,
               'ally_draw':0,
               'enemy_draw':0,
               'ally_barrier_aoe':0,
               'enemy_barrier_aoe':0,
               'ally_lifesteal_aoe':0,
               'enemy_lifesteal_aoe':0,
               'ally_rush_aoe':0,
               'enemy_rush_aoe':0,
               'ally_silence_aoe':0,
               'enemy_silence_aoe':0,
               'resurrect':0,
               'ally_recall_aoe':0,
               'enemy_recall_aoe':0,
               'ally_split_dmg':0,
               'enemy_split_dmg':0,
               'both_split_dmg':0,
               'ally_split_dmg_face':0,
               'enemy_split_dmg_face':0,
               'both_split_dmg_face':0,
               'summon':0,
               



               'other':0, #target==False, just run playerlist playernum functions
               'target_other':0, #target==True, lambda obj: obj can be card/player
               'myself':0, #lambda 
               
}

locationdict={
               'ally_board':0,
               'enemy_hp':0,
               'enemy_healminion':0,
               'enemy_atk':0,
               'enemy_kill':0,
               'enemy_freeze':0,
               'ally_hand_hp':0,
               'ally_hand_atk':0,
               'ally_hand_manacost':0,
               'ally_hand_discard':0,
               'choose_ally_face':0,
               'choose_enemy_face':0,
               'enemy_barrier':0,  
               'enemy_lifesteal':0,
               'enemy_rush':0,
               'enemy_silence':0,
               'enemy_recall':0,
}



strikedict={
               'enemy_healminion':1,
               'choose_enemy_face':1,
}


#Pygame stuff
#Fixed variables:
cardwidth,cardheight=75,108
clock=pygame.time.Clock()
screenwidth=1050
screenheight=650
buttonwidth,buttonheight = 120,40
win = pygame.display.set_mode((screenwidth,screenheight))
pygame.display.set_caption("Wrath of the Elements")
font=pygame.font.SysFont('arial',20,False,False)
font_mana=pygame.font.SysFont('comic sans ms',17,False,False)
font_card=pygame.font.SysFont('comic sans ms',10,False,False)
font_endgame = pygame.font.SysFont('Arial',200,False,False)

# text=font.render('your text here', 1, (0,0,0)) 
# win.blit(text,position)

leftshiftvalue = 5

endturnpos=(screenwidth-90,screenheight//2-20,80,40)

class Endturn():
    def __init__(self,pos=(endturnpos)):
        self.pos=pos

endturn = Endturn()






#all the classes
    
class Player:
    def __init__(self, deck, playernum=0, health=playerhealth, atk=0, armour=0, graveyard=list(), hand=list(), mana=0, maxmana=0, board=list(), spellyard = list(), board_x=0, board_y=0, board_width=0, board_height=0, hand_x=0, hand_y=0, hand_width=0, hand_height=0, nexus_x=0, nexus_y=0, nexus_width=0, nexus_height=0):
        self.deck=deck, 
        self.playernum=playernum
        self.health=health
        self.atk=atk
        self.armour=armour
        self.graveyard = graveyard
        self.hand=hand
        self.mana=mana
        self.maxmana=maxmana
        self.board = board
        self.discard_pile=list()
        self.board_x=board_x
        self.board_y=board_y
        self.board_width=board_width
        self.board_height=board_height
        self.hand_x=hand_x
        self.hand_y=hand_y
        self.hand_width=hand_width
        self.hand_height=hand_height
        self.nexus_x=nexus_x
        self.nexus_y=nexus_y
        self.nexus_width=nexus_width
        self.nexus_height=nexus_height
        self.nexus_pos=(nexus_x,nexus_y,nexus_width,nexus_height)
        self.millcount = 0
        self.atknum=0 #minion on atk board
        self.defnum=0 #minion on def board
        self.spellyard = spellyard


    #Deck functions: 
    def shuffles(self):
        random.shuffle(self.deck)

    def draw(self, amount):
        rlist = list()
        for _ in range(amount):
            try:
                card = self.deck.pop(0)
                card.display_update()
                self.hand.append(card)
                rlist.append(card)
            except IndexError:
                self.millcount+=1
                self.damage(-self.millcount) 

        checkendgame()
        self.centralize_hand()
        return rlist

    def boardcounter(self):
        self.atknum, self.defnum = 0,0
        for card in self.board:
            if card.played==1:
                self.defnum+=1
            if card.played==2:
                self.atknum+=1

    def mulligan(self): #To mull is a tuple of cardindex eg. (0,2,3)
        to_mull=list()
        while True:
            pressed = self.click1()
            if shutdown or endgame:
                break
            if pressed[1]=='endturn':
                break
            elif pressed[1]=='hand':
                cardindex = self.hand.index(pressed[0])   
                if cardindex in to_mull:
                    to_mull.remove(cardindex)
                    self.hand[cardindex].x_out=False
                    self.hand[cardindex].display_update()
                else:
                    to_mull.append(cardindex)
                    self.hand[cardindex].x_out=True
                    self.hand[cardindex].display_update()
        to_mull.sort(key=lambda x: -x)
        for cardindex in to_mull:
            self.hand[cardindex].x_out=False
            self.deck.append(self.hand.pop(cardindex))
        self.shuffles()
        self.draw(len(to_mull))
#choose up to4
#those selected mull (visual confirmation). else keep.
    



    def discard(self,discard_cls):
        try:
            if discard_cls.disc:
                self.boardcounter()
                if discard_cls.cardtype == 'unit': 
                    self.boardcounter()
                    discard_cls.played=2 if self.atknum<5 else 1 if self.defnum<2 else 0
                    self.board.append(discard_cls) if len(self.board)<7 else 0
                    self.hand.remove(discard_cls)
                elif discard_cls.cardtype == 'spell':
                    discard_cls.played=-1
                    discard_cls.playspell() #Must not be a target spell
                    self.hand.remove(discard_cls)
                print('disc is True')
            else:
                self.discard_pile.append(discard_cls)
                print('card appended to discard pile')
                self.hand.remove(discard_cls)
                print('card is discarded')
        except:
            print('not discarded') #for now

    #Player functions

    def cardstrike(self, selfindex):
        if self.board[selfindex].sleep == False and self.board[selfindex].frozen == False and self.board[selfindex].currentstats[0]:
            self.board[selfindex].selected=True
            obj = self.click2(strikedict)
            if type(obj) ==  Player:
                defended=False
                for card in playerlist[(self.playernum+1)%2].board:
                    if card.played==1 and self.board[selfindex].commando == False: 
                        defended=True
                if defended:
                    print('Hit Defenders first')
                    self.board[selfindex].selected=False
                elif self.board[selfindex].rush:
                    print('Cannot attack player')
                    self.board[selfindex].selected=False
                else:
                    #if self.board[selfindex].duelatk: 
                    #    self.board[selfindex].playduel(obj)
                    playerlist[(self.playernum+1)%2].damage(-self.board[selfindex].currentstats[0])
                    self.board[selfindex].selected=False
                    if self.board[selfindex].lifesteal == True:
                        self.heal(self.board[selfindex].currentstats[0])
                    checkdeath()
                    checkendgame()
                    self.board[selfindex].sleep=True
            elif type(obj) == cardmaker.Card:
                if self.board[selfindex].lifesteal == True and obj.barrier==False:
                    self.heal(self.board[selfindex].currentstats[0])
                self.board[selfindex].strike(obj)
                self.board[selfindex].selected=False
                checkdeath()
                checkendgame()
            else: #Did not click anything in click 2
                print('card strike failed')
                self.board[selfindex].selected=False
        else: #card is sleeping
            print('This unit is unable to strike')
          

        
    def gainmana(self,manaint):
        self.mana+=manaint

    def heal(self,healint): #heal is an int
        self.health+=healint
        if self.health >=playerhealth:
            self.health =  playerhealth
        #return self.health

    def damage(self, dmgint):
        for dmg in range(-dmgint):
            if self.armour>0:
                self.armour-=1
            elif self.health<-5:
                break
            else:
                self.health-=1
        if self.health<=0:
            endgame=True
        #return self.health

    def gainarmour(self, armourint):
        self.armour+=armourint
        if self.armour <0:
           self.armour = 0 
        
    def gainmaxmana(self,maxmanaint):
        self.maxmana += maxmanaint
        if self.maxmana>10:
            self.maxmana=10
        if self.maxmana<0:
            self.maxmana = 0
        

    def recall(self,cardindex=-1):
        self.board[cardindex].sleep = False if self.board[cardindex].charge == True else True
        self.board[cardindex].reset()
        self.hand.append(self.board.pop(cardindex))
        self.hand[-1].currentstats=self.hand[-1].maxstats
        
       
        while len(self.hand)>10:
            self.discard(self.hand[10])

    def movegraveyard(self,cardindex):
        self.graveyard.append(self.board.pop(cardindex))

    def resurrect(self,myattr,myvalue,mylist):
        random.shuffle(mylist)
        deadlist=list()
        card=None
        try:
            if myattr:
                for dedcard in mylist:
                    if getattr(dedcard,myattr)==myvalue:
                        card=dedcard
                        break
                    else:
                        pass
            else:
                card=mylist.pop(rng(0,len(mylist)-1))
            if card:
                self.boardcounter()
                if card.played==1 and self.defnum<2:
                    self.board.append(card)
                elif card.played==2 and self.atknum<5:
                    self.board.append(card)
                else:
                    raise Exception
        except ValueError:
            print('empty graveyard')
        except Exception:
            print('Board is full')

    def playcard(self,cardindex):  #cardindex is from hand
        # Is a unit
        if self.hand[cardindex].cardtype=='unit':
            if self.hand[cardindex].manacost<=self.mana:
                chosencard=self.hand[cardindex]
                chosencard.selected=True
                clicked=(0,0)
                in_def,in_atk=False,False
                while clicked==(0,0):
                    clicked = clicker()
                    if shutdown or endgame:
                        break
                    if inbutton(clicked,(self.board_x,self.board_y,self.board_width*2//7,self.board_height)):
                        in_def=True
                        break
                    elif inbutton(clicked,(self.board_x+self.board_width*2//7,self.board_y,self.board_width*5//7,self.board_height)):
                        in_atk=True
                        break
                self.boardcounter()
                exile=False
                if chosencard==self.hand[0] or chosencard==self.hand[-1]:
                    exile=True
                chosencard.exile=exile
                if in_def:
                    if self.defnum<2:
                        chosencard.sleep=True
                        if chosencard.effectdict!=spelldictnull: # Have effect
                            placeholder=cardmaker.Card('',played=1,shadow=True,player_list=playerlist,player=self.playernum)
                            self.board.append(placeholder)
                            refreshframes()
                            if chosencard.effectdict['target']: # Targetting effect
                                if chosencard.playspell():
                                    chosencard.played=1
                                    chosencard.changestat((-1,2,2))
                                    self.mana-=chosencard.manacost
                                    try: #to remove card from hand
                                       self.hand.remove(chosencard)
                                    except: #card is in discard pile due to discard_all
                                        self.discard_pile.remove(chosencard)
                                    self.board.remove(placeholder)
                                    self.board.append(chosencard)
                                else: #quitted targetting effect
                                    self.board.remove(placeholder)
                            else: #AOE effect
                                try: #to remove card from hand
                                    self.hand.remove(chosencard)
                                except: #card is in discard pile due to discard_all
                                    self.discard_pile.remove(chosencard)
                                chosencard.playspell()
                                chosencard.played=1 
                                chosencard.changestat((-1,2,2))
                                self.mana-=chosencard.manacost
                                self.board.remove(placeholder)
                                self.board.append(chosencard)
                        else: # No effect
                            self.hand[cardindex].played=1 
                            self.hand[cardindex].changestat((-1,2,2))
                            self.mana-=self.hand[cardindex].manacost
                            chosencard = self.hand[cardindex]
                            self.board.append(self.hand.pop(cardindex))
                    else:
                        print("Too many units on defence board!")
                elif in_atk:
                    if self.atknum<5:
                        if chosencard.effectdict!=spelldictnull: # Have effect
                            placeholder=cardmaker.Card('',played=2,shadow=True,player_list=playerlist,player=self.playernum)
                            self.board.append(placeholder)
                            refreshframes()
                            if chosencard.effectdict['target']: # Targetting effect
                                if chosencard.playspell():
                                    chosencard.played=2 
                                    chosencard.changestat((1,0,0))
                                    self.mana-=chosencard.manacost
                                    try: #to remove card from hand
                                       self.hand.remove(chosencard)
                                    except: #card is in discard pile due to discard_all
                                        self.discard_pile.remove(chosencard)
                                    self.board.remove(placeholder) 
                                    self.board.append(chosencard)   
                                else: #quitted targetting effect
                                    self.board.remove(placeholder)    
                            else: #AOE effect
                                try: #to remove card from hand
                                    self.hand.remove(chosencard)
                                except: #card is in discard pile due to discard_all
                                    self.discard_pile.remove(chosencard)
                                chosencard.playspell()
                                chosencard.played=2
                                chosencard.changestat((1,0,0))
                                self.mana-=chosencard.manacost
                                self.board.remove(placeholder) 
                                self.board.append(chosencard)
                        else: # No effect
                            self.hand[cardindex].played=2 #Testing
                            self.hand[cardindex].changestat((1,0,0))
                            self.mana-=self.hand[cardindex].manacost
                            chosencard = self.hand[cardindex]
                            self.board.append(self.hand.pop(cardindex))
                            
                    else:
                        print("Too many units on attack board!") 
                chosencard.selected=False

            else:
                    print("Not enough mana!") 

        #Is a Spell
        elif self.hand[cardindex].cardtype=='spell':
            if self.hand[cardindex].manacost<=self.mana:
                chosencard = self.hand[cardindex]
                if chosencard.effectdict!=spelldictnull: # Have effect
                    if chosencard.effectdict['target']: # Targetting effect
                        if chosencard.playspell():
                            chosencard.played=-1
                            self.mana-=chosencard.manacost
                            try: #to remove card from hand
                                self.hand.remove(chosencard)
                            except: #card is in discard pile due to discard_all
                                self.discard_pile.remove(chosencard)
                            self.spellyard.append(chosencard)
                        else: #quitted targetting effect
                            pass 
                    else: #AOE effect
                        chosencard.selected=True
                        refreshframes()
                        clicked=clicker()
                        while clicked==(0,0):
                            clicked=clicker()
                            if shutdown:
                                break
                        if inbutton(clicked,chosencard.pos):
                            try: #to remove card from hand
                                self.hand.remove(chosencard)
                            except: #card is in discard pile due to discard_all
                                self.discard_pile.remove(chosencard)
                            chosencard.playspell()
                            chosencard.played=-1
                            self.mana-=chosencard.manacost
                            self.spellyard.append(chosencard)
                        else:
                            chosencard.selected=False
                else: # No effect
                    chosencard.played=-1
                    self.mana-=chosencard.manacost
                    self.spellyard.append(chosencard)
            else:
                print("You have not enough mana left!")
           
        for player in playerlist:
            player.centralize_hand()
            player.centralize_board()

    
    # is in draw and playcard
    def centralize_hand(self):
        hand_box = (self.hand_x, self.hand_y, self.hand_width, self.hand_height)
        x_midpoint =  self.hand_x + self.hand_width // 2
        # cardwidth = 75 (already in global variables)
        leftshiftnum = len(self.hand) % 2
        central_card_num = len(self.hand) // 2
        if len(self.hand)%2 == 0:   #no central card
            x_pos = x_midpoint + leftshiftvalue//2 - (cardwidth+leftshiftvalue)*central_card_num
            for card in self.hand:
                card.pos = (x_pos, self.hand_y, cardwidth, cardheight)
                x_pos += leftshiftvalue + cardwidth
        else:   #central card 
            x_pos = x_midpoint - cardwidth//2 - (cardwidth+leftshiftvalue) * central_card_num
            for card in self.hand:
                card.pos = (x_pos, self.hand_y, cardwidth, cardheight)
                x_pos += leftshiftvalue + cardwidth

    # is in playercard and checkdeath
    def centralize_board(self):
        # board_box = (self.board_x, self.board_y, self.board_width, self.board_height)
        def_midpoint =  self.board_x+self.board_width // 7
        atk_midpoint = self.board_x+self.board_width *9 // 14
        atknum, defnum = 0,0
        for card in self.board:
            if card.played==2:
                atknum+=1
            else:
                defnum+=1
        leftshiftatk=atknum%2
        leftshiftdef=defnum%2
        central_card_atk = atknum // 2
        central_card_def = defnum // 2
        #For atk board
        if leftshiftatk == 0:   #no central atk card
            x_pos = atk_midpoint + leftshiftvalue//2 - (cardwidth+leftshiftvalue)*central_card_atk
            for card in self.board:
                if card.played==2:
                    card.pos = (x_pos, self.board_y, cardwidth, cardheight)
                    x_pos += leftshiftvalue + cardwidth
        else:   #central card 
            x_pos = atk_midpoint - cardwidth//2 - (cardwidth+leftshiftvalue) * central_card_atk
            for card in self.board:
                if card.played==2:
                    card.pos = (x_pos, self.board_y, cardwidth, cardheight)
                    x_pos += leftshiftvalue + cardwidth
        if leftshiftdef == 0:   #no central def card
            x_pos = def_midpoint + leftshiftvalue//2 - (cardwidth+leftshiftvalue)*central_card_def
            for card in self.board:
                if card.played==1:
                    card.pos = (x_pos, self.board_y, cardwidth, cardheight)
                    x_pos += leftshiftvalue + cardwidth
        else:   #central card 
            x_pos = def_midpoint - cardwidth//2 - (cardwidth+leftshiftvalue) * central_card_def
            for card in self.board:
                if card.played==1:
                    card.pos = (x_pos, self.board_y, cardwidth, cardheight)
                    x_pos += leftshiftvalue + cardwidth




    def click1(self):
        clicked=clicker()
        for card in self.board:
            if inbutton(clicked,card.pos):
                return (card,'board')
        for card in self.hand:
            if inbutton(clicked,card.pos):
                return (card,'hand')
        if inbutton(clicked,endturn.pos):
            return (0,'endturn')
        else:
            return (0,0)
    


    def click2(self,targetdict=locationdict):
        print('clicked2')
        ally_board=['ally_board']
        for card in self.board:
            ally_board.append((card, card.pos))

        ally_hand_unit=['ally_hand_hp', 'ally_hand_atk']
        for card in self.hand:
            if card.cardtype=='unit':
                ally_hand_unit.append((card,card.pos))

        ally_hand_spell=['ally_hand_manacost', 'ally_hand_discard']
        for card in self.hand:
            ally_hand_spell.append((card,card.pos))

        enemy_board=['enemy_atk','enemy_hp','enemy_kill','enemy_freeze', 'enemy_barrier','enemy_healminion','enemy_silence','enemy_recall']
        for card in playerlist[(self.playernum+1)%2].board:
            enemy_board.append((card,card.pos))

        clicked=clicker()
        while clicked==(0,0):
            clicked=clicker()
            if shutdown:
                break
        print(clicked)
        for key in targetdict:

            if key in ally_board and targetdict[key]!=0:
                for obj in ally_board:
                    if inbutton(clicked,obj[1]):
                        return obj[0]
            elif key in enemy_board and targetdict[key]!=0:
                for obj in enemy_board:
                    if inbutton(clicked,obj[1]):
                        return obj[0]
            elif key in ally_hand_unit and targetdict[key]!=0:
                for obj in ally_hand_unit:
                    if inbutton(clicked,obj[1]):
                        return obj[0]
            elif key in ally_hand_spell and targetdict[key]!=0:
                for obj in ally_hand_spell:
                    if inbutton(clicked,obj[1]):
                        return obj[0]
            elif key=='choose_ally_face' and targetdict[key]!=0:
                if inbutton(clicked,self.nexus_pos):
                     return self
            elif key=='choose_enemy_face' and targetdict[key]!=0:
                 if inbutton(clicked, playerlist[(self.playernum+1)%2].nexus_pos): 
                     return playerlist[(self.playernum+1)%2]
            else:   # does nothing
                pass
        #IF this runs, it means
        print('clicked2 did not click anything')

    def click3(self,targetdict=locationdict):
        #print('clicked3')
        ally_board=['ally_board']
        for card in self.board:
            ally_board.append((card, card.pos))
        if len(self.board)==1:
            ally_board.append((0,0))

        ally_hand_unit=['ally_hand_hp', 'ally_hand_atk']
        for card in self.hand:
            if card.cardtype=='unit':
                ally_hand_unit.append((card,card.pos))
        if len(ally_hand_unit)==2:
            ally_hand_unit.append((0,0))

        ally_hand_spell=['ally_hand_manacost', 'ally_hand_discard']
        for card in self.hand:
            ally_hand_spell.append((card,card.pos))
        if len(self.hand)==1:
            ally_hand_spell.append((0,0))

        enemy_board=['enemy_atk','enemy_hp','enemy_kill','enemy_freeze', 'enemy_barrier', 'enemy_healminion','enemy_silence','enemy_recall']
        for card in playerlist[(self.playernum+1)%2].board:
            enemy_board.append((card,card.pos))
        if len(playerlist[(self.playernum+1)%2].board)==0:
            enemy_board.append((0,0))

        clicked=clicker()
        while clicked==(0,0):
            clicked=clicker()
            if shutdown:
                break
        #print(clicked) 
        placeholder=cardmaker.Card('',player_list=playerlist)
        null = None
        for key in targetdict:
            if key in ally_board and targetdict[key]!=0:
                for obj in ally_board:
                    if inbutton(clicked,obj[1]):
                        return obj[0]
                if ally_board[-1] == (0,0):
                    null = placeholder
            elif key in enemy_board and targetdict[key]!=0:
                for obj in enemy_board:
                    if inbutton(clicked,obj[1]):
                        return obj[0]
                if enemy_board[-1] == (0,0):
                    null = placeholder
            elif key in ally_hand_unit and targetdict[key]!=0:
                for obj in ally_hand_unit:
                    if inbutton(clicked,obj[1]):
                        return obj[0]
                if ally_hand_unit[-1] == (0,0):
                    null = placeholder
            elif key in ally_hand_spell and targetdict[key]!=0:
                for obj in ally_hand_spell:
                    if inbutton(clicked,obj[1]):
                        return obj[0]
                if ally_hand_spell[-1] == (0,0):
                    null = placeholder
            elif key=='choose_ally_face' and targetdict[key]!=0:
                if inbutton(clicked,self.nexus_pos):
                     return self
            elif key=='choose_enemy_face' and targetdict[key]!=0:
                 if inbutton(clicked, playerlist[(self.playernum+1)%2].nexus_pos): 
                     return playerlist[(self.playernum+1)%2]
            else:   # does nothing
                pass
        #IF this runs, it means
        print('clicked3 did not click anything')
        if targetdict['choose_enemy_face'] or targetdict['choose_ally_face']:
            return None
        else:
            return null
                                     
    def discover(self,mylist,myattr,myvalue):
        global discoverlist
        discoverlist=list()
        random.shuffle(mylist)
        for card in mylist:
            if len(discoverlist)>2:
                break
            if type(card)==cardmaker.Card:
                if myattr:
                    if getattr(card,myattr)==myvalue:
                        newcard = copy.copy(card)
                        newcard.player=self.playernum
                        newcard.player_list=playerlist
                        newcard.display=card.display.copy()
                        newcard.sleep=False if (newcard.rush or newcard.charge) else True
                        discoverlist.append(newcard)
                    else: #The values are different
                        pass
                else:
                    newcard = copy.copy(card)
                    newcard.player=self.playernum
                    newcard.player_list=playerlist
                    newcard.display=card.display.copy()
                    newcard.sleep=False if (newcard.rush or newcard.charge) else True
                    discoverlist.append(newcard)
            else: #(mylist contains functions)
                newcard=card(self.playernum,playerlist)
                if myattr:
                    if getattr(newcard,myattr)==myvalue:
                        discoverlist.append(newcard)
                    else: #The values are different
                        pass
                else:
                    discoverlist.append(newcard)
        centralize(discoverlist,width=cardwidth,height=cardheight)
        if not discoverlist:
            print('No cards to discover!')
        while True:
            clock.tick(10)
            if not discoverlist:
                break
            refreshframes()
            clicked=clicker()
            if shutdown:
                break
            for card in discoverlist:
                if inbutton(clicked,card.pos):
                    self.hand.append(card)
                    discoverlist=list()
                    break
####



#other functions


def checkdeath(): 
    fulllist=list()
    for player in playerlist:
        templist=list()
        for cardindex,card in enumerate(player.board):
            if card.currentstats[1] <=0:
                templist.append((cardindex,card))
        templist.sort(key=lambda x: x[0],reverse=True) 
        for cardindex,card in templist:
            player.board[cardindex].reset()
            player.movegraveyard(cardindex)
            player.boardcounter()
        fulllist+=templist
    for cardindex, card in fulllist:
        card.playsnuff() if card.snuffed==True else 0
    for player in playerlist:
        player.boardcounter()
        player.centralize_board()
'''
#Old checkdeath            
def checkdeath(): 
    fulllist=list()
    for player in playerlist:
        templist=list()
        for cardindex,card in enumerate(player.board):
            if card.currentstats[1] <=0:
                templist.append((cardindex,card))
        templist.sort(key=lambda x: x[0],reverse=True) 
        for cardindex,card in templist:
                player.board[cardindex].reset()
                player.movegraveyard(cardindex)
                player.boardcounter()
                card.playsnuff() if card.snuffed==True else 0
        player.centralize_board()
'''    

def turn(whosturn): #whosturn=0 or 1
    for index,player in enumerate(playerlist):
        if index==whosturn:
            for card in player.board: 
                if card.turnstart:
                    card.playstartturn()
                    checkdeath()
                    checkendgame()
                if card.played==1:
                    card.sleep=True
            player.gainmaxmana(1)
            player.mana=player.maxmana
            player.draw(1)
        refreshframes()
    while True:
        checkdeath()
        if shutdown or endgame:
            break
        pressed = playerlist[whosturn].click1()
        if pressed[1]=='endturn':
            break
        elif pressed[1]=='hand':
            cardindex = playerlist[whosturn].hand.index(pressed[0])   
            playerlist[whosturn].playcard(cardindex)
        elif pressed[1]=='board':
            playerlist[whosturn].cardstrike(
                                                            playerlist[whosturn].board.index(pressed[0])
                                                            )     
        checkendgame()

    #Turn ends
    for index,player in enumerate(playerlist):
        if index!=whosturn:
            for card in player.board:
                card.sleep=False
                card.frozen=False
                card.rush=False
    for card in playerlist[whosturn].board: 
        if card.turnend:
            card.playendturn()
            checkdeath()
            checkendgame()
        if card.wither:
            card.changestat((0,-1,0))
    refreshframes()


def checkendgame():
    global endgame
    for player in playerlist:
        if player.health<=0:
            endgame=True
    return endgame

def gamestart():
    startfirst = rng(0,1)
    for player in playerlist:
        player.draw(4)
        player.mulligan()
        player.shuffles()
    if startfirst==1:
        print('opponent start first')
        playerlist[0].hand.append(cardmaker.Card('Mana Coin',manacost=0,cardtype='spell', effectdict={'ally_current_mana':1,'target':0},art=mana_blue,player=0,player_list=playerlist))
        playerlist[0].hand[-1].display_update()
    else:
        print('you start first')
        playerlist[1].hand.append(cardmaker.Card('Mana Coin', manacost=0,cardtype='spell', effectdict={'ally_current_mana':1,'target':0},art=mana_blue,player=1,player_list=playerlist))
        playerlist[1].hand[-1].display_update()
    refreshframes()
    return startfirst


#Pygame Functions Starts Here

def clicker():
    global shutdown
    mousepos= (0,0)
    clickedpos=(0,0)
    templist=list()
    for player in playerlist:
        templist+=[card for card in player.board]
        templist+=[card for card in player.hand]
    templist+=discoverlist
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shutdown=True
        if event.type == pygame.MOUSEBUTTONUP:
            mousepos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[2]:
        clickedpos = pygame.mouse.get_pos()
    for card in templist:
        card.showtext=True if inbutton(pygame.mouse.get_pos(), card.pos) else False
    refreshframes()
    return mousepos

def inbutton(click,buttonpos):
    value=False
    try:
        if click[0] in range(buttonpos[0],buttonpos[0]+buttonpos[2]):
            if click[1] in range(buttonpos[1],buttonpos[1]+buttonpos[3]):
                value=True
    except:
        pass
    return value


def refreshframes():
    
    drawbg()
    drawstatus()
    checkendgame()
    pygame.display.update()

def drawbg():
    win.blit(background,(0,0))
    pygame.draw.rect(win, (200,150,150),endturnpos)

    win.blit(red_nexus,(25,200))
    pygame.draw.rect(win, (255,255,255),playerlist[1].nexus_pos,1)
    nexus_str = str(playerlist[1].health) + ' / ' + str(playerhealth)
    text=font_mana.render(nexus_str, 1, (255,100,100)) 
    win.blit(text,(20,260))
    playerdeck1_str = str(len(playerlist[1].deck)) + ' / ' + ' 30 '
    text= font_mana.render(playerdeck1_str, 1, (255,100,100))
    win.blit(text, (screenwidth-100, 50 + cardheight + 10))
    if len(playerlist[1].deck) >0:	
        win.blit(card_back, (screenwidth-100, 50))
        win.blit(card_back, (screenwidth-102, 48))
        if len(playerlist[1].deck) > 10:
            win.blit(card_back, (screenwidth-104, 46))
            win.blit(card_back, (screenwidth-106, 44))
            if len(playerlist[1].deck) >20:
                win.blit(card_back, (screenwidth-108, 42))
                win.blit(card_back, (screenwidth-110, 40)) 
    else:
        #pygame.draw.rect(win, (80,40,0),(screenwidth-100,50,cardwidth,cardheight))
        pygame.draw.rect(win, (255,255,255),(screenwidth-100,50,cardwidth,cardheight),7)
    playerdeck0_str = str(len(playerlist[0].deck)) + ' / ' + ' 30 '
    text= font_mana.render(playerdeck0_str, 1, (100,100,255))
    win.blit(text, (screenwidth-100, 480 - 10-(text.get_height())))
    if len(playerlist[0].deck) >0:	
        win.blit(card_back, (screenwidth-100, 490))
        win.blit(card_back, (screenwidth-102, 488))
        if len(playerlist[0].deck) > 10:
            win.blit(card_back, (screenwidth-104, 486))
            win.blit(card_back, (screenwidth-106, 484))
            if len(playerlist[0].deck) >20:
                win.blit(card_back, (screenwidth-108, 482))
                win.blit(card_back, (screenwidth-110, 480)) 
    else:
        #pygame.draw.rect(win, (80,40,0),(screenwidth-100,490,cardwidth,cardheight))
        pygame.draw.rect(win, (255,255,255),(screenwidth-100,490,cardwidth,cardheight),7)

    win.blit(blue_nexus,(25,390))
    pygame.draw.rect(win, (255,255,255),playerlist[0].nexus_pos,1)
    nexus_str = str(playerlist[0].health) + ' / ' + str(playerhealth)
    text=font_mana.render(nexus_str, 1, (100,100,255)) 
    win.blit(text,(20,365))
    
    armour_str = str(playerlist[1].armour) if playerlist[1].armour else ''
    if armour_str:
        text=font_mana.render(armour_str, 1, (255,255,255))
        win.blit(armour_base,(43,218))
        armour_width, armour_height = text.get_size()
        win.blit(text,(64-armour_width//2, 240-armour_height//2))

    armour_str = str(playerlist[0].armour) if playerlist[0].armour else ''
    if armour_str:
        text=font_mana.render(armour_str, 1, (255,255,255))
        win.blit(armour_base,(43,408))
        armour_width, armour_height = text.get_size()
        win.blit(text,(64-armour_width//2, 430-armour_height//2))

    win.blit(mana_red, (screenwidth-150,200))
    mana_str = str(playerlist[1].mana) + ' / ' + str(playerlist[1].maxmana)
    text=font_mana.render(mana_str, 1, (255,100,100)) 
    win.blit(text,(screenwidth-100,210))

    win.blit(mana_blue, (screenwidth-150,390))
    mana_str = str(playerlist[0].mana) + ' / ' + str(playerlist[0].maxmana)
    text=font_mana.render(mana_str, 1, (100,100,255)) 
    win.blit(text,(screenwidth-100,400))

    #Which turn
    text=font_mana.render('Turn ' + str(turnnumber), 1, (255,255,255)) 
    win.blit(text,(screenwidth//2,10))

    text=font.render('End Turn', 1, (0,0,0)) 
    textwidth,textheight=text.get_width(),text.get_height()
    win.blit(text,(screenwidth-50-textwidth//2,screenheight//2-textheight//2))
    
def drawstatus():
    templist=list()
    for player in playerlist:
        while len(player.hand) >10:
            card=player.hand[-1]
            player.discard(card)

        for card in player.board:
            card.display_update()
        for card in player.hand:
            card.display_update()
        pygame.draw.rect(win,(255,255,255),(player.hand_x, player.hand_y, player.hand_width, player.hand_height),1)
        pygame.draw.rect(win,(255,255,255),(player.board_x,player.board_y,player.board_width, player.board_height),1)
        pygame.draw.line(win,(255,255,255),(player.board_x+player.board_width*2//7, player.board_y),(player.board_x+player.board_width*2//7,player.board_y+player.board_height),1)
        player.centralize_hand()
        player.centralize_board()
        for card in player.hand:
            win.blit(card.display,card.pos)
            templist.append(card)
        for card in player.board:
            win.blit(card.display,card.pos)
            templist.append(card)
    for card in discoverlist:
        card.display_update()
        win.blit(card.display,card.pos)
        templist.append(card)
    for card in templist:
        if card.showtext==True:
            to_blit = card.text_bubble()
            width,height = to_blit.get_size()
            x = card.pos[0]+(card.pos[2] - width) //2
            y = card.pos[1]-height
            pos=(x,y,width,height)
            win.blit(to_blit,pos)

def mainloop():
    global endgame,shutdown,playerlist,turnnumber, deck1, deck2
    turnnumber=0
    
    playerlist=list()
    playerlist.append(Player(deck=list(),playernum=0,atk=0,armour=0,graveyard=list(),hand=list(),mana=0, board=list(), 
                        hand_x=100, hand_y=490, hand_width=800, hand_height=cardheight,
                        board_x=100, board_y=360, board_width=800, board_height=cardheight,
                        nexus_x=25, nexus_y=390, nexus_width=blue_nexus.get_width(), nexus_height=blue_nexus.get_height()
                         ))
    playerlist.append(Player(deck=list(),playernum=1,atk=0,armour=0,graveyard=list(),hand=list(),mana=0,
    board=list(), 
                        hand_x=100, hand_y=50, hand_width=800, hand_height=cardheight,
                        board_x=100, board_y=180, board_width=800, board_height=cardheight,
              nexus_x=25, nexus_y=200, nexus_width=red_nexus.get_width(), nexus_height=red_nexus.get_height()
                         ))
    #Creating Cards
    playerlist[0].deck = importdeck(0,playerlist,'decks/'+deck1)
    playerlist[1].deck = importdeck(1,playerlist,'decks/'+deck2)

    #playerlist[0].deck = cardmaker.createdeck(0,playerlist)
    #playerlist[1].deck = cardmaker.createdeck(1,playerlist)

    #for player in playerlist:
    #    player.deck=cardmaker.createdeck(player.playernum,playerlist)
    
    #Game start
    refreshframes()
    print('Starting Game...')
    for player in playerlist:
        player.shuffles()
    whos_turn = gamestart()
    # whos_turn = 0

    #Mainloop
    while True:
        refreshframes()
        turnnumber+=1
        turn(whos_turn%2)
        whos_turn+=1
        if endgame or shutdown:
            break
    if endgame:
        if playerlist[0].health >0:
            text='You Win!'
        else:
            text='You Lose!'
        text_endgame=font_endgame.render(text, 1,(255,255,255))
        size = text_endgame.get_size()
        pos = (screenwidth//2 - size[0]//2, screenheight//2 - size[1]//2)
        win.blit(text_endgame, pos)
        pygame.display.update()
        time.sleep(2)
    endgame=False
    return True






#Home screen part:
def clicker2():
    global shutdown
    mousepos= (0,0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shutdown=True
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            mousepos = pygame.mouse.get_pos()
    return mousepos


def centralize(mylist,y=screenheight//2,midpoint = screenwidth//2,leftshiftvalue=10,width=buttonwidth,height=buttonheight):
    leftshiftnum = len(mylist)%2
    centralnum=len(mylist)//2
    if leftshiftnum: #is 1, central button
        x = midpoint - width//2 - (width+leftshiftvalue)*centralnum
        for button in mylist:
            button.pos = (x,y,width,height)
            x+= leftshiftvalue+width
    else:
        x=midpoint+leftshiftvalue//2-(width+leftshiftvalue)*centralnum
        for button in mylist:
            button.pos = (x,y,width,height)
            x+= leftshiftvalue+width


class Button():
    def __init__(self,text='Button',pos=(screenwidth,screenheight,buttonwidth,buttonheight),play=lambda:True):
        self.pos = pos
        self.text = text
        text = font.render(str(text),1,(0,0,0))
        self.art = pygame.Surface((self.pos[2],self.pos[3]))
        self.play=play
        self.selected=False
    def draw(self):
        self.art.fill((215,220,235))
        text = font.render(str(self.text),1,(0,0,0))
        width = text.get_width()
        self.art.blit(text,(self.pos[2]//2-width//2-2,5))
        if self.selected==True:
            pygame.draw.rect(self.art, (50,220,50),(0,0,buttonwidth,buttonheight),8)
        win.blit(self.art,self.pos,(0,0,self.pos[2],self.pos[3]))



class Manabutton(Button):
    def __init__(self,text='Button',pos=(screenwidth,screenheight,30,30),play=lambda:True):
        super().__init__(text,pos,play)
        self.selected=False
    def draw(self):
        self.art.fill((100,100,255))
        text = font.render(str(self.text),1,(0,0,0))
        width = text.get_width()
        self.art.blit(text,(self.pos[2]//2-width//2-2,3))
        if self.selected==True:
            pygame.draw.rect(self.art, (50,220,50),(0,0,30,30),4)
        win.blit(self.art,self.pos)

class Cardbutton(Button):
    def __init__(self,text='Button',pos=(screenwidth,screenheight,buttonwidth,17),play=lambda:True,name='',manacost='',type='', quantity=1):
        
        super().__init__(text,pos,play)
        self.name=name
        self.manacost=manacost
        self.type=type
        self.quantity=quantity
        if self.quantity==2:
            self.text += ' x2'
        else:
            self.text += ' x1'

        region  = getattr(cardmaker, name)(2,[]).region
        if region=='Neutral':
            self.color = (240,220,190)
        elif region=='Earth':
            self.color = (220,160,130)
        elif region=='Air':
            self.color = (255,255,240)
        elif region=='Water':
            self.color = (210,190,255)
        elif region=='Fire':
            self.color = (255,200,190)
        else:
            self.color = (0,0,0)
            print('Not defined')

    def draw(self):
        self.art.fill(self.color)
        
        if self.quantity==2:
            self.text = self.text[:-2] +  'x2'
        else:
            self.text = self.text[:-2] +  'x1'
        
        text = font_card.render(str(self.text),1,(0,0,0))
        width = text.get_width()
        self.art.blit(text,(self.pos[2]//2-width//2-2,2))
        win.blit(self.art,self.pos)
        

startgame=Button(text='Play',pos=(0,0,buttonwidth,buttonheight))
howtoplay=Button('How To Play')
deckcollection = Button('Deck Collection')

back=Button('< Back',pos=(10,10,buttonwidth,buttonheight))
next1=Button('Next >',pos=(screenwidth-buttonwidth-10,10,buttonwidth,buttonheight))


home_buttons = [startgame,howtoplay,deckcollection]
centralize(home_buttons)

  
regionselect=''
regionbuttons=list()
regionbuttons.append(Button('Air'))
regionbuttons.append(Button('Earth'))
regionbuttons.append(Button('Water'))
regionbuttons.append(Button('Fire'))
#regionbuttons.append(Button('Ice'))
#regionbuttons.append(Button('Shadow'))
#regionbuttons.append(Button('Light'))
regionbuttons.append(Button('Neutral'))

centralize(regionbuttons,25)

manaselect=''
manabuttons=list()
manabuttons.append(Manabutton('0'))
manabuttons.append(Manabutton('1'))
manabuttons.append(Manabutton('2'))
manabuttons.append(Manabutton('3'))
manabuttons.append(Manabutton('4'))
manabuttons.append(Manabutton('5'))
manabuttons.append(Manabutton('6'))
manabuttons.append(Manabutton('7'))
manabuttons.append(Manabutton('8'))
manabuttons.append(Manabutton('9'))
manabuttons.append(Manabutton('10'))

centralize(manabuttons,75,width=30,height=30)


deckselect=''
deckbuttons=list()
deckbuttons.append(Button('Deck 1'))
deckbuttons.append(Button('Deck 2'))
deckbuttons.append(Button('Deck 3'))
deckbuttons.append(Button('Deck 4'))
deckbuttons.append(Button('Deck 5'))
deckbuttons.append(Button('Deck 6'))
deckbuttons.append(Button('Deck 7'))
deckbuttons.append(Button('Deck 8'))
deckbuttons.append(Button('Deck 9'))
deckbuttons.append(Button('Deck 10'))

deckx,decky = 25,115
for button in deckbuttons:
    button.pos= (deckx,decky,buttonwidth,buttonheight)
    decky+=50


save = Button('Save')
save.pos = 945,590,buttonwidth-30,buttonheight

confirm = Button('Confirm')
confirm.pos = 945,590,buttonwidth-30,buttonheight


def drawhome(click=(0,0)):
    win.blit(background,(0,0))
    for button in home_buttons:
        button.draw()
    pygame.display.update()

rulestext='''Wrath of the Elements is a 1v1 turnbased cardgame between 2 opponents   
where Players take turns to summon minions and cast spells.  
GAMEPLAY:  
Each Player has a deck of 30 cards.  
Each player starts with 25hp, 0 mana and 4 cards which can be mulliganed (rerolled) at the start of the game.  
The Player that starts second gets a 'Mana Coin' card that gives the Player one mana for a turn.  
Each minion/spell costs mana to play.  
Every turn start, each Player gains 1 maximum mana, restores to full mana, and draws a card.  
Minions can be played on either the Defence board, or the Attack board.  
Unless they have RUSH or CHARGE, they will be ASLEEP for a turn when first played.  
Minons played on the Defence board will be granted -1/+2 effect.  
while minions on the Attack board will be granted +1/0 effect.  
Minions on the defence board cannot attack at all. They are always ASLEEP.  
Minions on the attack board can attack any minion.  
Minions can attack the Opponent only when there are no minions on the Opponent's defence board.  
Up to 2 minions can be played on the defence board and 5 minions on the attack board.  
Up to 10 cards can be kept in the Player's hand. If you draw a card with 10 cards in hand, DISCARD the card.  
If you have no cards left in the deck, you take 1 damage when you draw a card.  
Every successive card draw, you take 1 extra damage.  
The game ends when a Player's health drops below 0.  
'''

keywordtext='''SUMMON: Adds a card to a specific location, usually the board. Doesn't trigger CASTING.  
CASTING: Triggers a card's 'CASTING' effects, ONLY when a card is played from hand.  
SNUFF: Trigger a minion's SNUFF effects when it dies.  
TURNSTART: Trigger's a minion's TURNSTART effects at the start of the Player's turn.  
TURNEND: Trigger's a minion's TURNEND effects at the end of the Player's turn.  
ALLIANCE: Trigger a minion's ALLIANCE effect if minions of the same region are on your board.  
SILENCE: Removes all KEYWORDS from a minion. Reverts its stats to original stats.  
HEAL: Restores the target's health by HEAL amount, capped at its MAX Health.  
BUFF: Increases the target's MAX Attack / Health by BUFF amount.   
KILL: Deals damage equal to a minion's health. Ignores BARRIER.  
DESTROY: KILL a minion, but does NOT trigger SNUFF effects.  
OBLITERATE: Banishes the card from the game. Forever.  
ASLEEP: Unable to attack. Most minions are ASLEEP when played.  
RUSH: Not ASLEEP. Can only attack minions when first played. Loses 'RUSH' at the end of your turn.  
CHARGE: Not ASLEEP. Can attack minions or Player when first played.  
COMMANDO: Can attack Player even if there are minions on Player's defence board.  
LIFESTEAL: Heals the Player by its damage dealt on your turn.  
BARRIER: Immune to the first damage dealt. Loses 'barrier' after.  
FREEZE: FREEZE a minion. It cannot attack on the Player's next turn.  
RECALL: Return minion to Player's hand. It keeps any change in stats.  
DISCARD: Removes a minion from Player's hand into a 'discard pile'.  
RESURRECT: Summons a dead minion from the graveyard.  
ARMOUR: A secondary form of Player health. Damage taken is deducted from ARMOUR before health.'''


def drawhowtoplay(click=(0,0)):
    win.blit(background,(0,0))
    back.draw()
    next1.draw()
    font_rules=pygame.font.SysFont('Arial',40,False,False)
    font_rules.set_underline(True)
    text=font_rules.render('RULES',1,(255,255,255),(0,0,0))
    win.blit(text,((1050-text.get_width())//2,10))
    text=font_mana.render('Lorem ipsum',1,(0,0,0))
    height=text.get_height()
    y = 100
    for sentence in rulestext.split('  \n'):
        text=font_mana.render(sentence,1,(255,255,255),(0,0,0))
        win.blit(text,(30,y))
        y+=height+3
    pygame.display.update()


def drawkeywords(click=(0,0)):
    win.blit(background,(0,0))
    back.draw()
    font_rules=pygame.font.SysFont('Arial',40,False,False)
    font_rules.set_underline(True)
    text=font_rules.render('KEYWORDS',1,(255,255,255),(0,0,0))
    win.blit(text,((1050-text.get_width())//2,10))
    text=font_mana.render('Lorem ipsum',1,(0,0,0))
    height=text.get_height()
    y = 80
    for sentence in keywordtext.split('  \n'):
        text=font_mana.render(sentence,1,(255,255,255),(0,0,0))
        win.blit(text,(30,y))
        y+=height
    pygame.display.update()




def cardtoshow():
    global displaydict
    displaydict = dict()
    for cardname, cardclass in allcarddict.items():
        if manaselect or regionselect:
            if manaselect:
                if regionselect: #Both region and mana selected
                    if str(cardclass.manacost) == manaselect and cardclass.region==regionselect:
                        displaydict[cardname] = cardclass
                else: #Only mana selected
                    if str(cardclass.manacost) == manaselect:
                        displaydict[cardname] = cardclass
            else: #only region selected
                if cardclass.region==regionselect:
                    displaydict[cardname] = cardclass
                
    
def savedeck(mylist, filename):
    if filename:
        filename = 'decks/'+filename+'.txt'
        with open(filename, 'w') as f:
            for line in mylist:
                f.write(line + '\n')
        
    else:
        print('Not saving to any file!')

fileopen=False
newdeck=list()

def drawdeckcollection(click=(0,0)):
    global regionselect,manaselect,deckselect,newdeck,fileopen

    win.blit(background,(0,0))
    back.draw()
    save.draw()
    font_rules=pygame.font.SysFont('Arial',40,False,False)
    font_rules.set_underline(True)
    
    for button in regionbuttons: #Blit region selection
        if inbutton(click,button.pos):
            if regionselect!=button.text:
                regionselect = button.text
            else:
                regionselect=''
        if regionselect == button.text:
            button.selected=True
        else:
            button.selected=False
        button.draw()

    for button in manabuttons: #Blit mana selection
        if inbutton(click,button.pos):
            if manaselect!=button.text:
                manaselect = button.text
            else:
                manaselect=''
        if manaselect == button.text:
            button.selected=True
        else:
            button.selected=False
        button.draw()
            
    cardtoshow()
        
    x,y=170,115
    for cardname, cardclass in displaydict.items(): #Blit on screen
        cardclass.pos = x,y,cardwidth,cardheight
        cardclass.display_update()
        win.blit(cardclass.display,cardclass.pos)
        cardclass.showtext=True if inbutton(pygame.mouse.get_pos(),cardclass.pos) else False
        if cardclass.showtext==True:
            to_blit = cardclass.text_bubble()
            width,height = to_blit.get_size()
            textx = cardclass.pos[0]+(cardclass.pos[2] - width) //2
            texty = cardclass.pos[1]-height
            pos=(textx,texty,width,height)
            win.blit(to_blit,pos)
        x+=cardwidth+7
        if x>880:
            x=170
            y+=cardheight+25
                

    newdeck = sorted(sorted(newdeck,key=lambda button: button.text), key=lambda button: button.manacost)
    buttonx,buttony = 930, 10
    for button in newdeck: #Blit on screen
        button.pos=(buttonx,buttony,buttonwidth,17)
        buttony+=19
        button.draw()


    for button in deckbuttons: 
        if inbutton(click,button.pos):
            if deckselect!=button.text:
                deckselect = button.text
            else:
                deckselect=''
                newdeck=list()
                fileopen=False
        if deckselect == button.text:
            button.selected=True
        else:
            button.selected=False
        button.draw()

    if deckselect:
        if fileopen==True:
            total = 0
            for button in newdeck:
                total+=button.quantity

            for button in newdeck: #removing from deck
                if inbutton(click,button.pos):
                    if button.quantity==1:
                        newdeck.remove(button)
                    else: 
                        button.quantity-=1     
                    break

            for cardname,cardclass in displaydict.items(): #add to deck
                if inbutton(click,cardclass.pos):
                    if total<30:
                        havecard=False
                        for button in newdeck:
                            if button.name==cardname:
                                havecard=True
                                if button.quantity==1:
                                    button.quantity+=1
                                else:
                                    print('cannot add more than 2 card')
                                break
                        if havecard==False:
                            newdeck.append(Cardbutton(cardclass.name, name=cardname, manacost=cardclass.manacost, type=cardclass.cardtype))
                    
                    else:
                        print('More than 30 cards!') 
        else:
            newdeck=list()
            try:
                with open('decks/'+deckselect+'.txt' , 'r') as f:
                    for line in f:
                        mycard = getattr(cardmaker, line.strip())(2,list())
                        havecard=False
                        for button in newdeck:
                            if button.name==line.strip():
                                havecard=True
                                button.quantity+=1
                                break
                        if havecard==False:                        
                            newdeck.append(Cardbutton(mycard.name, name=line.strip(), manacost=mycard.manacost, 
type=mycard.cardtype))
                fileopen=True
            except:
                with open('decks/'+deckselect+'.txt' , 'w') as f:
                    pass
                print('no file, creating one now')
                fileopen=True
    else:
        newdeck=list()

    if inbutton(click,save.pos):
        total = 0
        for button in newdeck:
            total+=button.quantity
        if total<30:
            print('Not enuf cards!')
        else:
            print('saved :^)')
            newdecknames=list()
            for button in newdeck: #list of strings of truename
                for _ in range(button.quantity):
                    newdecknames.append(button.name)
            savedeck(newdecknames,deckselect)
        
    pygame.display.update()


playerselect=0
deck1 = 'Deck 1.txt'
deck2= 'Deck 1.txt'
mydeck=list()
def drawselectdeck1(click=(0,0)):
    global playerselect,deck1,mydeck
    win.blit(background,(0,0))
    back.draw()
    next1.draw()
    if inbutton(click,next1.pos):
        playerselect+=1
        loopframe(drawselectdeck2,[back])
        playerselect=0
    for button in deckbuttons:
        if inbutton(click, button.pos):
            mydeck=list()
            deck1 = button.text + '.txt'
            with open('decks/'+deck1 , 'r') as f:
                for line in f:
                    mycard = getattr(cardmaker, line.strip())(2,list())
                    mydeck.append(mycard)
 
        if deck1[:-4]==button.text:
            button.selected=True
        else:
            button.selected=False
        button.draw()
    x,y=170,115
    for cardclass in mydeck: #Blit on screen
        cardclass.pos = x,y,cardwidth,cardheight
        cardclass.display_update()
        win.blit(cardclass.display,cardclass.pos)
        cardclass.showtext=True if inbutton(pygame.mouse.get_pos(),cardclass.pos) else False
        if cardclass.showtext==True:
            to_blit = cardclass.text_bubble()
            width,height = to_blit.get_size()
            textx = cardclass.pos[0]+(cardclass.pos[2] - width) //2
            texty = cardclass.pos[1]-height
            pos=(textx,texty,width,height)
            win.blit(to_blit,pos)
        x+=cardwidth+7
        if x>880:
            x=170
            y+=cardheight+25
    font_rules=pygame.font.SysFont('Arial',40,False,False)
    font_rules.set_underline(True)
    text=font_rules.render('Player '+str(playerselect+1)+', Select Deck',1,(255,255,255),(0,0,0))
    win.blit(text,((1050-text.get_width())//2,10))
    pygame.display.update()


def drawselectdeck2(click=(0,0)):
    global playerselect,deck2,mydeck
    win.blit(background,(0,0))
    back.draw()
    confirm.draw()
    if inbutton(click,confirm.pos):
        confirm.play()
    for button in deckbuttons:
        if inbutton(click, button.pos):
            mydeck=list()
            deck2 = button.text + '.txt'
            with open('decks/'+deck2 , 'r') as f:
                for line in f:
                    mycard = getattr(cardmaker, line.strip())(2,list())
                    mydeck.append(mycard)
        if deck2[:-4]==button.text:
            button.selected=True
        else:
            button.selected=False
        button.draw()
    x,y=170,115
    for cardclass in mydeck: #Blit on screen
        cardclass.pos = x,y,cardwidth,cardheight
        cardclass.display_update()
        win.blit(cardclass.display,cardclass.pos)
        cardclass.showtext=True if inbutton(pygame.mouse.get_pos(),cardclass.pos) else False
        if cardclass.showtext==True:
            to_blit = cardclass.text_bubble()
            width,height = to_blit.get_size()
            textx = cardclass.pos[0]+(cardclass.pos[2] - width) //2
            texty = cardclass.pos[1]-height
            pos=(textx,texty,width,height)
            win.blit(to_blit,pos)
        x+=cardwidth+7
        if x>880:
            x=170
            y+=cardheight+25
    font_rules=pygame.font.SysFont('Arial',40,False,False)
    font_rules.set_underline(True)
    text=font_rules.render('Player '+str(playerselect+1)+', Select Deck',1,(255,255,255),(0,0,0))
    win.blit(text,((1050-text.get_width())//2,10))
    pygame.display.update()



def loopframe(disp_func=lambda:True,buttons=list()):
    global shutdown
    while True:
        clock.tick(10)
        if shutdown:
            break
        click=clicker2()
        disp_func(click)
        breakval=False
        for button in buttons:
            if inbutton(click,button.pos):
                breakval = button.play() or breakval
        if breakval==True:
            break



howtoplay.play = lambda: loopframe(drawhowtoplay,[back,next1])
next1.play     = lambda: loopframe(drawkeywords,[back])
deckcollection.play= lambda: loopframe(drawdeckcollection,[back])

def playgame():
    global endgame, playerselect
    mainloop()
    endgame=False
    playerselect=1
    return True
confirm.play = playgame

def importdeck(player_num, player_list, filename='decks/mydeck.txt'):
    deck=list()
    with open(filename,'r') as f:
        for line in f:
            cardfunc = getattr(cardmaker,line.strip())
            deck.append(cardfunc(player_num,player_list))
    return deck        


while True:
    clock.tick(10)
    if shutdown:
        break
    click=clicker2()
    drawhome()
    if inbutton(click,startgame.pos):
        loopframe(drawselectdeck1,[back])
    elif inbutton(click,howtoplay.pos):
        loopframe(drawhowtoplay,[back,next1])
    elif inbutton(click, deckcollection.pos):
        deckcollection.play()

pygame.quit()





