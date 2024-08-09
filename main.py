import pygame
import random
import sys
pygame.init()

screenX=700
screenY=400

gameWindow=pygame.display.set_mode((screenX,screenY))
clock=pygame.time.Clock()
caption=pygame.display.set_caption("Space Hunter")


class Button:
    def __init__(self,image,x,y,scale):
        height=image.get_height()
        width=image.get_width()
        self.image=pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.clicked=False

    def render_button(self):
        action=False
        mouse_pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]==1 and not(self.clicked):
                action=True
                self.clicked=True
        if pygame.mouse.get_pressed()[0]==0:
            self.clicked=False        
        gameWindow.blit(self.image,(self.rect.x,self.rect.y))
        return action



def text_screen(text,color,x,y,f_s=30):
    font=pygame.font.SysFont(None,f_s)
    screen_text=font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])



def mainscreen():
    running=True
    start_img=pygame.image.load("images/start.png")
    start_btn=Button(start_img,270,280,0.3)
    pygame.mixer.music.load("audio/mainscreen.mp3")
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.play()
    start=pygame.image.load("images/mainscreen.png")
    start=pygame.transform.scale(start,(screenX,screenY))
    start_cl=False
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return 0
            if event.type==pygame.USEREVENT:
                pygame.mixer.music.play()
        if start_cl:
            return "Start"
        gameWindow.blit(start,(0,0))
        start_cl=start_btn.render_button()
        text_screen("Use left and right arrow keys to play",(255,255,255),(screenX/2 + 80),screenY-screenY/7,18)
        pygame.display.flip()
        clock.tick(60)
        



def gamestart():
    asteroid_size=35
    rocket_size=90
    asteroid=pygame.image.load("images/asteroid.png")
    asteroid=pygame.transform.scale(asteroid,(asteroid_size,asteroid_size))
    pygame.mixer.music.stop()
    pygame.mixer.music.load("audio/gamesound.mp3")
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    bg=pygame.image.load("images/background.png")
    rocket=[]
    btn_pause=pygame.image.load("images/pause.png")
    pause_btn=Button(btn_pause,5,5,0.015)
    for i in range(0,10):
        url=f"images/rocket{i}.png"
        rockload=pygame.image.load(url)
        rockload=pygame.transform.scale(rockload,(rocket_size,rocket_size))
        rocket.append(rockload)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return 0
        gameWindow.fill((0,0,0))
        text_screen("Loading...",(255,255,255),(screenX/2)-40,screenY/2)
        pygame.display.flip()
    pygame.mixer.music.play()
    running=True
    as_x=random.randint(0,screenX-40)
    as_y=0

    asteroid_list=[[as_x,as_y]]
    asteroid_velocity=3

    r=0
    rocketX=250
    gamePause=False
    while running:
        rocket_rect=rocket[r].get_rect()
        rocket_rect.x=rocketX+25
        rocket_rect.y=screenY-80
        rocket_rect.w=30
        rocket_rect.h=60

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return 0
            if event.type==pygame.USEREVENT:
                pygame.mixer.music.play()
            if event.type==pygame.KEYDOWN and gamePause:
                gamePause=False
                continue
        if gamePause:
            gameWindow.fill((0,0,0))
            text_screen("Game Paused",(255,255,255),(screenX/2)-120,(screenY/2)-50,50)
            text_screen("Press any key to resume",(255,255,255),(screenX/2)-120,(screenY/2)+10)
            pygame.display.update()
            continue

        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if not(rocketX<0):
                rocketX-=15
        if keys[pygame.K_RIGHT]:
            if not(rocketX>screenX-rocket_size):
                rocketX+=15
                
        gameWindow.blit(bg,(0,0))
        r+=1
        if(r>9):
            r=0

        gameWindow.blit(rocket[r],(rocketX,screenY-90))
        as_rect=[]
        for i in asteroid_list:
            gameWindow.blit(asteroid,i)
            as_rect.append(asteroid.get_rect())

        for i in asteroid_list:
            i[1]+=asteroid_velocity
            j=asteroid_list.index(i)
            as_rect[j].x=i[0]
            as_rect[j].y=i[1]

        if(asteroid_list[len(asteroid_list)-1][1]>=screenY/3):
            as_X=random.randint(0,screenX-40)
            as_Y=-20
            asteroid_list.append([as_X,as_Y])


        if(asteroid_list[0][1]>screenY):
            asteroid_list.pop(0)

        for i in as_rect:
            if(rocket_rect.colliderect(i)):
                return "End"

        # pygame.draw.rect(gameWindow,(255,255,255),rocket_rect,2)
        gamePause=pause_btn.render_button()
        pygame.display.flip()

        clock.tick(60)

def gameover():
    pygame.mixer.music.stop()
    running=True
    over=pygame.image.load("images\gameover.jpg")
    over=pygame.transform.scale(over,(screenX,screenY))
    start_img=pygame.image.load("images/start.png")
    start_btn=Button(start_img,270,280,0.3)
    start_cl=False
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return 0
        
        gameWindow.blit(over,(0,0))
        text_screen("Use left and right arrow keys to play",(255,255,255),(screenX/3),screenY/2 + 50,18)
        if start_cl:
            return "Start"
        start_cl=start_btn.render_button()
        pygame.display.flip()
        clock.tick(60)


#Some simple steps to prevent excess memory usage
i=0
while True:
    if i==0:
        j=mainscreen()
    elif i==1:
        j=gamestart()
    elif i==2:
        j=gameover()
    if(j==0):
        break
    elif(j=="Start"):
        i=1
    elif(j=="End"):
        i=2
pygame.quit()