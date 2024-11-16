import pygame

# 初始化pygame
pygame.init()

import keyboard
# 设置手柄输入
pygame.joystick.init()
# keyboard = Controller()
# 检查是否连接了手柄
if pygame.joystick.get_count() == 0:
    print("没有找到手柄！")
    exit()
# 获取第一个手柄
joystick = pygame.joystick.Joystick(0)
joystick.init()
key_list={
    0:'A',
    1:'B',
    3:'X',
    4:'Y',
    6:'LB',
    7:'RB',
    8:'LT',
    9:'RT',
    10:'Back',
    11:'Start',
    12:'Middle',
    13:'motion_down',
    (0,0):'L_center',
    (0,1):'L_up',
    (1,1):'L_up_right',
    (1,0):'L_right',
    (0,-1):'L_down',
    (1,-1):'L_down_right',
    (-1,-1):'L_down_left',
    (-1,0):'L_left',
    (-1,1):'L_up_left',
}
key_map={
    'A':'z',
    'B':'x',
    'X':'e',
    'Y':'d',
    'LB':'q',
    'RB':'r',
    'LT':'t',
    'RT':'y',
    'L_up':'w',
    'L_right':'d',
    'L_down':'s',
    'L_left':'a',
}
running= True
flag=0
while running:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            # print(event.button)
            print(key_list[event.button],key_map[key_list[event.button]])
            keyboard.press(key_map[key_list[event.button]])
            keyboard.release(key_map[key_list[event.button]])

        elif event.type == pygame.JOYHATMOTION:
            x, y = event.value
            # print(x, y)
            if key_list[(x,y)] in key_map:
                print(key_list[(x,y)],key_map[key_list[(x,y)]])
                last_key=key_map[key_list[(x,y)]]
                keyboard.press(key_map[key_list[(x,y)]])
            if x == 0 and y == 0:
                keyboard.release(last_key)
                print('stop')
        # else:
        #     print(event.type)


pygame.quit()
