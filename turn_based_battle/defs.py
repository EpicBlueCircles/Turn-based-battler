import pygame
import time
import random
import math
import pyganim
import ai
import dialog

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
GREY = (100,100,100)

pygame.init()
font = pygame.font.SysFont('Calibri', 15, True, False)
size = (1250, 700)
gScreen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
class Music(object):
	def __init__(self, musicc):
		self.musicc = "Assets/music/"+musicc+".ogg"
		self.playing = True
		
	def play(self):
		if self.playing:
			pygame.mixer.music.stop()
			pygame.mixer.music.load(self.musicc)
			pygame.mixer.music.play(-1, 0.0)
			#pygame.mixer.music.set_endevent(intodone)
		self.playing = False
	def reset(self):
		self.playing = True
	def stop(self):
		pygame.mixer.music.stop()
	def fadeout(self, time):
		pygame.mixer.music.fadeout(time)
		
cattheme = Music("Raxxo_Patchy_Aid")
cootheme = Music("Raxxo_Stand_Your_Ground")
theeCoosomeTheme = Music("brilliant_scientist-technological_defect")
maicetheme = Music("A_Tiny_Tiny_Clever_Commander")
sivtheme = Music("WaterflameFinalBattle")
noutheme = Music("supierior_nouledge")
maptheme = Music("Raxxo_Bent_to_the_Core")
durrictheme = Music("the_legend_durric")
alphatheme = Music("Hiroari_Shoots_a_Strange_Bird_Till When_Remix")
zaroltheme = Music("dBu_music_Suwa_Foughten_Field")
defulttheme = Music("dbu_trick_or_die")

menuui = pygame.image.load("assets/ui/menu.png")
lockedchar = pygame.image.load("assets/battlers/locked.png")
lockedskill = pygame.image.load("assets/moveboxes/locked.png")
selector1 = pygame.image.load("assets/ui/selector1.png")
selector2 = pygame.image.load("assets/ui/selector2.png")
selector3 = pygame.image.load("assets/ui/selector3.png")
mouse_pointer = pygame.image.load('Assets/mouse.png')
mouse_pointer2 = pygame.image.load('Assets/mouse2.png')
health_border = pygame.image.load('Assets/health_border.png')
coupback = pygame.image.load('Assets/moveboxes/coupback.png')
battleSelector = pygame.image.load('Assets/ui/battleSelector.png')
targetSelector = pygame.image.load('Assets/ui/targetSelector.png')
aitest = False
				
def hitDetect(p1, p2, p3, p4):
	if p2[0] > p3[0] and p1[0] < p4[0] and p2[1] > p3[1] and p1[1] < p4[1]:
		return True
	else:
		return False
		
def convertVel(input):
	
	radians = math.radians(input)
	x_vel = math.cos(radians)
	y_vel = math.sin(radians)
	velocity = (x_vel, y_vel)
	return velocity
	
class SpreetSheet(object):
	def __init__(self, img, row, colm):
		self.img = img
		self.image = pygame.image.load(self.img)
		self.row = row
		self.colm = colm
		self.animation = pyganim.PygAnimation(list(zip(pyganim.getImagesFromSpriteSheet(self.img, rows = self.row, cols = self.colm, rects = []),[100] * self.row * self.colm)))
		self.animation.play()
	def image_at(self, rectangle):
		rect = pygame.Rect(rectangle)
		
		image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
		image.blit(self.image, (0, 0), rect)
		return image
		
wekNums = SpreetSheet("Assets/ui/numbers/wekNum.png", 1, 10)
normNums = SpreetSheet("Assets/ui/numbers/normNum.png", 1, 10)
resistNums = SpreetSheet("Assets/ui/numbers/resistNum.png", 1, 10)
critOverlay = SpreetSheet("Assets/ui/numbers/critNum.png", 1, 10)

def getDamageImage(type, damage, crit):
	global wekNums
	global normNums
	global resistNums
	damList = []
	for i in str(damage):
		damList.append(i)
		
	numbox = pygame.Surface([len(damList) * 12, 25], pygame.SRCALPHA, 32).convert_alpha()
	if type == "wek":
		for i in damList:
			numbox.blit(wekNums.image_at([12 * int(damList[i-1]),0,12,25]), [damList.index(i) * 12, 0])
		
	elif type == "resist":
		for i in damList:
			numbox.blit(resistNums.image_at([12 * int(i),0,12,25]), [damList.index(i) * 12, 0])
		
	else:
		for i in damList:
			numbox.blit(normNums.image_at([12 * int(i),0,12,25]), [damList.index(i) * 12, 0])
			
			
	if crit:
		for i in damList:
			numbox.blit(critOverlay.image_at([12 * int(i),0,12,25]), [damList.index(i) * 12, 0])
	
	return numbox
		
	


log =[]				
timer = 0
printing = False			

		
messages = []
effectMessages = []
theMessage = ""
theEffectMessage = ""
damageImg = "null"
damage = 189
critical = False
damageImg = getDamageImage("norm", damage, critical)
def printc(text, battler, thesebattlers):
	global disptextc
	global printingc
	global logc
	global timerc
	
	newtextc = font.render(text,True,BLACK)
	logc.append(newtextc)

	
	disptextc = newtextc
	timerc = 90
	for i in range(timerc):
		gScreen.blit(disptextc, [thesebattlers[battler].x, thesebattlers[battler].y + 10])
		
def dispSkills(player):
	global lockedskill
	x = 0
	y = 0

	for i in player.skills:
		
		if x > 1:
			x = 0
			y += 1
		
		gScreen.blit(i.text, [330+ 6 + x*175, y*30 + 370 + 5 + size[1] - 500])
		if i.cost <= player.power:
			gScreen.blit(i.type.img, [330 + x*175, y*30 + 370 + size[1] - 500])
		
		else:
			gScreen.blit(lockedskill, [330 + x*175, y*30 + 370 + size[1] - 500])
		
		x += 1	
		
	pygame.draw.rect(gScreen, GREEN, [21,371 + size[0] - 500,player.hp / 278,28])
	pygame.draw.rect(gScreen, BLUE, [10, size[0] - 70, player.power * 2, 28])
	gScreen.blit(font.render("HP: " + str(player.hp), True, (0,0,255)), [75, 376 + size[1] - 500])
	gScreen.blit(font.render("Power: " + str(player.power), True, (255,255,255)), [75, 426 + size[1] - 500])
	gScreen.blit(font.render(player.name + "'s turn", True, (255,255,255)), [75, 476 + size[1] - 500])


class Type(object):
	def __init__(self, name, weks, strs):
		self.name = name
		self.weks = weks
		self.strs = strs
		self.img = pygame.image.load("assets/moveboxes/" + self.name.lower() +".png")

normal = Type("Normal", ["Tech", "Ghost"], ["nul"])
fire = Type("Fire", ["Water"], ["Earth"])
water = Type("Water", ["Air", "Electric", "Grass"], ["Fire"])
air = Type("Air", ["Earth", "Electric"], ["Water", "Fighting"])
earth = Type("Earth", ["Fire", "Grass", "Fighting", "Tech", "Astral"], ["Air", "Poison"])
dark = Type("Dark", ["Light"], ["Normal"])
light = Type("Light", ["Dark"], ["Normal"])
#-----------------------------------------
grass = Type("Grass", ["Fire","Ice", "Tech"], ["Water", "Earth"])
electic = Type("Electric", ["Earth"], ["Water", "Air"])
ice = Type("Fire", ["Fire", "Fighting"], ["Grass"])
fighting = Type("Fighting", ["Physic"], ["Normal"])
acid = Type("Acid", ["Earth", "Grass"], [""])
poison = Type("Poison", ["Dark"], ["Grass"])
blood = Type("Blood", ["Acid", "Poison"], ["Dark"])
ghost = Type("Ghost", ["Physic", "Magic"], ["Fighting", "Normal"])
magic = Type("Magic", ["Fighting", "Astral"], ["Chaos"])
astral = Type("Astral", ["Chaos"], ["Ghost", "Tech"])


physic = Type("Physic",["Normal", "astral"], ["Fighting"])
tech = Type("Tech", ["Electric", "Acid", "Astral"], ["Earth", "Chaos"])
unknown = Type("Unknown", ["none"], ["none"])
chaos = Type("Chaos", ["Tech"], ["Physic"])
minion = Type("Minion", ["none"], ["none"])


		
def ScrollSelect(player, char):
	while running:
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_down = True
						
			elif event.type == pygame.MOUSEBUTTONUP:
				mouse_down = False
	
		mouse_pos = pygame.mouse.get_pos()
		
		pygame.draw.rect(gScreen, GRAY, [0,0, size[0], size[1]])
		x = 0
		y = 0

		for i in player.scrolls:
			if x > 1:
				x = 0
				y += 1
			
			gScreen.blit(i.skill.text, [11 + x*175, y*30 + 10])
			gScreen.blit(i.skill.type.img, [5 + x*175, y*30 + 5])
			i.cords = [5 + x*175, y*30 + 5]
			
			x += 1
		for i in player.scrolls:
			if hitDetect(mouse_pos, mouse_pos, i.cords, [i.cords[0] + 165, i.cords[1] + 25]):
				if mouse_down:
					i.apply(char, player)
					mouse_down = False
	
class Equip(object):
	def __init__(self, name, str, int, con, mag, agil, crit, dodgeChance, lvl, slot):
		self.name = name
		self.str = str
		self.int = int
		self.con = con
		self.mag = mag
		self.agil = agil
		self.crit = crit
		self.dodgeChance = dodgeChance
		self.lvl = lvl
		self.slot = slot
		
emptySlot = Equip("Nothing", 0, 0, 0, 0, 0, 0, 0, 0, "")
				
class Effect(object):
	def __init__(self, effect):
		self.effect = effect
		self.endeffect = 0
		self.img = pygame.image.load("Assets/ui/effects/" + effect + ".png")
		self.canend = True
		self.damage = 0
		
	def apply(self, target):
		global effectMessages
		global theEffectMessage
		if self.effect == "burn":
			effectMessages.append(target.name + " is on fire!")
			target.effects.append(self.buildNew())
			
		if self.effect == "bleed":
			effectMessages.append(target.name + " is bleeding out!")
			target.effects.append(self.buildNew())
		
		if self.effect == "poison":
			effectMessages.append(target.name + " is poisoned!")
			target.effects.append(self.buildNew())
			
		if self.effect == "defend":
			target.con += target.basecon * target.basecon
			effectMessages.append(target.name + " is defending!")
			target.effects.append(self.buildNew())
			
		if self.effect == "forceshield":
			target.con += target.basecon * 3
			target.mag += target.basemag * 3
			effectMessages.append(target.name + " has a shield up!")
			target.effects.append(self.buildNew())
			
		if self.effect == "confusion":
			target.con -= target.basecon / 2
			target.mag -= target.basemag / 2
			effectMessages.append(target.name + " is confused!")
			target.effects.append(self.buildNew())
			
		if self.effect == "rebuff":
			target.str += target.basestr * 1.4
			target.int += target.baseint * 1.4
			effectMessages.append(target.name + " is encouraged!")
			target.effects.append(self.buildNew())
			
		if self.effect == "meditate":
			target.power += 1
			target.con -= 10
			target.mag += 5
			effectMessages.append(target.name + " is meditating!")
			target.effects.append(self.buildNew())
			
		if self.effect == "planAhead":
			planned = False
			for i in target.effects:
				if i.effect == "planAhead":
					i.endeffect, planned = 0, True
			if not planned:
				target.effects.append(self.buildNew())
				effectMessages.append(target.name + " is scheming!")
			else:
				effectMessages.append(target.name+" is perfecting their plans!")
			target.misc += 1
			print "planned: ", target.misc
			target.crit += 2
			target.modHitChance += 10
			target.int = target.int + (target.int / 5)
			target.str = target.str + (target.str / 5)
			
		if self.effect == "dodgeUp":
			target.dodgeChance += 25
			effectMessages.append(target.name + " is prepared!")
			target.effects.append(self.buildNew())
			
		if self.effect == "neverThere":
			target.dodgeChance += 100
			effectMessages.append(target.name + " dissapeared")
			target.effects.append(self.buildNew())
			
		if self.effect == "slowed":
			target.agil -= 5
			target.dodgeChance -= 10
			effectMessages.append(target.name + " is slowed!")
			target.effects.append(self.buildNew())
			
		if self.effect == "magicMute":
			effectMessages.append(target.name+" is Muted!")
			target.effects.append(self.buildNew())

		if self.effect == "passedOut":
			effectMessages.append(target.name+" passed out!")
			target.effects.append(self.buildNew())
			target.actions -= 5

		if self.effect == "mindSpiked":
			effectMessages.append(target.name+" has been mind spiked!")
			target.effects.append(self.buildNew())

		if self.effect == "disgusted":
			effectMessages.append(target.name+" is DISGUSTED")
			target.effects.append(self.buildNew())
			target.modHitChance -= 20
			target.dodgeChance -= 5

		if self.effect == "observing":
			effectMessages.append(target.name+" is observing.")
			target.effects.append(self.buildNew())

		if self.effect == "devidedefend":
			target.effects.append(self.buildNew())

		if self.effect == "vulnerable":
			target.effects.append(self.buildNew())
			effectMessages.append(target.name+" is vulnerable!")
			
		if self.effect == "spurred":
			target.effects.append(self.buildNew())
			effectMessages.append(target.name+" is onto something!")
			target.str *= 2
			target.int *= 2
			target.crit *= 2
			target.modHitChance += 10

		if self.effect == "stunned":
			effectMessages.append(target.name+" is Stunned!")
			target.effects.append(self.buildNew())
			target.actions -= 2

		if self.effect == "earthStage":
			target.effects.append(self.buildNew())
			target.con += 50
			target.mag += 50
			target.int -= 20
			target.str -= 20
			try:
				moonStagef.end(target)
			except:
				pass
			try:
				otherStagef.end(target)
			except:
				pass
				
		if self.effect == "moonStage":
			target.effects.append(self.buildNew())
			target.mag += 50
			target.int += 50
			target.str -= 25
			target.con -= 25
			try:
				earthStagef.end(target)
			except:
				pass
			try:
				otherStagef.end(target)
			except:
				pass
			
		if self.effect == "otherStage":
			target.effects.append(self.buildNew())
			target.int += 75
			target.crit += 10
			target.dodgeChance += 20
			target.con -= 50
			target.mag -= 50
			try:
				moonStagef.end(target)
			except:
				pass
			try:
				earthStagef.end(target)
			except:
				pass

			
	def end(self, target):
		target.effects.remove(self)
		if self.effect == "poison":
			effectMessages.append(target.name + " is no longer poisoned!")
			
		if self.effect == "bleed":
			effectMessages.append(target.name + " is no longer bleeding!")
		
		if self.effect == "burn":
			effectMessages.append(target.name + " is no longer on fire!")
		
		if self.effect == "defend":
			effectMessages.append(target.name + " is no longer defending!")
			target.con -= target.basecon * target.basecon
			
		if self.effect == "forceshield":
			target.con -= target.basecon * 3
			target.mag -= target.basemag * 3
			effectMessages.append(target.name + " no longer has a shield up!")
		
		if self.effect == "confusion":
			target.con += target.basecon / 2
			target.mag += target.basemag / 2
			effectMessages.append(target.name + " is no longer confused!")
		
		if self.effect == "rebuff":
			target.str -= target.basestr * 1.4
			target.int -= target.baseint * 1.4
			effectMessages.append(target.name + " is no longer encouraged. :(")
		
		if self.effect == "meditate":
			target.con += 10
			target.mag -= 5
			effectMessages.append(target.name + " is no longer meditating!")
		
		if self.effect == "planAhead":
			for i in range(target.misc):
				target.crit -= 2
				target.modHitChance -= 10
				target.int = target.int - (target.int / 5)
				target.str = target.str - (target.str / 5)
			target.misc = 0
			effectMessages.append(target.name + " is no longer scheming!")
		
		if self.effect == "dodgeUp":
			target.dodgeChance -= 25
			effectMessages.append(target.name + " is no longer prepared!")
		
		if self.effect == "neverThere":
			target.dodgeChance -= 100
			effectMessages.append(target.name + " reapeared!")
			
		if self.effect == "slowed":
			target.agil -= 5
			target.dodgeChance -= 10
			effectMessages.append(target.name + " is no longer slowed!")

		if self.effect == "passedOut":
			effectMessages.append(target.name + " is no longer passed out!")
			target.actions += 5

		if self.effect == "mindSpiked":
			effectMessages.append(target.name + " is no longer mind spiked!")

		if self.effect == "disgusted":
			effectMessages.append(target.name+" has overcome their disgust!")
			target.modHitChance += 20
			target.dodgeChance += 5

		if self.effect == "observing":
			effectMessages.append(target.name + " is no longer observing!")
			
		if self.effect == "vulnerable":
			effectMessages.append(target.name + " has overcome their vulnerability!")
			
		if self.effect == "spurred":
			effectMessages.append(target.name+" has lost the glint in their eye.")
			target.str /= 2
			target.int /= 2
			target.crit /= 2
			target.modHitChance -= 10

		if self.effect == "stunned":
			effectMessages.append(target.name+" is no longer stunned.")
		
	def update(self, target):
		if self.effect == "magicMute":
			target.power -= 1
			effectMessages.append(target.name+"'s power was Muted!")
			if self.endeffect == 1:
				self.end(target)
			self.endeffect += 1
		
		if self.effect == "burn":
			self.damage = 25 + random.randint(1, 25)
			self.endeffect = random.randint(1,3)
			target.hp -= self.damage
			effectMessages.append(target.name + " is on fire!   " + target.name + " takes " + str(self.damage) + " damage")
			if self.endeffect == 2 and self.canend:
				effectMessages.append(target.name + " put out the fire!")
				self.end(target)
				
		if self.effect == "bleed":
			damage = target.hp / 4
			target.hp -= damage
			effectMessages.append(target.name + " is on bleeding out!   " + target.name + " takes " + str(damage) + " damage")
			self.endeffect = random.randint(1,3)
			if self.endeffect == 2:
				effectMessages.append(target.name + " is no longer bleeding")
				self.end(target)

		if self.effect == "defend":
			self.endeffect += 1
			if self.endeffect == 2:
				self.end(target)
				
		if self.effect == "forceshield":
			self.endeffect = random.randint(1,2)
			if self.endeffect == 2:
				self.end(target)
				
		if self.effect == "confusion":
			self.endeffect = random.randint(1,2)
			if self.endeffect == 2:
				self.end(target)
				
		if self.effect == "poison":
			damage = target.hp / 10
			target.hp -= damage
			effectMessages.append(target.name + " is poisoned!   " + target.name + " takes " + str(damage) + " damage")
			self.endeffect = random.randint(1,4)
			if self.endeffect == 2:
				self.end(target)
				
		if self.effect == "rebuff":
			if self.endeffect >= 1:
				self.end(target)
			self.endeffect += 1
			
		if self.effect == "meditate":
			if magicMute in target.effects:
				effectMessages.append(target.name + "'s Meditate was Muted!")
			else:
				effectMessages.append(target.name + " is Meditating.")
				target.power += 1
			if self.endeffect == 3:
				self.end(target)
			self.endeffect += 1
				
		if self.effect == "planAhead":
			if self.endeffect == 1:
				self.end(target)
			self.endeffect += 1
		
		if self.effect == "dodgeUp":
			
			if self.endeffect == 1:
				self.end(target)
			self.endeffect += 1
			
		
				
		if self.effect == "guarded":
			effectMessages.append(target.name + " is being guarded by " + target.guarder.name + "!")
			if self.endeffect == 1:
				effectMessages.append(target.name + " is no longer being guarded by " + target.guarder.name + "!")
				target.guarder = "nul"
				self.end(target)
			self.endeffect += 1	
			
		if self.effect == "neverThere":
			self.endeffect = random.randint(1,3)
			if self.endeffect == 1:
				self.end(target)

		if self.effect == "slowed":
			self.endeffect = random.randint(1,3)
			if self.endeffect == 1:
				self.end(target)
				
		if self.effect == "passedOut":
			self.endeffect = random.randint(1,2)
			if self.endeffect == 1:
				self.end(target)
		if self.effect == "mindSpike":
			self.endeffect = random.randint(1,3)
			if self.endeffect == 1:
				self.end(target)
		
		if self.effect == "death":
			pass
			#Death stufff here

		if self.effect == "disgusted":
			self.endeffect = random.randint(1, 3)
			if self.endeffect == 1:
				self.end(target)

		if self.effect == "observing":
			if self.endeffect == 1:
				self.end(target)
			self.endeffect += 1
			
		if self.effect == "devidedefend":
			if self.endeffect == 1:
				self.end(target)
			self.endeffect += 1

		if self.effect == "vulnerable":
			self.endeffect = random.randint(1, 5)
			if self.endeffect <= 4:
				self.end(target)
				
		if self.effect == "spurred":
			if self.endeffect == 1:
				self.end(target)
			self.endeffect += 1

		if self.effect == "stunned":
			target.actions += 1
			if self.endeffect == 1:
				self.end(target)
			self.endeffect += 1

	def resetStats(self, target):
		target.con = target.basecon
		target.mag = target.basemag
		target.str = target.basestr
		target.int = target.baseint
		target.crit = target.basecrit
		target.dodgeChance = target.basedodgeChance
		target.agil = target.baseagil
			
	def buildNew(self):
		neweff = Effect(self.effect)
		return neweff
				
burn = Effect("burn")
magicmute = Effect("magicMute")
defense = Effect("defend")
bleed = Effect("bleed")
forceshield = Effect("forceShield")
confusion = Effect("confusion")
immortal = Effect("immortal")
block = Effect("block")
poisoned = Effect("poison")
rebuff = Effect("rebuff")
meditatef = Effect("meditate")
planAheadf = Effect("planAhead")
dodgeUp = Effect("dodgeUp")
death = Effect("death")
earthStagef = Effect("earthStage")
otherStagef = Effect("otherStage")
moonStagef = Effect("moonStage")
guarded = Effect("guarded")
passedOut = Effect("passedOut")
neverTheref = Effect("neverThere")
slowed = Effect("slowed")
mindSpiked = Effect("mindSpiked")
disgusted = Effect("disgusted")
observing = Effect("observing")
devidedefend = Effect("devidedefend")
vulnerable = Effect("vulnerable")
spurred = Effect("spurred")
stunned = Effect("stunned")

negeff = [burn, magicmute, bleed, poisoned, confusion, disgusted, mindSpiked, slowed, passedOut, vulnerable]
poseff = [defense, forceshield, immortal, block, rebuff, meditatef, planAheadf, dodgeUp, earthStagef, otherStagef, moonStagef, observing, devidedefend, spurred]


class Skill(object):
	def __init__(self, name, type, phys, atk, var, spd, crit, hitChance, cost, effects, spec):
		self.name = name
		self.type = type
		self.atk = atk
		self.var = var
		self.spd = spd
		self.phys = phys
		self.cost = cost
		self.spec = spec
		self.crit = crit
		
		self.hitChance = hitChance
		self.effects = effects
		self.text = font.render(name, True, WHITE)
		self.desc = ""
		self.uses = 1
		self.damageImg = "null"
		
		
	def use(self, user, target, battlers1, battlers2, thesebattlers):
		global theMessage
		global messages
		global damageImg
		damage = 0
		
		theMessage = ""
		targetmultiplier = 1 + ((target.lvl - 1) / 10)
		usermultiplier = 1 + ((user.lvl - 1) / 10)
		message = ""
		effective = 0
		critical = False
		damageImg = getDamageImage("norm", damage, critical)
		
		hit = (self.hitChance + user.modHitChance) - ((target.dodgeChance + target.equipDodgeChance) * targetmultiplier)
		
		if guarded in target.effects:
			target = target.guarder

		if target.ability == "Cuteness":
			hit -= 25
		if user.ability == "Blood hunt":
			hit += 25
		if user.ability == "Frenzy" and user.hp <= user.maxhp/5:
			hit += 2
		if observing in target.effects:
			user.marks += 1
		if user.name in ["Battle Drone"]:
			if user.misc != 0:
				if user.misc == target:
					hit *= 2
				else:
					hit *= 0.6

		if random.randint(1,100) < hit or "trueHit" in self.spec:
			critical, effective = False, 0

			if self.phys:
				damage = (user.str + user.equipStr + self.atk+ random.randint(0, self.var)) * usermultiplier - (target.con + target.equipCon) * targetmultiplier
			else:
				damage = (user.int + user.equipInt + self.atk + random.randint(0, self.var)) * usermultiplier  - (target.mag + target.equipMag) * targetmultiplier
				
			for i in target.types:
				if self.type.name in i.weks:
					message = " It's super effective!"
					effective = 1
			for i in target.types:
				if self.type.name in i.strs:
					damage /= 2
					message = " It's not very effective!"
					effective = -1
			
			#apply lock-on boost
			if user.name in ["Battle Drone"]:
				if user.misc != 0:
					if user.misc == target:
						user.crit *= 2
					else:
						user.crit *= 0.6
					
			if random.randint(1,30) + (user.crit * usermultiplier) + user.equipCrit > 30:
				if effective == 1:
					message += " CRITICAL HIT!"
				else:
					message = "CRITICAL HIT!"
				critical = True
				if not len(self.effects) == 0:
					self.effects[1].apply(target)
			
			#remove lock-on boost
			if user.name in ["Battle Drone"]:
				if user.misc != 0:
					if user.misc == target:
						user.crit /= 2
					else:
						user.crit /= 0.6
					
			if target.ability == "Creepus":
				user.marks += 1
				if critical:
					user.marks += 1
			
			for i in self.spec:
				if i == "coup":
					self.uses = 0
				if i == "vampire":
					user.hp += damage
					if critical:
						user.hp += math.floor(damage/10)
				if i == "defend":
					damage = 0
					defense.apply(user)
				if i == "powerUp":
					damage = 0
					if magicMute in user.effects:
						theMessage += user.name+"'s power was Muted!"
					else:
						user.power += 2
				if i == "lifepact":
					damage = user.hp / 2 + user.int
					user.hp /=2
				if i == "fullmana":
					damage = ((user.power * (user.int + self.atk)) / 8)
					user.power = 0
				if i == "shroud":
					user.con += 6
					user.mag += 6
				if i == "Shield":
					forceshield.apply(user)
				if i == "atkUp":
					damage = 0
					planAheadf.apply(user)
				if i == "division":
					damage = target.maxhp/5
					if critical:
						damage += target.maxhp/10
				if i == "immortal":
					immortal.apply(user)
				if i == "heal":
					damage = 0
					target.hp += 100
					if target.ability == "3 worlds":
						target.hp -= user.int * 2
					if critical:
						target.hp += user.int
				if i == "block":
					damage = 0
					block.apply(user)
				if i == "observing":
					observing.apply(user)
				if i == "powerdrain":
					damage = 0
					if magicMute in user.effects:
						theMessage += user.name+"'s Power drain was Muted!"
						user.power += math.floor(target.power/5)
					else:
						user.power += target.power
					target.power = 0
				if i == "revenge":
					damage = user.maxhp - user.hp
				if i == "recover":
					damage = 0
					heal = target.maxhp / 4 
					if target.ability == "3 worlds":
						heal /= 3
					target.hp += heal
					if critical:
						target.hp += math.floor(heal/5)
				if i == "stare":
					target.con /=2
					target.mag /=2
				if i == "mark":
					target.marks += 1
					if critical:
						target.marks += 1
				if i == "creepyAtk":
					temp = target.mag
					if temp <= 0:
						temp = (-1)/(-1 + temp)
						print "Detected devision by 0. Modding to: "+str(temp)
					damage = math.floor((user.int * (1.08 ** target.marks))/target.mag)
				if i == "endeffect":
					user.effects = []
				if i == "removeEff":
					for j in target.effects:
						if j in negeff:
							j.end(target)
				if i == "removeUff":
					target.con = target.basecon
					target.mag = target.basemag
					target.int = target.baseint
					target.str = target.basestr
					target.crit = target.basecrit
					target.agil = target.baseagil
				if i == "lifeTransfer":
					user.hp -= user.hp/4
					target.hp += (user.hp/4) * 2
					if critical:
						target.hp += math.floor(user.hp/5)
				if i == "powerTransfer":
					transfered = user.power
					if critical:
						transfered += 1
					if magicMute in target.effects:
						theMessage += user.name+"'s Transfer was Muted!"
						transfered = math.floor(transfered/5)
					target.power += transfered
					user.power -= user.power
					theMessage += user.name + " transfered "+str(transfered)+" power to "+target.name
				if i == "meditate":
					meditatef.apply(user)
				if i == "dodgeUp":
					dodgeUp.apply(user)
				if i == "otherStage":
					otherStagef.apply(user)
				if i == "earthStage":
					earthStagef.apply(user)
				if i == "moonStage":
					moonStagef.apply(user)
				'''if i == "againstOdds":
					if user in player1.battlers:
						for b in player2.battlers:
							damage += b.hp / 10
						for c in player1.battlers:
							damage += (c.maxhp - c.hp) / 6
					if user in player2.battlers:
						for b in player1.battlers:
							damage += b.hp / 10
						for c in player2.battlers:
							damage += (c.maxhp - c.hp) / 6
					damage += target.hp / 6
					damage = math.floor(damage) - target.con'''
				if i == "takeBlow":
					target.guarder = user
					guarded.apply(target)
				if i == "mindReading":
					user.dodgeChance += 5
					if critical:
						user.dodgeChance += 1

				if i == "neverThere":
					neverTheref.apply(user)
				
				if "create" in i:
					spawned = ""
					if "Creep" in i:
						spawned = miniCreep.buildNew()
					if "Worship" in i:
						spawned = Worshipper.buildNew()
					if "Cubes" in i:
						spawned = Cubes.buildNew()
					if "drone" in i:
						spawned = battleDrone.buildNew()
					#Be sure spawned is valid!
					if spawned != "":
						if user.isAi:
							spawned.isAi = True
						if user in battlers1:
							Left = True
							rand1 = battlers1
						else:
							Left = False
							rand1 = battlers2

						for x in range(3):
							rand, succeded = x*75 + 325, True
							for y in rand1:
								if rand == y.basey:
									succeded = False
							if succeded:
								spawned.basey = rand
								if Left:
									spawned.basex = 50
									battlers1.append(spawned)
								else:
									spawned.basex = size[0] - 100
									battlers2.append(spawned)
								thesebattlers.append(spawned)
								break

				if i == "mindSpike":
					mindSpiked.apply(target)

				if i == "obsBoost":
					damage = math.floor(damage * (1.01 ** target.marks))

				if i == "vulnerable":
					vulnerable.apply(user)
				if i == "charge":
					defense.apply(user)
					user.power += 3
				if i == "conPierce":
					damage += target.con
				if i == "magPierce":
					damage += target.mag
				if i == "lockOn":
					user.misc = target
					theMessage += user.name + " has Locked onto " + target.name + "!"
				if i == "spur":
					spurred.apply(user)
				if i == "overclock":
					target.actions += 1
					if critical:
						target.actions += 1
					theMessage += target.name + " has been OVERCLOCKED"

			if user.ability == "Frenzy" and user.hp <= user.maxhp/5:
				damage = math.floor(damage * 1.25)
						
			if user.hp > 0:
				if target.ability == "3 worlds":
					damage /= 3
				
				if effective == 1:
					damage *= 2
				if critical:
					damage *= 2

				for i in target.effects:
					if i == devidedefend:
						damage -= math.floor(damage/5)
					if i == vulnerable:
						damage += math.ceil(damage/10)
				damage = int(round(damage, 0))
				print damage
				if damage < 0 or "nodam" in self.spec:
					damage = 0

					theMessage += user.name + " deals no damage to " + target.name + " using " + self.name + message 
				else:
					theMessage += user.name + " uses " + self.name + " and deals " + str(damage) + " damage to " + target.name + message

				if mindSpiked in user.effects:
					theMessage += user.name + " is mind spiked!"
					theMessage += "The mind spike dealt " + str(damage) + " back to " + user.name
					user.hp = user.hp * usermultiplier - damage
					
				if not len(self.effects) == 0:
					if random.randint(1,self.effects[0]) == 1:
						self.effects[1].apply(target)
					
				target.hp = target.hp * targetmultiplier - damage
				
		else:
			damage = 0
			theMessage += user.name + " missed!"
			
		messages.append(theMessage)
		if effective == 1:
			damageImg = getDamageImage("wek", damage, critical)
		elif effective == 0:
			damageImg = getDamageImage("norm", damage, critical)
		elif effective == -1:
			damageImg = getDamageImage("resist", damage, critical)
		else:
			damageImg = getDamageImage("norm", damage, critical)
		self.damageImg = damageImg
		#print damageImg
				
#Skill("", normal, True, 0, 0, 0, 0, 100, 0, [], [""])
#def __init__(self, name, type, phys, atk, var, spd, crit, hitChance, cost, effects, spec):

nothing = Skill("nothing", normal, True, 0, 0, 0, 0, 100, 0, [], ["nodam", "trueHit"])
nothing.desc = ""
basicAtk = Skill("Basic Attack", normal, True, 5, 5, 1, 0,90, 0, [], [""])
basicAtk.desc = "A basic attack, like using a weapon or claws."
fireBall = Skill("Fire ball", fire, False, 7, 3, -1, 0,90, 2, [1, burn], [""])
fireBall.desc = "Summons a small fireball, chance to cause burn."
waterSpout = Skill("Water Spout", water, False, 2, 10, -1, 0,90, 2, [], [""])
waterSpout.desc = "Creates a fountain of water."
airBlast = Skill("Air Blast", air, False, 7, 1, 2, 0,95, 2, [], [""])
airBlast.desc = "A strong blast of air pushes foes away"
earthShot = Skill("Earth Shot", earth, False, 12, 4, -5, 0,90, 2, [], [""])
earthShot.desc = "Magical rock throwing."
axeLegs = Skill("Axe Legs", fighting, True, 65, 25, 7, 2, 99, 0, [], [""])
axeLegs.desc = "Strong axe blades click into place before spinning rapidly, quickly removing your foe's limbs."
defend = Skill("Defend", normal, True, 0, 0, 0, 0,100, 0, [], ["defend", "trueHit"])
defend.desc = "Brace yourself against incomming physical damage."
scar = Skill("Scar", dark, True, 30, 5, 2, 0,97, 1, [3,bleed], ["vampire"])
scar.desc = "Mangle your foe's flesh and steal a bit of their life, can cause horrible bleeding."
nuke = Skill("Nuke", fire, True, 200, 100, -4, 0,100, 20, [], ["trueHit", "hitAll"])
nuke.desc = "Drops a nuke on all foes, dealing heavy damage."
shardSwarm = Skill("Shard Swarm", chaos, False, 20, 30, 4, 0,90, 10, [], [""])
shardSwarm.desc = "Summons a swarm of sharp energy shards to slice up your foes."
magicMute = Skill("Magic Mute", chaos, False, 0, 0, -2, 0,100, 5, [1,magicmute], ["trueHit"])
magicMute.desc = "Prevents opponents from gaining power."

powerUp = Skill("Power Up", chaos, False, 0, 0, 10, 0,100, 2, [], ["powerup", "trueHit"])
powerUp.desc = "Builds power by absorbing choatic energy."

destroy = Skill("Destroy", chaos, False, 100, 100, -100, 15,100, 7, [], [""])
destroy.desc = "Destroys absolutely everything, but takes a long time to cast."
vampire = Skill("Vampire", blood, False, 20, 10, 5, 20,90, 2, [], ["vampire", "vampire"])
vampire.desc = "Drains the blood of your foes to heal yourself."
meteorStorm = Skill("Meteor Storm", astral, False, 100, 50, -100, 0,75, 7, [2, burn], [""])
meteorStorm.desc = "Calls down a meteor storm to crush opponents, can cause burns."
block = Skill("Block", fighting, True, 0, 0, 10, 0,100, 1, [], ["block", "trueHit"])
block.desc = "Prevents incomming physical damage."
powerDrain = Skill("Power Drain", astral, False, 25, 25, -10, 0,100, 2, [], ["powerdrain", "trueHit"])
powerDrain.desc = "Drains power from opponents to use for yourself."
#-----------------------------------------------------------
tangle = Skill("Tangle", grass, True, 4, 5, 0, 7, 100, 1, [1, slowed], [""])
tangle.desc = "Tangles foes within a strong vine."
#-----------------------------------------------------------
slash = Skill("Slash", normal, True, 11, 10, 3, 5,90, 0, [], [""])
slash.desc = "Splice up foes with a sword or claw."
bite = Skill("Bite", normal, True, 10, 5, 0, 5, 92, 0, [4,bleed], [""])
bite.desc = "Take a large bite out of your foe, has a chance of causeing bleeding."
kick = Skill("Kick", fighting, True, 20, 5, 4, 0, 70, 1, [], [""])
kick.desc = "Kick your foes in the face!"
dodge = Skill("Dodge", fighting, True, 0, 0, 10, 10, 100, 2, [], ["trueHit", "dodgeUp"])
dodge.desc = "Prepare yourself to dodge the next attack."
rip = Skill("Rip", dark, True, 20, 15, -1, 0,90, 3, [1,bleed], [""])
rip.desc = "Rip your foes to shreds and cause heavy bleeding"
consumeFlesh = Skill("Consume Flesh", blood, True, 30, 8, -5, 0,90, 3, [2,bleed], ["vampire"])
consumeFlesh.desc = "Eat some of the foe's flesh that you ripped off. Has a chance to cause bleeding."
#----------------------------------------------------------------
chaosBolt = Skill("Chaos Bolt", chaos, False, 10, 20, 1, 0,90, 1, [], [""])
chaosBolt.desc = "Cause a bolt of chaotic energy to bounce between foes, searing the flesh."
setFire = Skill("Set Fire", fire, False, 5, 20, -1, 0,90, 3, [1,burn], ["hitAll"])
setFire.desc = "Watch them all burn to ashes."
forceShield = Skill("Force Shield", magic, False, 0, 0, -2, 0,100, 2, [], ["shield", "nodam", "trueHit"])
forceShield.desc = "Put up a shield of energy to block incomming damage."

chaosBeam = Skill("Chaos Beam", chaos, False, 20, 20, -10, 0,94, 0, [], ["fullmana"])
chaosBeam.desc = "Convert all of your power into choatic energy then blast it at your foe."
meditate = Skill("Meditate", magic, False, 0, 0, 0, 0,100, 0, [], ["nodam", "trueHit", "meditate"])
meditate.desc = "Gain power through inner focus."
lifePact = Skill("Life Pact", blood, False, 0, 0, -2, 0,100, 4, [], ["lifepact", "trueHit"])
lifePact.desc = "Make a pact with your foe, if you take damage, so do they."
shroud = Skill("Shroud", dark, False, 0, 0, 10, 0,100, 2, [], ["shroud", "trueHit"])
shroud.desc = "Shroud yourself in darkness to avoid getting hit."
#-------------------------------------------------------------------
bludgeon = Skill("Bludgeon", fighting, True, 10, 2, -1, 0,90, 0, [], [""])
bludgeon.desc = "Bash your foe's brains in with a blunt weapon."
stab = Skill("Stab", fighting, True, 5, 7, 2, 0,100, 0, [], [""])
stab.desc = "Stab Stab Stab!"
confuse = Skill("Confuse", physic, False, 0, 0, 10, 0,80, 2, [1,confusion], [""])
confuse.desc = "Confuse your foe to lower their damage and defenses."

planAhead = Skill("Plan Ahead", tech, False, 0, 0, -10, 0,100, 0, [], ["atkUp", "trueHit"])
planAhead.desc = "Focus on planning your next move, immporving its weak points."
erase =Skill("Erase", unknown, False, 0, 0, -10, 0,100, 5, [], ["division"])
erase.desc = "Use the magic of the pencil to erase foes from existance."
create = Skill("Create", unknown, False, 0, 0, -10, 0,100, 0, [], ["createCreep", "trueHit"])
create.desc = "Create a creep"
create2 = Skill("Create", unknown, False, 0, 0, -10, 0,100, 0, [], ["createWorship", "trueHit"])
create2.desc = "Create a worshiper to worship you, giving you power."
create3 = Skill("Create", unknown, False, 0, 0, -10, 0,100, 0, [], ["createCubes", "trueHit"])
create3.desc = "Clone more CUBES!"
createdrone = Skill("Create", unknown, False, 0, 0, -10, 0,100, 5, [], ["createdrone", "trueHit"])
createdrone.desc = "Clone more Battle Drones!"
mend = Skill("Mend", magic, False, 0,0, 1, 0,100, 3, [], ["heal", "trueHit"])
mend.desc = "Heal yourself or an ally."
#------------------------------------------------------------------
zap = Skill("Lightning", electic, False, 5, 10, 3, 4, 100, 0, [], [""])
zap.desc = "A stray electron zaps your foe."
energiBeam = Skill("Energy Beam", tech, False, 77, 10, -3, 0,90, 5, [], [""])
energiBeam.desc = "A strong electronic beam fries foes."
wellspring = Skill("Wellspring", tech, False, 0, 0, 3, 0,100, -10, [], ["trueHit"])
wellspring.desc = "Generate power through technology."
#-----------------------------------------------------------------
bladeFlash = Skill("Blade Flash", fighting, True, 6, 5, 10, 2,90, 1, [], [""])
bladeFlash.desc = "Quick draw your sword, cutting into your foe before anyone else can act."
cleave = Skill("Cleave", fighting, True, 20, 20, -2, 2,90, 2, [2, bleed], [""])
cleave.desc = "Bring back your blade for a heavy blow, can cause bleeding."
revenge = Skill("Revenge", dark, False, 0, 0, 10, 0,100, 5, [], ["revenge"])
revenge.desc = "All the rage you have against your foes is released in a fury of blows."
#----------------------------------------------------------------------
obsidianBlast = Skill("Obsidian Blast", fire, False, 30, 10, -3, 0,90, 5, [1, burn] ,[""])
obsidianBlast.desc = "Create burnning obsidian shards to burn your foe."
recover = Skill("Recover", magic, False, 0, 0, 10, 0,100, 7, [], ["recover", "endeffect", "trueHit"])
recover.desc = "Recover lost energy, ending all negative effects and healing yourself."
psionicRadiance = Skill("Psionic Radiance", physic, False, 47, 10, -2, 3,100, 3, [], [""])
psionicRadiance.desc = "Use the power of physic energy to cause horrible headaches."
#--Creepus
stare = Skill("Stare", physic, False, 30, 10, -2, 15,100, 3, [], [""])
stare.desc = "Jiiiiiiiiiiiiiiiiii"
blink = Skill("Blink", physic, True, 5, 5, 1, 0,100, 0, [], ["mark"])
blink.desc = "Blink Blink"
creepyAtk = Skill("Creep Attack", physic, False, 5, 5, 1, 0,90, 0, [], ["creepyAtk"])
creepyAtk.desc = "Use all the knowledge you have about your enemy to find their weakest point."
observeDefend = Skill("Observational Defence", fighting, True, 0, 0, 4, 3, 0, 1, [], ["observing", "observing", "nodam", "trueHit", "defend"])
observeDefend.desc = "Defend with the intent of observation in mind."
inhale = Skill("Inhale", air, False, 0, 0, 3, 0, 100, 2, [], ["defend", "heal", "trueHit", "observing", "removeEff"])
inhale.desc = "Inhale to absorb some healthy particles, healing yourself and defending."
observe = Skill("Observe", unknown, False, 0, 0, 3, 2, 100, 1, [], ["mark", "mark", "mark", "mark", "mark", "mark", "nodam", "trueHit"])
observe.desc = "Watch your foe to learn about them."
exhale = Skill("Exhale", air, False, 5, 10, 3, 0, 85, 0, [], ["mark", "hitAll"])
exhale.desc = "Breath out to cause minor damage to all foes."
#--Other creepus
induceDisgust = Skill("Induce Disgust", acid, False, 0, 2, 3, 3, 95, 2, [1, disgusted], ["nodam"])
induceDisgust.desc = "Disgust your enemy so much they can't even look in your direction."
sneezeFire = Skill("Sneeze Fire", fire, False, 18, 6, 3, 3, 110, 4, [1, burn], ["hitall", "obsBoost"])
sneezeFire.desc = "Sneeze a burst of flames to engulf all opponents."
sneeze = Skill("Sneeze", acid, False, 14, 6, 6, 0, 90, 1, [2, poisoned], [""])
sneeze.desc = "Sneeze to cause minor damage and chance of poison."
loudspeaker = Skill("Loudspeaker", air, False, 2, 2, 5, 18, 92, 1, [], [""])
loudspeaker.desc = "Blast your opponent with your Booming voice."
gristlyDefend = Skill("Gristly Defence", earth, True, 0, 0, 6, 0, 0, 1, [], ["defence", "devidedefend", "trueHit", "nodam"])
gristlyDefend.desc = "Defend with your beard, greatly reducing incoming damage"
growBeard = Skill("Grow Beard", earth, True, 0, 0, 4, 0, 0, 4, [], ["removeEff", "nodam", "truehit", "heal"])
growBeard.desc = "Grow out your beard and refresh yourself, removing negative effects and healing."
extendWhiskers = Skill("Extend Whiskers", earth, True, 0, 0, 2, 0, 0, 1, [], ["vulnerable", "mark", "mark", "mark", "mark", "mark", "mark", "mark", "mark", "trueHit", "nodam"])
extendWhiskers.desc = "Gather extensive knowledge of your target, but leave yourself vulnerable to attacks."
onionBreath = Skill("Onion Breath Offence", poison, True, 30, 4, 3, 12, 95, 4, [1, poisoned], [""])
onionBreath.desc = "Exhale with extreme stench, poisoning your opponent."
mustacheMuscles = Skill("Mustache Muscles", fighting, True, 30, 6, 1, 10, 90, 4, [], ["obsBoost"])
mustacheMuscles.desc = "Use your facial hair to attack your opponent."

eggon = Skill("Egg On", normal, True, 0, 0, 10, 10, 100, 2, [1, rebuff], ["trueHit", "nodam"])
eggon.desc = "Cheer on yourself or your friends to increase damage and hit chance."
rebuke = Skill("Rebuke", normal, True, 0, 0, 10, 2, 100, 1, [], ["removeEff", "trueHit", "nodam"])
rebuke.desc = "Cheer on your friends to remove all their negative effects."

blast = Skill("Blast", tech, False, 20, 20, 5, 8, 95, 2, [2, burn], [""])
blast.desc = "Fire a bolt of energy into your foes. Can cause burns."
fission = Skill("Fission", fire, False, 20, 40, -1, 0, 90, 0, [2, burn], ["powerDown", "fullmana"])
fission.desc = "Break appart nearby atoms to cause major damage."
fusion = Skill("Fusion", fire, False, 1, 40, -1, 0, 100, 1, [2,burn], ["powerUp"])
fusion.desc = "Collect nearby atoms from foes in order to gain power and cause burns."

lifeTransfer = Skill("Life Transfer", blood, False, 0, 0, 10, 0,100, 2, [], ["lifeTransfer", "nodam"])
lifeTransfer.desc = "Transfer some life force to an ally."
powerTransfer = Skill("Power Transfer", tech, False, 0, 0, 10, 0, 100, 0, [], ["powerTransfer", "nodam", "trueHit"])
powerTransfer.desc = "Transfer some power to an ally."

earthStage = Skill("Earth Stage", astral, False, 10, 15, 10, 0, 100, 0, [], ["trueHit","hitAll","earthStage"])
earthStage.desc = ""
moonStage = Skill("Moon Stage", astral, False, 10, 15, 10, 0, 100, 0, [], ["trueHit","hitAll","moonStage"])
moonStage.desc = ""
otherStage = Skill("Otherworld Stage", astral, False, 10, 15, 10, 0, 100, 0, [], ["trueHit","hitAll","otherStage"])
otherStage.desc = ""
voidSnap = Skill("Void Snap", astral, False, 30, 10, 4, 5, 97, 1, [2,bleed], [""])
voidSnap.desc = "Open a hole in the fabric of reality to cause damage. May cause bleeding."
chains = Skill("Chains", normal, True, 30, 2, 1, 5, 90, 1, [], [""])
chains.desc = "Whip foes with chains."
earthenVortex = Skill("Earthen Vortex", earth, False, 30, 40, 5, 6, 90, 2, [2, slowed], ["hitAll"])
earthenVortex.desc = "Cause a vortex of earthen energy."
astralVortex = Skill("Astral Vortex", astral, False, 50, 40, 5, 6, 90, 3, [], ["hitAll"])
astralVortex.desc = "Cause a vortex of astral energy."
chaosVortex = Skill("Chaos Vortex", chaos, False, 20, 60, 5, 6, 90, 2, [], ["hitAll"])
chaosVortex.desc = "Cause a vortex of chaotic energy."

againstOdds = Skill("Against The Odds", light, True, 0, 10, 3, 13, 90, 7, [], ["againstOdds"])
againstOdds.desc = "Perservere against the odds stacked against you."
takeBlow = Skill("Take The Blow", fighting, True, 0, 0, 12, 10, 100, 1, [], ["takeBlow", "trueHit", "nodam"])
takeBlow.desc = "Jump in to take a blow for an ally."
powerStrike = Skill("Power Strike", fighting, True, 75, 10, -1, 0, 40, 1, [], [""])
powerStrike.desc = "Put all of your strength into one attack. Has a low chance of hitting."
antiPhysic = Skill("Anti Physic", unknown, False, 30, 20, 5, 15, 90, 2, [], [""])
mindReading = Skill("Mind Reading", physic, False, 20, 20, 5, 2, 100, 2, [], ["mindReading"])
mindReading.desc = "Read your foes mind to gain knowledge about their next attack."
neverThere = Skill("Never There", physic, False, 0,0, 20, 0, 100, 2, [], ["trueHit", "neverThere"])
neverThere.desc = "You were never there in the first place."
colorfulBullet = Skill("colorfulBullet", magic, False, 10,5, 1, 2, 90, 0, [], [""])
colorfulBullet.desc = "Summon a few bullets of magic energy to injure your foes."
never = Skill("And Never Come Back", unknown, False, 200, 50, 20, 5, 100, 7, [], ["trueHit"])
never.desc = "Never. Come. Back."
mindDisk = Skill("Mind disk", physic, False, 20, 10, 4, 5, 100, 0, [2, slowed], ["dodgeUp"])
mindDisk.desc = "Thow a mind disk at a foe to slow them. Increases your dodge chance."
daggerStorm = Skill("Dagger Storm", light, True, 40, 50, 10, 7, 99, 3, [], ["hitAll"])
daggerStorm.desc = "Summon a swarm of daggers to shred your foes."
eldritchAppuratus = Skill("Eldritch Appuratus", tech, False, 0, 0, 3, 2, 100, 3, [], ["powerUp", "recover"])
windSlash = Skill("Wind Slash", air, False, 20, 10, 5, 3, 90, 1, [], [""])
windSlash.desc = "Slash so fast, your opponents will not even know what hit them."
rejuvinate = Skill("rejuvinate", magic, False, 0,0, 5, 3, 100, 4, [], ["recover", "recover"])
rejuvinate.desc = "Heal yourself alot."
mindSpike = Skill("Mind Spike", physic, False, 0,0, 5, 3, 100, 3, [], ["mindSpike", "nodam"])
mindSpike.desc = "Make them pay for hurting you or your friends."
#--Forest--
leafStorm = Skill("Leaf Storm", grass, False, 20, 15, 8, 4, 90, 1, [],["hitAll"])
leafStorm.desc = "Send a swarm of leafs through your foe"
spores = Skill("Spores", poison, False, 5, 5, 2, 3, 90, 1, [1,poisoned], [""])
spores.desc = "Use deadly spores to poison your foe."
absorb = Skill("Absorb", grass, False, 20, 20, 5, 3, 90, 1, [], ["vampire"])
absorb.desc = "Absorb some your foe's life force."
#--Type basics
sandStorm = Skill("Sandstorm", earth, False, 10, 20, 5, 3, 90, 1, [], ["hitAll"])
sandStorm.desc = "Send out a sandstorm to blind your foes."
iceShard = Skill("Ice Shard", ice, False, 15, 15, 5, 6, 90, 1, [2, slowed], [""])
iceShard.desc = "Shoot a shard of ice to impale your foe. May cause slowness"
basicEarth = Skill("Earthy attack", earth, True, 5, 5, 1, 0, 90, 0, [], [""])

diveBomb = Skill("Dive Bomb", air, True, 30, 5, 7, 4, 87, 2, [], [""])
diveBomb.desc = "Leap into the air and ram into your opponent."
#def __init__(self, name, type, phys, atk, var, spd, crit, hitChance, cost, effects, spec):
soulDraw = Skill("Soul Beam", ghost, False, 30, 10, 4, 5, 100, 1, [],["soulDraw"])
soulConsume = Skill("Soul Consume", ghost, False, 0, 0, 10, 5, 100, 1, [],["soulConsume", "nodam"])
soulRage = Skill("Soul Rage", ghost, False, 10, 10, 1, 0, 100, 4, [], ["soulRage"])

charge = Skill("Charge", tech, False, 0, 0, 10, 2, 100, 2, [], ["charge", "nodam", "trueHit"])
charge.desc = "Defend yourself as you gain slight a power bonus"
powerShot = Skill("Power Shot", tech, True, 15, 15, 2, 7, 80, 3, [], ["conPierce"])
powerShot.desc = "Discharge a powerful shot to pierce through defences"
rapidSpray = Skill("Rapid Spray", tech, False, 5, 5, 4, 1, 120, 1, [], ["hitAll"])
rapidSpray.desc = "Fire off hundreds of ronuds in quick succession on all your opponenets"
lockOn = Skill("Lock On", tech, False, 0, 0, 4, 0, 120, 2, [], ["lockOn", "nodam"])
lockOn.desc = "Increase fighting capabilities on one target, lowering vs. others"

FireIce = Skill("Firey Ice", fire, False, 3, 0, 0, 2, 95, 1, [1, slowed], [""])
FireIce.desc = "Ice, but hot as fire."
IceFire = Skill("Icy Fire", ice, False, 5, 1, 4, 1, 110, 1, [3, burn], [""])
IceFire.desc = "Fire, but cold as ice."
spurofmoment = Skill("Spur of the Moment", fighting, False, 0, 0, 0, 5, 100, 5, [], ["trueHit", "nodam", "vulnerable", "spur"])
spurofmoment.desc = "Come up with a crazy plan that just might work. Boosts next attack greatly."

wispFire = Skill("Fire of the Wisp", fire, False, 30, 7, 6, 4, 99, 1, [2, burn], [""])

#------------- COUP DE GRACE------------------
testcoup = Skill("test coup", ice, False, 10, 10, 10, 10, 99, 1, [], ["coup"])
bloodHunt = Skill("Blood Hunt", blood, True, 32, 6, 1, 5, 100, 1, [], ["vampire", "vampire", "vampire", "trueHit", "conPierce", "coup"])
bloodHunt.desc = "Consume their flesh, without fail. Nothing can stop your bite."
stunningDisplay = Skill("Stunning Display", light, False, -1, 1, 10, 1, 100, 0, [1, stunned], ["trueHit", "hitall", "coup"])
stunningDisplay.desc = "Provide a stunning display to distract your opponents. None can resist the sight."
overcoup = Skill("Overclock", tech, True, 0, 0, 5, 1, 100, 0, [], ["trueHit", "nodam", "overclock", "coup"])
overcoup.desc = "Overclock your target to enable more actions per turn!"
fullcoup = Skill("Full Recovery", light, True, 0, 0, 5, 1, 100, 1, [], ["trueHit", "nodam", "recover", "recover", "recover", "recover", "removeEff", "coup"])
fullcoup.desc = "Recover a full health pool, and remove negative effects."
fullerase = Skill("Full Erase", unknown, True, 100, 0, 0, 1, 100, 5, [], ["trueHit", "division", "division", "division", "division", "division", "division", "coup"])
fullerase.desc = "Remove your target from existance."
allKnowing = Skill("All Knowing", unknown, False, 10, 1, 0, 2, 100, 6, [], ["trueHit", "coup", "createCreep", "observe", "observe", "observeDefend"])
allKnowing.desc = "Focus on your target, summoning 2 creeps and observe."
accessOrb = Skill("Access the Orb", magic, False, 0, 0, 1, 2, 100, 4, [], ["trueHit", "nodam", "powerUp", "powerUp", "powerUp", "powerUp", "powerUp", "coup"])
accessOrb.desc = "Access a remote orb of power, refilling your reserves."
singleHit = Skill("Single Hit", fighting, True, 100, 10, 10, 8, 100, 6, [1, passedOut], ["coup"])
singleHit.desc = "Its all you'll need."



#Skill("", normal, True, 0, 0, 0, 0, 100, 0, [], [""])
#def __init__(self, name, type, phys, atk, var, spd, crit, hitChance, cost, effects, spec):

#----------skills for testing--------

instantkill = Skill("Insta kill", unknown, False, 99999, 9999, 99, 15, 100, 0, [], ["trueHit"])
instantkill.desc = "BAM! You dead now."

allSkills = [instantkill, mindSpike, rejuvinate, windSlash, eldritchAppuratus, daggerStorm, mindDisk, never, colorfulBullet, neverThere, mindReading, antiPhysic, powerStrike, takeBlow, againstOdds, chaosVortex, astralVortex, earthenVortex, chains, voidSnap, otherStage, moonStage, earthStage, powerTransfer, lifeTransfer, fusion, fission, blast, rebuke, eggon, sneeze, exhale, inhale, observe, creepyAtk, blink, stare, psionicRadiance, recover, obsidianBlast, revenge, cleave, bladeFlash, wellspring, energiBeam, zap, mend, erase, planAhead, confuse, stab, bludgeon, shroud, lifePact, meditate, chaosBeam, forceShield, setFire, chaosBolt, consumeFlesh, rip, dodge, kick, bite, slash, tangle, powerDrain, block, meteorStorm, vampire, destroy, powerUp, magicMute, shardSwarm, nuke, scar, defend, axeLegs, earthShot, airBlast, waterSpout, fireBall, basicAtk, nothing]
allSkillScrolls = []

class Char(object):
	def __init__(self, name, types, hp, str, int, con, mag, agil, crit, dodgeChance, skills, ability, image, cords, menuImg):
		self.name = name
		self.hp = hp
		self.maxhp = hp
		self.str = str
		self.basestr = str
		self.types = types
		self.int = int
		self.baseint = int
		self.con = con
		self.basecon = con
		self.mag = mag
		self.basemag = mag
		self.agil = agil
		self.baseagil = agil
		self.lvl = 1
		self.xp = 0
		self.effects = []
		self.skills = skills
		self.image = image
		self.img = image
		self.cords = cords
		self.maxhp = hp
		self.crit = crit
		self.basecrit = crit
		self.dodgeChance = dodgeChance
		self.basedodgeChance = dodgeChance
		self.modHitChance = 0
		self.ability = ability
		self.marks = 0
		self.power = 1
		self.menuImg = menuImg
		self.goskill = nothing
		self.target = ["bob"]
		self.updated = False
		self.x = 0
		self.y = 0
		self.basey = 0
		self.basex = 0
		self.ym = 1
		self.guarder = "hi"
		self.misc = 0
		self.vital = True
		self.actions = 1
		#AI stuff
		self.savingfor = "none"
		self.aimisc = 0
		self.isAi = False
		self.equips = {"Head":emptySlot, "Chest":emptySlot, "Legs":emptySlot, "Feet":emptySlot, "Weapon":emptySlot}
		self.equipStr = 0
		self.equipInt = 0
		self.equipCon = 0
		self.equipMag = 0
		self.equipAgil = 0
		self.equipCrit = 0
		self.equipDodgeChance = 0
		self.ableSkills = []
		self.battlerpos = 0
		self.coups = []

	def updateEquips(self):
		self.equipStr = self.equips["Head"].str + self.equips["Chest"].str + self.equips["Legs"].str + self.equips["Feet"].str + self.equips["Weapon"].str
		self.equipInt = self.equips["Head"].int + self.equips["Chest"].int + self.equips["Legs"].int + self.equips["Feet"].int + self.equips["Weapon"].int
		self.equipCon = self.equips["Head"].con + self.equips["Chest"].con + self.equips["Legs"].con + self.equips["Feet"].con + self.equips["Weapon"].con
		self.equipMag = self.equips["Head"].mag + self.equips["Chest"].mag + self.equips["Legs"].mag + self.equips["Feet"].mag + self.equips["Weapon"].mag
		self.equipAgil = self.equips["Head"].agil + self.equips["Chest"].agil + self.equips["Legs"].agil + self.equips["Feet"].agil + self.equips["Weapon"].agil
		self.equipCrit = self.equips["Head"].crit + self.equips["Chest"].crit + self.equips["Legs"].crit + self.equips["Feet"].crit + self.equips["Weapon"].crit
		self.equipDodgeChance = self.equips["Head"].dodgeChance + self.equips["Chest"].dodgeChance + self.equips["Legs"].dodgeChance + self.equips["Feet"].dodgeChance + self.equips["Weapon"].dodgeChance
		
	def buildNew(self):
		newchar = Char(self.name, self.types, self.hp, self.str, self.int, self.con, self.mag, self.agil, self.crit, self.dodgeChance, self.skills, self.ability, pygame.transform.scale(pygame.image.load(self.image), [50, 50]), self.cords, pygame.transform.scale(pygame.image.load(self.image), [42, 42]))
		newchar.img = pygame.image.load(self.image)
		newchar.ableSkills = self.ableSkills
		newchar.target = [NOT]
		newchar.coups = self.coups
		return newchar
		
	def reBuild(self):
		newchar = Char(self.name, self.types, self.hp, self.str, self.int, self.con, self.mag, self.agil, self.crit, self.dodgeChance, self.skills, self.ability, self.image, self.cords, self.menuImg)
		newchar.img = self.image
		newchar.ableSkills = self.ableSkills
		newchar.coups = self.coups
		return newchar
	
punchingBag = Char("Punching Bag", [unknown], 1000, 0, 0, 0, 0, 0, 0, 0, [nothing], "Regen", "Assets/battlers/locked.png", [47, 23], "")
	
magicCoo = Char("Majikz Coosome", [fire, ice], 500, 15, 15, 10, 10, 10, 12, 30, [basicAtk, rapidSpray, IceFire, FireIce, meditate, eggon, spurofmoment], "", "Assets/battlers/wip.png", [25, 20], "")

NOT = Char("???", [unknown], 0, 0, 0, 0, 0, 0, 0, 0, [nothing], "", "Assets/battlers/locked.png", [-1,0], "")
NOT.ableSkills = [nothing]

Mage = Char("Meigis", [normal, chaos], 500, 5, 15, 5, 15, 4, 0, 10, [basicAtk, fireBall, waterSpout, airBlast, earthShot, defend], "", "Assets/battlers/Mage.png", [5,0], "")
Mage.ableSkills = [fireBall, waterSpout, airBlast, earthShot]

Mouther = Char("Mouther", [earth], 500, 20, 0, 10, 5, 4, 0, 10, [basicAtk, bite, consumeFlesh, defend], "", "Assets/battlers/Mouther.png", [4,0], "")
Mouther.ableSkills = []

Maice = Char("Maice", [normal], 500, 15, 15, 10, 10, 6, 2, 11, [basicAtk, slash, bite, eggon], "", "Assets/battlers/nazrin.png", [3, 0], "") 
Maice.ableSkills = []

Nic = Char("Nic", [chaos], 500, 15, 50, 10, 25, 4, 0, 10, [basicAtk, magicMute, shardSwarm, powerUp, defend], "", "Assets/battlers/nic.png", [5,8], "")
Nic.ableSkills = []
Epic = Char("Epic", [tech], 1000, 25, 50, 35, 45, 7, 10, 10, [basicAtk,energiBeam, wellspring, defend], "", "Assets/battlers/epic.png", [7,8], "")
Epic.ableSkills = []

Scarlet = Char("Scarlet", [dark, blood], 100, 20, 20, 5, 20, 6, 0, 10, [basicAtk, scar, vampire, destroy, lifePact, defend], "", "Assets/battlers/vamp.png", [1,0], "")
Scarlet.ableSkills = [scar, vampire, destroy, lifePact, consumeFlesh]
Scarlet.coups = [testcoup, testcoup, testcoup]

Flan = Char("Flan", [dark,blood], 200, 35, 30, 10, 20, 7, 10, 20, [slash, rip, scar, vampire, destroy, lifePact, setFire, lifeTransfer], "watch them burn", "Assets/battlers/flandre.png", [5,7], "")
Nue = Char("Nue", [astral, dark], 300, 25, 40, 10, 50, 4, 15, 10, [basicAtk, meteorStorm, powerTransfer, forceShield, powerDrain, stab, meditate, defend], "Unidentifiable", "Assets/battlers/nue.png", [4,7], "")
Okuu = Char("Okuu", [fire, tech], 500, 15, 50, 30, 10, 1, 5, 5, [bludgeon, blast, fusion, fission, nuke, forceShield, recover], "Radiation", "Assets/battlers/reiji.png", [3,7], "")
Lapis = Char("Lapis", [astral], 400, 20, 20, 10, 10, 4, 5, 20, [chains, voidSnap, earthStage, moonStage, otherStage, earthenVortex, chaosVortex, astralVortex], "3 worlds", "Assets/battlers/lapis.png", [6,7], "")

Koishi = Char("Koishi", [unknown, physic], 400, 10, 55, 80, 100, 10, 6, 30, [colorfulBullet,mindReading, antiPhysic, neverThere, never, recover, voidSnap], "", "Assets/battlers/komeiji.png", [7,7], "")

Nou = Char("Nou Furueteru", [physic], 300, 10, 50, 55, 90, 11, 7, 25, [colorfulBullet, mindDisk, mindReading, recover, forceShield, rejuvinate, meditate, defend], "", "Assets/battlers/Nou.png", [8,8], "")

Alpha = Char("Alpha", [normal, earth, fighting], 500, 50, -50, 30, 5, 5, 0, 10, [basicAtk, slash, cleave, bladeFlash, revenge, mend, defend], "", "Assets/battlers/alpha.png", [8,4], "")
Alpha.ableSkills = [slash, cleave, bladeFlash, revenge, mend, windSlash] 
Alpha.coups = [singleHit]
Siv = Char("Siv", [normal, earth, dark, physic, chaos, magic], 250, 0, 50, 0, 38, 5, 7, 10, [basicAtk, chaosBolt, setFire, forceShield, chaosBeam, meditate, lifePact, shroud], "", "Assets/battlers/siv.png", [4,2], "")
Siv.ableSkills = [chaosBolt, setFire, forceShield, chaosBeam, meditate, lifePact, shroud, confuse] 

Durric = Char("Durric", [earth, light, fighting, physic], 1000, 25, 25, 75, 25, 0, 0, 1, [basicAtk, forceShield, cleave, obsidianBlast, recover, psionicRadiance, mend, takeBlow], "Regen", "Assets/battlers/Durric.png", [4, 4], "")
Durric.ableSkills = [forceShield, cleave, obsidianBlast, recover, psionicRadiance, mend, takeBlow, rejuvinate, mindSpike]
Durric.coups = [fullcoup]

Coo33 = Char("Coo33", [dark, blood], 250, 50, 0, 30, 0, 10, 10, 10, [basicAtk, slash, bite, kick, dodge, rip, consumeFlesh, defend], "Blood hunt", "Assets/battlers/Coo33.png", [3,3], "")
Coo33.ableSkills = []
Coo33.coups = [bloodHunt]
CoosomeJoe = Char("Coosome Joe", [light, tech], 500, 25, 25, 25, 25, 5, 2, 10, [basicAtk, bludgeon, erase, create2, confuse, planAhead, mend, defend], "Frenzy", "Assets/battlers/Coosome.png",  [3, 4], "")
CoosomeJoe.ableSkills = []
CoosomeJoe.coups = [fullerase]
Catsome = Char("Catsome", [light, physic], 1000, 10, 35, 10, 15, 5, 5, 10, [slash, bite, eggon, rebuke, mend, recover], "Cuteness", "Assets/battlers/catsome.png",[6,9], "")
Catsome.ableSkills = []
Catsome.coups = [stunningDisplay]
Cubes = Char("Cubes", [tech], 400, 25, 35, 60, 30, 4, 5, 30, [zap, energiBeam, wellspring, planAhead, create3], "", "Assets/battlers/wip.png", [0,13], "")
Cubes.coups = [overcoup]

Creep = Char("Creepy Bald Guy", [physic, unknown], 750, 10, 10, 15, 50, 0, 0, 0, [creepyAtk, blink, stare, inhale, exhale, observe], "Creepus", "Assets/battlers/Creepy_Bald_Guy.png", [3, 15], "")
KnowingEye = Char("Knowing Eye", [physic, unknown, astral], 750, 0, 75, 0, 75, 5, 6, 5, [creepyAtk, observe, meditate, magicMute, forceShield, create], "Creepus", "Assets/battlers/knowingeye.png", [4, 15], "")
KnowingEye.coups = [allKnowing]
NotScaryGhost = Char("Not Scary Ghost", [ghost], 1000, 0, 0, 50, 75, 2, 0, 10, [basicAtk, sneeze, forceShield, recover, takeBlow], "tank", "Assets/battlers/Not_Scary_Ghost.png", [2, 15], "")
NotScaryGhost.coups = [fullcoup]
Noseclops = Char("Noseclops", [water, fire, acid], 400, 25, 15, 15, 10, 5, 7, 10, [basicAtk, sneeze, induceDisgust, stare, inhale, sneezeFire, observeDefend], "Creepus", "Assets/battlers/wip.png", [1, 15], "")
Mouthstash = Char("Mouthstash", [earth, air, poison], 400, 25, 10, 20, 10, 5, 2, 10, [basicEarth, loudspeaker, onionBreath, mustacheMuscles, gristlyDefend, growBeard, extendWhiskers, inhale], "Creepus", "Assets/battlers/wip.png", [0, 15], "")

#def __init__(self, name, types, hp, str, int, con, mag, agil, crit, dodgeChance, skills, ability, image, cords, menuImg):
hZarol = Char("Zarol", [magic, chaos], 900, 15, 25, 20, 30, 6, 3, 10, [], "", "Assets/battlers/hZarol.png", [20,20], "")
shyron = Char("Shyron", [ghost], 1200, 25, 50, 20, 45, 14, 6, 25, [soulConsume, soulDraw, soulRage], "Soul Eater", "Assets/battlers/shyron.png", [21,20], "")

theeCoosome = Char("Thee Coosome", [tech], 750, 30, 20, 30, 25, 4, 4, 10, [basicAtk, rapidSpray, planAhead, createdrone], "Frenzy", "Assets/battlers/theCoosome2.png", [22,20], "")
theeCoosome.coups = [overcoup, overcoup, overcoup]
battleDrone = Char("Battle Drone", [tech, minion], 500, 10, 10, 10, 10, 7, 4, 20, [basicAtk, rapidSpray, powerShot, energiBeam, lockOn, dodge, charge, takeBlow], "Regen", "Assets/battlers/battleDrone.png", [23, 20], "")

John = Char("Regalious John", [fighting], 750, 35, 25, 20, 34, 5, 5, 10, [], "", "Assets/battlers/john.png", [23, 20], "")

Xsion = Char("Xsion", [dark, blood, magic], 500, 40, 40, 25, 25, 8, 7, 50, [], "", "Assets/battlers/xsion1.png", [24, 20], [])
Xsion2 = Char("Xsion", [dark, blood, magic], 500, 50, 50, 20, 20, 8, 9, 50, [], "", "Assets/battlers/xsion2.png", [25, 20], [])

Protagonist = Char("Protagonist", [normal], 750, 25, 15, 20, 10, 2, 6, 5, [basicAtk, powerStrike, eggon, mend, instantkill], "Frenzy", "Assets/battlers/wip.png", [1,1], "")

Axeurlegs = Char("Axurlegs", [grass], 10, 30, 0, 0, 1, 2, 3, 0, [axeLegs], "", "Assets/battlers/axeurlegs.png", [10,0], "")
Axeurlegs.coups = [singleHit]
Dandylion = Char("Dandy Lion", [grass], 600, 20, 15, 5, 20, 2, 2, 10, [slash, bite, tangle], "Frenzy", "Assets/battlers/wip.png", [11,0], "")

Shroom = Char("Shroom", [grass, poison], 500, 10, 20, 10, 15, 3, 3, 10, [spores, absorb, sneeze], "", "Assets/battlers/shroom.png", [10, 1], "")
frostShroom = Char("Frost Shroom", [ice, poison], 500, 10, 20, 10, 15, 3, 3, 10, [spores, iceShard, sneeze], "", "Assets/battlers/frostShroom.png", [11, 1], "")
caveShroom = Char("Cave Shroom", [earth, poison], 500, 10, 20, 10, 15, 3, 3, 10, [spores, earthShot, sneeze], "", "Assets/battlers/caveShroom.png", [12, 1], "")
sandShroom = Char("Sand Shroom", [earth, poison], 500, 10, 20, 10, 15, 3, 3, 10, [spores, sandStorm, sneeze], "", "Assets/battlers/desertShroom.png", [13, 1], "")
goldShroom = Char("Gold Shroom", [poison], 500, 10, 20, 10, 15, 3, 3, 10, [spores, sneeze], "", "Assets/battlers/goldShroom.png", [14, 1], "")

seeGull = Char("Seegull", [water, air], 300, 15, 20, 6, 10, 7, 4, 15, [airBlast, stare, diveBomb], "", "Assets/battlers/seeGull.png", [15, 15], "")
crawFish = Char("Craw Fish", [water], 350, 20, 12, 20, 10, 4, 4, 10, [slash, defend], "", "Assets/battlers/crawFish.png", [16, 15], "")

wisp = Char("Wisp", [fire, ghost], 200, 10, 25, 1, 25, 3, 4, 20, [fireBall, wispFire], "", "Assets/battlers/wisp.png", [13, 2], "")

#def __init__(self, name, types, hp, str, int, con, mag, agil, crit, dodgeChance, skills, ability, image, cords, menuImg):
Worshipper = Char("Worshipper", [magic, chaos, minion], 300, 5, 15, 6, 10, 0, 0, 0, [basicAtk, fireBall, powerTransfer, lifeTransfer, meditate], "Frenzy", "Assets/battlers/wip.png", [2,0], "")
miniCreep = Char("Creepy Bald Guy", [physic, unknown, minion], 300, 6, 6, 8, 10, 0, 0, 0, [creepyAtk, blink, stare, inhale, exhale, observe], "Creepus", "Assets/battlers/Creepy_Bald_Guy.png", [3, 14], "")

NO = NOT.buildNew()	

unlockedchars = [Koishi.buildNew(), Lapis.buildNew(), Flan.buildNew(), Okuu.buildNew(), Nue.buildNew(), Scarlet.buildNew(), Mage.buildNew(), Mouther.buildNew(), Nic.buildNew(), Siv.buildNew(), Coo33.buildNew(), CoosomeJoe.buildNew(), Epic.buildNew(), Alpha.buildNew(), Durric.buildNew(), Creep.buildNew(), Catsome.buildNew(), KnowingEye.buildNew(), Protagonist.buildNew(), Worshipper.buildNew(), miniCreep.buildNew(), Axeurlegs.buildNew(), Dandylion.buildNew(), Cubes.buildNew(), Shroom.buildNew(), frostShroom.buildNew(), caveShroom.buildNew(), sandShroom.buildNew(), goldShroom.buildNew(), NotScaryGhost.buildNew(), seeGull.buildNew(), crawFish.buildNew(), Noseclops.buildNew(), Mouthstash.buildNew(), theeCoosome.buildNew(), battleDrone.buildNew(), punchingBag.buildNew()]

equipment = []

class Player(object):
	def __init__(self, name):
		
		self.battlers = [NO, NO, NO]
		self.name = name
		self.wins = 0
		self.losses = 0
		self.scrolls = []
	
		
		self.x1 = 0
		self.y1 = 0
		self.x2 = 0
		self.y2 = 0
		self.x3 = 0
		self.y3 = 0
		
	def reBuild(self):
		self.battlers = [NO, NO, NO]
		self.x1 = 0
		self.y1 = 0
		self.x2 = 0
		self.y2 = 0
		self.x3 = 0
		self.y3 = 0
	
	
player1 = Player("1")
player2 = Player("2")


class Arena(object):
	def __init__(self, name, effect, img):
		self.name = name
		self.effect = effect
		self.img = pygame.image.load(img)

rift = Arena("Rift", "", "assets/arena/riftnou.png")
defultarena = Arena("Defult", "", "assets/arena/defult.png")

class Battle(object):
	def __init__(self, name, battlers1, battlers2, arena, dialog, mult, music, post):
		self.battlers1 = battlers1
		self.battlers2 = battlers2
		self.name = name
		self.music = music
		self.arena = arena
		self.dialog = dialog
		self.mult = mult
		self.post = post
		if not self.mult:
			for i in self.battlers2:
				i.isAi = True
		for i in self.battlers1:
			if i.name == "???":
				i.isAi = True
		for i in self.battlers2:
			if i.name == "???":
				i.isAi = True
		
	def battle(self):
		global size
		global coupback
		global lockedskill
		thebattler = 0
		powergiven = False
		pickenm = False
		increment = 0
		mincrement = 0
		thesebattlers = []
		battling = True
		diatimer = 0
		talking = True
		ready = False
		mouse_down = False
		printing = False
		textc = font.render(" ",True,BLACK)
		limit = 6
		dispskill = nothing
		global done
		global running
		global messages
			
		if self.mult == False:
			limit = 6
			
		if self.post == "Get catsome":
			self.battlers1 = [Protagonist.buildNew(), NO, Catsome.buildNew()]
		
		if self.post == "dandylion":
			self.battlers2[0].vital, self.battlers2[2].vital = False, False

		if self.post == "Coos":
			self.battlers2[2].vital = False
		
		thesebattlers += self.battlers1 + self.battlers2
		
		
		x = 0
		y = 0
		for i in thesebattlers:
			if y > 2:
				y = 0
				x += 1
			i.basex = x * (size[0] - 150) + 50
			i.basey = y * 75 + 325
			y += 1
		for i in range(len(thesebattlers)):
			thesebattlers[i-1].battlerpos = i
			
		for i in self.battlers1:
			if i.name == "???" or i == NO or i == NOT:
				self.battlers1.remove(i)
		for i in self.battlers2:
			if i.name == "???" or i == NO or i == NOT:
				self.battlers2.remove(i)
		

		for i in thesebattlers:
			if i.name == "???" or i == NO or i == NOT:
				thesebattlers.remove(i)
		
		
		origbattlers = thesebattlers
		for i in origbattlers:
			print "orig:", i.name
		origbattlers1 = self.battlers1
		origbattlers2 = self.battlers2
		dialog.PreDialogeRun(self, self.battlers1, self.battlers2, thesebattlers)
		
		quitting = False
		while battling:
			self.music.play()
			agillist = []

			for p in thesebattlers:
				if not quitting:
					#update effects and all that good stuff
					for i in p.effects:
						for k in thesebattlers:
							if k.ability == "watch them burn" and i == 	burn:
								i.canend = False
								i.damage *= 2
						i.update(p)
					if p.ability == "Unidentifiable":
						p.marks /= 2
					if p.ability == "Radiation":
						for l in thesebattlers:
							l.hp -= 25
							messages.append(p.name + "'s radiation hurt everyone!")
						

					if p.ability == "Regen":
						p.hp += 25
						messages.append(p.name + " is healing themself!")
					
						
					p.power += 1
					p.updateEquips()
					p.x = p.basex
					p.y = p.basey

					for action in range(p.actions):
						ready, selected = False, False
						while not ready and not p.isAi:
							gScreen.fill(WHITE)
							gScreen.blit(self.arena.img, [0,0])
							for event in pygame.event.get(): 
								if event.type == pygame.QUIT: 
									ready = True							
									battling = False
									done, running, quitting = True, False, True
									break
								elif event.type == pygame.MOUSEBUTTONDOWN:
									mouse_down = True
								
								elif event.type == pygame.MOUSEBUTTONUP:
									mouse_down = False
									
							mouse_pos = pygame.mouse.get_pos()
							
							
							#displaying and picking skills
							if p.hp > 0 and not passedOut in p.effects:
								x = 0
								selected = False
								for i in p.coups:
									thisxcord = 700 + 180*x
									thisycord = size[1] - 35
									if hitDetect(mouse_pos, mouse_pos, [thisxcord, thisycord], [thisxcord + 169, thisycord + 29]):
									
										dispskill = p.coups[x]
										if mouse_down and p.coups[x].uses == 1:
											mouse_down = False
											p.goskill = p.coups[x]
											selected = True
										
											
									x += 1
									
								x = 0
								y = 0
								for i in p.skills:
								
									if x > 1:
										x = 0
										y += 1
									
									thisxcord = 330 + x*175
									thisycord = y*30 + 370 + size[1] - 500
									if hitDetect(mouse_pos, mouse_pos,[thisxcord, thisycord], [thisxcord + 165, thisycord + 25]):
										dispskill = p.skills[x + y*2]
										
										
										if mouse_down:
											mouse_down = False
											
												
											if p.skills[x + y*2].cost <= p.power:
												p.goskill = p.skills[x + y*2]
												selected = True
														
									x += 1
														
								if selected:
									mouse_down = False
									print "skill picked:", p.goskill.name
									pickenm = True
			
								if pickenm:	
									p.target = ["nul"]
									for i in thesebattlers:
										
											
										if hitDetect(mouse_pos, mouse_pos, (i.basex, i.basey), (i.basex + 50,i.basey + 50)):
											gScreen.blit(targetSelector, [i.basex - 2, i.basey - 2])
											if mouse_down:
												p.target[0] = i
												ready = True
												
											mouse_down = False
										
										if ready:
											#print p.target[0].name
											
											if "hitAll" in  p.goskill.spec:
												p.target = []
												if p in self.battlers1:
													p.target = self.battlers2
												elif p in self.battlers2:
													p.target = self.battlers1
											
											pickenm = False
										

								#----------------
							
							else:
								p.goskill = nothing
								p.target = [p]
								ready = True

							for i in thesebattlers:	
								if i.hp > 0:
								
									gScreen.blit(i.image,[i.basex,i.basey])
									gScreen.blit(battleSelector, [p.basex - 2, p.basey - 2])
									pygame.draw.rect(gScreen, RED, [i.basex, i.basey - 10,int(i.hp) / 20,5])
									 
									for f in range(len(i.effects)):
										gScreen.blit(i.effects[f].img, [i.basex - f * 10, i.basey])
									
									
								y += 1
							#ANIMATIONS!
							
							pygame.draw.rect(gScreen, BLACK, [0,size[1] - 150,size[0],150])
						
							gScreen.blit(health_border, [10, 360 + size[0] - 500])
							pygame.draw.rect(gScreen, GREY, [320, size[1] - 140, 370, 130])
							gScreen.blit(battleSelector, [p.basex - 2, p.basey - 2])
							x = 0
							
							for pos in p.coups:
								pygame.draw.rect(gScreen, GREY, [700 + 180*x, size[1] - 35, 169, 28])
								gScreen.blit(coupback, [700 + 180*x, size[1] - 35])
								gScreen.blit(font.render(dispskill.name + "   Cost: " + str(dispskill.cost), True, WHITE), [700, size[1] - 140])
								if pos.uses == 1:
									gScreen.blit(pos.type.img, [702 + 180*x, size[1] - 33])
									gScreen.blit(font.render(pos.name, True, WHITE), [709 + 180*x, size[1] - 28])
									
								else:
									gScreen.blit(lockedskill, [702 + 180*x, size[1] - 33])
									
								x += 1
								
							gScreen.blit(font.render(dispskill.name + "   Cost: " + str(dispskill.cost), True, WHITE), [700, size[1] - 140])
							gScreen.blit(font.render(dispskill.desc, True, WHITE), [700, size[1] - 125])
						
							x = 0
							y = 0

							if p.hp > 0:
								dispSkills(p)
							#------
							
							if mouse_down:
								gScreen.blit(mouse_pointer2,mouse_pos)
							else:
								gScreen.blit(mouse_pointer,mouse_pos)
							for i in thesebattlers:
								if i.hp <= 0:
									i.effects.append(death)
									
							if thebattler == len(thesebattlers):
								pygame.draw.rect(gScreen, BLACK, [0,size[1] - 150,size[0],150])


							pygame.display.flip()
					 
							# --- Limit to 60 frames per second
							clock.tick(60)
							
						if p.isAi:
							p = ai.runAI(p, self.battlers1, self.battlers2)
							print p.name + " has "+str(p.power)+" power, saving for: "+ p.savingfor + ". Using: " + p.goskill.name + " on " + p.target[0].name
						print "appending to agillist"
						agillist.append([p, p.goskill, p.target])

			if not quitting:
				print "sorting agillist"
				for i in range(len(agillist)):
					for j in range(len(agillist)-1-i):
						if agillist[j][0].agil + agillist[j][0].equipAgil + agillist[j][1].spd  < agillist[j+1][0].agil + agillist[j + 1][0].equipAgil + agillist[j+1][1].spd:
							agillist[j], agillist[j+1] = agillist[j+1], agillist[j]
				
				print "taking actions"
				x = 0
				while x < len(agillist):
					p = agillist[x][0]
					skill = agillist[x][1]
					targets = agillist[x][2]
					#print "thebattler:", thebattler
										
					if len(p.target) > 1:
						for t in targets:
							skill.use(p, t, self.battlers1, self.battlers2, thesebattlers)
						
					
						p.power -= skill.cost
						
					else:
						skill.use(p, targets[0], self.battlers1, self.battlers2, thesebattlers)
						agillist[x].append(skill.damageImg)
						p.power -= skill.cost
				
					for i in thesebattlers:
						if i.hp <= 0:
							#thesebattlers.remove(i)
							if i in self.battlers1:
								self.battlers1.remove(i)
							if i in self.battlers2:
								self.battlers2.remove(i)
					x += 1
				

				skillPrinting = True
				effectPrinting = False
				loop = 0
				timer = -1
				print "----------"
				for item in messages:
					print item
				print "----------"
				currentBattler = 0
				currentTarget = 0
				setVel = False
				print "displaying skills"
				while skillPrinting and not quitting:
					aniBattler = agillist[currentBattler][0]
					gScreen.blit(self.arena.img, [0,0])
					
					for i in thesebattlers:	
						if i.hp > 0:
							gScreen.blit(i.image,[i.x,i.y])

					try:
						if not setVel:
							yDiff = aniBattler.target[0].basey - aniBattler.basey
							xDiff = (aniBattler.target[0].basex - aniBattler.basex)
							hypot = math.hypot(xDiff, yDiff)
							vel = [xDiff/hypot, yDiff/hypot]
							print "Length of battlers, messages: ", len(thesebattlers), len(messages)
							print "Thisbattler, Loop: ", currentBattler, loop
							print vel
							setVel = True
							timer = 90
							
					except:
						if not setVel:
							vel = [0,0]
							timer = 90
					
					if len(aniBattler.target) > 1:
						
						if aniBattler in self.battlers1:
							if aniBattler.x < 625:
								aniBattler.x += vel[0] * 3
								aniBattler.y += vel[1] * 3
							else:
								print "incrmenting loop"
								loop += 1
								currentTarget += 1
								
						else:
							if aniBattler.x < 625:
								aniBattler.x += vel[0] * 3
								aniBattler.y += vel[1] * 3
							else:
								print "incrmenting loop, multiple targets"
								loop += 1
								currentTarget += 1
								
						if currentTarget >= len(aniBattler.target):
							currentBattler += 1
							currentTarget = 0
							aniBattler.x = aniBattler.basex
							aniBattler.y = aniBattler.basey
								
					else:
						if timer == 1:
							#ANIMATION HERE
							print "Exiting from battler loop"
							loop += 1
							currentBattler += 1
							aniBattler.x = aniBattler.basex
							aniBattler.y = aniBattler.basey
							setVel = False
						else:
							aniBattler.x += vel[0] * 3
							aniBattler.y += vel[1] * 3

					if timer > 0:
						timer -= 1
					if loop >= len(messages) or currentBattler >= len(thesebattlers):
						skillPrinting = False
						effectPrinting = True
						loop = 0
						currentBattler = 0
						messages = []
						theMessage = ""
						timer = 240
						print "ending loop"
						
					pygame.draw.rect(gScreen, BLACK, [0,size[1] - 150,size[0],150])
					try:
						gScreen.blit(font.render(messages[loop], True, WHITE), [10, size[1] - 140])
					except:
						print "Loop: " + str(loop) + " > messages: " + str(len(messages))
						
					#print agillist[currentBattler][3]
					gScreen.blit(agillist[currentBattler][3], [aniBattler.target[0].basex, aniBattler.target[0].basey + 10])
					#gScreen.blit(disptext, [10, 320 + size[1] - 500])
					pygame.display.flip()	
					clock.tick(60)
					
				print "printing effects"
				loop = 0
				while effectPrinting and not quitting:
					gScreen.blit(self.arena.img, [0,0])
					for i in thesebattlers:	
						if i.hp > 0:
							gScreen.blit(i.image,[i.x,i.y])
							
					if timer >= 1:
						timer -= 1
							
					if timer <= 0:
						timer = 240
						loop += 1
					print "loop:", loop
					print "len message", len(effectMessages)
					if loop >= len(effectMessages) - 1:
						effectPrinting = False
					
					pygame.draw.rect(gScreen, BLACK, [0,size[1] - 150,size[0],150])
					#gScreen.blit(disptext, [10, 320 + size[1] - 500])
					if len(effectMessages) > 0:
						gScreen.blit(font.render(effectMessages[loop], True, WHITE), [10, size[1] - 140])
					else:
						effectPrinting = False
						
					
					pygame.display.update()	
					clock.tick(60)
				#------End animations and printing-----
				print "prepping for next battle"
				for i in thesebattlers:
					i.updated = False

				loss = True
				for i in self.battlers1:
					#print i.vital
					if i.vital and i.hp > 0:
						loss = False
				if loss:
					printb("Player 2 WINS!")
					print "Player 2 Wins"
					for b in thesebattlers:
						b = b.reBuild()
					self.music.reset()
					self.music.stop()
					battling = False
					break

				loss = True
				for i in self.battlers2:
					#print i.vital
					if i.vital and i.hp > 0:
						loss = False
				if loss:
					printb("Player 1 WINS!")
					print "Player 1 Wins"
					for b in thesebattlers:
						b = b.reBuild()
					for battler in origbattlers1:
					
						for b in origbattlers2:
							battler.xp += b.xp
					for b in origbattlers1:
						#xp curve equaation:
						if b.xp >= 50 * 2 ** b.lvl:
							b.xp = 0
							b.lvl += 1
							printb(b.name + " leveled up!")
							
						
					self.music.reset()
					self.music.stop()
					battling = False
					break

				pygame.display.flip()
				clock.tick(60)
			
		#-------------------------------POST BATTLE----------------------------
		if len(self.battlers1) == 0:
			dialog.LossDialogeRun(self, origbattlers1, origbattlers2, thesebattlers)
		if len(self.battlers2) == 0:
			dialog.WinDialogeRun(self, origbattlers1, origbattlers2, thesebattlers)
		
#preb is list of lists, inb is dictionary, losb is list of lists, winb is list of lists
class Dialoge(object):
	def __init__(self, preb, losb, winb):
		self.prebattle = preb
		self.lossbattle = losb
		self.winbattle = winb

NoDial = Dialoge([[0, ""]],[[0, ""]],[[0, ""]])
#Battle([], [], "", NoDial, False, 	maicetheme, "")

#stage 1
MousDial = Dialoge([[1, "Ahh!"], [0, "Wha--?"], [1, "Get-- Agh, I need to.."], [0, "Whoah, Calm Down!"], [1, "GET OUT OF MY WAY!"]], [[1, "*huff*"], [1, "I need to hurry up before that", "monster catches up with me..."]], [[1, "I.. I'm sorry."], [1, "I was panicking there."], [0, "I could tell. Why?"], [1, "Well, I'm being chased by.."], [1, "Well, you look like a nice guy,", "maybe you can help me?"], [0, "Depends, but I'll try"], [1, "A monster named 'Catsome' is chasing after me,","And I need some help dealing with it."], [0, "Sure, where can I-"], [1, "Thanks, I'll be heading off now!"]])
MousFight = Battle("Maice Fight",[], [NO, Maice.buildNew(), NO], defultarena, MousDial, False,	maicetheme, "")
CatDial = Dialoge([[0, "Are you this 'Catosme' i've heard so much about?"], [1, "Yes, that is one title I reply to..."], [1, "Anyway, have you seen a little friend of mine running about?"], [0, "I was sent here by it to avenge it."], [1, "So it wants you to try to hit on me?"], [0, "Please no."], [1, "So we're going to skip the formalities", "and get right to the good parts, eh?"]], [[1, "Ah, that was nice being on top."], [0, "What is it with you and innuendos?"], [1, "I guess it's just one of the things in me."]], [[1, "Ah, I give! Safe word, Safe word!"], [0, "Please stop with the innuendos."], [1, "Well, that little Maice charachter was", "running away after stealing something of mine."], [1, "So you think you can help me get back", "what was taken from me?"], [0, "Sure, I guess so."], [1, "Then let's head off!"]])
CatsomeFight = Battle("Catosme Fight", [], [	NO, Catsome.buildNew(), NO], defultarena, CatDial, False, cattheme, "")
MiecDial = Dialoge([[1, "Ah, there you are. I see", "you brought some Friends this time."], [3, "Ah! There's the Cat!"], [3, "And.. I thought you were going to help me!", "you TRAITOR!"], [0, "something stole something"], [2, "You are Horrible!"], [4, "Why would you trust this scum?"], [3, "I don't even know."], [1, "Well then,", "Let's start this party."]],[[3, "lol rekt"]],[[3, "omg ded"]])
MiecFight = Battle("Mouses Fight",[], [Maice.buildNew(), Maice.buildNew(), Maice.buildNew()], defultarena, MiecDial, False, maicetheme, "Get catsome")

#forest stage 1
ForDial = Dialoge([[0, "So this is the forest."], [3, "Why hello, fine traveler.", "What brings you to my forest?"], [1, "Who are you, with that fine maine?"], [3, "I am a Dandy Lion."], [2, "*click*"], [0, "wait, what was that noise?"], [4, "*click*"], [3 ,"and I must have you", "LEAVE MY FOREST!"]],[[3, "And I wish you a good day."]],[[3, "If... I must.", "You have proven yourself worthy to enter my forest."], [1, "Thank you, my fellow feline."]])

ForFight1 = Battle("Forest Fight", [], [Axeurlegs.buildNew(), Dandylion.buildNew(), Axeurlegs.buildNew()], defultarena, ForDial, False, defulttheme, "dandylion")
ForFight2 = Battle("Forest 2", [], [Shroom.buildNew(), Dandylion.buildNew(), Shroom.buildNew()], defultarena, "", False, defulttheme, "")
Alphight = Battle("Alpha Fight", [], [Axeurlegs.buildNew(), Alpha.buildNew(), Axeurlegs.buildNew()], defultarena, ForDial, False, sivtheme, "")

CooDial = Dialoge([[2, "Ah, Coosome! it's been a while!"], [3, "Indeed it has, Cat."], [0, "You know him?"], [2, "Of course! We are all over each other!"], [3, "What Cat means to say, is that we are one and the same."], [2, "We stick together! so Lets have a FOURSOME!"], [0, "But who else is joining me?"], [1, "I'll stand in for Catsome. Lets do this."]], [[3, "You fought well.", "But not well enough."], [2, "Is that really all? I'm not satisfied yet."]], [[3, "Nice one, you fought well there."], [2, "Is it done already? I'm not quite satisfied yet..."]])
CoosomeFight = Battle("Coosome Fight", [], [Catsome.buildNew(), NO, CoosomeJoe.buildNew()], defultarena, CooDial, False, 	cootheme, "coosome") 
C33Dial = Dialoge([[5, "Ah, Coosome! it's been a while!"], [4, "Indeed it has, Cat."], [1, "You know him?"], [5, "Of course! We are all over each other!"], [4, "What Cat means to say, is that we are one and the same."], [5, "We stick together! so Lets have a FOURSOME!"], [1, "But who else is joining me?"], [2, "I'll stand in for Catsome. Lets do this."]], [[4, "You fought well.", "But not well enough."], [5, "Is that really all? I'm not satisfied yet."]], [[4, "Nice one, you fought well there."], [5, "Is it done already? I'm not quite satisfied yet..."]])
Coo33Fight = Battle("Coo33 fight", [], [CoosomeJoe.buildNew(), Coo33.buildNew(), Catsome.buildNew()], defultarena, C33Dial, False, cootheme, "Coos")

KnowingEyeFight = Battle("knowingeye fight", [], [NO, KnowingEye.buildNew(), NO], defultarena, C33Dial, False, defulttheme, "knowingeye")

NouDial = Dialoge([[3, "!"], [2, "Hello?"], [3, "Hiya!"], [1, "Finally, a person in this strange place.", "We have-"], [3, "Oh yes I know, I know everything.", "Except for what my master Knows!", "She truely knows everything"], [0, "Even more than-"], [3, "Yes, even more than that, abomination.", "I must say that you and you're group seem very excited to get you're hands on this knowledge", "Unforunatly, I cannot allwow that"]], [[0, "Ugg"]], [[0, "Ugg"]])
NouFight = Battle("Nou Fight", [], [NO, Nou.buildNew(), NO], rift, NouDial, False, 	noutheme, "")

theeCoosomeFight = Battle("theeCoosome Fight", [], [battleDrone.buildNew(), theeCoosome.buildNew(), battleDrone.buildNew()], defultarena, CooDial, False, theeCoosomeTheme, "") 

class Stage(object):
	def __init__(self, name, playerbattlers, battles, cords, nextstages):
		self.name = name
		self.battles = battles
		self.cords = cords
		self.locked = True
		self.nextstages = nextstages
	def run(self):
		if self.name == "Forest 2":
			forestbattlelist = [ForFight1]
			self.battles = forestbattlelist[random.randint(0, len(forestbattlelist) - 1)]
			
		for i in self.battles:
			i.battlers1 = self.playerbattlers
		for i in self.battles:
		
			for j in i.battlers1:
				if j.name == "???" or j == NO or j == NOT:
					i.battlers1.remove(j)
		
					
			if len(i.battlers1) == 1:
				i.battlers1 = [NO, i.battlers1[0], NO]
			if len(i.battlers1) == 2:
				i.battlers1 = [i.battlers1[0], NO, i.battlers1[1]]
		
				
				
			
			i.battle()
		for i in self.nextstages:
			i.locked = False
			maptheme.reset()

st8 = Stage("", "", [], [359,516], [])
st7 = Stage("", "", [], [523,431], [st8])
st6 = Stage("", "", [], [720,360], [st7])
st5 = Stage("", "", [NouFight], [675,240], [st6])
st4 = Stage("", "", [KnowingEyeFight], [540,313], [st5])
st3 = Stage("", "", [theeCoosomeFight], [393,292], [st4])
st2 = Stage("", "", [ForFight1], [280, 221], [st3])
st1 = Stage("", "", [MousFight, CatsomeFight, MiecFight], [317,48], [st2])
		
st1.locked = False
st3.locked = False
st4.locked = False
st5.locked = False

class World(object):
	def __init__(self, stages):
		self.stages = stages
		self.cords = [0,0]
		self.image = pygame.image.load("Assets/ui/maptest.png")
		self.vel = [0,0]
	
		
	def run(self, mult):
		mouse_down = False
		global done
		running = True
		while running:
			maptheme.play()
			for event in pygame.event.get(): 
				if event.type == pygame.QUIT: 
					running, done = False, True
				elif event.type == pygame.MOUSEBUTTONDOWN:
					mouse_down = True
				
				elif event.type == pygame.MOUSEBUTTONUP:
					mouse_down = False
				if event.type == pygame.KEYDOWN:
		
					if event.key == K_w:
				
						self.vel[1] = 5
					
					if event.key == K_d:
				
						self.vel[0] = -5
					
					if event.key == K_s:
				
						self.vel[1] = -5
					
					if event.key == K_a:
				
						self.vel[0] = 5
					
				elif event.type == pygame.KEYUP:
			
					if event.key == pygame.K_d or event.key == pygame.K_a:
				
						self.vel[0] =0
					if event.key == pygame.K_w or event.key == pygame.K_s:
				
						self.vel[1] =0
				
			mouse_pos = pygame.mouse.get_pos()
			
			for i in self.stages:
				
				pygame.draw.rect(gScreen, RED, [i.cords[0], i.cords[1], 16,16])
				if hitDetect(mouse_pos, mouse_pos, [i.cords[0] + self.cords[0], i.cords[1]+ self.cords[1]], [i.cords[0] + 16, i.cords[1] + 16]):
					if mouse_down and not i.locked:
						i.playerbattlers = CharSelect(aitest, mult)
						i.run()
						i.completed = True
					
					
			
			self.cords[0] += self.vel[0]
			self.cords[1] += self.vel[1]
			gScreen.fill(BLACK)
			
			gScreen.blit(self.image, [self.cords[0], self.cords[1]])
			
			for i in self.stages:
				if i.locked:
					gScreen.blit(lockedchar, [i.cords[0] + self.cords[0], i.cords[1] + self.cords[1]])
				else:
					pygame.draw.rect(gScreen, RED, [i.cords[0] + self.cords[0], i.cords[1] + self.cords[1], 16,16])
			
			if mouse_down:
				gScreen.blit(mouse_pointer2,mouse_pos)
			else:
				gScreen.blit(mouse_pointer,mouse_pos)
   
			pygame.display.flip()
   
  
			clock.tick(60)
		

theWorld = World([st1, st2, st3, st4, st5, st6, st7, st8])

class SkillScroll(object):
	def __init__(self, skill):
		self.skill = skill
		self.cords = []
	def apply(self, char, player):
		
		while running:
			for event in pygame.event.get(): 
				if event.type == pygame.QUIT: 
					running = False
				elif event.type == pygame.MOUSEBUTTONDOWN:
					mouse_down = True
							
				elif event.type == pygame.MOUSEBUTTONUP:
					mouse_down = False
								
			mouse_pos = pygame.mouse.get_pos()
			x = 0
			y = 0
			for i in p.skills:
							
				if x > 1:
					x = 0
					y += 1
								
				thisxcord = 330 + x*175
				thisycord = y*30 + 370 + size[1] - 500
				if hitDetect(mouse_pos, mouse_pos,[thisxcord, thisycord], [thisxcord + 165, thisycord + 25]):
					if x == 0 and y ==0:
						dispskill = p.skills[0]
						if mouse_down:
							char.skills[0] = self.skill
							running = False
						
					elif x == 1 and y == 0:
						dispskill = p.skills[1]
						if mouse_down:
							char.skills[1] = self.skill
							running = False
					elif x == 0 and y == 1:
						dispskill = p.skills[2]
						if mouse_down:
							char.skills[2] = self.skill
							running = False
					elif x == 1 and y == 1:
						dispskill = p.skills[3]
						if mouse_down:
							char.skills[3] = self.skill
							running = False
					elif x == 0 and y == 2:
						dispskill = p.skills[4]
						if mouse_down:
							char.skills[4] = self.skill
							running = False
					elif x == 1 and y == 2:
						dispskill = p.skills[5]
						if mouse_down:
							char.skills[5] = self.skill
							running = False
					elif x == 0 and y == 3:
						dispskill = p.skills[6]
						if mouse_down:
							char.skills[6] = self.skill
							running = False
					elif x == 1 and y == 3:
						dispskill = p.skills[7]
						if mouse_down:
							char.skills[7] = self.skill
							running = False
					else:
						dispskill = nothing
					
				
				x += 1
			
			
			pygame.draw.rect(gScreen, GREY, [0,0,size[0],size[1]])
		
			dispSkills(char)
			gScreen.blit(font.render(self.skill.name + "   Cost: " + str(self.skill.cost), True, WHITE), [0, 0])
			gScreen.blit(font.render(self.skill.desc, True, WHITE), [0, 15])
			gScreen.blit(font.render(dispskill.name + "   Cost: " + str(dispskill.cost), True, WHITE), [700, size[1] - 140])
			gScreen.blit(font.render(dispskill.desc, True, WHITE), [700, size[1] - 125])
			
	def buildNew(self):
		newscroll = SkillScroll(self.skill)
		return newscroll
		
for i in allSkills:
	scroll = SkillScroll(i)
	allSkillScrolls.append(scroll.buildNew())

def CharSelect(aitest, mult):
	global done
	global unlockedchars
	done = False
	dispchar2 = NO		
	
	battling = False

	thesebattlers = []
	thisplayer = player1
	thisplayer.reBuild()

	mouse_down = False
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				done = True 
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_down = True
				
			elif event.type == pygame.MOUSEBUTTONUP:
				mouse_down = False
				
			elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						thisplayer.y3 -= 1
						if thisplayer.y3 < 0:
							thisplayer.y3 = 24
					if event.key == pygame.K_DOWN:
						thisplayer.y3 += 1
						if thisplayer.y3 > 24:
							thisplayer.y3 = 0
					if event.key == pygame.K_LEFT:
						thisplayer.x3 -= 1
						if thisplayer.x3 < 0:
							thisplayer.x3 = 48
					if event.key == pygame.K_RIGHT:
						thisplayer.x3 += 1
						if thisplayer.x3 > 48:
							thisplayer.x3 = 0
					if event.key == pygame.K_w:
						thisplayer.y1 -= 1
						if thisplayer.y1 < 0:
							thisplayer.y1 = 24
					if event.key == pygame.K_s:
						thisplayer.y1 += 1
						if thisplayer.y1 > 24:
							thisplayer.y1 = 0
					if event.key == pygame.K_a:
						thisplayer.x1 -= 1
						if thisplayer.x1 < 0:
							thisplayer.x1 = 48
					if event.key == pygame.K_d:
						thisplayer.x1 += 1
						if thisplayer.x1 > 48:
							thisplayer.x1 = 0
					if event.key == pygame. K_i:
						thisplayer.y2 -= 1
						if thisplayer.y2 < 0:
							thisplayer.y2 = 24
					if event.key == pygame.K_k:
						thisplayer.y2 += 1
						if thisplayer.y2 > 24:
							thisplayer.y2 = 0
					if event.key == pygame.K_j:
						thisplayer.x2 -= 1
						if thisplayer.x2 < 0:
							thisplayer.x2 = 48
					if event.key == pygame.K_l:
						thisplayer.x2 += 1
						if thisplayer.x2 > 48:
							thisplayer.x2 = 0
				
		mouse_pos = pygame.mouse.get_pos()
		y = 0
		x = 0
		for i in range(1225):
			
			if x > 48:
				x = 0
				y += 1
			
			for f in unlockedchars:
				if thisplayer.x1 == f.cords[0] and thisplayer.y1 == f.cords[1]:
					dispchar = f
					thisplayer.battlers[0] = f.reBuild()
					break
				else:
					dispchar = NO
					thisplayer.battlers[0] = NO

			x += 1
			
		y = 0
		x = 0
		for i in range(1225):
			
			if x > 48:
				x = 0
				y += 1
			
			for f in unlockedchars:
				if thisplayer.x2 == f.cords[0] and thisplayer.y2 == f.cords[1]:
					dispchar2 = f
					thisplayer.battlers[1] = f.reBuild()
					break
				else:
					dispchar2 = NO
					thisplayer.battlers[1] = NO

			x += 1
			
		y = 0
		x = 0
		for i in range(1225):
			
			if x > 48:
				x = 0
				y += 1
			for f in unlockedchars:
				if thisplayer.x3 == f.cords[0] and thisplayer.y3 == f.cords[1]:
					dispchar2 = f
					thisplayer.battlers[2] = f.reBuild()
					break
				else:
					dispchar2 = NO
					thisplayer.battlers[2] = NO

			x += 1

		if hitDetect(mouse_pos, mouse_pos, [1079, 634], [1248, 698]):
			if thisplayer == player2:
				if mouse_down:
					if aitest:
						mult = False
						for i in player2.battlers:
							i.isAi = True
					theBattle = Battle("No name", player1.battlers, player2.battlers, defultarena, NoDial, mult, defulttheme, "")
					theBattle.battle()
					player1.reBuild()
					player2.reBuild()
					thisplayer = player1
					
					mouse_down = False
							
			if mouse_down:
				if mult == False and aitest == False:
					return player1.battlers
				else:
					thisplayer = player2
					mouse_down = False
					time.sleep(1)
		
		
		gScreen.fill(WHITE)
		gScreen.blit(menuui, [0, 0])
		x = 0
		y = 0
		
		for i in range(1225):
			loaded = False
			if x > 48:
				x = 0
				y += 1
			
			for f in unlockedchars:
				if f.cords[0] == x and f.cords[1] == y:
					gScreen.blit(f.img, [3 + 22*x,5 + 22*y])
					loaded = True
			
			if not loaded:
				gScreen.blit(lockedchar, [3 + 22*x,5 + 22*y])
				loaded = False
					
			x += 1
				
		gScreen.blit(selector1, [thisplayer.x1*22 + 1, thisplayer.y1*22 + 3])
		gScreen.blit(selector2, [thisplayer.x2*22 + 1, thisplayer.y2*22 + 3])
		gScreen.blit(selector3, [thisplayer.x3*22 + 1, thisplayer.y3*22 + 3])
		
		for i in range(len(thisplayer.battlers)):
			localbattler = thisplayer.battlers[i]
			#	gScreen.blit(dispchar2.image, [644, 370])
			gScreen.blit(localbattler.menuImg, [4, i * 47 + 559])
			gScreen.blit(font.render(localbattler.name, True, BLACK), [56, i * 47 + 559])
			
			atypes = ""
			for f in localbattler.types:
				atypes += f.name + " "
			gScreen.blit(font.render(atypes, True, BLACK), [56, i * 47 + 575 + 550])
			gScreen.blit(font.render("Str: " + str(localbattler.str) + "   Con: " + str(localbattler.con) + "   Int: " + str(localbattler.int) + "   Mdf: " + str(localbattler.mag) + "   Agil: " + str(localbattler.agil) + "   Crit: " + str(localbattler.crit), True, BLACK), [56, i * 47 + 574])
		
		if mouse_down:
			gScreen.blit(mouse_pointer2,mouse_pos)
		else:
			gScreen.blit(mouse_pointer,mouse_pos)
		
		cootheme.reset()
		pygame.display.flip()	
		clock.tick(60)

