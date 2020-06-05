## 导入相关模块
import random
import pygame
import sys

from pygame.locals import *
#from button import Button


snake_speed = 6 #贪吃蛇的速度
windows_width = 800
windows_height = 600 #游戏窗口的大小
cell_size = 20       #贪吃蛇身体方块大小,注意身体大小必须能被窗口长宽整除

''' #初始化区
由于我们的贪吃蛇是有大小尺寸的, 因此地图的实际尺寸是相对于贪吃蛇的大小尺寸而言的
'''
map_width = int(windows_width / cell_size)
map_height = int(windows_height / cell_size)

# 颜色定义
white = (255, 255, 255)
black = (0, 0, 0)
gray = (230, 230, 230)
darkGray = (40, 40, 40)
darkGreen = (0, 155, 0)
darkRed = (116,0,0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
darkBlue =(0,0, 139)



BG_COLOR = black #游戏背景颜色

ImageRule_up='game_rule_up.png'
ImageRule_down='game_rule_down.png'
ImageStart_up='game_start_up.png'
ImageStart_down='game_start_down.png'
ImageOver_up='game_over_up.png'
ImageOver_down='game_over_down.png'
ImageRe_up='restart_up.png'
ImageRe_down='restart_down.png'


# 定义方向
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

HEAD = 0 #贪吃蛇头部下标


#初始化并播放背景音乐
pygame.mixer.init()  #初始化混音器
pygame.mixer.music.load('7895.wav')  #加载背景音乐
pygame.mixer.music.set_volume(0.2)  #设置音量
pygame.mixer.music.play()   #播放背景音乐


#主函数
def main():
	pygame.init() # 模块初始化
	snake_speed_clock = pygame.time.Clock() # 创建Pygame时钟对象
	screen = pygame.display.set_mode((windows_width, windows_height)) #
	screen.fill(white)

	pygame.display.set_caption("SNAKE~s") #设置标题
	show_start_info(screen,snake_speed_clock)               #欢迎信息
	while True:
            	 running_game(screen, snake_speed_clock)
            	 show_gameover_info(screen)
        
#游戏运行主体
def running_game(screen,snake_speed_clock):
        startx1 = random.randint(3, map_width - 8) #开始位置
        starty1 = random.randint(3, map_height - 8)
        startx2 = random.randint(8, map_width - 8) #开始位置
        starty2 = random.randint(8, map_height - 8)
        snake1_coords = [{'x': startx1, 'y': starty1},  #初始贪吃蛇
                  {'x': startx1 - 1, 'y': starty1},
                  {'x': startx1 - 2, 'y': starty1}]
        snake2_coords = [{'x': startx2, 'y': starty2},  #初始贪吃蛇
                  {'x': startx2 - 1, 'y': starty2},
                  {'x': startx2 - 2, 'y': starty2}]

        direction1 ='right'        #  开始时向右移动
        direction2 = 'up'
        

       
        food = get_random_location()     #实物随机位置

        while True:
                for event in pygame.event.get():
                        if event.type == QUIT:
                                terminate()
                        elif event.type == KEYDOWN:
                                #方向键控制玩家一
                                if event.key == K_LEFT  and direction1 != 'right':
                                        direction1 = 'left'
                                if event.key == K_RIGHT  and direction1 != 'left':
                                        direction1 = 'right'
                                if event.key == K_UP and direction1 != 'dowm':
                                        direction1 = 'up'
                                if event.key == K_DOWN  and direction1 != 'up':
                                        direction1 = 'down'
                                #‘W’‘A’‘S’‘D’控制玩家2
                                if  event.key == K_d and direction2 != 'left':
                                        direction2 = 'right'
                                if  event.key == K_w and direction2 != 'down':
                                        direction2 = 'up'
                                if  event.key == K_s and direction2 != 'up':
                                        direction2 = 'down'
                                if  event.key == K_a and direction2 != 'right':
                                        direction2 = 'left'
                                if event.key == K_ESCAPE:
                                        terminate()

                move_snake(direction1, snake1_coords) #移动蛇
                move_snake(direction2, snake2_coords) #移动蛇

                ret1 = snake_is_alive(snake1_coords)
                ret2 = snake_is_alive(snake2_coords)
                ret3=not ret1
                ret4=not ret2
                if ret3  :
                        break
                
                snake_is_eat_food1(snake1_coords, food,screen) #判断蛇是否吃到食物
                snake_is_eat_food2(snake2_coords, food,screen)
		
                screen.fill(BG_COLOR)
                draw_grid(screen)
                draw_snake1(screen, snake1_coords,blue)
                draw_snake2(screen, snake2_coords,red)
                draw_food(screen, food)
                draw_score1(screen, len(snake1_coords) - 3)
                draw_score2(screen, len(snake2_coords) - 3)
                pygame.display.update()
                snake_speed_clock.tick(snake_speed) #控制fps

def drawPressKeyMsg(screen):
        BASICFONT = pygame.font.Font('myfont.ttf', 18)
        pressKeySurf = BASICFONT.render('Press a key to play.', True, white)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (windows_width - 200, windows_height - 30)
        screen.blit(pressKeySurf, pressKeyRect)
		
#定义一个按钮类
class Button(object):
    def __init__(self, upimage, downimage,position):
        self.imageUp = pygame.image.load(upimage).convert_alpha()
        self.imageDown = pygame.image.load(downimage).convert_alpha()
        self.position = position
        self.game_start = False
        
    def isOver(self):
        point_x,point_y = pygame.mouse.get_pos()
        x, y = self. position
        w, h = self.imageUp.get_size()

        in_x = x - 200 < point_x < x + 200
        in_y = y - 300 < point_y < y + 300
        return in_x and in_y

    def render(self,screen):
        w, h = self.imageUp.get_size()
        x, y = self.position
        
        if self.isOver():
            screen.blit(self.imageDown, (x-400,y-300))
        else:
            screen.blit(self.imageUp, (x-400, y-300))
    def isStart(self):
        if self.isOver():
            b1,b2,b3 = pygame.mouse.get_pressed()
            if b1 == 1:
                self.game_start = True
                #bg_sound.play_pause()
                #btn_sound.play_sound()
                #bg_sound.play_sound()


def ran_color():
        colorArr=[white,gray,darkGray,darkGreen,darkRed,green,red,blue,darkBlue]
        i=random.randint(0,8)
        color=colorArr[i]
        return color
        

#将食物画出来
def draw_food(screen, food):
        x = food['x'] * cell_size
        y = food['y'] * cell_size
        appleRect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(screen, ran_color(), appleRect)
#将贪吃蛇画出来
def draw_snake1(screen, snake_coords,color):
        for coord in snake_coords:
                x = coord['x'] * cell_size
                y = coord['y'] * cell_size
                wormSegmentRect = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(screen, darkBlue, wormSegmentRect)
                wormInnerSegmentRect = pygame.Rect(                #蛇身子里面的第二层亮绿色
                        x + 4, y + 4, cell_size - 8, cell_size - 8)
                pygame.draw.rect(screen, color, wormInnerSegmentRect)
def draw_snake2(screen, snake_coords,color):
        for coord in snake_coords:
                x = coord['x'] * cell_size
                y = coord['y'] * cell_size
                wormSegmentRect = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(screen, darkRed, wormSegmentRect)
                wormInnerSegmentRect = pygame.Rect(                #蛇身子里面的第二层亮绿色
                        x + 4, y + 4, cell_size - 8, cell_size - 8)
                pygame.draw.rect(screen,color, wormInnerSegmentRect)
#画网格
def draw_grid(screen):
        for x in range(0, windows_width, cell_size):  # draw 水平 lines
                pygame.draw.line(screen, darkGray, (x, 0), (x, windows_height))
        for y in range(0, windows_height, cell_size):  # draw 垂直 lines
                pygame.draw.line(screen, darkGray, (0, y), (windows_width, y))
#移动贪吃蛇
def move_snake(direction, snake_coords):
        if direction == 'up':
                newHead = {'x': snake_coords[HEAD]['x'], 'y': snake_coords[HEAD]['y'] - 1}
        elif direction == 'down':
                newHead = {'x': snake_coords[HEAD]['x'], 'y': snake_coords[HEAD]['y'] + 1}
        elif direction == 'left':
                newHead = {'x': snake_coords[HEAD]['x'] - 1, 'y': snake_coords[HEAD]['y']}
        elif direction == 'right':
                newHead = {'x': snake_coords[HEAD]['x'] + 1, 'y': snake_coords[HEAD]['y']}

        snake_coords.insert(0, newHead)
#判断蛇死了没
def snake_is_alive(snake_coords):
        tag = True
        if snake_coords[HEAD]['x'] == -1 or snake_coords[HEAD]['x'] == map_width or snake_coords[HEAD]['y'] == -1 or \
                        snake_coords[HEAD]['y'] == map_height:
                 tag = False # 蛇碰壁啦
        for snake_body in snake_coords[1:]:
                if snake_body['x'] == snake_coords[HEAD]['x'] and snake_body['y'] == snake_coords[HEAD]['y']:
                        tag = False # 蛇碰到自己身体啦
        return tag

#判断贪吃蛇是否吃到食物
def snake_is_eat_food1(snake_coords, food,screen):  #如果是列表或字典，那么函数内修改参数内容，就会影响到函数体外的对象。
        if snake_coords[HEAD]['x'] == food['x'] and snake_coords[HEAD]['y'] == food['y']:
                food['x'] = random.randint(0, map_width - 1)
                food['y'] = random.randint(0, map_height - 1) # 实物位置重新设置
               # draw_snake1(screen, snake_coords,black)
               # draw_snake1(screen, snake_coords,ran_color)
        else:
                del snake_coords[-1]  # 如果没有吃到实物, 就向前移动, 那么尾部一格删掉
def snake_is_eat_food2(snake_coords, food,screen):  #如果是列表或字典，那么函数内修改参数内容，就会影响到函数体外的对象。
        if snake_coords[HEAD]['x'] == food['x'] and snake_coords[HEAD]['y'] == food['y']:
                food['x'] = random.randint(0, map_width - 1)
                food['y'] = random.randint(0, map_height - 1) # 实物位置重新设置
               # draw_snake2(screen, snake_coords,black)
                #draw_snake2(screen, snake_coords,ran_color())
        else:
                del snake_coords[-1]  # 如果没有吃到实物, 就向前移动, 那么尾部一格删掉
#食物随机生成
def get_random_location():
        return {'x': random.randint(0, map_width - 1), 'y': random.randint(0, map_height - 1)}

#开始信息显示
def show_start_info(screen,snake_speed_clock):
        titleFont = pygame.font.Font('myfont.ttf', 125)
        titleSurf1 = titleFont.render('Snake!', True, white, darkGreen)
        degrees1 = 0
        degrees2 = 0
        Imageguize = pygame.image.load("gameover.png").convert_alpha()
        button1=Button(ImageRule_up,ImageRule_down,(900,700))
        button2=Button(ImageStart_up,ImageStart_down,(400,700))
        while True:
                screen.fill(BG_COLOR)
                rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
                rotatedRect1 = rotatedSurf1.get_rect()
                rotatedRect1.center = (400,300)
                screen.blit(rotatedSurf1, rotatedRect1)
                button1.render(screen)
                button2.render(screen)
                button2.isStart()
                button2.isStart()
                #drawPressKeyMsg(screen)
 
                pygame.display.update()
                snake_speed_clock.tick(snake_speed)
                degrees1 += 3  # rotate by 3 degrees each frame
                degrees2 += 7  # rotate by 7 degrees each frame


                #鼠标监听事件
                for event in pygame.event.get():  # event handling loop
                        if event.type == KEYDOWN:
                                if event.key == K_ESCAPE or event.key == K_q:  #终止程序
                                        terminate() #终止程序
                        if event.type == MOUSEBUTTONDOWN:
                                mouse_x,mouse_y = pygame.mouse.get_pos()
                                mouse_down = event.button
                                mouse_down_x,mouse_down_y = event.pos
                                if 0<mouse_x<400 and 300<mouse_y<800 and pygame.mouse.get_pressed():
                                        return  #结束此函数, 开始游戏
                                #elif 600<mouse_x<900 and 500<mouse_y<900 and pygame.mouse.get_pressed():
                                        #screen.blit(Imageguize,(500,700))
                               # mouxe_x,mouse_y = event.pos
                                #move_x,move_y = event.rel
                                #if event.pos == button2.isOver:
                                 #       if event.type == MOUSEBUTTONDOWN:
                                  #              button2.gamestart = event.button
                                #mouse_down_x,mouse_down_y = event.pos
                                   #     elif event.type == MOUSEBUTTONUP:
                                    #            button2.gamestart = event.button
                                #mouse_up_x,mouse_up_y = event.pos
                                #if button2.is_start== True:
                                   # running_game(screen, snake_speed_clock)
                               # terminate()     #终止程序
                       # elif event.type == KEYDOWN:
                       #         if (event.key == K_ESCAPE):  #终止程序
                       #                 terminate() #终止程序
                        #        else:

#游戏结束信息显示
def show_gameover_info(screen):
        font = pygame.font.Font('myfont.ttf', 100)
        gameSurf = font.render('Game', True, white)
        overSurf = font.render('Over', True, white)
        button3=Button(ImageOver_up,ImageOver_down,(400,700))
        button4=Button(ImageRe_up,ImageRe_down,(900,700))
        while True:
                button3.render(screen)
                button4.render(screen)
                button3.isStart()
                button4.isStart()
                
        
                gameRect = gameSurf.get_rect()
                overRect = overSurf.get_rect()
                gameRect.midtop = (windows_width / 2, 100)
                overRect.midtop = (windows_width / 2, 250)
                screen.blit(gameSurf, gameRect)
                screen.blit(overSurf, overRect)
                #drawPressKeyMsg(screen)
                pygame.display.update()


                #鼠标监听事件
                for event in pygame.event.get():  # event handling loop
                        if event.type == MOUSEBUTTONDOWN:
                                mouse_x,mouse_y = pygame.mouse.get_pos()
                                mouse_down = event.button
                                mouse_down_x,mouse_down_y = event.pos
                                if 0<mouse_x<400 and 300<mouse_y<800 and pygame.mouse.get_pressed():
                                        terminate() #终止程序
                                elif 600<mouse_x<900 and 300<mouse_y<800 and pygame.mouse.get_pressed():
                                        return
        # while True:  #键盘监听事件
        #        for event in pygame.event.get():  # event handling loop
         #               if event.type == QUIT:
          #                      terminate()     #终止程序
          #              elif event.type == KEYDOWN:
          #                      if event.key == K_ESCAPE or event.key == K_q:  #终止程序
           #                             terminate() #终止程序
           #                     else:
           #                             return #结束此函数, 重新开始游戏

#画成绩
def draw_score1(screen,score):
        font = pygame.font.Font('myfont.ttf', 30)
        scoreSurf = font.render('得分: %s' % score, True, blue)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (windows_width - 120, 10)
        screen.blit(scoreSurf, scoreRect)
def draw_score2(screen,score):
        font = pygame.font.Font('myfont.ttf', 30)
        scoreSurf = font.render('得分: %s' % score, True, red)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (windows_width - 750, 10)
        screen.blit(scoreSurf, scoreRect)
#程序终止
def terminate():
        pygame.quit()
        sys.exit()


main()
