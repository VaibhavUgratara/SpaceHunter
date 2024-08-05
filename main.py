import pygame
import random
pygame.init()

screenX=576
screenY=360

gameWindow=pygame.display.set_mode((screenX,screenY))
clock=pygame.time.Clock()
caption=pygame.display.set_caption("Space Hunter")


def mainscreen():
    running=True
    pygame.mixer.music.load("audio/mainscreen.mp3")
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.play()
    start=pygame.image.load("images/mainscreen.png")
    start=pygame.transform.scale(start,(screenX,screenY))
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                gamestart()
                return
            if event.type==pygame.USEREVENT:
                pygame.mixer.music.play()

        gameWindow.blit(start,(0,0))
        pygame.display.flip()
        clock.tick(60)
        



def gamestart():
    asteroid=pygame.image.load("images/asteroid.png")
    asteroid=pygame.transform.scale(asteroid,(35,35))
    pygame.mixer.music.stop()
    bg=pygame.image.load("images/background.jpg")
    rocket1=pygame.image.load("images/rocket1.png")
    rocket1=pygame.transform.scale(rocket1,(75,75))
    rocket2=pygame.image.load("images/rocket2.png")
    rocket2=pygame.transform.scale(rocket2,(75,75))
    rocket3=pygame.image.load("images/rocket3.png")
    rocket3=pygame.transform.scale(rocket3,(75,75))

    rocket=[rocket1,rocket2,rocket3]
    running=True
    as_x=random.randint(0,screenX)
    as_y=0

    asteroid_list=[[as_x,as_y]]
    asteroid_velocity=1

    add_Asteroid=False
    r=0
    speed=0
    rocketX=250

    while running:
        rocket_rect=rocket[r].get_rect()
        rocket_rect.x=rocketX+11
        rocket_rect.y=290
        rocket_rect.w=50
        rocket_rect.h=60

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if not(rocketX<0):
                rocketX-=10
        if keys[pygame.K_RIGHT]:
            if not(rocketX>screenX-75):
                rocketX+=10
                
        gameWindow.blit(bg,(0,0))
        if(speed==5):
            r+=1
            if(r>2):
                r=0
            speed=0

        gameWindow.blit(rocket[r],(rocketX,280))
        as_rect=[]
        for i in asteroid_list:
            gameWindow.blit(asteroid,i)
            as_rect.append(asteroid.get_rect())

        for i in asteroid_list:
            i[1]+=asteroid_velocity
            j=asteroid_list.index(i)
            as_rect[j].x=i[0]
            as_rect[j].y=i[1]

        if(asteroid_list[0][1]>=screenY/2):
            if not add_Asteroid:
                as_X=random.randint(0,screenX-20)
                as_Y=-20
                asteroid_list.append([as_X,as_Y])
                add_Asteroid=True


        if(asteroid_list[0][1]>screenY):
            asteroid_list.pop(0)
            add_Asteroid=False

        for i in as_rect:
            if(rocket_rect.colliderect(i)):
                gameover()
                return

        speed+=1
        # pygame.draw.rect(gameWindow,(255,255,255),rocket_rect,2)
        pygame.display.flip()

        clock.tick(60)

def gameover():
    running=True
    over=pygame.image.load("images\gameover.jpg")
    over=pygame.transform.scale(over,(screenX,screenY))
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                gamestart()
                return
        
        gameWindow.blit(over,(0,0))
        pygame.display.flip()
        clock.tick(60)

mainscreen()
pygame.quit()