import pygame
pygame.init()

#PICTURES
background=pygame.image.load('resources/Background.jpg')
red_nexus=pygame.image.load('resources/Crystal Red.png')
blue_nexus=pygame.image.load('resources/Crystal Blue.png')
mana_red = pygame.image.load('resources/Mana Red.png')
mana_blue = pygame.image.load('resources/Mana Blue.png')
card_back = pygame.image.load('resources/Card Back.jpg')
card_base = pygame.image.load('resources/Card Front.jpg')
armour_base = pygame.image.load('resources/Armour.png')

#NEUTRAL
#minions
icespritepic=pygame.image.load('resources/neutral/icesprite.jpg')
generousmerchantpic=pygame.image.load('resources/neutral/generousmerchant.jpg')
clericapprenticepic=pygame.image.load('resources/neutral/clericapprentice.jpg')
banditpic=pygame.image.load('resources/neutral/bandit.jpg')
drunkenbrawlerpic=pygame.image.load('resources/neutral/drunkenbrawler.jpg')
dhampirpic=pygame.image.load('resources/neutral/dhampir.jpg')
swiftmessengerpic=pygame.image.load('resources/neutral/swiftmessenger.jpg')
pickpocketeerpic=pygame.image.load('resources/neutral/pickpocketeer.jpg')
magicalwisppic=pygame.image.load('resources/neutral/magicalwisp.jpg')
icemaidenpic=pygame.image.load('resources/neutral/icemaiden.jpg')
defiantsergeantpic=pygame.image.load('resources/neutral/defiantsergeant.jpg')
shieldbearerpic=pygame.image.load('resources/neutral/shieldbearer.jpg')
angrylibrarianpic=pygame.image.load('resources/neutral/angrylibrarian.jpg')
lonelytrollpic=pygame.image.load('resources/neutral/lonelytroll.jpg')
swiftharpypic=pygame.image.load('resources/neutral/swiftharpy.jpg')
gladiatorpic=pygame.image.load('resources/neutral/gladiator.jpg')
necromancerpic=pygame.image.load('resources/neutral/necromancer.jpg')
chaaarrgepic=pygame.image.load('resources/neutral/chaaarrge.jpg')
anubispic=pygame.image.load('resources/neutral/anubis.jpg')
rovingcaravanpic=pygame.image.load('resources/neutral/rovingcaravan.jpg')
hiredhitmanpic=pygame.image.load('resources/neutral/hiredhitman.jpg')
deadlyassassinpic=pygame.image.load('resources/neutral/deadlyassassin.jpg')
playfultricksterpic=pygame.image.load('resources/neutral/playfultrickster.jpg')
generalharkpic=pygame.image.load('resources/neutral/generalhark.jpg')
shivapic=pygame.image.load('resources/neutral/shiva.jpg')
erebuspic=pygame.image.load('resources/neutral/erebus.jpg')

#spells
knifepic=pygame.image.load('resources/neutral/knife.jpg')
divineprotectionpic=pygame.image.load('resources/neutral/divineprotection.jpg')
iciclespic=pygame.image.load('resources/neutral/icicles.jpg')
catalystpic=pygame.image.load('resources/neutral/catalyst.jpg')

serenitypic=pygame.image.load('resources/neutral/serenity.jpg')
frostspearpic=pygame.image.load('resources/neutral/frostspear.jpg')
mirrorpic=pygame.image.load('resources/neutral/mirror.jpg')
assassinatepic=pygame.image.load('resources/neutral/assassinate.jpg')
dragonfirepic=pygame.image.load('resources/neutral/dragonfire.jpg')
urchinsunitepic=pygame.image.load('resources/neutral/urchinsunite.jpg')
grandconcessionpic=pygame.image.load('resources/neutral/grandconcession.jpg')


#AIR
#alphabetical order

aeroarchivistpic=pygame.image.load('resources/air/aeroarchivist.jpg')
aerospic=pygame.image.load('resources/air/aeros.jpg')
airspritepic=pygame.image.load('resources/air/airsprite.jpg')
airwhistlepic=pygame.image.load('resources/air/airwhistle.jpg')
bisonspiritspic=pygame.image.load('resources/air/bisonspirits.jpg')
callofthewindpic=pygame.image.load('resources/air/callofthewind.jpg')
cloudpic=pygame.image.load('resources/air/cloud.jpg')
cloudsorcererpic=pygame.image.load('resources/air/cloudsorcerer.jpg')
cyclospic=pygame.image.load('resources/air/cyclos.jpg')
flyingbisonpic=pygame.image.load('resources/air/flyingbison.jpg')
halospic=pygame.image.load('resources/air/halos.jpg')
hurricanepic=pygame.image.load('resources/air/hurricane.jpg')
lastbreathpic=pygame.image.load('resources/air/lastbreath.jpg')
miragepic=pygame.image.load('resources/air/mirage.jpg')
miragesorcererpic=pygame.image.load('resources/air/miragesorcerer.jpg')
scrapdealerpic=pygame.image.load('resources/air/scrapdealer.jpg')
tempestpic=pygame.image.load('resources/air/tempest.jpg')
whirlwindpic=pygame.image.load('resources/air/whirlwind.jpg')
windfaepic=pygame.image.load('resources/air/windfae.jpg')
windmaguspic=pygame.image.load('resources/air/windmagus.jpg')
windsblessingpic=pygame.image.load('resources/air/windsblessing.jpg')
zephyrpic=pygame.image.load('resources/air/zephyr.jpg')


#EARTH 
#minions
armoursmithpic=pygame.image.load('resources/earth/armoursmith.jpg')
armourstrikepic=pygame.image.load('resources/earth/armourstrike.jpg')
catapultpic=pygame.image.load('resources/earth/catapult.jpg')
earthenchiefpic=pygame.image.load('resources/earth/earthenchief.jpg')
earthfaepic=pygame.image.load('resources/earth/earthfae.jpg')
earthquakepic=pygame.image.load('resources/earth/earthquake.jpg')
earthsigilpic=pygame.image.load('resources/earth/earthsigil.jpg')
earthspiritspic=pygame.image.load('resources/earth/earthspirits.jpg')
earthspritepic=pygame.image.load('resources/earth/earthsprite.jpg')
elvengrovepic=pygame.image.load('resources/earth/elvengrove.jpg')
hardenpic=pygame.image.load('resources/earth/harden.jpg')
mountainscallpic=pygame.image.load('resources/earth/mountainscall.jpg')
mudspritepic=pygame.image.load('resources/earth/mudsprite.jpg')
mudurchinpic=pygame.image.load('resources/earth/mudurchin.jpg')
nympharcherpic=pygame.image.load('resources/earth/nympharcher.jpg')
quicksanddevilpic=pygame.image.load('resources/earth/quicksanddevil.jpg')
rockelementalpic=pygame.image.load('resources/earth/rockelemental.jpg')
rockfaepic=pygame.image.load('resources/earth/rockfae.jpg')
stoneimppic=pygame.image.load('resources/earth/stoneimp.jpg')
stoneplatepic=pygame.image.load('resources/earth/stoneplate.jpg')
stonesergeantpic=pygame.image.load('resources/earth/stonesergeant.jpg')
terrapic=pygame.image.load('resources/earth/terra.jpg')
woodnymphpic=pygame.image.load('resources/earth/woodnymph.jpg')


#WATER 
#minions
waterspritepic=pygame.image.load('resources/water/watersprite.jpg')
smallblobpic=pygame.image.load('resources/water/smallblob.jpg')
waternymphpic=pygame.image.load('resources/water/waternymph.jpg')
waterwellpic=pygame.image.load('resources/water/waterwell.jpg')
mediumblobpic=pygame.image.load('resources/water/mediumblob.jpg')
waterpriestpic=pygame.image.load('resources/water/waterpriest.jpg')
watergathererpic=pygame.image.load('resources/water/watergatherer.jpg')
waterpaladinpic=pygame.image.load('resources/water/waterpaladin.jpg')
surgingelementalpic=pygame.image.load('resources/water/surgingelemental.jpg')
perpetualblobpic=pygame.image.load('resources/water/perpetualblob.jpg')
mermentraderpic=pygame.image.load('resources/water/mermentrader.jpg')
largeblobpic=pygame.image.load('resources/water/largeblob.jpg')
rainbringerpic=pygame.image.load('resources/water/rainbringer.jpg')
watersylphpic=pygame.image.load('resources/water/watersylph.jpg')
bloodbenderpic=pygame.image.load('resources/water/bloodbender.jpg')
watershrinepic=pygame.image.load('resources/water/watershrine.jpg')
waterspiritspic=pygame.image.load('resources/water/waterspirits.jpg')
blobosauruspic=pygame.image.load('resources/water/blobosaurus.jpg')

#spells
rainpic=pygame.image.load('resources/water/rain.jpg')
floodpic=pygame.image.load('resources/water/flood.jpg')
waterjetpic=pygame.image.load('resources/water/waterjet.jpg')
bluecatalystpic=pygame.image.load('resources/water/bluecatalyst.jpg')
redcatalystpic=pygame.image.load('resources/water/redcatalyst.jpg')
sirenscallpic=pygame.image.load('resources/water/sirenscall.jpg')
tsunamipic=pygame.image.load('resources/water/tsunami.jpg')


#FIRE 
#minions
firespritepic=pygame.image.load('resources/fire/firesprite.jpg')
firegoblinpic=pygame.image.load('resources/fire/firegoblin.jpg')
impeggpic=pygame.image.load('resources/fire/impegg.jpg')
explosiveurchinpic=pygame.image.load('resources/fire/explosiveurchin.jpg')
fireimppic=pygame.image.load('resources/fire/fireimp.jpg')
flamehatchlingpic=pygame.image.load('resources/fire/flamehatchling.jpg')
flameurchinpic=pygame.image.load('resources/fire/flameurchin.jpg')
firemaguspic=pygame.image.load('resources/fire/firemagus.jpg')
pyromaniacpic=pygame.image.load('resources/fire/pyromaniac.jpg')
flametwirlerpic=pygame.image.load('resources/fire/flametwirler.jpg')
flamedemonpic=pygame.image.load('resources/fire/flamedemon.jpg')
flarevanguardpic=pygame.image.load('resources/fire/flarevanguard.jpg')
kindlestonepic=pygame.image.load('resources/fire/kindlestone.jpg')
kindlegempic=pygame.image.load('resources/fire/kindlegem.jpg')
urchinringleaderpic=pygame.image.load('resources/fire/urchinringleader.jpg')
explosivewraithpic=pygame.image.load('resources/fire/explosivewraith.png')
infernalspiritspic=pygame.image.load('resources/fire/infernalspirits.jpg')
amaterasupic=pygame.image.load('resources/fire/amaterasu.jpg')
#spells
offeringpic=pygame.image.load('resources/fire/offering.jpg')
sparkpic=pygame.image.load('resources/fire/spark.jpg')
combustionpic=pygame.image.load('resources/fire/combustion.jpg')
implosionpic=pygame.image.load('resources/fire/implosion.jpg')
unholypactpic=pygame.image.load('resources/fire/unholypact.jpg')
eruptionpic=pygame.image.load('resources/fire/eruption.jpg')


#TOKENS
spritepic=pygame.image.load('resources/neutral/sprite.jpg')
