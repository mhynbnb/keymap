'''
File : draft.py
Auther : MHY
Created : 2024/11/16 17:11
Last Updated : 
Description : 
Version : 
'''
import threading

import keyboard

def on_press(e):
    print(f'按键按下: {e.name}')
    if e.name  == 'esc':
        # 按下Esc键退出监听
        keyboard.unhook_all()
    if e.name  == 'enter':
        keyboard.hook(on_press)

def on_release(e):
    print(f'按键释放: {e.name}')
    if e.name  == 'esc':
        # 按下Esc键退出监听
        keyboard.unhook_all()

keyboard.on_release(on_release)
threading.Thread(keyboard.wait()).start()
keyboard.on_press(on_press)