import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

font=pygame.font.Font('arial.ttf',25)

class Direction(Enum):
    RIGHT=1
    LEFT=2
    UP=3
    DOWN=4

Point=namedtuple('Point','x,y')

WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE1=(0,0,255)
BLUE2=(0,100,255)
BLACK=(0,0,0)

BLOCK_SIZE=20
SPEED=20

class SnakeGame:
    
    # initializing game
    def __init__(self,w=640,h=480) :
        self.w=w
        self.h=h

        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Snake Game by @whothefisyash')
        self.clock=pygame.time.Clock()

        self.direction=Direction.RIGHT  #initial direction
        self.head=Point(self.w/2,self.h/2)
        self.snake=[
            self.head,
            Point(self.head.x - BLOCK_SIZE ,self.head.y),
            Point(self.head.x - (2*BLOCK_SIZE) ,self.head.y)
        ]
        self.score=0 
        self._place_food() #food is placed initially
    

    # placing food
    def _place_food(self):
        x=random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE) *BLOCK_SIZE
        y=random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE) *BLOCK_SIZE
        self.food= Point(x,y)
        if(self.food in self.snake): #if food is in snake then recursively call this fn
            self._place_food()
    

    
    def _is_collision(self):
        # hitting boundary
        if((self.head.x > self.w-BLOCK_SIZE) 
           or (self.head.x <0 ) 
           or (self.head.y > self.h-BLOCK_SIZE) 
           or (self.head.y<0) ):
            return True
        
        # hitting own body
        if(self.head in self.snake[1:]):
            return True
        
        return False


        
    def _update_ui(self):
        self.display.fill(BLACK)
        for i,pt in enumerate(self.snake):
            if i == 0:  # Head
                pygame.draw.rect(self.display, GREEN, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            else:
                # rectangle representing segment of snake
                pygame.draw.rect(self.display ,BLUE1,pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE))
                # rectangle smaller of size 12,12 for visual effect
                pygame.draw.rect(self.display ,BLUE2,pygame.Rect(pt.x+4,pt.y+4,12,12))
            
        # rectangle for food item 
        pygame.draw.rect(self.display,RED,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))
        
        text=font.render('Score : ' + str(self.score),True,WHITE)
        self.display.blit(text,[0,0]) #blit used to draw text on main display surface at co ordinate 0,0

        pygame.display.flip() #updates screen

    
    def _move(self,direction):
        x=self.head.x
        y=self.head.y

        if(direction == Direction.RIGHT):
            x=x+BLOCK_SIZE
        elif(direction == Direction.LEFT):
            x=x-BLOCK_SIZE
        elif(direction == Direction.DOWN):
            y=y+BLOCK_SIZE
        elif(direction == Direction.UP):
            y=y-BLOCK_SIZE
        
        self.head = Point(x,y)

    
    # playing game setup
    def play_step(self):

        # 1.collect user input
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                quit()
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_LEFT):
                    self.direction = Direction.LEFT
                elif(event.key == pygame.K_RIGHT):
                    self.direction = Direction.RIGHT
                elif(event.key == pygame.K_UP):
                    self.direction = Direction.UP
                elif(event.key == pygame.K_DOWN):
                    self.direction = Direction.DOWN
        
        # 2.move
        self._move(self.direction)  #updates head
        self.snake.insert(0,self.head)  #addds new head to beginning

        # 3.check if game is over or not
        game_over=False
        if(self._is_collision()):
            game_over=True
            return game_over,self.score
        
        # 4.placing new food
        if self.head == self.food:
            self.score=self.score+1
            self._place_food()
        else:
            self.snake.pop()

        # 5.update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6.return game over and score
        return game_over,self.score
            

if(__name__ == '__main__'):
    game=SnakeGame()

    while(True):
        game_over,score=game.play_step()

        if(game_over == True):
            break
    
    print('Final score :',score)

    pygame.quit()
