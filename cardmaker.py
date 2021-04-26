#!/usr/bin/env python
import random
from random import shuffle, randint as rng
import time
import pygame
import copy
from picturedump import *
pygame.init()

#/resources
cardwidth,cardheight=75,108

font_card=pygame.font.SysFont('times new roman',10,False,False) 
font_bubble=pygame.font.SysFont('comic sans ms',10,False,False) 
cardlist=list()

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
               'summon':0, #tuple
               



               'other':0, #target==False, just run playerlist playernum functions
               'target_other':0, #target==True, lambda obj: obj can be card/player
               'myself':0, #lambda 
               'discover':0, #tuple
               'resurrect':0,
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




def spelldictdesc(player_list, key, value, obj):
    if key=='target':
        pass
    elif type(obj) == int: #Is AOE
        if key=='ally_hand_manacost_aoe':
            return [card.changemana(value) for card in player_list[obj].hand]
        if key == 'ally_deck_manacost_aoe':
            return [card.changemana(value) for card in player_list[obj].deck]
        if key == 'ally_hand_discard_aoe':
            return [player_list[obj].discard(card) for card in player_list[obj].hand.copy()]
        if key == 'enemy_hand_discard_aoe':
            return [player_list[(obj_1)%2].discard(card) for card in player_list[(obj+1)%2].hand.copy()]
        #if key == 'ally_hand_discard_aoe':
          # return [player_list[obj].discard_pile.append(player_list[obj].hand.pop(-1)) for _ in range(len(player_list[obj].hand))]
        if key == 'ally_deck_discard_aoe': 
            return [player_list[obj].discard_pile.append(player_list[obj].deck.pop(-1)) for _ in range(len(player_list[obj].deck))]
        if key == 'enemy_deck_discard_aoe': 
            return [player_list[(obj+1)%2].discard_pile.append(player_list[(obj+1)%2].deck.pop(-1)) for _ in range(len(player_list[(obj+1)%2].deck))]
        if key =='ally_freeze_aoe':
            return [card.freeze() for card in player_list[obj].board]
        if key == 'enemy_freeze_aoe':
            return [card.freeze() for card in player_list[(obj+1)%2].board]
        if key ==  'ally_kill_aoe':
            return [card.kill() for card in player_list[obj].board]
        if key == 'enemy_kill_aoe':
            return [card.kill() for card in player_list[(obj+1)%2].board]
        if key == 'ally_atk_aoe':
            return [card.changestat((value,0,0)) for card in player_list[obj].board]
        if key == 'enemy_atk_aoe':
            return [card.changestat((value,0,0)) for card in player_list[(obj+1)%2].board]
        if key == 'ally_hp_aoe': #buff max hp
            return [card.changestat((0,value,0)) for card in player_list[obj].board]
        if key == 'enemy_hp_aoe': #buff max hp
            return [card.changestat((0,value,0)) for card in player_list[(obj+1)%2].board]
        if key == 'ally_healminion_aoe': #heal current hp
            return [card.changestat((0,0,value)) for card in player_list[obj].board]
        if key == 'enemy_healminion_aoe': #heal current hp
            return [card.changestat((0,0,value)) for card in player_list[(obj+1)%2].board]
        if key == 'ally_draw':
           return player_list[obj].draw(value)
        if key ==  'enemy_draw':
            return player_list[(obj+1)%2].draw(value)
        if key == 'ally_face':
            return player_list[obj].damage(value) if value<0 else player_list[obj].heal(value)
        if key == 'enemy_face':
            return player_list[(obj+1)%2].damage(value) if value<0 else player_list[(obj+1)%2].heal(value)
        if key == 'ally_current_mana':
            return player_list[obj].gainmana(value)
        if key == 'enemy_current_mana':
            return player_list[(obj+1)%2].gainmana(value)
        if key == 'ally_max_mana': 
            return player_list[obj].gainmaxmana(value)
        if key == 'enemy_max_mana':
            return player_list[(obj+1)%2].gainmaxmana(value)
        if key == 'ally_armour':
            return player_list[obj].gainarmour(value)
        if key == 'enemy_armour':
            return player_list[(obj+1)%2].gainarmour(value)
        if key == 'ally_barrier_aoe':
        	return [card.gainbarrier() for card in player_list[obj].board]
        if key == 'enemy_barrier_aoe':
        	return [card.gainbarrier() for card in player_list[(obj+1)%2].board]
        if key == 'ally_lifesteal_aoe':
        	return [card.gainlifesteal() for card in player_list[obj].board]
        if key == 'enemy_lifesteal_aoe':
        	return [card.gainlifesteal() for card in player_list[(obj+1)%2j].board]
        if key == 'ally_rush_aoe':
        	return [card.gainrush() for card in player_list[obj].board]
        if key == 'enemy_rush_aoe':
        	return [card.gainrush() for card in player_list[(obj+1)%2].board]
        if key == 'ally_silence_aoe':
        	return [card.silence() for card in player_list[obj].board]
        if key == 'enemy_silence_aoe':
        	return [card.silence() for card in player_list[(obj+1)%2].board]
        if key == 'ally_recall_aoe':
        	return [player_list[obj].recall() for _ in range(len(player_list[obj].board))]
        if key == 'enemy_recall_aoe':
        	return [player_list[(obj+1)%2].recall() for _ in range(len(player_list[(obj+1)%2].board))]
        if key == 'ally_split_dmg':
            templist=list()
            templist+=player_list[obj].board
            for _ in range(value):
                if templist:
                    random.shuffle(templist)
                    card=templist[0]
                    card.changestat((0,0,-1))
                    if card.currentstats[1]<1:
                        templist.remove(card)
            return
        if key == 'enemy_split_dmg':
            templist=list()
            templist+=player_list[(obj+1)%2].board
            for _ in range(value):
                if templist:
                    random.shuffle(templist)
                    card=templist[0]
                    card.changestat((0,0,-1))
                    if card.currentstats[1]<1:
                        templist.remove(card)
            return
        if key == 'both_split_dmg':
            templist=list()
            templist+=player_list[obj].board
            templist+=player_list[(obj+1)%2].board
            for _ in range(value):
                if templist:
                    random.shuffle(templist)
                    card=templist[0]
                    card.changestat((0,0,-1))
                    if card.currentstats[1]<1:
                        templist.remove(card)
            return
        if key == 'ally_split_dmg_face':
            templist=list()
            templist+=player_list[obj].board
            templist.append(player_list[obj])
            for _ in range(value):
                if templist:
                    random.shuffle(templist)
                    item=templist[0]
                    if type(item)==Card:
                        item.changestat((0,0,-1))
                        if item.currentstats[1]<1:
                            templist.remove(item)
                    else: #type==Player
                        item.damage(-1)
            return
        if key == 'enemy_split_dmg_face':
            templist=list()
            templist+=player_list[(obj+1)%2].board
            templist.append(player_list[(obj+1)%2])
            for _ in range(value):
                if templist:
                    random.shuffle(templist)
                    item=templist[0]
                    if type(item)==Card:
                        item.changestat((0,0,-1))
                        if item.currentstats[1]<1:
                            templist.remove(item)
                    else: #type==Player
                        item.damage(-1)
            return
        if key == 'both_split_dmg_face':
            templist=list()
            templist+=player_list[obj].board
            templist.append(player_list[obj])
            templist+=player_list[(obj+1)%2].board
            templist.append(player_list[(obj+1)%2])
            for _ in range(value):
                if templist:
                    random.shuffle(templist)
                    item=templist[0]
                    if type(item)==Card:
                        item.changestat((0,0,-1))
                        if item.currentstats[1]<1:
                            templist.remove(item)
                    else: #type==Player
                        item.damage(-1)
            return
               
           
    else: #Is target spell
        #Target
        if key == 'target_hp':
            return obj.changestat((0,value,0)) if type(obj)==Card else 0
        if key == 'target_healminion':
            return obj.changestat((0,0,value)) if type(obj)==Card else 0
        if key == 'target_atk':
            return obj.changestat((value,0,0)) if type(obj)==Card else 0
        if key == 'target_kill':
            return obj.kill() if type(obj)==Card else 0
        if key == 'target_freeze':
            return obj.freeze() if type(obj)==Card else 0
        if key == 'target_hand_hp':
            return obj.changestat((0,value,0)) if type(obj)==Card else 0
        if key == 'target_hand_atk':
            return obj.changestat((value,0,0)) if type(obj)==Card else 0
        if key == 'target_hand_manacost':
            return obj.changemana(value) if type(obj)==Card else 0
        if key == 'target_hand_discard':
            return player_list[obj.player].discard(obj) if type(obj)==Card else 0
        if key == 'target_face':
            return (obj.damage(value) if value<0 else obj.heal(value)) if type(obj)!=Card and type(obj) != int else 0
        if key == 'target_barrier':
            return obj.gainbarrier() if type(obj)==Card else 0
        if key == 'target_lifesteal':
            return obj.gainlifesteal() if type(obj)==Card else 0
        if key == 'target_rush':
            return obj.gainrush() if type(obj)==Card else 0
        if key == 'target_silence':
            return obj.silence() if type(obj)==Card else 0
        if key == 'target_recall':
            print('running recall')
            return player_list[obj.player].recall(player_list[obj.player].board.index(obj)) if type(obj)==Card else 0
        

    if key == 'other':
        return value(obj)
    if key == 'myself':
        return value(obj)
    if key == 'target_other':
        return value(obj)
    if key == 'duel':
        return value(obj)

    if key == 'summoning':
        #value[0] #how many minions
        #value[1] #which place, 1 for hand, 2 for board
        for _ in range(value[0]):
            if value[1]==1:
                obj.addhand=1
                obj.addboard=0
                obj.summon()
            elif value[1]==2:
                obj.addhand=0
                obj.addboard=1
                obj.summon()
        return 

    if key == 'discover':
        #value[0] how many times
        #value[1] which place to dicover from
        #value[2] getattr , value[3] attr
        #eg (1, 'randomcard', 'mana', 3)  means discover a 3 mana card from the cardlist
        newvalue=list()
        for n in value:
            newvalue.append(n)
        for n in range(4-len(newvalue)):
            newvalue.append(None)
        value=tuple(newvalue)
        for _ in range(value[0]):
            if value[1]=='cardlist':
                player_list[obj].discover(cardlist,value[2],value[3])
            elif value[1]=='legendarylist':
                player_list[obj].discover(legendarylist,value[2],value[3])
            elif value[1]=='allydeck': 
                player_list[obj].discover(player_list[obj].deck,value[2],value[3])
            elif value[1]=='enemydeck':
                player_list[obj].discover(player_list[(obj+1)%2].deck,value[2],value[3])
            elif value[1]=='allygraveyard':
                player_list[obj].discover(player_list[obj].graveyard,value[2],value[3])
            elif value[1]=='enemygraveyard':
                player_list[obj].discover(player_list[(obj+1)%2].graveyard,value[2],value[3])
        return

    if key == 'resurrect':
        #value[0] how many times
        #value[1] which place to resurrect from
        #value[2] getattr , value[3] attr
        #eg (1, 'mana', 3,'allygraveyard')  means discover a 3 mana card from the allygraveyard
        newvalue=list()
        for n in value:
            newvalue.append(n)
        for n in range(3-len(newvalue)):
            newvalue.append(None)
        if len(newvalue)==3:
            newvalue.append('allygraveyard')
        value=tuple(newvalue)
        for _ in range(value[0]):
            if value[3]=='allygraveyard':
                templist=player_list[obj].graveyard
                player_list[obj].resurrect(value[1],value[2],templist)
            elif value[3]=='enemygraveyard':
                templist=player_list[(obj+1)%2].graveyard
                player_list[obj].resurrect(value[1],value[2],templist)
            elif value[3]=='bothgraveyard': 
                if rng(0,1):
                    templist= player_list[obj].graveyard
                else:
                    templist=player_list[(obj+1)%2].graveyard 
                player_list[obj].resurrect(value[1],value[2],templist)        
        return
#Card class
class Card():
    def __init__(self, name, stats=(0,0), cardtype='unit', manacost=0, manamax=0,  #Card info
                        sleep=True, frozen=False, lifesteal=False, barrier=False, rush=False, charge=False, snuffed=False, turnend = False, turnstart = False, commando = False, addboard = 0, addhand=0, disc=False, duelatk=False, dueldef=False,exile=False,wither=False,#Conditionals
                        effectdict=spelldictnull, snuffdict=spelldictnull, targetdict=locationdict, turnenddict=spelldictnull, turnstartdict=spelldictnull, dueldict=spelldictnull,newcard=None,  #Spells
                        text='This minion does nothing.', x_out=False, selected=False, shadow=False, showtext=False, #Visuals
                        art=pygame.Surface((10,10)), pos=(0,0,cardwidth,cardheight), #Pygame
                        played=0, player_list=list(), player=0,#Which player and board
                        region='Neutral',
                        ):
        self.name=name
        self.stats=stats
        self.maxstats=self.stats
        self.currentstats=self.stats
        self.text=text
        self.art=art
        self.display=card_base.copy() #self.display=display
        self.cardtype=cardtype 
        self.player=player
        self.manacost=manacost
        self.effectdict=effectdict
        self.sleep=sleep
        self.frozen=frozen
        self.x_out=x_out
        self.selected=selected
        self.shadow=shadow
        self.showtext=showtext
        self.bubble=pygame.Surface((0,0))
        self.pos=pos
        self.played=played
        self.targetdict=targetdict
        self.player_list = player_list
        self.lifesteal = lifesteal
        self.barrier = barrier
        self.rush = rush
        self.charge=charge
        self.snuffed = snuffed
        self.snuffdict=snuffdict
        self.turnend = turnend
        self.turnenddict=turnenddict
        self.turnstart = turnstart
        self.turnstartdict  = turnstartdict
        self.commando =  commando
        self.duelatk=duelatk  #if attacked
        self.dueldef=dueldef  #if defending
        self.dueldict=dueldict
        self.exile=exile
        self.wither=wither
        self.addboard=addboard
        self.addhand=addhand
        self.newcard=newcard
        self.region=region
        self.disc=disc

     
    def changestat(self, addstat=(0,0,0)): #addstat = (atk, maxhp, currenthp)
        maxatk,maxhp = self.maxstats
        atk,hp = self.currentstats
        maxatk+=addstat[0] if maxatk+addstat[0] >0 else 0
        atk=atk+addstat[0] if atk+addstat[0] >=0 else 0
        maxhp+=addstat[1]
        hp+=addstat[1]
        if addstat[2]<0:
            if self.barrier:
                self.barrier=False
            else:
                hp+=addstat[2]
        else:
            hp = min(addstat[2]+hp, maxhp)
        self.currentstats=(atk,hp)
        self.maxstats=(maxatk,maxhp)
        self.display_update()
        return self

    def silence(self):
        self.lifesteal=False
        self.barrier=False
        self.freeze=False
        self.rush=False
        self.turnstart=False
        self.turnend = False
        self.snuffed = False
        self.addboard = False
        self.addhand = False
        self.commando=False
        self.duelatk=False
        self.dueldef=False
        self.maxstat = self.stats
        atk = self.stats[0]
        hp = min(self.currentstats[1],self.stats[1])
        self.currentstats=atk,hp
        self.display_update()

    def strike(self, Oppcard):  #Oppcard is a Card class
        if self.barrier:
            if Oppcard.currentstats[0]>0:
                self.barrier=False
        else:
            self.changestat((0,0,-Oppcard.currentstats[0]))
        if Oppcard.barrier:
            if self.currentstats[0]>0:
                Oppcard.barrier=False    
        else:
            Oppcard.changestat((0,0,-self.currentstats[0]))
        if self.duelatk:
            self.playduel(Oppcard)
        if Oppcard.dueldef:
            Oppcard.playduel(self)
        self.sleep=True

    def kill(self):
        if self.barrier:
            self.currentstats = (self.currentstats[0],0)
        else:
            self.changestat((0,0,-self.currentstats[1]))

    def reset(self):
        self.currentstats=self.maxstats
        if self.rush or self.charge:
            self.sleep=False
        else:
            self.sleep=True
        self.display_update()

    def freeze(self):
        self.frozen=True

    def gainbarrier(self):
        self.barrier = True
    	
    def gainlifesteal(self):
        self.lifesteal = True
    	
    def gainrush(self):
        self.rush = True

    def changemana(self,value):
        self.manacost +=value
        if self.manacost < 0:
           self.manacost = 0 
        if self.manacost>10:
            self.manacost=10

    def playspell(self):
        returnvalue=True
        if self.effectdict['target']:
            self.selected=True
            clicklist=list()
            if self.cardtype=='spell':
                for _ in range(self.effectdict['target']):
                    card = self.player_list[self.player].click2(self.targetdict)
                    if card:
                        clicklist.append(card)
            if self.cardtype == 'unit':
                for _ in range(self.effectdict['target']):
                    card = self.player_list[self.player].click3(self.targetdict)
                    if card:
                        clicklist.append(card)
            clicklist=list(set(clicklist))
            if self in clicklist:
                clicklist.remove(self)
            if len(clicklist) == self.effectdict['target']:
                for targetted in clicklist:
                    for key,value in self.effectdict.items():
                        if 'target' in key and value:
                            spelldictdesc(self.player_list,key,value,targetted)
                for key,value in self.effectdict.items():
                    if key=='myself' and value:
                        spelldictdesc(self.player_list,key,value,self)
                    elif key=='summoning' and value:
                        spelldictdesc(self.player_list,key,value,self)
                    elif value and not ('target' in key):
                        spelldictdesc(self.player_list,key,value,self.player)
                self.selected=False
            else:
                self.selected=False
                returnvalue= False

        else:
            for key,value in self.effectdict.items():
                if key=='myself' and value:
                    spelldictdesc(self.player_list,key,value,self)
                elif key=='summoning' and value:
                    spelldictdesc(self.player_list,key,value,self)
                elif value:
                    spelldictdesc(self.player_list,key,value,self.player)
        return returnvalue

    def playduel(self,obj=None): 
        returnvalue=True
        if self.dueldict['target']:
            self.selected=True
            clicklist=list()
            if self.cardtype == 'unit':
                for _ in range(self.dueldict['target']):
                    card = self.player_list[self.player].click3(self.targetdict)
                    if card:
                        clicklist.append(card)
            clicklist=list(set(clicklist))
            if len(clicklist) == self.dueldict['target']:
                for targetted in clicklist:
                    for key,value in self.dueldict.items():
                        if 'target' in key and value:
                            spelldictdesc(self.player_list,key,value,targetted)
                for key,value in self.dueldict.items():
                    if key=='myself' and value:
                        spelldictdesc(self.player_list,key,value,self)
                    elif key=='summoning' and value:
                        spelldictdesc(self.player_list,key,value,self)
                    elif value and not ('target' in key):
                        spelldictdesc(self.player_list,key,value,self.player)
                self.selected=False
            else:
                self.selected=False
                returnvalue= False
        else:
            for key,value in self.dueldict.items():
                if key=='duel' and value: #Duel the opponent card or player
                    spelldictdesc(self.player_list,key,value,obj) #obj is opponent card or player
                elif key=='myself' and value:
                    spelldictdesc(self.player_list,key,value,self)
                elif key=='summoning' and value:
                    spelldictdesc(self.player_list,key,value,self)
                elif value:
                    spelldictdesc(self.player_list,key,value,self.player)
        return returnvalue


    def playsnuff(self):
        self.player_list[self.player].boardcounter()
        if self.snuffdict!= spelldictnull:
            for key,value in self.snuffdict.items():
                if key=='myself' and value:
                    spelldictdesc(self.player_list,key,value,self)
                elif key=='summoning' and value:
                    spelldictdesc(self.player_list,key,value,self)
                elif value:
                    spelldictdesc(self.player_list,key,value,self.player)

    def playendturn(self):     
        if self.turnenddict!= spelldictnull:
            for key,value in self.turnenddict.items():
                if key=='myself' and value:
                    spelldictdesc(self.player_list,key,value,self)
                elif key=='summoning' and value:
                    spelldictdesc(self.player_list,key,value,self)
                elif value:
                    spelldictdesc(self.player_list,key,value,self.player)

    def playstartturn(self):     
        if self.turnstartdict!= spelldictnull:
            for key,value in self.turnstartdict.items():
                if key=='myself' and value:
                    spelldictdesc(self.player_list,key,value,self)
                elif key=='summoning' and value:
                    spelldictdesc(self.player_list,key,value,self)
                elif value:
                    spelldictdesc(self.player_list,key,value,self.player)

    def text_bubble(self):
        text=font_bubble.render(self.text, 1, (0,0,0),(255,255,255))
        self.bubble = text
        return self.bubble

   
    def display_update(self):  
        #blitting base and art
        self.display.blit(card_base.copy(),(0,0))
        artwidth = self.art.get_width()
        artpos = (cardwidth - artwidth)//2, 10
        self.display.blit(self.art,artpos)
 

        text=font_card.render(self.name, 1, (0,0,0))
        namewidth,nameheight = text.get_size()
        if namewidth <= 50: #short 1 line name
            self.display.blit(text, ((cardwidth-namewidth)//2,75))
        else: #long name 2 lines
            if ' ' in self.name or '-' in self.name:
                top,bot = self.name.split(' ', 1) if ' ' in self.name else self.name.split('-', 1)
                text1 = font_card.render(top,1,(0,0,0))
                namewidth1 = text1.get_width()
                text2 = font_card.render(bot,1,(0,0,0))
                namewidth2 = text2.get_width()
                self.display.blit(text1, ((cardwidth-namewidth1)//2,75-nameheight//2))
                self.display.blit(text2, ((cardwidth-namewidth2)//2,75+nameheight//2))
            else: #dont care name long
                self.display.blit(text, ((cardwidth-namewidth)//2,75))
                

        #blit manacost
        text=font_card.render(str(self.manacost),1,(255,255,255))
        pygame.draw.circle(self.display,(100,100,255),(10,10),12)
        manawidth, manaheight = text.get_size()
        self.display.blit(text, (10-manawidth//2,10-manaheight//2))

        if self.x_out:
            pygame.draw.line(self.display, (255,0,0),(0,0),(cardwidth,cardheight),10)
            pygame.draw.line(self.display, (255,0,0),(0,cardheight),(cardwidth,0),10)
            ## self.display.blit(big_x,(0,0))

        if self.barrier == True:
            pygame.draw.rect(self.display, (255,200,80), (0,0,cardwidth,cardheight), 6)

        if self.rush == True:
            pygame.draw.polygon(self.display, (0,120,0), ((cardwidth//2,0),(0,60),(cardwidth,60)), 3)

        if self.frozen == True:
        	pygame.draw.arc(self.display, (173, 216, 230), (0,0,cardwidth,cardheight), (0), (6.28),5)

        if self.lifesteal == True:
        	pygame.draw.arc(self.display, (255,105,180), (0,0,cardwidth,cardheight), (0), (6.28),5)

        if self.snuffed==True:
        	pygame.draw.polygon(self.display, (120, 81, 169), ((cardwidth//2,0),(0,cardheight//3),(cardwidth//4,cardheight),(cardwidth//4*3,cardheight),(cardwidth, cardheight//3)),3)

        if self.selected == True:
            pygame.draw.rect(self.display, (100,255,100), (0,0,cardwidth,cardheight), 4)

        if self.cardtype=='unit':
            atk, hp = self.currentstats
            coloratk = (0,0,0)
            colorhp = (0,0,0)
            if self.currentstats[1] < self.maxstats[1]: 
                colorhp=(255,0,0)
            elif self.maxstats[1]>self.stats[1]:
                colorhp=(0,255,0)
            if self.currentstats[0] < self.stats[0]:   
                coloratk=(255,0,0)
            elif self.maxstats[0]>self.stats[0]:
                coloratk=(0,255,0)
            atktext = font_card.render(str(atk), 1, (coloratk))
            hptext = font_card.render(str(hp), 1, (colorhp))
            atkwidth,atkheight = atktext.get_size()
            hpwidth,hpheight = hptext.get_size()
            pygame.draw.circle(self.display,(255,255,255),(7,cardheight-7),10)
            pygame.draw.circle(self.display,(255,255,255),(cardwidth - 7,cardheight - 7),10)
            self.display.blit(atktext, (7-atkwidth//2, cardheight-7-atkheight//2))
            self.display.blit(hptext, (cardwidth - 7 - hpwidth//2 ,cardheight-7-hpheight//2))
            if self.sleep:
                text=font_card.render('zzZ',1,(0,0,0))
                self.display.blit(text,(55,5))
        if self.shadow:
            pygame.draw.rect(self.display, (100,100,100), (0,0,cardwidth,cardheight)) 
            pygame.draw.rect(self.display, (0,0,0), (0,0,cardwidth,cardheight),6)
            self.display.set_colorkey((100,100,100))

    def summon(self,obj=None):
        for _ in range(self.addboard):
            self.player_list[self.player].boardcounter()
            card = self.newcard(self.player,self.player_list)
            card.played=2 if self.player_list[self.player].atknum<5 else 1 if self.player_list[self.player].defnum<2 else 0
            self.player_list[self.player].board.append(card) if len(self.player_list[self.player].board) <7 else 0
        for _ in range(self.addhand):
            card = self.newcard(self.player,self.player_list)
            self.player_list[self.player].hand.append(card) if len(self.player_list[self.player].hand)<10 else 0


#TESTING CARDs
def comets(playernum,playerlist): #all minions + face
    mydict={'target':0,'both_split_dmg_face':4}
    return Card(name='Comets',cardtype='spell',manacost=0,player=playernum,text='4 split ALL',effectdict=mydict,player_list=playerlist)

def volley(playernum,playerlist): #enemy minions
    mydict={'target':0,'enemy_split_dmg':4}
    return Card(name='Volley',cardtype='spell',manacost=0,player=playernum,text='3 split enemy minons',effectdict=mydict,player_list=playerlist)

def artillery(playernum,playerlist): #enemy minons+face
    mydict={'target':0,'enemy_split_dmg_face':4}
    return Card(name='Artillery',cardtype='spell',manacost=0,player=playernum,text='4 split enemy all',effectdict=mydict,player_list=playerlist)

def pandemic(playernum,playerlist): #self minions
    mydict={'target':0,'ally_split_dmg':4}
    return Card(name='Pandemic',cardtype='spell',manacost=0,player=playernum,text='4 split ally minions',effectdict=mydict,player_list=playerlist)

def traitors(playernum,playerlist): #self minons+face
    mydict={'target':0,'ally_split_dmg_face':4}
    return Card(name='Traitors',cardtype='spell',manacost=0,player=playernum,text='4 split ally all',effectdict=mydict,player_list=playerlist)

def wall(playernum,playerlist,n=5,a=1): #1/5
    return Card(name='Wall',cardtype='unit',stats=(a,n),manacost=0,player=playernum,text='Wall',player_list=playerlist)


def summoner(playernum, playerlist):
    mydict={'target':0, 'summoning':(1,1)}
    return Card(name='Summoner',stats=(1,1),cardtype='unit',manacost=0,player=playernum,art=red_nexus,sleep=True,newcard=lastbreath,text='add lastbreath',player_list=playerlist,effectdict=mydict)

def otherguy(playernum,playerlist): 
    mydict = { 'target':1, 'target_other':lambda obj:obj.changestat((0,len(playerlist[playernum].hand),0)) }
    mytarget = {'target':1, 'ally_board':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Otherguy',stats=(1,1),cardtype='unit',manacost=1,player=playernum,art=red_nexus,sleep=True,effectdict=mydict,targetdict=mytarget,text='buff by len hand',player_list=playerlist)

def myguy(playernum,playerlist): 
    mydict = { 'target':0, 'myself':lambda obj:obj.changestat((0,len(playerlist[playernum].hand),0)) }
    return Card(name='Myguy',stats=(1,0),cardtype='unit',manacost=1,player=playernum,art=red_nexus,sleep=True,effectdict=mydict,text='buff self len hand',player_list=playerlist)

def halver(playernum,playerlist):
    mydict = { 'target':0, 'other':lambda obj:playerlist[(obj+1)%2].damage(-playerlist[(obj+1)%2].health//2) }
    return Card(name='Halver',stats=(0,1),cardtype='unit',manacost=1,player=playernum,art=red_nexus,sleep=True,effectdict=mydict,text='half enemy health',player_list=playerlist)

def kill1(playernum,playerlist):
    mydict = { 'target':1, 'target_kill':1}
    mytarget = {'target':1, 'enemy_kill':1,'ally_board':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='kill1',cardtype='spell',manacost=0,player=playernum,art=red_nexus,effectdict=mydict,targetdict=mytarget,text='kill an enemy minion',player_list=playerlist)

def discoverer(playernum,playerlist):
    mydict = { 'target':0, 'discover':(1,'legendarylist') }
    return Card(name='Discoverer',stats=(0,1),cardtype='unit',manacost=0,player=playernum,art=red_nexus,effectdict=mydict,text='discover a minion',player_list=playerlist,sleep=False)

def discoverer1(playernum,playerlist):
    mydict = { 'target':0, 'discover':(1,'allygraveyard') }
    return Card(name='Discoverer1',stats=(0,1),cardtype='unit',manacost=0,player=playernum,art=red_nexus,effectdict=mydict,text='discover a minion',player_list=playerlist,sleep=False)

def discoverer2(playernum,playerlist):
    mydict = { 'target':0, 'discover':(1,'enemygraveyard') }
    return Card(name='Discoverer2',stats=(0,1),cardtype='unit',manacost=0,player=playernum,art=red_nexus,effectdict=mydict,text='discover a minion',player_list=playerlist,sleep=False)

def discoverer3(playernum,playerlist):
    mydict = { 'target':0, 'discover':(1,'cardlist','manacost',5) }
    return Card(name='Discoverer3',stats=(0,1),cardtype='unit',manacost=0,player=playernum,art=red_nexus,effectdict=mydict,text='discover a minion',player_list=playerlist,sleep=False)

def discoverer4(playernum,playerlist):
    mydict = { 'target':0, 'discover':(1,'allydeck') }
    return Card(name='Discoverer4',stats=(0,1),cardtype='unit',manacost=0,player=playernum,art=red_nexus,effectdict=mydict,text='discover a minion',player_list=playerlist,sleep=False)

def discoverer5(playernum,playerlist):
    mydict = { 'target':0, 'discover':(1,'enemydeck') }
    return Card(name='Discoverer5',stats=(0,1),cardtype='unit',manacost=0,player=playernum,art=red_nexus,effectdict=mydict,text='discover a minion',player_list=playerlist,sleep=False)

def randomsummon(playernum,playerlist):
    def newcarder():
        random.shuffle(cardlist)
        for card in cardlist:
            if card(playernum,playerlist).cardtype=='unit':
                break
        return card
    mydict={'target':0,'summoning':(1,2)}
    return Card(name='randomsummon',stats=(1,1),cardtype='unit',manacost=0,player=playernum,art=red_nexus,newcard=newcarder(),addboard=1,text='summon new card',player_list=playerlist)

def transformer(playernum,playerlist):
    def newcarder(obj):
        random.shuffle(cardlist)
        newcard=None
        for card in cardlist:
            if card(playernum,playerlist).cardtype=='unit' and card(playernum,playerlist).manacost==obj.manacost+1:
                newcard=card
                break
        if newcard: #there is a suitable card
            newobj=newcard(obj.player,obj.player_list)
            newobj.played=obj.played
            playerlist[obj.player].board.remove(obj)
            playerlist[obj.player].board.append(newobj)
    mydict = {'target':1, 'target_other':newcarder}
    mytarget = {'target':1, 'enemy_hp':1,'ally_board':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Transformer',cardtype='spell',manacost=0,player=playernum,art=red_nexus,text='transform',player_list=playerlist,effectdict=mydict,targetdict=mytarget)

def duelist1(playernum,playerlist):
    mydict = { 'target':0, 'duel':lambda obj: obj.freeze()}
    return Card(name='Attacker',stats=(0,2),cardtype='unit',manacost=0,player=playernum,art=red_nexus,dueldict=mydict,text='duel: freeze opp',player_list=playerlist,sleep=False,duelatk=True)

def duelist2(playernum,playerlist):
    mydict = { 'target':1, 'target_healminion':2}
    mytarget = {'target':1, 'ally_board':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Duelist2',stats=(0,3),cardtype='unit',manacost=0,player=playernum,art=red_nexus,dueldict=mydict,targetdict=mytarget,text='heal ally minion 2',player_list=playerlist,sleep=False,duelatk=True)

def duelist3(playernum,playerlist):
    mydict = { 'target':0, 'enemy_freeze_aoe': 1}
    return Card(name='Duelist3',stats=(0,3),cardtype='unit',manacost=0,player=playernum,art=red_nexus,dueldict=mydict,text='duel def: freeze all enemies',player_list=playerlist,sleep=False,duelatk=True,dueldef=True)

def duelist4(playernum,playerlist):
    mydict = { 'target':0, 'summoning': (1,2)}
    return Card(name='Duelist4',stats=(0,3),cardtype='unit',manacost=0,player=playernum,art=red_nexus,dueldict=mydict,text='duel def: summon duelist1',player_list=playerlist,sleep=False,duelatk=True,dueldef=True, newcard=duelist1)

def revivespell(playernum,playerlist):
    mydict = { 'target':0, 'resurrect':(1,'manacost',0)}
    return Card(name='Revivespell',stats=(2,4),cardtype='spell',manacost=0,player=playernum,art=necromancerpic,sleep=True,effectdict=mydict,text='resurrect 1',player_list=playerlist)

#NEUTRAL
#Minions
#1 drops
def magic(playernum,playerlist):
    def feed():
        random.shuffle(cardlist)
        card = cardlist[0]
        playerlist[playernum].hand.append(card(playernum,playerlist))
    mydict={'target':0,'other':lambda obj: feed()}
    return Card(name='Magic',cardtype='unit',stats=(0,1),manacost=1,text='Add random card to hand',effectdict=mydict,art=magicalwisppic,player=playernum,player_list=playerlist)

def generousmerchant(playernum,playerlist): #give ally +1+1
    mydict = { 'target':1, 'target_hp':1, 'target_atk':1}
    mytarget = {'target':1, 'ally_board':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Generous Merchant',stats=(0,2),cardtype='unit',manacost=1,player=playernum,art=generousmerchantpic,sleep=True,effectdict=mydict,targetdict=mytarget,text='give ally 1/1',player_list=playerlist)

def clericapprentice(playernum,playerlist):
    mydict = { 'target':1, 'target_healminion':2}
    mytarget = {'target':1, 'ally_board':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Cleric Apprentice',stats=(1,1),cardtype='unit',manacost=1,player=playernum,art=clericapprenticepic,sleep=True,effectdict=mydict,targetdict=mytarget,text='heal ally by 2',player_list=playerlist)

def bandit(playernum,playerlist): 
   return Card(name='Bandit',stats=(1,2),cardtype='unit',manacost=1,player=playernum,art=banditpic,sleep=True,player_list=playerlist)

def drunkenbrawler(playernum,playerlist): 
    mydict = { 'target':2, 'target_hand_discard':2}
    mytarget = {'target':2, 'ally_hand_discard':2,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Drunken Brawler',stats=(3,4),cardtype='unit',manacost=1,player=playernum,art=drunkenbrawlerpic,sleep=True,effectdict=mydict,targetdict=mytarget,text='discard 2',player_list=playerlist)


#2 drops
def dhampir(playernum,playerlist): #vanilla
    return Card(name='Dhampir',stats=(1,3),cardtype='unit',manacost=2,player=playernum,art=dhampirpic,sleep=True,player_list=playerlist, lifesteal=True)

def swiftmessenger(playernum,playerlist): 
    mydict = { 'target':0, 'ally_draw':1}
    return Card(name='Swift Messenger',stats=(1,1),cardtype='unit',manacost=2,player=playernum,art=swiftmessengerpic,sleep=True,effectdict=mydict, text='draw 1',player_list=playerlist)

def pickpocketeer(playernum,playerlist):
    mydict = { 'target':0, 'ally_draw':1}
    return Card(name='Pick-Pocketeer',stats=(1,2),cardtype='unit',manacost=2,player=playernum,art=pickpocketeerpic,sleep=True,player_list=playerlist,snuffdict=mydict,text='Snuff: Draw 1',snuffed=True)

def magicalwisp(playernum,playerlist):
    def feed():
        random.shuffle(cardlist)
        card = cardlist[0]
        playerlist[playernum].hand.append(card(playernum,playerlist))
    mydict={'target':0,'other':lambda obj: feed()}
    return Card(name='Magical Wisp',cardtype='unit',stats=(1,2),manacost=2,text='Add random card to hand',effectdict=mydict,art=magicalwisppic,player=playernum,player_list=playerlist)


#3 drops
def defiantsergeant(playernum,playerlist): 
    mydict = { 'target':1, 'target_hand_discard':1}
    mytarget = {'target':1, 'ally_hand_discard':1,'choose_enemy_face':0,'choose_ally_face':0,}
    return Card(name='Defiant Sergeant',stats=(4,5),cardtype='unit',manacost=3,player=playernum,art=defiantsergeantpic,sleep=True,effectdict=mydict,targetdict=mytarget, text='discard a card',player_list=playerlist)

def shieldbearer(playernum,playerlist): 
    mydict = { 'target':1, 'target_hp':2,'target_atk':1}
    mytarget = {'target':1, 'ally_board':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Shield-bearer',stats=(2,2),cardtype='unit',manacost=3,player=playernum,art=shieldbearerpic,sleep=True,effectdict=mydict,targetdict=mytarget, text='buff 1/2',player_list=playerlist)

def angrylibrarian(playernum,playerlist):
    mydict = { 'target':0, 'ally_silence_aoe':1, 'enemy_silence_aoe':1}
    return Card(name='Angry Librarian',stats=(2,4),cardtype='unit',manacost=3,player=playernum,art=angrylibrarianpic,sleep=True,effectdict=mydict,text='silence all',player_list=playerlist)

def icemaiden(playernum,playerlist): 
    mydict = { 'target':1, 'target_freeze':1}
    mytarget = {'target':1, 'enemy_freeze':1,'choose_enemy_face':0,'choose_ally_face':0,}
    return Card(name='Ice Maiden',stats=(3,3),cardtype='unit',manacost=3,player=playernum,art=icemaidenpic,sleep=True,effectdict=mydict,targetdict=mytarget, text='freeze 1 target',player_list=playerlist)


#4 drops
def lonelytroll(playernum,playerlist): 
    return Card(name='Lonely Troll',stats=(3,5),cardtype='unit',manacost=4,player=playernum,art=lonelytrollpic,sleep=True,player_list=playerlist)

def swiftharpy(playernum,playerlist):
    return Card(name='Swift Harpy',stats=(4,3),cardtype='unit',manacost=4,player=playernum,art=swiftharpypic,sleep=False,rush=True,player_list=playerlist)

def gladiator(playernum, playerlist):
    def team(obj):
        obj.changestat((len(playerlist[playernum].board), len(playerlist[playernum].board), 0))
    mydict = { 'target':0, 'myself':team}
    return Card(name='Gladiator',stats=(1,1),cardtype='unit',manacost=4,player=playernum,art=gladiatorpic,sleep=False,effectdict=mydict,text='When played, gain +1/1. For each ally on board, gain +1/1',player_list=playerlist)

#5 drops
def necromancer(playernum,playerlist):
    mydict = { 'target':0, 'resurrect':(1,)}
    return Card(name='Necro-mancer',stats=(2,4),cardtype='unit',manacost=5,player=playernum,art=necromancerpic,sleep=True,effectdict=mydict,text='resurrect 1',player_list=playerlist)

def chaaarrge(playernum,playerlist): #LEGENDARY
    return Card(name='CHAAARRGE',stats=(5,1),cardtype='unit',manacost=5,player=playernum,art=chaaarrgepic,sleep=False,charge=True,text='Charge',player_list=playerlist,commando=True)

def anubis(playernum,playerlist): #LEGENDARY
    def rofl():
        for card in playerlist[playernum].hand:
            if card.snuffed ==True:
                card.currentstats = (0,1)
                card.maxstats = (0,1)
                card.manacost = 1
            else: 
                pass 
    mydict = { 'target':0, 'other':lambda obj:rofl()}
    return Card(name='Anubis',stats=(4,5),cardtype='unit',manacost=5,player=playernum,art=anubispic,sleep=True,effectdict=mydict,text='Snuff handminions are 0/1, cost 1',player_list=playerlist)

def rovingcaravan(playernum,playerlist): 
    mydict = { 'target':0, 'ally_hand_discard_aoe':1, 'ally_draw':3}
    return Card(name='Roving Caravan',stats=(4,3),cardtype='unit',manacost=5,player=playernum,art=rovingcaravanpic,sleep=False,rush=True,effectdict=mydict,text='discard all draw 3',player_list=playerlist)


#6 drops
def hiredhitman(playernum,playerlist):
    mydict = { 'target':1, 'target_healminion':-3}
    mytarget = {'target':1, 'enemy_healminion':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Hired Hitman',stats=(4,6),cardtype='unit',manacost=6,player=playernum,art=hiredhitmanpic,sleep=True,effectdict=mydict,targetdict=mytarget,text='deal 3 to enemy minion',player_list=playerlist)

#7 drops
def deadlyassassin(playernum,playerlist):
    mydict = { 'target':1, 'target_kill':1}
    mytarget = {'target':1, 'enemy_kill':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Deadly Assassin',stats=(3,4),cardtype='unit',manacost=7,player=playernum,art=deadlyassassinpic,sleep=True,effectdict=mydict,targetdict=mytarget,text='kill an enemy minion',player_list=playerlist)

#8 mana
def playfultrickster(playernum,playerlist):
    def newcarder():
        lenlist=len(playerlist[playernum].deck)
        playerlist[playernum].deck=list()
        for _ in range(lenlist):
            random.shuffle(cardlist)
            card = cardlist[0]
            playerlist[playernum].deck.append(card(playernum,playerlist))
    mydict={'target':0,'other':lambda obj: newcarder()}
    return Card(name='Playful Trickster',cardtype='unit',stats=(7,8),manacost=8,text='Your deck are random cards',effectdict=mydict,art=playfultricksterpic,player=playernum,player_list=playerlist,sleep=True)

#9 mana
def generalhark(playernum,playerlist): #LEGENDARY
    mydict = { 'target':0, 'other': lambda obj: playerlist[(playernum+1)%2].damage(-playerlist[(playernum+1)%2].health//2)}
    mydict2 = { 'target':0, 'summoning':(1,1)}
    return Card(name='General Hark',stats=(8,5),cardtype='unit',manacost=9,player=playernum,art=generalharkpic,sleep=True,effectdict=mydict,snuffdict=mydict2,snuffed=True,text='deal dmg to opp face=half his current health round down. snuff: return it to hand',player_list=playerlist,newcard=generalhark)

#10 drops
def shiva(playernum,playerlist): #LEGENDARY
    mydict = { 'target':0, 'enemy_kill_aoe':1, 'ally_kill_aoe':1, 'ally_hand_discard_aoe':1}
    return Card(name='Shiva',stats=(13,14),cardtype='unit',manacost=10,player=playernum,art=shivapic,sleep=True,effectdict=mydict, text='Kill all on board, discard your hand',player_list=playerlist)

def erebus(playernum,playerlist): #LEGENDARY
    mydict = { 'target':0, 'other':lambda obj: playerlist[(playernum+1)%2].damage(-100) if len(playerlist[playernum].deck) + len(playerlist[playernum].hand) == 0 else 0}
    return Card(name='Erebus',stats=(10,10),cardtype='unit',manacost=10,player=playernum,art=erebuspic,sleep=True,snuffdict=mydict,snuffed=True, text='snuff: if you have no cards left, deal 100 damage to the opponent',player_list=playerlist)
#Spells
#0 cost spells
def knife(playernum,playerlist):
    mydict = { 'target':1, 'target_healminion':-1, 'target_face':-1}
    mytarget = {'target':1, 'enemy_healminion':1,'ally_board':1,'choose_enemy_face':1,'choose_ally_face':1}
    return Card(name='Knife',art=knifepic,cardtype='spell',manacost=0,player=playernum,effectdict=mydict, targetdict=mytarget,text='Deal 1 to anyth',player_list=playerlist)

#1 mana spells
def divineprotection(playernum,playerlist):
    mydict = { 'target':1, 'target_barrier':1}
    mytarget = {'target':1, 'enemy_barrier':1, 'ally_board':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Divine Protection',art=divineprotectionpic,cardtype='spell',manacost=1,player=playernum,effectdict=mydict, targetdict=mytarget,text='give barrier',player_list=playerlist)
   

#2 mana spells

def icicles(playernum,playerlist):
    mydict = { 'target':2, 'target_freeze':1}
    mytarget = {'target':2, 'enemy_freeze':1, 'ally_board':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Icicles',art=iciclespic,cardtype='spell',manacost=2,player=playernum,effectdict=mydict, targetdict=mytarget,text='Freeze 2',player_list=playerlist)

def catalyst(playernum,playerlist):
    mydict = { 'target':0, 'ally_max_mana':1}
    return Card(name='Catalyst',art=catalystpic,cardtype='spell',manacost=2,player=playernum,effectdict=mydict, text='Gain an empty mana crystal',player_list=playerlist)



# 3 cost spells 
def serenity(playernum,playerlist):
    mydict = { 'target':0, 'ally_draw':2,}
    return Card(name='Serenity',art=serenitypic
,cardtype='spell',manacost=3,player=playernum,effectdict=mydict, text='Draw 2',player_list=playerlist)


#4 cost spells
def mirror(playernum,playerlist):
    def cp(obj):
        newcard = copy.copy(obj)
        newcard.player=playernum
        newcard.player_list=playerlist
        newcard.display=obj.display.copy()
        newcard.sleep=False if (newcard.rush or newcard.charge) else True
        playerlist[playernum].boardcounter()
        newcard.played=2 if playerlist[playernum].atknum<5 else 1 if self.playerlist[playernum].defnum<2 else 0
        playerlist[playernum].board.append(newcard) if len(playerlist[playernum].board) <7 else 0
    mydict = {'target':1, 'target_other':cp}
    mytarget = {'target':1, 'enemy_hp':1,'ally_board':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Mirror',cardtype='spell',manacost=4,player=playernum,art=mirrorpic,effectdict=mydict,targetdict=mytarget,text='copy a minion',player_list=playerlist)

def frostspear(playernum,playerlist): 
    mydict = { 'target':1, 'target_healminion':-5, 'target_face':-5}
    mytarget = {'target':1, 'enemy_healminion':-5,'ally_board':-5,'choose_enemy_face':1,'choose_ally_face':1}
    return Card(name='Frost Spear',art=frostspearpic,cardtype='spell',manacost=4,player=playernum,effectdict=mydict, targetdict=mytarget,text='Deal 5 to anyth',player_list=playerlist)
    
#5 cost spells
def assassinate(playernum,playerlist):
    mydict = { 'target':1, 'target_kill':1}
    mytarget = {'target':1, 'enemy_kill':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Assassinate',cardtype='spell',manacost=5,player=playernum,art=assassinatepic,effectdict=mydict,targetdict=mytarget,text='kill an enemy minion',player_list=playerlist)


#6 cost spells
def dragonfire(playernum,playerlist):
    mydict = { 'target':0, 'enemy_healminion_aoe':-5,'ally_healminion_aoe':-5, 'ally_face':-5, 'enemy_face':-5}
    return Card(name='Dragonfire',art=dragonfirepic,cardtype='spell',manacost=6,player=playernum,effectdict=mydict, text='Deal 5 to ALL',player_list=playerlist)

def urchinsunite(playernum,playerlist):
    mydict={'target':0,'summoning':(5,2)}
    return Card(name='Urchins Unite',cardtype='spell',manacost=6,text='summon 5 Urchins',newcard=urchin,effectdict=mydict,art=urchinsunitepic,player=playernum,player_list=playerlist)

#7 cost spells
def grandconcession(playernum,playerlist):
    mydict = { 'target':0,  'ally_hand_manacost_aoe':-3,}
    return Card(name='Grand Concession',art=grandconcessionpic,cardtype='spell',manacost=7,player=playernum,effectdict=mydict, text='aoe discount mana 3',player_list=playerlist)










#AIR
#Minions:
#1 mana
def airsprite(playernum,playerlist):
    mydict = { 'target':1, 'target_hand_discard':1,'other':lambda obj: playerlist[playernum].draw(1)}
    mytarget = {'target':1, 'ally_hand_discard':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Air Sprite',stats=(0,1),cardtype='unit',manacost=1,player=playernum,art=airspritepic,sleep=True,effectdict=mydict,targetdict=mytarget,text='discard 1 draw 1',player_list=playerlist,region='Air')

#2 mana:
def cyclos(playernum,playerlist):
    mydict = { 'target':1, 'target_hand_discard':1}
    mytarget = {'target':1, 'ally_hand_discard':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Cyclos',stats=(3,3),cardtype='unit',manacost=2,player=playernum,art=cyclospic,sleep=True,effectdict=mydict,targetdict=mytarget,text='discard 1',player_list=playerlist,region='Air')

def windfae(playernum,playerlist): 
    return Card(name='Wind Fae',stats=(2,2),cardtype='unit',manacost=2,player=playernum,art=windfaepic,disc=True,sleep=True,text='Summon if discarded',player_list=playerlist,region='Air')

def miragesorcerer(playernum,playerlist):
    def lol(obj):
        for _ in range(3):
            newcard = copy.copy(obj)
            newcard.display=obj.display.copy()
            playerlist[playernum].deck.append(newcard)
        random.shuffle(playerlist[playernum].deck)
    mydict = { 'target':1, 'target_other':lol}
    mytarget = {'target':1,'ally_hand_hp':1,'choose_enemy_face':0,'choose_ally_face':0, 'ally_board':0}
    return Card(name='Mirage Sorcerer',cardtype='unit',manacost=2,stats=(2,2),player=playernum,art=miragesorcererpic,effectdict=mydict,targetdict=mytarget,text='shuffle 3 copies of a handminion into the deck',player_list=playerlist,region='Air')

#3 mana:
def halos(playernum,playerlist): 
    mydict = { 'target':0, 'other':lambda obj:playerlist[playernum].draw(1) if len(playerlist[playernum].discard_pile)>0 else 0}
    return Card(name='Halos',stats=(2,4),cardtype='unit',manacost=3,player=playernum,art=halospic,sleep=True,effectdict=mydict,text='Draw 1 if discard pile>0',player_list=playerlist,region='Air')


#4 mana:

def aeros(playernum,playerlist):
    mydict = { 'target':1, 'target_hand_discard':1}
    mytarget = {'target':1, 'ally_hand_discard':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Aeros',stats=(5,4),cardtype='unit',manacost=4,player=playernum,art=aerospic,rush=True,sleep=False,effectdict=mydict,targetdict=mytarget,text='discard 1',player_list=playerlist,region='Air')

def scrapdealer(playernum,playerlist): 
    def chooser():
        card=None
        random.shuffle(playerlist[playernum].discard_pile)
        for select in playerlist[playernum].discard_pile:
            if select.cardtype=='unit':
                card=select
                break
        if len(playerlist[playernum].hand)>10:
            pass
        elif card:
            card.manacost=0
            playerlist[playernum].hand.append(card)
    mydict = { 'target':0, 'other':lambda obj:chooser()}
    return Card(name='Scrap Dealer',stats=(3,5),cardtype='unit',manacost=4,player=playernum,art=scrapdealerpic,sleep=True,effectdict=mydict,text='Add random discarded minion to hand. Costs 0',player_list=playerlist,region='Air')

def cloudsorcerer(playernum,playerlist):
    def lol(obj):
        for _ in range(3):
            newcard = cloud(playernum,playerlist)
            newcard.manacost=0
            playerlist[playernum].deck.append(newcard)
        random.shuffle(playerlist[playernum].deck)
    mydict = { 'target':0, 'other':lol}
    return Card(name='Cloud Sorcerer',cardtype='unit',manacost=4,stats=(2,4),player=playernum,art=cloudsorcererpic,effectdict=mydict,text='shuffle 3 clouds into the deck',player_list=playerlist,region='Air')

def windmagus(playernum,playerlist):
    mydict = {'target':0, 'ally_draw':2, 'enemy_draw':2}
    return Card(name='Wind Magus',stats=(3,4),cardtype='unit',manacost=4,player=playernum,art=windmaguspic,sleep=True,effectdict=mydict,text='Draw 2 all',player_list=playerlist,region='Air')

#5mana:
def aeroarchivist(playernum,playerlist): 
    def chooser():
        x=list()
        random.shuffle(playerlist[playernum].discard_pile)
        for card in playerlist[playernum].discard_pile:
            if card.cardtype=='unit':
                x.append(card)
            if len(x) >2:
                break
        for card in x:
            playerlist[playernum].discard_pile.remove(card)
            playerlist[playernum].hand.append(card) 
            playerlist[playernum].discard(card) if len(playerlist[playernum].hand)>10 else 0
    mydict = { 'target':0, 'other':lambda obj:chooser()}
    return Card(name='Aero- Archivist',stats=(5,5),cardtype='unit',manacost=5,player=playernum,art=aeroarchivistpic,sleep=True,effectdict=mydict,text='Add 3 discarded minions to hand',player_list=playerlist,region='Air')

#6 mana
def flyingbison(playernum,playerlist): 
    mydict = { 'target':2, 'target_hand_discard':2}
    mytarget = {'target':2, 'ally_hand_discard':2,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Flying Bison',stats=(7,7),cardtype='unit',manacost=6,player=playernum,art=flyingbisonpic,sleep=False,effectdict=mydict,targetdict=mytarget,text='discard 2',player_list=playerlist,charge=True,region='Air')






#Spells:
# 1 mana 
def lastbreath(playernum,playerlist): 
    mydict = { 'target':1,  'target_other': lambda obj:  playerlist[playernum].discard(playerlist[playernum].hand[rng(0,len(playerlist[playernum].hand)-1)]), 'target_healminion':-4, 'target_face':-4,
}
    mytarget = {'target':1,'enemy_healminion':1,'ally_board':1,'choose_enemy_face':1,'choose_ally_face':1}
    return Card(name='Last Breath',cardtype='spell',manacost=1,player=playernum,art=lastbreathpic,effectdict=mydict,targetdict=mytarget,text='deal 4 to anything, discard 1 random card (can be itself)',player_list=playerlist,region='Air')

def mirage(playernum,playerlist,n=3):
    def lol(obj):
        for _ in range(5):
            newcard = copy.copy(obj)
            newcard.display=obj.display.copy()
            playerlist[playernum].deck.append(newcard)
        random.shuffle(playerlist[playernum].deck)
    mydict = { 'target':1, 'target_other':lol}
    mytarget = {'target':1,'ally_hand_hp':1,'choose_enemy_face':0,'choose_ally_face':0, 'ally_board':0}
    return Card(name='Mirage',cardtype='spell',manacost=1,player=playernum,art=miragepic,effectdict=mydict,targetdict=mytarget,text='shuffle 5 copies of a handminion into the deck',player_list=playerlist,region='Air')



# 2 mana
def callofthewind(playernum,playerlist):
    mydict = { 'target':0, 'other':lambda obj: playerlist[playernum].draw(3 if len(playerlist[playernum].hand)<3 else 1)}
    return Card(name='Call of the Wind',cardtype='spell',manacost=2,player=playernum,art=callofthewindpic,sleep=True,text='Draw 1. 2 more if you have < 3 cards in hand',player_list=playerlist,region='Air',effectdict=mydict)

def airwhistle(playernum,playerlist): 
    mydict = { 'target':1,'target_recall':1}
    mytarget = {'target':1,'enemy_recall':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Air Whistle',cardtype='spell',manacost=2,player=playernum,art=airwhistlepic,text='Recall enemy',player_list=playerlist,region='Air',effectdict=mydict,targetdict=mytarget)

def zephyr(playernum,playerlist):
    def poof():
        drawlist = [playerlist[playernum].deck[n] for n in range (3 if len(playerlist[playernum].deck) >2 else len(playerlist[playernum].deck))]
        for n in range(3):
            xlist = playerlist[playernum].draw(1)
            if len(xlist) == 0:
                pass
            elif xlist[0] in playerlist[playernum].hand: #Is still in the hand
                if xlist[0].cardtype=='spell':
                    playerlist[playernum].discard(xlist[0]) 
                
    mydict = { 'target':0, 'other':lambda obj: poof() }
    return Card(name='Zephyr',cardtype='spell',manacost=2,player=playernum,art=zephyrpic,sleep=True,text='Draw 3 discard spells',player_list=playerlist,region='Air',effectdict=mydict)

#5 mana 
def tempest(playernum,playerlist): 
    mydict = { 'target':2,'target_recall':2,'other': lambda obj: playerlist[playernum].draw(1)}
    mytarget = {'target':2,'enemy_recall':2,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Tempest',cardtype='spell',manacost=5,player=playernum,art=tempestpic,text='Recall 2 enemy, draw 1',player_list=playerlist,region='Air',effectdict=mydict,targetdict=mytarget)

# 6 mana 
def windsblessing(playernum,playerlist): 
    mydict = { 'target':0, 'ally_draw':3}
    return Card(name="Wind's Blessing",cardtype='spell',manacost=6,player=playernum,art=windsblessingpic,disc=True,text='Draw 3 when played or discarded',player_list=playerlist,region='Air',effectdict=mydict)

def whirlwind(playernum,playerlist):
    mydict = { 'target':0, 'ally_recall_aoe':1, 'enemy_recall_aoe':1}
    return Card(name='Whirlwind',cardtype='spell',manacost=6,player=playernum,art=whirlwindpic,disc=True,text='Recall ALL',player_list=playerlist,region='Air',effectdict=mydict)
    
#7 mana
#add discarded to hand



#10 mana 
def bisonspirits(playernum,playerlist): #LEGENDARY
    mydict = {'target':0, 'summoning':(2,2)}
    return Card(name='Bison Spirits',cardtype='spell',manacost=10,player=playernum,art=bisonspiritspic,effectdict=mydict,text='summon 2 flying bisons',player_list=playerlist,newcard=flyingbison,region='Air')

#10 mana
def hurricane(playernum,playerlist): #LEGENDARY
    def op():
        for player in playerlist:
            player.board=list()
            for card in player.hand.copy():
                player.discard(card)
            while True:
                if len(player.deck)>0:  
                    player.draw(1)
                if len(player.deck) == 0 or len(player.hand) == 10:
                    break 
            player.discard_pile+=player.deck
            player.deck=list()

    mydict = { 'target':0,'other': lambda obj: op()}
    return Card(name='Hurricane',cardtype='spell',manacost=10,player=playernum,art=hurricanepic,text='Destroy board, discard hand, draw 10, destroy decks',player_list=playerlist,region='Air',effectdict=mydict)    




#EARTH
#1 mana
def earthfae(playernum,playerlist):
    return Card(name='Earth Fae',cardtype='unit',stats=(1,1),manacost=1,player=playernum,art=earthfaepic,player_list=playerlist,barrier=True,region='Earth')

def mudsprite(playernum,playerlist):
    return Card(name='Mud Sprite',cardtype='unit',stats=(0,1),manacost=1,player=playernum,art=mudspritepic,player_list=playerlist,barrier=True,region='Earth')

def earthsprite(playernum,playerlist): 
    mydict = {'target':0, 'summoning':(1,1)}
    return Card(name='Earth Sprite',cardtype='unit',stats=(0,1),manacost=1,player=playernum,art=earthspritepic,player_list=playerlist,newcard=mudsprite,region='Earth',text='add 1/1 barrier to hand',effectdict=mydict)

#2 mana
def mudurchin(playernum,playerlist):
    return Card(name='Mud Urchin',cardtype='unit',stats=(1,2),manacost=2,player=playernum,art=mudurchinpic,text='barrier',player_list=playerlist,barrier=True,region='Earth')

#3 mana
def woodnymph(playernum,playerlist):
    mydict = {'target':1, 'target_barrier':1}
    mytarget = {'target':1, 'ally_board':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Wood Nymph',cardtype='unit',stats=(2,3),manacost=3,player=playernum,art=woodnymphpic,text='give ally barrier',player_list=playerlist,region='Earth',effectdict=mydict, targetdict=mytarget)

def stoneimp(playernum,playerlist):
    mydict = {'target':0, 'other':lambda obj:playerlist[playernum].draw(1) if 1 in  [1 if card.region=='Earth' else 0 for card in playerlist[playernum].board] else 0}
    return Card(name='Stone Imp',cardtype='unit',stats=(3,3),manacost=3,player=playernum,art=stoneimppic,text='alliance: draw 1',player_list=playerlist,region='Earth',effectdict=mydict)

#4 mana
def rockfae(playernum,playerlist):
    mydict = {'target':0, 'summoning':(1,2)}
    return Card(name='Rock Fae',cardtype='unit',stats=(3,1),manacost=4,player=playernum,art=rockfaepic,text='barrier,snuff summon 1/1 barrier',snuffed=True,snuffdict=mydict,newcard=earthfae,player_list=playerlist,region='Earth',barrier=True)

def nympharcher(playernum,playerlist):
    mydict = { 'target':1, 'target_other': lambda obj: obj.changestat((0,0,-2)) if (1 in  [1 if card.region=='Earth' else 0 for card in playerlist[playernum].board]) else 0,}
    mytarget = {'target':1,'enemy_hp':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Nymph Archer',cardtype='unit',stats=(4,4),manacost=4,player=playernum,art=nympharcherpic,text='alliance: deal 2 to an enemy minion',player_list=playerlist,region='Earth',effectdict=mydict,targetdict=mytarget)


#5 mana
def stonesergeant(playernum,playerlist):
    mydict = {'target':2, 'target_hp': 2, 'target_atk': 2}
    mytarget = {'target':2, 'ally_board':1, 'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Stone Sergeant',cardtype='unit',stats=(1,2),manacost=5,player=playernum,art=stonesergeantpic,text='+2/+2 for 2 allies ',player_list=playerlist,region='Earth',effectdict=mydict,targetdict=mytarget)

#6 mana
def armoursmith(playernum,playerlist):
    mydict = {'target':0, 'ally_armour':4}
    return Card(name='Armour- Smith',cardtype='unit',stats=(5,7),manacost=6,player=playernum,art=armoursmithpic,text='turnstart 4 armour',player_list=playerlist,region='Earth',turnstart=True,turnstartdict=mydict)

def earthenchief(playernum,playerlist):
    mydict = {'target':0, 'other': lambda obj: [card.changestat((1,1,0)) for card in playerlist[playernum].board] if (1 in  [1 if card.region=='Earth' else 0 for card in playerlist[playernum].board]) else 0}
    return Card(name='Earthen Chief',cardtype='unit',stats=(5,6),manacost=6,player=playernum,art=earthenchiefpic,text='alliance: give allies 1/1',player_list=playerlist,region='Earth',effectdict=mydict)

#7 mana
def rockelemental(playernum,playerlist): 
    return Card(name='Rock Elemental',cardtype='unit',stats=(7,7),manacost=7,player=playernum,art=rockelementalpic,player_list=playerlist,region='Earth')


#8 mana
def quicksanddevil(playernum,playerlist):
    mydict = {'target':0, 'ally_healminion_aoe':-3,'enemy_healminion_aoe':-3,'ally_atk_aoe':3,'enemy_atk_aoe':3}
    return Card(name='Quicksand Devil',cardtype='unit',stats=(5,6),manacost=8,effectdict=mydict,text='+3/-3 to ALL minions',art=quicksanddevilpic,player=playernum,player_list=playerlist,region='Earth')

# 9 mana
def elvengrove(playernum,playerlist):
    mydict = {'target':0, 'ally_barrier_aoe':1}
    return Card(name="Elven Grove",cardtype='unit',stats=(9,9),manacost=9,effectdict=mydict,text='Give allies barrier',art=elvengrovepic,player=playernum,player_list=playerlist,region='Earth',rush=True,sleep=False)

def terra(playernum,playerlist):
    return Card(name='Terra',cardtype='unit',stats=(9,9),manacost=9,text='Mountain',art=terrapic,player=playernum,player_list=playerlist,region='Earth',barrier=True)




#Spells
#1 mana
def armourstrike(playernum,playerlist):
    mydict = { 'target':1, 'target_other':lambda obj: obj.changestat((0,0,-playerlist[playernum].armour))}
    mytarget = {'target':1, 'ally_board':1,'enemy_healminion':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Armour Strike',cardtype='spell',stats=(0,0),manacost=1,player=playernum,art=armourstrikepic,text='deal dmg = armour to minion',player_list=playerlist,effectdict=mydict,targetdict=mytarget,region='Earth')

#2 mana
def harden(playernum,playerlist):
    mydict = { 'target':1, 'target_hp':1,'target_atk':2,'other':lambda obj: playerlist[playernum].draw(1) }
    mytarget ={'target':1, 'ally_board':1,'enemy_hp':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Harden',cardtype='spell',manacost=2,player=playernum,art=hardenpic,text='+2/+1, draw 1',player_list=playerlist,effectdict=mydict,targetdict=mytarget,region='Earth')

#3 mana
def stoneplate(playernum,playerlist):
    mydict = { 'target':0, 'ally_armour':5,'ally_draw':1}
    return Card(name='Stone Plate',cardtype='spell',stats=(0,0),manacost=3,player=playernum,art=stoneplatepic,text='draw 1 gain 5 armour',player_list=playerlist,effectdict=mydict,region='Earth')

def catapult(playernum,playerlist):
    mydict = {'target':1, 'target_healminion':-4, 'other':lambda obj:playerlist[playernum].gainarmour(5) if 1 in  [1 if card.region=='Earth' else 0 for card in playerlist[playernum].board] else 0}
    mytarget = {'target':1,'enemy_healminion':1,'ally_board':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Catapult',cardtype='spell',manacost=3,player=playernum,art=catapultpic,text='Deal 4 minion, alliance: gain 5 armour',player_list=playerlist,region='Earth',effectdict=mydict,targetdict=mytarget)


#7 mana
def earthquake(playernum,playerlist):
    mydict = {'target':0, 'ally_healminion_aoe':-7,'enemy_healminion_aoe':-7}
    return Card(name='Earthquake',cardtype='spell',manacost=7,effectdict=mydict,text='deal 7 to ALL minions',art=earthquakepic,player=playernum,player_list=playerlist,region='Earth')

def earthsigil(playernum,playerlist):
    def myfunc(obj):
        add77=False
        if playerlist[playernum].deck:
            myregion = playerlist[playernum].deck[0].region
            if myregion == 'Earth':
                add77=True
                obj.addboard=1
        return add77
    mydict = {'target':0, 'myself': lambda obj: obj.summon() if myfunc(obj) else 0, 'ally_draw':1, 'ally_armour':7}
    return Card(name='Earth Sigil',cardtype='spell',manacost=7,player=playernum,art=earthsigilpic,text='7 armour, draw 1, if Earth, summon 7/7',player_list=playerlist,region='Earth',effectdict=mydict,newcard=rockelemental)


#9 mana
def mountainscall(playernum,playerlist):
    mydict = {'target':1, 'target_healminion':9, 'target_face':9,'summoning':(1,2)}
    mytarget =  {'target':1,'ally_board':1,'enemy_healminion':1,'choose_enemy_face':1,'choose_ally_face':1}
    return Card(name="Mountain's Call",cardtype='spell',manacost=9,effectdict=mydict,targetdict=mytarget,text='heal 9  anyth, summon 9/9 barrier',newcard=terra,art=mountainscallpic,player=playernum,player_list=playerlist,region='Earth')

#10 mana
def earthspirits(playernum, playerlist): #LEGENDARY
    def action(obj):
        x=list()
        for card in playerlist[playernum].deck:
            if len(x)>3:
                break
            if card.region=='Earth' and card.cardtype == 'unit':
                x.append(card)
        for card in x:
            playerlist[playernum].boardcounter()
            playerlist[playernum].deck.remove(card)
            if len(playerlist[playernum].board) >= 7:
                playerlist[playernum].discard_pile.append(playerlist[playernum])
            else:
                if playerlist[playernum].atknum<5:
                    card.played=2
                elif playerlist[playernum].defnum<2:
                    card.played=1
                playerlist[playernum].board.append(card)
    mydict = {'target':0, 'other':action }
    return Card(name='Earth Spirits',cardtype='spell',manacost=10,effectdict=mydict,text='Summon 4 earth minions',art=earthspiritspic,player=playernum,player_list=playerlist,region='Earth')

#WATER

#1 mana
def smallblob(playernum,playerlist):
    def rushing(obj):
        obj.sleep, obj.rush=False,True
    mydict={'target':0,'myself':rushing}
    return Card(name='Small Blob',cardtype='unit',stats=(1,1),manacost=1,text='I am smol',effectdict=mydict,art=smallblobpic,player=playernum,player_list=playerlist,region='Water',sleep=False,rush=True)

def watersprite(playernum,playerlist):
    def myfunc():
        return 1 if playerlist[playernum].mana>9 or playerlist[playernum].maxmana>9 else 0
    mydict = {'target':1, 'target_other':lambda obj: (obj.changestat((0,0,-3)) if type(obj)==Card else obj.damage(-3)) if myfunc() else 0}
    mytarget = {'target':1, 'enemy_healminion':1,'ally_board':1,'choose_enemy_face':1,'choose_ally_face':1}
    return Card(name='Water Sprite',cardtype='unit',stats=(0,1),manacost=1,effectdict=mydict,targetdict=mytarget,text='Deal 3 anyth if 10 mana crystals',art=waterspritepic,player=playernum,player_list=playerlist,region='Water')

#2 mana
def waternymph(playernum,playerlist):
    return Card(name='Water Nymph',cardtype='unit',stats=(1,3),manacost=2,text='Rush',rush=True,sleep=False,art=waternymphpic,player=playernum,player_list=playerlist,region='Water')

#3 mana
def waterwell(playernum,playerlist):
    mydict={'target':0, 'ally_draw':1}
    return Card(name='Water Well',cardtype='unit',stats=(0,3),manacost=3,text='end turn draw 1',turnenddict=mydict,turnend=True,art=waterwellpic,player=playernum,player_list=playerlist,region='Water')


def mediumblob(playernum,playerlist):
    def rushing(obj):
        obj.sleep, obj.rush=False,True
    mydict={'target':0,'summoning':(2,2)}
    mydict2={'target':0,'myself':rushing}
    return Card(name='Medium Blob',cardtype='unit',stats=(2,2),manacost=3,text='summon 2 1/1s when die',effectdict=mydict2,snuffed=True,snuffdict=mydict,newcard=smallblob,art=mediumblobpic,player=playernum,player_list=playerlist,region='Water',sleep=False,rush=True)


#4 mana
def waterpriest(playernum,playerlist):
    mydict = {'target':1, 'target_face':4, 'target_healminion':4}
    mytarget = {'target':1, 'enemy_healminion':1,'ally_board':1,'choose_enemy_face':1,'choose_ally_face':1}
    return Card(name='Water Priest',cardtype='unit',stats=(3,4),manacost=4,effectdict=mydict,targetdict=mytarget,text='Heal 4 anyth',art=waterpriestpic,player=playernum,player_list=playerlist,region='Water')

def watergatherer(playernum,playerlist):
    mydict = {'target':0, 'other':lambda obj: playerlist[playernum].gainmaxmana(1) if (1 in  [1 if card.region=='Water' else 0 for card in playerlist[playernum].board]) else 0 }
    return Card(name='Water Gatherer',cardtype='unit',stats=(3,4),manacost=4,effectdict=mydict,text='alliance: 1 empty mana',art=watergathererpic,player=playernum,player_list=playerlist,region='Water')

#5 mana
def waterpaladin(playernum,playerlist):
    mydict = {'target':0, 'myself':lambda obj: obj.changestat((0,-len(playerlist[(playernum+1)%2].hand),0)) }
    return Card(name='Water Paladin',cardtype='unit',stats=(3,12),manacost=5,effectdict=mydict,text='Lose max hp = len opp hand',art=waterpaladinpic,player=playernum,player_list=playerlist,region='Water')

def surgingelemental(playernum,playerlist):
    return Card(name='Surging Elemental',cardtype='unit',stats=(5,2),manacost=5,text='rush barrier',rush=True,sleep=False,barrier=True,art=surgingelementalpic,player=playernum,player_list=playerlist,region='Water')


#6 mana
def perpetualblob(playernum,playerlist):
    mydict={'target':0,'summoning':(1,2)}
    return Card(name='Perpetual Blob',cardtype='unit',stats=(3,3),manacost=6,text='summon itself when die',snuffed=True,snuffdict=mydict,newcard=perpetualblob,art=perpetualblobpic,player=playernum,player_list=playerlist,region='Water')

def mermentrader(playernum,playerlist):
    mydict={'target':0,'ally_hand_manacost_aoe':-1}
    return Card(name='Mermen Trader',cardtype='unit',stats=(5,5),manacost=6,text='turnend discount 1',turnend=True,turnenddict=mydict,art=mermentraderpic,player=playernum,player_list=playerlist,region='Water')

#7 mana
def largeblob(playernum,playerlist):
    def rushing(obj):
        obj.sleep, obj.rush=False,True
    mydict={'target':0,'summoning':(2,2)}
    mydict2={'target':0,'myself':rushing}
    return Card(name='Large Blob',cardtype='unit',stats=(4,4),manacost=7,text='summon 2 2/2s when die',effectdict=mydict2,snuffed=True,snuffdict=mydict,newcard=mediumblob,art=largeblobpic,player=playernum,player_list=playerlist,region='Water',sleep=False,rush=True)

#8 mana
def rainbringer(playernum,playerlist):
    mydict={'target':0,'enemy_split_dmg':8}
    return Card(name='Rain- bringer',cardtype='unit',stats=(4,8),manacost=8,text='deal 8 random split enemy minions',effectdict=mydict,art=rainbringerpic,player=playernum,player_list=playerlist,region='Water')

def watersylph(playernum,playerlist):
    mydict={'target':0,'summoning':(1,1)}
    return Card(name='Water Sylph',cardtype='unit',stats=(7,7),manacost=8,text='Start&End: Add rain hand',turnstart=True,turnstartdict=mydict,turnend=True,turnenddict=mydict,newcard=rain,art=watersylphpic,player=playernum,player_list=playerlist,region='Water')

#9 mana
def bloodbender(playernum,playerlist):
    mydict = { 'target':0, 'ally_face':7}
    return Card(name='Blood- bender',stats=(7,10),cardtype='unit',manacost=9,player=playernum,art=bloodbenderpic,snuffdict=mydict,snuffed=True,text='snuff: heal 7 face',lifesteal=True,player_list=playerlist,region='Water')

#10 mana
def waterspirits(playernum,playerlist): #LEGENDARY
    mydict = { 'target':0, 'resurrect':(1,'region','Water')}
    return Card(name='Water Spirits',stats=(8,11),cardtype='unit',manacost=10,player=playernum,art=waterspiritspic,sleep=True,turnenddict=mydict,turnend=True,text='end turn resurrect 1 water minion',player_list=playerlist,region='Water')

def watershrine(playernum,playerlist):
    def myfunc(obj):
        chosencard=None
        for card in playerlist[playernum].deck:
            if card.cardtype=='unit':
                chosencard=card
                break
        if chosencard:
            playerlist[playernum].boardcounter()
            if len(playerlist[playernum].board)<7:
                playerlist[playernum].deck.remove(chosencard)
                playerlist[playernum].board.append(chosencard)
                chosencard.played=2 if playerlist[playernum].atknum<5 else 1 if playerlist[playernum].defnum<2 else 0
            else: #board is full, dont summon minion
                pass
    mydict={'target':0,'other':myfunc}
    return Card(name='Water Shrine',stats=(0,10),cardtype='unit',manacost=10,player=playernum,art=watershrinepic,text='turnend summon minion from deck',turnend=True,turnenddict=mydict,player_list=playerlist,region='Water')

def blobosaurus(playernum,playerlist):
    def rushing(obj):
        obj.sleep, obj.rush=False,True
    mydict={'target':0,'summoning':(2,2)}
    mydict2={'target':0,'myself':rushing}
    return Card(name='Blobosaurus',cardtype='unit',stats=(8,8),manacost=10,text='summon 2 4/4s when die',effectdict=mydict2,snuffed=True,snuffdict=mydict,newcard=largeblob,art=blobosauruspic,player=playernum,player_list=playerlist,region='Water')

#Spells
#1 mana
def rain(playernum,playerlist): #all minions
    mydict={'target':0,'both_split_dmg':4}
    return Card(name='Rain',cardtype='spell',manacost=1,player=playernum,text='4 split all minons',effectdict=mydict,player_list=playerlist,region='Water',art=rainpic)

#2 mana
def waterjet(playernum,playerlist):
    mydict = { 'target':1, 'target_healminion':-3, 'other':lambda obj: playerlist[playernum].heal(3)}
    mytarget = {'target':1, 'enemy_healminion':1,'ally_board':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Water Jet',art=waterjetpic,cardtype='spell',manacost=2,player=playernum,effectdict=mydict,targetdict=mytarget, text='Deal 3 minion, heal 3',player_list=playerlist, region='Water')

#3 mana
def bluecatalyst(playernum,playerlist):
    mydict = { 'target':0, 'ally_max_mana':1, 'ally_draw':1}
    return Card(name='Blue Catalyst',art=bluecatalystpic,cardtype='spell',manacost=3,player=playernum,effectdict=mydict, text='Draw 1. Gain empty mana',player_list=playerlist, region='Water')

def flood(playernum,playerlist):
    mydict = { 'target':0, 'enemy_healminion_aoe':-2,'ally_healminion_aoe':-2}
    return Card(name='Flood',art=floodpic,cardtype='spell',manacost=3,player=playernum,effectdict=mydict, text='Deal 2 to all minions',player_list=playerlist,region='Water')

#6 mana
def redcatalyst(playernum,playerlist):
    mydict = { 'target':0, 'ally_draw':3,'ally_max_mana':1}
    return Card(name='Red Catalyst',art=redcatalystpic,cardtype='spell',manacost=6,player=playernum,effectdict=mydict, text='Draw 3. Gain empty mana',player_list=playerlist, region='Water')

#10 mana 
def sirenscall(playernum,playerlist):
    def lol():
        playerlist[playernum].draw(5)
        playerlist[playernum].gainarmour(5)
    mydict = { 'target':1, 'target_healminion':-5, 'target_face':-5,'target_other':lambda obj:lol(),'summoning':(1,2)}
    mytarget = {'target':1, 'enemy_healminion':1,'ally_board':1,'choose_enemy_face':1,'choose_ally_face':1}
    return Card(name="Siren's Call",art=sirenscallpic,cardtype='spell',manacost=10,player=playernum,effectdict=mydict, targetdict=mytarget,text='Deal 5, draw 5. 5 amr, summon 5/5',player_list=playerlist, newcard=naga, region='Water')


def tsunami(playernum,playerlist): #deal aoe damage
    pass


#FIRE
#minions 
#1 mana 
def firegoblin(playernum,playerlist):
    mydict = {'target':0,'ally_face':-3}
    return Card(name='Fire Goblin',cardtype='unit',stats=(2,2),manacost=1,player=playernum,art=firegoblinpic,text='Deal 3 to you hero',player_list=playerlist,region='Fire',effectdict=mydict)


def firesprite(playernum,playerlist):
    mydict={'target':0,'summoning':(1,2)}
    return Card(name='Fire Sprite',cardtype='unit',stats=(0,1),manacost=1,text='snuff summon 1/1',snuffed=True,snuffdict=mydict,newcard=sprite,art=firespritepic,player=playernum,player_list=playerlist,region='Fire')

#2 mana
def impegg(playernum,playerlist):
    mydict={'target':0,'summoning':(1,2)}
    return Card(name='Imp Egg',cardtype='unit',stats=(0,2),manacost=2,text='Wither. Snuff: summon 3/3',snuffed=True,snuffdict=mydict,newcard=fireimp,art=impeggpic,player=playernum,player_list=playerlist,region='Fire',wither=True)

def explosiveurchin(playernum,playerlist): #for urchin ringleader
    mydict={'target':0,'enemy_split_dmg_face':2}
    return Card(name='Explosive Urchin',cardtype='unit',stats=(2,2),manacost=2,text='snuff 2 random dmg',snuffed=True,snuffdict=mydict,art=explosiveurchinpic,player=playernum,player_list=playerlist,region='Fire')

# 3 mana
def fireimp(playernum, playerlist): 
    mydict={'target':0,'both_split_dmg_face':4}
    return Card(name='Fire Imp',cardtype='unit',stats=(3,3),manacost=3,player=playernum,art=fireimppic,text='4 ALL split',player_list=playerlist,region='Fire',effectdict=mydict)

def flamehatchling(playernum,playerlist):
    mydict={'target':0,'summoning':(1,2)}
    return Card(name='Flame Hatchling',cardtype='unit',stats=(0,3),manacost=3,text='Wither. snuff summon 5/3',snuffed=True,snuffdict=mydict,newcard=flamedemon,art=flamehatchlingpic,player=playernum,player_list=playerlist,region='Fire',wither=True)

def flameurchin(playernum,playerlist):
    mydict={'target':0,'other': lambda obj: playerlist[(playernum+1)%2].board[rng(0,len(playerlist[(playernum+1)%2].board)-1)].kill() if playerlist[(playernum+1)%2].board else 0}
    return Card(name='Flame Urchin',cardtype='unit',stats=(2,2),manacost=3,text='snuff Kill random enemy',snuffed=True,snuffdict=mydict,art=flameurchinpic,player=playernum,player_list=playerlist,region='Fire')

def firemagus(playernum,playerlist):
    mydict = {'target':1,'target_other': lambda obj: obj.playsnuff()}
    mytarget = {'target':1,'enemy_hp':1,'ally_board':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Firemagus',cardtype='unit',stats=(2,3),manacost=3,player=playernum,art=firemaguspic,text="Trigger a card's snuff effect",player_list=playerlist,region='Fire',effectdict=mydict, targetdict=mytarget)

#4 mana
def pyromaniac(playernum,playerlist):
    def feed():
        for card in playerlist[playernum].board:
            card.playsnuff()
        for card in playerlist[(playernum+1)%2].board:
            card.playsnuff()
    mydict = {'target':0, 'other': lambda obj: feed()}
    return Card(name='Pyro- Maniac',cardtype='unit',stats=(1,7),manacost=4,player=playernum,art=pyromaniacpic,text='Start Turn: trigger all snuffs',player_list=playerlist,region='Fire',turnstart=True,turnstartdict=mydict)

def flametwirler(playernum,playerlist):
    mydict = { 'target':0, 'ally_draw':1}
    return Card(name='Flame Twirler',stats=(3,4),cardtype='unit',manacost=4,player=playernum,art=flametwirlerpic,sleep=True,player_list=playerlist,snuffdict=mydict,text='Snuff: Draw 1',snuffed=True,region='Fire')


def flamedemon(playernum, playerlist):  #Useless
    return Card(name='Flame Demon',cardtype='unit',stats=(6,3),manacost=4,player=playernum,art=flamedemonpic,player_list=playerlist,region='Fire')

#5 mana
def flarevanguard(playernum,playerlist):
    mydict = { 'target':0, 'other': lambda obj: [card.changestat((1,2,0)) if card.played==1 else 0 for card in playerlist[playernum].board]}
    return Card(name='Flare Vanguard',stats=(5,2),cardtype='unit',manacost=5,player=playernum,art=flarevanguardpic,sleep=False,player_list=playerlist,snuffdict=mydict,text='Snuff: give def minion 1/2',snuffed=True,rush=True,region='Fire')



#6 mana
def kindlestone(playernum, playerlist): 
    return Card(name='Kindle Stone',cardtype='unit',stats=(4,5),manacost=6,player=playernum,art=kindlestonepic,player_list=playerlist,region='Fire')

def kindlegem(playernum,playerlist):
    mydict={'target':0,'summoning':(1,2)}
    return Card(name='Kindle Gem',cardtype='unit',stats=(3,5),manacost=6,text='snuff summon 4/5',snuffed=True,snuffdict=mydict,newcard=kindlestone,art=kindlegempic,player=playernum,player_list=playerlist,region='Fire')

#7 mana 
def urchinringleader(playernum,playerlist): #LEGENDARY
    mydict={'target':0, 'summoning':(2,2)}
    return Card(name='Urchin Ringleader',cardtype='unit',stats=(4,5),manacost=7,text='summon 2 explosive urchins',newcard=explosiveurchin,art=urchinringleaderpic,player=playernum,player_list=playerlist,region='Fire',effectdict=mydict)

#8 mana
def explosivewraith(playernum,playerlist):
    mydict={'target':0,'other': lambda obj: playerlist[(playernum+1)%2].board[rng(0,len(playerlist[(playernum+1)%2].board)-1)].kill() if playerlist[(playernum+1)%2].board else 0}
    return Card(name='Explosive Wraith',cardtype='unit',stats=(5,7),manacost=8,text='lifesteal, snuff kill random enemy',lifesteal=True,snuffed=True,snuffdict=mydict,art=explosivewraithpic,player=playernum,player_list=playerlist,region='Fire')

#9 mana 
def amaterasu(playernum,playerlist): #LEGENDARY
    def fire():
        for card in playerlist[playernum].graveyard:
            if card.region == 'Fire':
                card.changestat((2,2,0))
        for card in playerlist[playernum].hand:
            if card.region == 'Fire':
                card.changestat((2,2,0))
        for card in playerlist[playernum].deck:
            if card.region == 'Fire':
                card.changestat((2,2,0))
        for card in playerlist[playernum].board:
            if card.region == 'Fire':
                card.changestat((2,2,0))
    mydict = {'target':0, 'other': lambda obj: fire()}
    return Card(name='Amaterasu',cardtype='unit',stats=(3,6),manacost=9,text='All allies everywhere 3/3',snuffed=True,snuffdict=mydict,art=amaterasupic,player=playernum,player_list=playerlist,region='Fire')



#10 mana 
def infernalspirits(playernum,playerlist): #LEGENDARY
    def omgz():
        random.shuffle(playerlist[playernum].graveyard)
        templist=list()
        for card in playerlist[playernum].graveyard:
            if card.snuffdict!=spelldictnull:
                templist.append(card)
        for card in templist:
            playerlist[playernum].boardcounter()
            if len(playerlist[playernum].board)<7:
                playerlist[playernum].graveyard.remove(card)
                playerlist[playernum].board.append(card)
                card.played=2 if playerlist[playernum].atknum<5 else 1 if playerlist[playernum].defnum<2 else 0
            else: #board is full, dont summon minion
                break         
    mydict={'target':0,'other':lambda obj: omgz()}
    return Card(name='Infernal Spirits',cardtype='unit',stats=(5,5),manacost=10,text='summon all ded snuff minions',effectdict=mydict,art=infernalspiritspic,player=playernum,player_list=playerlist,region='Fire')


#Spells
#0 mana
def offering(playernum,playerlist):
    mydict = { 'target':1, 'target_other':lambda obj: obj.kill(), 'other':lambda obj: playerlist[playernum].heal(4)}
    mytarget = {'target':1, 'ally_board':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Offering',cardtype='spell',manacost=0,player=playernum,art=offeringpic,effectdict=mydict,targetdict=mytarget,text='kill ally heal 4',player_list=playerlist,region='Fire')

# 1 mana 
def spark(playernum,playerlist):
        
    mydict = { 'target':1, 'target_other':lambda obj:obj.changestat((0,0,-4)), 'other':lambda obj: playerlist[playernum].draw(1)}
    mytarget = {'target':1, 'ally_board':1,'choose_enemy_face':0,'choose_ally_face':0}
    return Card(name='Spark',cardtype='spell',manacost=1,player=playernum,art=sparkpic,effectdict=mydict,targetdict=mytarget,text='Draw 1 deal 4 ally',player_list=playerlist,region='Fire')

# 2 mana 
def combustion(playernum,playerlist):
    def lol():
        for card in playerlist[playernum].board:
            if card.snuffed == True:
                card.playsnuff()
    mydict = { 'target':0, 'other':lambda obj: lol()}
    return Card(name='Combustion',cardtype='spell',manacost=2,player=playernum,art=combustionpic,effectdict=mydict,text='Trigger your snuffs',player_list=playerlist,region='Fire')

def implosion(playernum,playerlist):
    def lol():
        templist = list()
        dedlist = list()
        count=0
        for player in playerlist:
            for card in player.board:
                templist.append(card) 
        count=0
        while True and count<20:
            count+=1
            if count>20:
                break
            for card in templist: 
                card.changestat((0,0,-1))
                if card.currentstats[1]<=0:
                    dedlist.append(card)
            for card in dedlist:
                card.reset()
                playerlist[card.player].graveyard.append(card)
                playerlist[card.player].board.remove(card)
                card.playsnuff() if card.snuffed==True else 0                    
            if len(dedlist):
                templist=list()
                for player in playerlist:
                    for card in player.board:
                        templist.append(card)   
                dedlist=list()
                continue
            else:
                break                
    mydict = { 'target':0, 'other':lambda obj: lol()}
    return Card(name='Implosion',cardtype='spell',manacost=2,player=playernum,art=implosionpic,effectdict=mydict,text='Deal 1 to all, repeat if any die',player_list=playerlist,region='Fire')



# 5 mana
def unholypact(playernum,playerlist): 
    mydict = { 'target':0, 'ally_draw':3,'ally_face':-3}
    return Card(name='Unholy Pact',cardtype='spell',manacost=5,player=playernum,art=unholypactpic,text='Draw 3 ,-3hp',player_list=playerlist,region='Fire',effectdict=mydict) 

#8 mana 
def eruption(playernum,playerlist):
    mydict = { 'target':0,  'enemy_kill_aoe':1, 'ally_kill_aoe':1}
    return Card(name='Eruption',art=eruptionpic,cardtype='spell',manacost=8,player=playernum,effectdict=mydict, text='AOE Kill all',player_list=playerlist,region='Fire')



#Tokens

def sprite(playernum, playerlist): 
    return Card(name='Sprite',cardtype='unit',stats=(1,1),manacost=1,player=playernum,art=spritepic,player_list=playerlist)

def urchin(playernum, playerlist): 
    return Card(name='Urchin',cardtype='unit',stats=(2,2),manacost=2,player=playernum,art=red_nexus,player_list=playerlist)

def cloud(playernum,playerlist):
    mydict = { 'target':0, 'ally_draw':1}
    return Card(name='Cloud',stats=(1,1),cardtype='unit',manacost=2,player=playernum,art=cloudpic,effectdict=mydict,player_list=playerlist,rush=True, sleep=False,region='Air')

def imp(playernum, playerlist): 
    return Card(name='Imp',cardtype='unit',stats=(3,3),manacost=3,player=playernum,art=red_nexus,player_list=playerlist)

def wraith(playernum, playerlist): 
    return Card(name='Wraith',cardtype='unit',stats=(5,5),manacost=5,player=playernum,art=red_nexus,player_list=playerlist,region='Shadow')

def naga(playernum, playerlist): 
    return Card(name='Naga',cardtype='unit',stats=(5,5),manacost=5,player=playernum,art=red_nexus,player_list=playerlist)


#CARD LIST
cardlist = [
#Air
#minions
airsprite, cyclos, windfae,halos,miragesorcerer,windmagus,aeros,cloudsorcerer,scrapdealer, aeroarchivist, flyingbison, 
#spells
lastbreath, mirage, callofthewind, airwhistle, zephyr, tempest, windsblessing, whirlwind, hurricane, bisonspirits,

#Earth
#minions
earthsprite, earthfae, mudurchin, woodnymph, stoneimp, rockfae, nympharcher, stonesergeant, armoursmith, earthenchief, rockelemental, quicksanddevil, elvengrove, terra,
#spells
armourstrike, harden, stoneplate, catapult, earthquake, earthsigil, mountainscall, earthspirits,
 
#Water
#minions
smallblob, watersprite, waternymph, waterwell, mediumblob, waterpriest, watergatherer, waterpaladin, surgingelemental, perpetualblob, mermentrader, largeblob, rainbringer, watersylph, waterspirits, bloodbender, watershrine,blobosaurus,
#spells
rain,waterjet,bluecatalyst,flood,redcatalyst,sirenscall,

#Fire
#minions
fireimp,firesprite,firegoblin,impegg,explosiveurchin,flamehatchling,flameurchin,firemagus,pyromaniac,flametwirler,flarevanguard,flamedemon,kindlestone,kindlegem,urchinringleader,explosivewraith,amaterasu,infernalspirits,
#spells
offering,spark,implosion,combustion,unholypact,eruption,


#Neutral
#minions
generousmerchant,clericapprentice,bandit,drunkenbrawler,dhampir,swiftmessenger,pickpocketeer,icemaiden,defiantsergeant,shieldbearer,angrylibrarian,lonelytroll,swiftharpy,necromancer,chaaarrge,anubis,rovingcaravan,hiredhitman, deadlyassassin, shiva,magicalwisp,gladiator,generalhark,erebus,playfultrickster,
#spells
knife, divineprotection,icicles,catalyst,serenity,frostspear,assassinate,dragonfire,urchinsunite,grandconcession,mirror,
]
legendarylist=[
#Air
bisonspirits, hurricane,
#Earth
earthspirits,
#Water
waterspirits,
#Fire
infernalspirits, amaterasu,urchinringleader,

#Neutral
anubis,chaaarrge,shiva,generalhark,erebus,
]
tokenlist=[
sprite,imp,urchin,cloud,naga,wraith,
]




