import pygame
import random
import numpy as np

from setting import *

"""细胞类，单个细胞"""

class Square:
    # 初始化
    stage = 0



    # 状态 0：空白
    # 状态 1：正常人
    # 状态 2：刚刚传染
    # 状态 3：传染性病人
    # 状态 4：咳嗽病人

    # 状态 -1：展台边缘
    # 状态 -2：门

    def __init__(self, ix, iy, stage):
        self.ix = ix
        self.iy = iy
        self.stage = stage  # 状态
        self.move_flag = False

        self.person_stage = {'now_watch_time':0,'total_watch_time':0}
                            # 这一次看展的时间     #累计看展时间


    # 计算周围有多少个感染者
    def count_neighbour_affect_num(self):
        surround_infector_num = 0
        surround_new_ill_num = 0
        pre_x = self.ix - 1 if self.ix > 0 else 0
        for i in range(pre_x, self.ix + 1 + 1):
            pre_y = self.iy - 1 if self.iy > 0 else 0
            for j in range(pre_y, self.iy + 1 + 1):
                if i == self.ix and j == self.iy:  # 判断是否为自身
                    continue
                if self.if_location_invalid(i, j):  # 判断是否越界
                    continue
                if Room.cells[i][j].stage == 3:  # 此时这个邻居是感染者
                    # 如果是在上下左右
                    surround_infector_num += 1
                if Room.cells[i][j].stage == 2:  # 此时这个邻居是新患者
                    surround_new_ill_num += 1
        # print(count_0)
        self.infector = surround_infector_num
        # if self.s1_1!=0:
        #     print(count_1,count_0,self.ix,self.iy)
        self.new_patient = surround_new_ill_num

    # 判断是否越界
    def if_location_invalid(self, x, y):
        if x >= Room.room_x or y >= Room.room_y:
            return True
        if x < 0 or y < 0:
            return True
        return False


    # 按规则迭代
    def next_iter(self):

        self.person_enter()

        #self.person_show_location()

        if move_sequence:
            self.person_move_sequence()
        else:

            self.person_move_random()

        self.person_change()

        self.person_exit()

    def refresh_move(self):
        self.move_flag = False

    def person_show_location(self):
        if self.stage >= 1 and self.stage <= 4:
            print('时间%s 位置(%s,%s) 状态%s 移动：%s'%(Room.now_time,self.ix,self.iy,self.stage,self.move_flag))

    def person_enter(self):
        if self.ix == 1 and self.iy == 1: #保证每时间片只进行一次进入计算
            if Room.now_time % enter_time_freqence == 0:
                if Room.inner_people_num < allow_inner_max: #没超上限
                    if Room.current_people_num < total_people_num:  # 没进完
                        index = random.randint(7, 13)
                        # print('%d,%d位置进入' % (self.ix, self.iy))
                        self.enter_a_new_person(index)
                        Room.current_people_num += 1
                        Room.inner_people_num += 1

    def random_number(self, choice, probability):
        np.random.seed(0)
        p = np.array(probability)
        index = np.random.choice(choice, p=p.ravel())
        return index

    def enter_a_new_person(self,enter_y):
        for single_enter_rate in enter_rate:
            if Room.current_people_num == total_people_num * single_enter_rate:
                Room.cells[1][enter_y].stage = 3  # 进入一个得病的
                # print("时间:%s,y:%s" % (Room.now_time, enter_y))
                # for cell in Room.cells[1]:
                #     print(cell.stage, end="")
                # print()
                break #终止对于后续enter_rate的判断，不然永远只显示最后一个
            else:
                Room.cells[1][enter_y].stage = 1  # 进入一个正常人

    def exit_a_person(self):
        self.stage = 0

    def move_by_p(self,p_array):
        p_result = np.random.choice([0, 1, 2, 3], 1, p = p_array)
                   # 向上    向右   向下   向左
        xy_array = [[0,-1], [1,0],[0,1], [-1,0]]

        xy_result = xy_array[p_result[0]]
        next_x = self.ix+xy_result[0]
        next_y = self.iy+xy_result[1]

        if self.if_location_invalid(next_x, next_y):
            return [self.ix, self.iy]
        else:
            return [next_x, next_y]

    def person_move_random(self):
        if self.stage >= 1 and self.stage <= 4 and self.move_flag == False:  # 是个人
            # print('(%d,%d)'%(self.ix,self.iy))
            if (self.is_watching() == False):
                next_des = [self.ix,self.iy]

                if self.iy<=15:
                    if self.ix <=25:
                        next_des = self.move_by_p(p_x25y15)
                    if self.ix <=85:
                        next_des = self.move_by_p(p_x85y15)
                    else:
                        next_des = self.move_by_p(p_x99y15)
                elif self.iy<=25:
                    if self.ix <= 25:
                        next_des = self.move_by_p(p_x25y25)
                    elif self.ix <= 35:
                        next_des = self.move_by_p(p_x35y25)
                    elif self.ix <= 85:
                        next_des = self.move_by_p(p_x85y25)
                    else:
                        next_des = self.move_by_p(p_x99y25)
                elif self.iy <=85:
                    if self.ix <= 35:
                        next_des = self.move_by_p(p_x35y85)
                    elif self.ix > 35 and self.ix <= 85:
                        next_des = self.move_by_p(p_x85y85)
                    else:
                        next_des = self.move_by_p(p_x99y85)
                else:
                    if self.ix <= 35:
                        next_des = self.move_by_p(p_x35y99)
                    elif self.ix > 35 and self.ix <= 85:
                        next_des = self.move_by_p(p_x85y99)
                    else:
                        next_des = self.move_by_p(p_x99y99)

                if self.stage == 3 or self.stage == 4:
                    if Room.infected_people_num <= 10 and infect_button == True:
                        if self.ix>35 and self.ix <=85 and self.iy>25 and self.iy<85:
                            next_des = self.move_by_p(p_infect)

                if  Room.cells[next_des[0]][next_des[1]].stage == 0:
                    Room.cells[next_des[0]][next_des[1]].stage = self.stage
                    Room.cells[next_des[0]][next_des[1]].person_stage = self.person_stage
                    Room.cells[next_des[0]][next_des[1]].move_flag = True
                    self.stage = 0
                    self.person_stage =  {'now_watch_time':0,'total_watch_time':0}
                    self.move_flag = False

    def person_move_sequence(self):
        if self.stage >= 1 and self.stage <= 4 and self.move_flag == False:  # 是个人
            # print('(%d,%d)'%(self.ix,self.iy))
            if (self.is_watching() == False):
                next_des = [self.ix, self.iy]

                if self.ix <= 25 and self.iy <=25:   #1
                    next_des = self.move_by_p(p_2_down)
                    if next_des[0]==26:
                        next_des[0]= 25
                elif self.ix<=85 and self.iy <=35:    #2
                    next_des = self.move_by_p(p_2_right)
                    if next_des[1]==25:
                        next_des[1] = 26
                    if next_des[1]==35:
                        next_des[1] = 34
                elif self.ix>85 and self.iy <=45:    #3
                    next_des = self.move_by_p(p_2_down)
                    if next_des[1] == 25:
                        next_des[1] = 26

                elif self.ix>=25 and self.iy <=55:   #4
                    next_des = self.move_by_p(p_2_left)
                    if next_des[1] == 45:
                        next_des[1] = 46
                    if next_des[1] == 56:
                        next_des[1] = 55
                elif self.ix <= 25 and self.iy <=65:   #5
                    next_des = self.move_by_p(p_2_down)
                    if next_des[0]==26:
                        next_des[0]= 25
                elif self.ix <= 85 and self.iy <= 75:  #6
                    next_des = self.move_by_p(p_2_right)
                    if next_des[1] == 65:
                        next_des[1] = 66
                    if next_des[1] == 75:
                        next_des[1] = 74
                elif self.ix > 85 and self.iy <= 85:  # 7
                    next_des = self.move_by_p(p_2_down)
                    if next_des[1] == 85:
                        next_des[1] = 86
                elif self.ix >= 0 and self.iy <= 95:  # 4
                    next_des = self.move_by_p(p_2_left)
                    if next_des[1] == 85:
                        next_des[1] = 86
                    if next_des[1] == 96:
                        next_des[1] = 95

                if Room.cells[next_des[0]][next_des[1]].stage == 0:
                    Room.cells[next_des[0]][next_des[1]].stage = self.stage
                    Room.cells[next_des[0]][next_des[1]].person_stage = self.person_stage
                    Room.cells[next_des[0]][next_des[1]].move_flag = True
                    self.stage = 0
                    self.person_stage = {'now_watch_time': 0, 'total_watch_time': 0}
                    self.move_flag = False



    def is_watching(self):
        # pre_x = self.ix - 1 if self.ix > 0 else 0
        # for i in range(pre_x, self.ix + 1 + 1):
        #     pre_y = self.iy - 1 if self.iy > 0 else 0
        #     for j in range(pre_y, self.iy + 1 + 1):
        #         if i == self.ix and j == self.iy:
        #             continue
        #         if self.if_location_invalid(i, j):
        #             continue
        #         if Room.cells[i][j].stage == -1:  # 周围有展台
        #             return False
        #         else:
        #             return False
        return False

    def person_exit(self):
        if self.stage >= 1 and self.stage <= 4:
            if (self.ix ==1 and (self.iy >= 86 and self.iy <= 92)) \
                    or ((self.ix == 0) and (self.iy>=92)):
                if self.stage == 3 or self.stage == 4:
                    Room.virus_exist = False
                if Room.virus_exist == False:
                    Room.virus_exit_time = Room.now_time + exit_time
                    Room.virus_exist = True
                self.exit_a_person()
                Room.leave_people_num += 1
                Room.inner_people_num -= 1


    def person_change(self):

        if self.stage == 3 or self.stage == 4:
            if (Room.now_time % infector_cough_freqence) <= 2:
                self.stage = 4 # 变成咳嗽者
                pre_x = self.ix - 1 if self.ix > 0 else 0
                for i in range(pre_x, self.ix + 1 + 1):
                    pre_y = self.iy - 1 if self.iy > 0 else 0
                    for j in range(pre_y, self.iy + 1 + 1):
                        if i == self.ix and j == self.iy:
                            continue
                        if self.if_location_invalid(i, j):
                            continue
                        if Room.cells[i][j].stage == 1:  # 周围有正常人
                            p_result = np.random.choice([1,2], 1, p=infector_probability)
                            Room.cells[i][j].stage = p_result[0]
                            if p_result[0] == 2:
                                Room.infected_people_num += 1

            else:
                self.stage = 3 #变回带毒者

"""细胞网格类，处在一个长cx,宽cy的网格中"""


class Room:
    cells = []
    room_x = 0
    room_y = 0
    current_people_num = 0
    leave_people_num = 0
    inner_people_num = 0
    infected_people_num = 0
    now_time = 0
    virus_exit_time = -1
    virus_exist = True

    # 初始化
    def __init__(self, room_x, room_y):
        Room.room_x = room_x
        Room.room_y = room_y
        self.init_room()

    # 初始化房间
    def init_room(self):
        for i in range(Room.room_x):
            cell_list = []
            for j in range(Room.room_y):
                new_cell = (Square(i, j, 0))
                # 进入一个CEll的判断
                for one_exhibition in exhibition_coordinate:
                    if (abs(one_exhibition[0] - i) <= exhibition_ratio and abs(
                            one_exhibition[1] - j) <= exhibition_ratio):
                        new_cell = Square(i, j, -1)  # 设置为展台
                        break
                        # print("=>%d,%d 展台" %(i,j))
                for one_door in door_coordinate:
                    if (i == one_door[0] and j == one_door[1]):
                        new_cell = Square(i, j, -2)  # 设置为门
                        break
                        # print("=>%d,%d 门" %(i,j))
                for one_door in out_door_coordinate:
                    if (i == one_door[0] and j == one_door[1]):
                        new_cell = Square(i, j, -3)  # 设置为出口
                        break
                        # print("=>%d,%d 门" %(i,j))
                cell_list.append(new_cell)
            Room.cells.append(cell_list)

    # 依次迭代
    def next_iter(self):
        Room.now_time += 1
        for cell_list in Room.cells:
            for item in cell_list:
                item.refresh_move()
        for cell_list in Room.cells:
            for item in cell_list:
                item.next_iter()

    def calc_neighbour_count(self):
        return
        # for cell_list in Room.cells:
        #     for item in cell_list:
        #         item.count_neighbour_affect_num()

    def num_of_game(self):
        # global count0_,count1_,count2_
        enter_num = Room.current_people_num

        exit_num = Room.leave_people_num

        inner_num = Room.inner_people_num

        infected_num = Room.infected_people_num

        now_time = Room.now_time

        virus_exit_time = Room.virus_exit_time

        return enter_num,inner_num, exit_num, infected_num,now_time,virus_exit_time

        '''界面类'''


class Game:
    screen = None
    count0 = 0
    count1 = 9
    count2 = 0
    count3 = 0

    def __init__(self, width, height, cx, cy , screen):  # 屏幕宽高，房间区域空间大小
        self.width = width
        self.height = height
        self.cx_rate = int(width / cx)
        self.cy_rate = int(height / cy)
        self.screen = screen  #
        self.cells = Room(cx, cy)

    def show_life(self):
        # img = pygame.image.load('./picture.png')
        #
        # self.screen.blit(img, (0,0))

        # self.screen = self.screen.convert_alpha()

        for cell_list in self.cells.cells:
            for item in cell_list:
                x = item.ix+5
                y = item.iy
                if item.stage == 0:
                    pygame.draw.rect(self.screen, WHITE,
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])
                elif item.stage == 1:
                    pygame.draw.rect(self.screen, GREEN,
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])
                elif item.stage == 2:
                    pygame.draw.rect(self.screen, YELLOW,
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])
                elif item.stage == 3:
                    pygame.draw.rect(self.screen, S_RED,
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])
                elif item.stage == 4:
                    pygame.draw.rect(self.screen, RED,
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])
                elif item.stage == -1:
                    pygame.draw.rect(self.screen, BLUE,
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])
                elif item.stage == -2:
                    pygame.draw.rect(self.screen, ORANGE,
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])
                elif item.stage == -3:
                    pygame.draw.rect(self.screen, PINK,
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])



