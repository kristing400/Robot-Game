import pygame,sys

class Struct(object):pass
data = Struct()
###########################CLASS#############################
class Button(object):
	def __init__(self,name,data,buttons = None):
		self.name = name
		self.bounds =database[name][0]
		self.lead = database[name][1]
	
	def drawText(self,canvas):
		if self.name =="Note1" or self.name =="Note2":
			name = "Note"
		elif self.name =="Stairs2":
			name = "Stairs"
		else:
			name = self.name
		x,y,_,_ = self.bounds
		text =data.font.render(name,True,(255,255,255))
		canvas.blit(text,(x,y-30))

class Item(Button):
	def __init__(self,name,data):
		Button.__init__(self,name,data)
		
		self.img = pygame.image.load("%s.png"%self.name)

	def drawItem(self,x,y,canvas):
		canvas.blit(self.img,(x,y))
###################################DATA########################
database = dict()
database["Ladder"] = (831,323,1001,434),None
database['Hammer'] = (840,245,972,378),None
database['Cupboard'] = (238,119,440,224),4
database['Drawers'] = (942,92,1068,273),5
database["Stairs"] = (712,77,853,236),7
database["Charger"] = (135,182,255,314),None
database["Note1"] = (228,101,337,136),None
database["Pot"] = None,None
database["Deposit Box"] = (1081,208,1180,500),None
database["Locked"] = (615,83,796,245),None
database["Bottle"] = (521,469,589,538),6
database["Key"] = (590,240,840,444),None
database["Plant"] = None,None
database["Lights"] = (283,32,375,139),None
database["Box"] = (33,415,171,514),None
database['Car'] = (219,353,556,500),"Car"
database['Pipes'] = (840,76,889,149),"Pipes"
database["Frame"] = (865,105,1013,276),None
database["Note2"] = (715,127,778,202),None
database["Stairs2"] = (847,226,1000,269), 1
database["Truck"] =  (297,146,598,284), None
###############################INIT##########################################3
def init(data):
	pygame.init()
	data.exit = False
	data.selectedItem = None
	data.gameOver = False
	data.size = width,height = 1200,700
	data.screen = pygame.display.set_mode(data.size)
	data.battery = 40
	data.items = []
	data.maxInventory = 5
	data.scenes = []
	data.currentScene =0#index of current scene
	data.subScene = 0
	data.loc = 0
	data.zoomIn = False
	data.drawersImg = pygame.image.load("Drawers.png")
	data.error = None
	data.speed = 1
	data.count = 0
	data.maxCount = 40
	data.fadeCount = 0
	data.font = pygame.font.Font("pokemon_pixel_font.ttf",30)
	data.fade = [False,True,False,False]
	data.buttons1 = [Button("Lights",data),Button("Box",data),Button("Ladder",data),Button("Cupboard",data),Button("Drawers",data),Button("Bottle",data),Button("Stairs",data)]
	data.cupboard = [Item("Hammer",data)]
	data.drawers = [Button("Locked",data),Button("Frame",data)]
	data.bottle = [Item("Key",data)]
	data.scene2 = [Button("Charger",data),Button("Deposit Box",data), Button("Car",data),Button("Pipes",data),Button("Stairs2",data),Button("Truck", data)]
	data.car = [Item("Note1",data)]
	data.pipes = [Item("Note2",data)]

#########################drawFunctions###############################

def drawBag(data):
	toolbar = pygame.image.load("toolbar.png")
	data.screen.blit(toolbar,(0,0))
	text = "Click to use items."
	font = pygame.font.Font("pokemon_pixel_font.ttf", 20)
	ins = font.render(text,True,(255,255,255))
	data.screen.blit(ins,(245,620))
	drawBattery(data)
	x,y = 396,586
	for item in data.items:
		# if item.name =="Note1":
		# 	img = pygame.image.load("1.png")
		# elif item.name =="Note2":
		# 	img = pygame.image.load("2.png")
		img = item.img
		img = pygame.transform.scale(img,(82,82))
		data.screen.blit(img,(x,y))
		x+=135

def fadeIn(data,image,j):
	for i in range (0,225,5):
	    data.screen.fill((0,0,0))    
	    image.set_alpha(i)
	    data.screen.blit(image,(0,5))
	    pygame.display.flip()
	    pygame.time.delay(0)
	pygame.time.delay(1000)
	data.fade[j] = True
    
def drawbackArrow(data):
	if data.zoomIn and data.currentScene <3:
		img = pygame.image.load("arrow.png")
		data.screen.blit(img,(1033,13))

def drawUnderground(data):#scene1
	img = pygame.image.load("scene1.png")
	if data.fade[1] ==False:
		fadeIn(data,img,1)
		data.fadeCount+=1
		if data.fadeCount<=1:
			data.fade[1] = False
	else:

		data.screen.blit(img,(0,5))
		if data.subScene==0:
			text = "... I finally woke up..."
			quote =data.font.render(text,True,(255,255,255))
			data.screen.blit(quote,(30,610))
		elif data.subScene==1:
			text = "... I need to leave this basement before my battery runs out."
			quote =data.font.render(text,True,(255,255,255))
			data.screen.blit(quote,(30,610))
		elif data.subScene ==2:
			text = "But there is something very important that I need to find in this room first."
			quote =data.font.render(text,True,(255,255,255))
			data.screen.blit(quote,(30,610))
		else:
			
			if data.subScene ==4:
				zoomIn = pygame.image.load("cupboard.png")
				data.screen.blit(zoomIn,(0,5))
				for item in data.cupboard:
					x,y,_,_ = item.bounds
					item.drawItem(x,y,data.screen)
			elif data.subScene ==5:
				zoomIn = data.drawersImg
				data.screen.blit(zoomIn,(0,5))
			elif data.subScene ==6:
				zoomIn = pygame.image.load("bottle.png")
				data.screen.blit(zoomIn,(0,5))
				for item in data.bottle:
					x,y,_,_ = item.bounds
					item.drawItem(x,y,data.screen)
			

# def drawBag(data):


def drawIntro(data):#index 0 
	img = pygame.image.load("intro1.png")
	data.screen.blit(img,(data.loc,5))
	intro = None
	if data.subScene == 0:
		play = data.font.render("Play",True,(255,255,255))
		data.screen.blit(play,(580,610))
	else:
		if data.subScene ==1:
			intro = "In the year 2075, the world has become devoured by the selfishness and greed of humans."
		if data.subScene ==2:
			intro ="With every individual striving to be the most powerful being, the Earth has turned into hell."
		if data.subScene ==3:
			intro = "Men sought to kill each other with poisonous weapons and nuclear bombs."
		if data.subScene==4:
			intro = "It didn't take long until the atmosphere can no longer provide basic human needs."
		if data.subScene ==5:
			intro = "Living organisms became extinct one after another, and the world became lifeless."
		if data.subScene ==6:
			intro = "However, there is only one, a lonely robot built through great minds of mankind who calls this planet ""home""."
			data.screen.fill((0,0,0))
			img = pygame.image.load("robot.png")
			img = pygame.transform.scale(img,(1200,550))
			if data.fade[0] == False:
				fadeIn(data,img,0)
			else:
				data.screen.blit(img,(0,5))
		if data.subScene==7:
			data.screen.fill((0,0,0))
		text =data.font.render(intro,True,(255,255,255))
		data.screen.blit(text,(30,610))
def drawFinal(data):
	if data.subScene == 0:
		img = pygame.image.load("final.png")
		if data.fade[2] ==False:
			fadeIn(data,img,2)
		else:
			data.screen.blit(img,(0,5))
	else:
		img = pygame.image.load("colorintro.png")
		# if data.fade[3] ==False:
		# 	fadeIn(data,img,3)
		# else:
		data.screen.blit(img,(data.loc,5))
		restart = data.font.render("Restart",True, (255,255,255))
		data.screen.blit(restart,(575,610))


def drawBattery(data):
	if data.battery>50:
		color = 255,255,255
	else:
		color = 255,0,0
	frame = pygame.image.load("battery.png")
	percent = data.battery*0.01
	rect = 47,608,round(104*percent),37
	pygame.draw.rect(data.screen,color,rect)
	data.screen.blit(frame,(41,606))
	clicksLeft = str(data.battery/2)
	text = data.font.render(clicksLeft,True,(255,255,255))
	data.screen.blit(text,(175,616))
def drawError(data):
	if data.error!= None:
		if data.error == "stairs":
			text = "I can't leave this room without finding the important item!"
		elif data.error == "error":
			text = "Nothing interesting here."
		elif data.error == "key":
			text = "Doesn't seem like I can take this bottle, but I see a key."
		elif data.error == "plant":
			text = "Can't open."
		elif data.error =='find':
			text = "I finally found the last valuable thing left on Earth. But I need to make sure it will survive!"
		elif data.error == "puzzle":
			text = "Looks like some sort of blueprint. I need to find the missing pieces."
		elif data.error =="complete":
			text = "I completed the blueprint and a hidden door unlocked! I've obtained the flower pot that can sustian life!"
		if data.count<data.maxCount:
			append = data.font.render(text,True,(255,255,255))
			data.screen.blit(append,(30,610))
		else:
			data.error = None
			data.count = 0

def drawGameOver(data):
	data.screen.fill((0,0,0))
	if data.subScene ==1:
		text = "Looks like I won't be able to make it...Need to rest and recharge.."
		quote = data.font.render(text,True,(255,255,255))
		data.screen.blit(quote,(100,350))
def drawUpstairs(data):
	if data.zoomIn==False:
		img = pygame.image.load("scene2.png")
		data.screen.blit(img,(0,5))
	else:
		img = pygame.image.load("%s.png" % data.zoomIn.lead)
		data.screen.blit(img,(0,5))
		if data.zoomIn.name =="Car":
			for item in data.car:
				item.drawItem(0,5,data.screen)
		elif data.zoomIn.name =="Pipes":
			for item in data.pipes:
				item.drawItem(0,5,data.screen)
def redrawAll():
	if data.gameOver:
		drawGameOver(data)
	else:
		if data.currentScene == 0:
			drawIntro(data)
		if data.currentScene==1:
			drawUnderground(data)
			if data.subScene>2:
				if data.error== None:
					drawBag(data)
				drawError(data)
		if data.currentScene ==2:
			drawUpstairs(data)
			if data.error == None:
				drawBag(data)
			drawError(data)

		if data.currentScene==3:
			drawFinal(data)
		drawbackArrow(data)

##############################MOUSE######################
def isLegal(data):
	if data.subScene ==3:
			for item in data.items:
				if item.name =="Plant":
					return True
			return False
	elif data.selectedItem == None:
		return False
	else:

		if data.subScene ==5:
			if data.selectedItem.name =="Key":
				return True
			else:
				return False
		elif data.subScene ==6:
			if data.selectedItem.name =="Hammer":
				return True
			else: return False


def undergroundMouse(data,mx,my):#index:1
	if data.subScene <=2 and data.fade[1]:
		data.subScene+=1
	elif data.fade[1]:
		data.battery-=2
		if data.subScene ==3:
			for button in data.buttons1:
				if inBounds(mx,my,button.bounds):
					if button.name =="Stairs":
						if isLegal(data):
							data.subScene = 7
						else:
							data.error = "stairs"

					elif button.lead != None:
						data.subScene = button.lead
						data.zoomIn =True
					else:
						data.error = "error"

		else:
			if inBackBounds(mx,my):
					data.subScene =3
					data.zoomIn = False
			elif data.subScene ==4:
				for button in data.cupboard:
					if inBounds(mx,my,button.bounds):
						data.items.append(button)
						data.cupboard.remove(button)
			elif data.subScene ==6:
				for button in data.bottle:
					if inBounds(mx,my,button.bounds):
						if isLegal(data):
							data.items.append(button)
							data.bottle.remove(button)
						else:
							data.error ="key"
			elif data.subScene ==5:
				for button in data.drawers:
					if inBounds(mx,my,button.bounds):
						if button.name is "Locked":
							if isLegal(data):
								data.items.append(Item("Plant",data))
								data.error = "find"
							else:
								data.error = "plant"
						elif button.name is "Frame":
							if completedPuzzle(data):
								l = []
								for item in data.items:
									if item.name !="Note1" and item.name !="Note2":
										l.append(item)
								data.items = l
								data.items.append(Item("Pot",data))
								data.drawersImg = pygame.image.load("complete.png")
								data.error = "complete"
							else:
								data.error = "puzzle"

		if data.selectedItem!= None:
			if data.selectedItem.name is "Pot" or data.selectedItem.name is "Plant":
				x0,y0= 396,586
				for item in data.items:
					x1,y1 = x0+82,y0+82
					if inBounds(mx,my,(x0,y0,x1,y1)):
						if data.selectedItem.name == "Pot" and item.name == "Plant":
							data.currentScene = 3
							data.subScene = 0
						elif data.selectedItem.name == "Plant" and item.name == "Pot":
							data.currentScene = 3
							data.subScene = 0
					x0+=140
			data.selectedItem = None
		useItems(data,mx,my)
def completedPuzzle(data):
	count = 0
	for item in data.items:
		if item.name == "Note1" or item.name =="Note2":
			count+=1
	return count ==2

def useItems(data,mx,my):
	x0,y0= 396,586
	for item in data.items:
		x1,y1 = x0+82,y0+82
		if inBounds(mx,my,(x0,y0,x1,y1)):
			data.selectedItem = item
		x0+=140

def finalMouse(data,x,y):
	if data.fade[2] and data.subScene ==0:
		data.subScene+=1
	elif data.subScene==1:
		if restartBounds(x,y):
			init(data)
			


def introMouse(data,x,y):
	if data.subScene >=7:
		data.currentScene+=1
		data.subScene = 0
	elif data.subScene==0:
		if inStartBounds(x,y):
			data.subScene+=1
	else:
		data.subScene+=1
def scene2Mouse(data,x,y):
	data.battery-=1
	if data.zoomIn== False:
		for button in data.scene2:
			if inBounds(x,y,button.bounds):
				if button.name =="Charger":
					data.battery = 40
				elif button.name =="Stairs2":
					data.currentScene = 1
					data.subScene = 3
				elif button.lead != None:
					data.zoomIn = button
				else:
					data.error = "error"
	else:
		if inBackBounds(x,y):	data.zoomIn = False
		elif data.zoomIn.name =="Car":
			for item in data.car:
				if inBounds(x,y,item.bounds):
					item.img = pygame.image.load("1.png")
					data.items.append(item)
					data.car.remove(item)
		elif data.zoomIn.name =="Pipes":
			for item in data.pipes:
				if inBounds(x,y,item.bounds):
					item.img = pygame.image.load("2.png")
					data.items.append(item)
					data.pipes.remove(item)
	if data.selectedItem!= None:
		data.selectedItem = None
	useItems(data,x,y)

def mouse(data):
	x,y = pygame.mouse.get_pos()
	if data.gameOver:
		if data.subScene >=2:
			init(data)
			data.currentScene = 1
		data.subScene+=1
	else:
		if data.currentScene == 0:
			introMouse(data,x,y)
		elif data.currentScene ==1:
			undergroundMouse(data,x,y)
		elif data.currentScene ==2:
			scene2Mouse(data,x,y)
		else:
			finalMouse(data,x,y)
		
###############################BOUNDS######################
def inBackBounds(x,y):
	x0,y0,x1,y1 = 1033,13,1191,95
	return x<x1 and x>x0 and y>y0 and y<y1
def restartBounds(x,y):
	x0,y0,x1,y1 = 575,610,650,637
	return x<x1 and x>x0 and y>y0 and y<y1

def inBounds(x,y,bounds):
	x0,y0,x1,y1 = bounds
	return x<x1 and x>x0 and y>y0 and y<y1
def inStartBounds(x,y):
	x0,y0,x1,y1 = 580,610,622,637
	return x<x1 and x>x0 and y>y0 and y<y1
###########################HOVER###################
def hover(data):
	if data.gameOver==False:
		x,y = pygame.mouse.get_pos()
		if data.currentScene == 0 and data.subScene == 0:
			if inStartBounds(x,y):
				pygame.draw.rect(data.screen,(255,255,255),(576,610,44,27),1)
		elif data.currentScene == 1 and data.subScene>2:
			if data.subScene ==3:
				for button in data.buttons1:
					if inBounds(x,y,button.bounds):
						button.drawText(data.screen)
			elif data.subScene ==4:
				for button in data.cupboard:
					if inBounds(x,y,button.bounds):
						button.drawText(data.screen)
			elif data.subScene ==5:
				for button in data.drawers:
					if inBounds(x,y,button.bounds):
						button.drawText(data.screen)
			elif data.subScene ==6:
				for button in data.bottle:
					if inBounds(x,y,button.bounds):
						button.drawText(data.screen)
			drawUseItem(data,x,y)
		elif data.currentScene ==2:
			if data.zoomIn ==False:
				for button in data.scene2:
					if inBounds(x,y,button.bounds):
						button.drawText(data.screen)
			else:
				itemsHover(x,y,data)
			drawUseItem(data,x,y)
		elif data.currentScene==3 and data.subScene ==1:
			if restartBounds(x,y):
				pygame.draw.rect(data.screen,(255,255,255),(570,610,83,27),2)

def itemsHover(x,y,data):
	if data.zoomIn.name =="Car":
		for item in data.car:
			if inBounds(x,y,item.bounds):
				item.drawText(data.screen)
	elif data.zoomIn.name =="Pipes":
		for item in data.pipes:
			if inBounds(x,y,item.bounds):
				item.drawText(data.screen)

def drawUseItem(data,x,y):
	if data.selectedItem != None:
		img = pygame.transform.scale(data.selectedItem.img,(200,200))
		data.screen.blit(img, (x-100,y-100))
###################################TIMER FIRED####################################
def timerFired(data):
	if data.gameOver!= True:
		if data.currentScene == 0:
			intro(data)
		elif data.currentScene ==1:
			if data.error != None:
				data.count+=1
			else:	underground(data)
		elif data.currentScene ==2:
			if data.error != None:
				data.count+=1
		else:
			intro(data)
		if data.battery <=0:
				data.gameOver = True
				data.subScene = 0


def intro(data):#exit intro once going thru all intro frames
	data.loc -=data.speed
	if data.loc <=-200 or data.loc >= 0:
		data.speed *=-1

def underground(data):
	if data.subScene ==7:
		data.currentScene+=1
		data.subScene = 0
#######################RUN FUNCTION#####################################
def game():#runs game
	init(data)
	while data.exit ==False:
			# if data.gameOver:
			# 	pygame.time.delay(1000)
		for event in pygame.event.get():
			if event.type==pygame.QUIT: sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN: mouse(data)
		data.screen.fill((0,0,0))
		timerFired(data)
		redrawAll()
		hover(data)
		pygame.display.flip()
		if data.subScene==6 and data.currentScene==0:
			pygame.time.delay(2000)



game()