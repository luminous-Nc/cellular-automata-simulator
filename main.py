# coding:utf-8



from pylab import *
import random
import numpy as np
import pygame
import sys
import matplotlib.pyplot as plt

from entity import Game, Square, Room
from setting import *

if __name__ == '__main__':

    plt.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

    g_enter_num = []
    g_inner_num = []
    g_exit_num = []
    g_infected_num = []
    plot_data = []
    pygame.init()
    pygame.display.set_caption("元胞自动机展会模拟")
    width = 700
    height = 700
    screen = pygame.display.set_mode([width + 200, height])
    model_game = Game(width, height, 100, 100, screen)

    font = pygame.font.SysFont('C:/Windows/Fonts/simhei.ttf', 28)
    # 文本与颜色
    text_in = font.render("IN", 1, (0, 0, 0))
    text_out = font.render("OUT", 1, (0, 0, 0))


    text_in_pos = text_in.get_rect(center=(20,80))
    text_out_pos = text_out.get_rect(center=(20,630))

    text_center = font.render("Kunming International Exhibition Center", 1, (0,0,0))
    text_center_pos = text_center.get_rect(center=(410,22))

    clock = pygame.time.Clock()
    k1 = 0
    while True:

        model_game.screen.fill(GREY)#底部全置灰
        clock.tick(game_time)  # 每秒循环10次
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # model_game.cells.calc_neighbour_count()



        enter_num, inner_num, exit_num, infected_num, now_time , virus_exit_time = model_game.cells.num_of_game()
        if virus_exit_time == now_time:  # 退出条件
            sys.exit()
        text_time = font.render("Time:%d" % now_time, 1, (0, 0, 0))
        text_time_pos = text_time.get_rect(center=(800, 50))
        text_total_num = font.render("All:%d"%inner_num, 1, (0, 0, 0))
        text_total_num_pos = text_total_num.get_rect(center=(800, 80))
        text_ill_num = font.render("Infected:%d"%infected_num,1,(255,255,0))
        text_ill_num_pos = text_ill_num.get_rect(center=(800,110))



        plot_data = [enter_num,inner_num,exit_num,infected_num]

        # g_enter_num.append(enter_num)
        # g_inner_num.append(inner_num)
        # g_exit_num.append(exit_num)
        # g_infected_num.append(infected_num)

        # plt.bar(range(4), plot_data, width = 0.3, align='center', color=['steelblue','deepskyblue','peru','red'], alpha=0.8)
        #
        # plt.ylabel('人')
        #
        # plt.title('模拟实时数据')
        #
        # plt.xticks(range(4),['总入场人数','当前场内人数','离场人数','被感染人数'])
        #
        # plt.ylim([0,300])
        #
        # for x,y in enumerate(plot_data):
        #     plt.text(x, y,'%s' %round(y,1),ha='center')
        #
        # # plt.plot(g_enter_num, color='y', label='总入场人数')
        # # plt.plot(g_inner_num, color='b', label='当前场内人数')
        # # plt.plot(g_exit_num, color='r', label='离场人数')
        # # plt.plot(g_infected_num, color='g', label='被感染人数')
        # # plt.ylim([0,80000])
        # # plt.legend()
        # # plt.xlabel('时间单位')
        # # plt.ylabel('人数单位')
        # plt.pause(0.1)#0.1秒停一次
        # plt.clf()#清除

        # plt.close()#退出


        model_game.show_life()

        screen.blit(text_time, text_time_pos)

        screen.blit(text_in,text_in_pos)
        screen.blit(text_out, text_out_pos)
        screen.blit(text_total_num,text_total_num_pos)
        screen.blit(text_ill_num,text_ill_num_pos)

        screen.blit(text_center,text_center_pos)

        pygame.display.flip()
        model_game.cells.next_iter()

    # plt.show()#显示