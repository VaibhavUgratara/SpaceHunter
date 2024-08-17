import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'
import pygame, random, json,string

pygame.init()

screenX=700
screenY=400

gameWindow=pygame.display.set_mode((screenX,screenY))
clock=pygame.time.Clock()
caption=pygame.display.set_caption("Space Hunter")


pygame.mixer.init()

class HighScore:
    def __init__(self):
        if not (os.path.exists("score.json")):
            with open("score.json","w") as highscore:
                params={"HighScore":0}
                json.dump(params,highscore)
                highscore.close()
        with open("score.json","r") as highscore:
            self.data=json.load(highscore)
            highscore.close()

    def write_score(self,player_score):
        if int(self.data["HighScore"]) < player_score:
             with open("score.json","w") as highscore:
                params={"HighScore":player_score}
                json.dump(params,highscore)
                highscore.close()
                self.data["HighScore"]=player_score
        



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

score=0
high_Score=HighScore()
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
        text_screen("Use left and right arrow keys to play",(255,255,255),(screenX/2 + 80),screenY-screenY/7,20)
        text_screen("and spacebar to shoot",(255,255,255),(screenX/2 + 80),360,20)
        pygame.display.flip()
        clock.tick(60)
        



def gamestart():
    for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return 0
            
    gameWindow.fill((0,0,0))
    text_screen("Loading...",(255,255,255),(screenX/2)-40,screenY/2)
    pygame.display.flip()
    global high_Score,score
    # print(high_Score.data["HighScore"])
    laser_sound=pygame.mixer.Sound("audio/laser.mp3")
    explosion_sound=pygame.mixer.Sound("audio/explosion.mp3")
    score=0
    asteroid_size=35
    rocket_size=90
    asteroid=pygame.image.load("images/asteroid.png")
    asteroid=pygame.transform.scale(asteroid,(asteroid_size,asteroid_size))
    laser=pygame.image.load("images/laser.png")
    laser=pygame.transform.scale(laser,(15,30))
    explosion=pygame.image.load("images/explosion.png")
    explosion=pygame.transform.scale(explosion,(asteroid_size+2,asteroid_size+2))
    pygame.mixer.music.stop()
    pygame.mixer.music.load("audio/gamesound.mp3")
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    bg=pygame.image.load("images/background.png")
    rocket=[]
    btn_pause=pygame.image.load("images/pause.png")
    btn_play=pygame.image.load("images/play.png")
    pause_btn=Button(btn_pause,5,5,0.015)
    play_btn=Button(btn_play,300,150,0.05)
    for i in range(0,10):
        url=f"images/rocket{i}.png"
        rockload=pygame.image.load(url)
        rockload=pygame.transform.scale(rockload,(rocket_size,rocket_size))
        rocket.append(rockload)

    pygame.mixer.music.play()
    running=True
    as_x=random.randint(0,screenX-40)
    as_y=0

    asteroid_list=[[as_x,as_y]]
    asteroid_velocity=3

    r=0
    rocketX=250
    gamePause=False
    pause_text=False
    laser_list=[]
    boost_time=0
    while running:
        if boost_time==500:
            asteroid_velocity+=0.5
            boost_time=0
        rocket_rect=rocket[r].get_rect()
        rocket_rect.x=rocketX+25
        rocket_rect.y=screenY-80
        rocket_rect.w=30
        rocket_rect.h=50

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return 0
            if event.type==pygame.USEREVENT:
                pygame.mixer.music.play()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    laser_list.append([rocket_rect.x+7,rocket_rect.y-20])
                    laser_sound.play()
                    

        if gamePause:
            if not pause_text:
                text_screen("Game Paused",(255,255,255),240,(screenY/2)-100,50)
                pause_text=True
            gamePause=play_btn.render_button()
            if(gamePause):
                gamePause=False
                pause_text=False
            else:
                gamePause=True
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
        hi_score=string.Template("High-Score: $x")
        if score>int(high_Score.data["HighScore"]):
            hi_score=hi_score.substitute({"x":score})
        else:
            hi_score=hi_score.substitute({"x":high_Score.data["HighScore"]})
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
            # pygame.draw.rect(gameWindow,(255,255,255),(as_rect[j]),2)

        laser_rect=[]
        for i in laser_list:
            gameWindow.blit(laser,i)
            laser_rect.append(laser.get_rect())
            i[1]-=10
            j=laser_list.index(i)
            laser_rect[j].x=i[0]
            laser_rect[j].y=i[1]+10
            # pygame.draw.rect(gameWindow,(255,255,255),(laser_rect[j]),2)

        for i in as_rect:
            if(rocket_rect.colliderect(i)):
                return "End"
            for j in laser_rect:
                if(j.colliderect(i)):
                    score+=1
                    gameWindow.blit(explosion,i)
                    explosion_sound.play()
                    try:
                        asteroid_list.pop(as_rect.index(i))
                        laser_list.pop(laser_rect.index(j))
                        laser_rect.pop(laser_rect.index(j))
                    except:
                        pass

        # pygame.draw.rect(gameWindow,(255,255,255),rocket_rect,2)
        if len(asteroid_list)>0:
            if(asteroid_list[len(asteroid_list)-1][1]>=screenY/3):
                as_X=random.randint(0,screenX-40)
                as_Y=-20
                asteroid_list.append([as_X,as_Y])
            if(asteroid_list[0][1]>screenY):
                asteroid_list.pop(0)
        else:
            asteroid_list=[[random.randint(0,screenX-40),as_y]]
        if(len(laser_list)>0) and (laser_list[0][1]<-30):
            laser_list.pop(0)
        gamePause=pause_btn.render_button()
        text_screen(f"Score: {score}",(255,255,255),60,10)
        text_screen(f"{hi_score}",(255,255,255),screenX-150,10)
        pygame.display.flip()

        clock.tick(40)
        boost_time+=1

def gameover():
    global score,high_Score
    pygame.mixer.music.stop()
    running=True
    over=pygame.image.load("images\gameover.jpg")
    over=pygame.transform.scale(over,(screenX,screenY))
    start_img=pygame.image.load("images/start.png")
    start_btn=Button(start_img,270,280,0.3)
    start_cl=False
    high_Score.write_score(score)
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return 0
        
        gameWindow.blit(over,(0,0))
        text_screen("Use left and right arrow keys to play and spacebar to shoot",(255,255,255),180,screenY/2 + 50,18)
        text_screen(f"Your score {score}",(255,255,255),(screenX/2) - 45,(screenY/2) +20 + 50,25)
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