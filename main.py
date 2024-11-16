'''
File : main.py
Auther : MHY
Created : 2024/11/16 13:14
Last Updated : 
Description : 
Version : 
'''
import json
import sys
import threading

import keyboard
from PyQt5.QtCore import QTimer, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QTableWidget, QFileDialog
from ui import Ui_MainWindow
import pygame
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
class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        '''初始化pygame和手柄'''
        self.joystick_init()
        '''变量区'''
        self.KEYBOARD_LISTEN=False
        self.START_MAP=False
        self.is_timer_active = False
        self.row,self.column=0,0
        self.last_key=0
        self.key_map = {}
        '''连续点击频率默认为只读'''
        self.spinBox.setReadOnly(True)
        '''定时捕获手柄输入，定时器开关取决于焦点是否在单元格内'''
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.joystick_clicked)
        '''定时检测焦点是否离开单元格'''
        self.timer2= QTimer(self)
        self.timer2.timeout.connect(self.check_table)
        self.timer2.start(100)
        '''开始映射定时器'''
        self.timer_map=QTimer(self)
        self.timer_map.timeout.connect(self.map)
        '''检测鼠标是否点击单元格'''
        self.tableWidget.cellClicked.connect(self.on_cell_entered)
        '''禁用QTableWidget键盘快捷键'''
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        '''开始映射'''
        self.pushButton.clicked.connect(self.start_map)
        '''连续点击'''
        self.radioButton.clicked.connect(self.constant_click)
        '''捕获键盘输入'''
        keyboard.on_press(self.on_press)
        '''菜单栏'''
        self.actionload.triggered.connect(self.import_config)
        self.actionexport.triggered.connect(self.export_config)

    def import_config(self):
        '''加载配置文件'''
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("JSON  files (*.json)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            file_name = file_dialog.selectedFiles()[0]
            print(f"Selected JSON file: {file_name}")
            with open(file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
                r=0
                for key, value in data.items():
                    self.tableWidget.setItem(r, 0, QTableWidgetItem(key))
                    self.tableWidget.setItem(r, 1, QTableWidgetItem(value))
                    r+=1
    def export_config(self):
        '''导出配置文件'''
        data={}
        file_name, _ = QFileDialog.getSaveFileName(self,  "保存文件", "config.json", "JSON Files (*.json)")
        print(file_name)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                for row in range(self.tableWidget.rowCount()):
                    item1 = self.tableWidget.item(row, 0)
                    item2 = self.tableWidget.item(row, 1)
                    if item1 is not None and item2 is not None:
                        key = item1.text()
                        value = item2.text()
                        data[key] = value
                json.dump(data, file, ensure_ascii=False)
    def joystick_init(self):
        '''初始化'''
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            print("没有找到手柄！")
        else:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            joystick_name= self.joystick.get_name()
            print(joystick_name)
            self.comboBox.addItem(joystick_name)
    def on_cell_entered(self, row, column):
        '''检测单元格焦点'''
        print(f"光标进入单元格: ({row}, {column})")
        self.row=row
        self.column=column
        self.is_timer_active = True
        self.timer.start(100)

    def check_table(self):
        '''检测表格焦点'''
        if self.tableWidget.hasFocus():
            pass
        else:
            self.is_timer_active = False

    def on_press(self,e):
        '''键盘按下事件'''
        print(f'按键按下: {e.name}')
        if self.is_timer_active==False:
            self.KEYBOARD_LISTEN=False
            keyboard.unhook_all()
        else:
            if self.column == 1:
                self.tableWidget.setItem(self.row, self.column, QTableWidgetItem(e.name))
                self.tableWidget.viewport().update()
    def joystick_clicked(self):
        '''手柄点击事件'''
        if not self.is_timer_active:
            pygame.event.clear()
            pygame.event.pump()
            # print('没有聚焦')
            return
        if not self.KEYBOARD_LISTEN:
            keyboard.on_press(self.on_press)
            self.keyboard_thread=threading.Thread(target=keyboard.wait)
            self.keyboard_thread.start()
            self.KEYBOARD_LISTEN=True
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                # print(event.button)
                if event.button in key_list:
                    print(key_list[event.button])
                    if self.column == 0:
                        self.tableWidget.setItem(self.row, self.column, QTableWidgetItem(key_list[event.button]))

            elif event.type == pygame.JOYHATMOTION:
                x, y = event.value
                if (x, y) in key_list and (x,y)!=(0,0):
                    print(key_list[(x, y)])
                    if self.column == 0:
                        self.tableWidget.setItem(self.row, self.column, QTableWidgetItem(key_list[(x, y)]))
            elif event.type == pygame.JOYAXISMOTION:
                pass

    def start_map(self):
        '''开始映射'''
        if self.START_MAP==False:
            self.timer.stop()
            self.timer2.stop()
            self.key_map={}
            for row in range(self.tableWidget.rowCount()):
                item1 = self.tableWidget.item(row, 0)
                item2 = self.tableWidget.item(row, 1)
                if item1 is not None and item2 is not None:
                    key = item1.text()
                    value = item2.text()
                    self.key_map[key] = value

            print(self.key_map)
            self.timer_map.start(1)
            self.pushButton.setText('停止映射')
            self.START_MAP=True
        else:
            self.timer.start(100)
            self.timer2.start(100)
            self.timer_map.stop()
            self.pushButton.setText('开始映射')
            self.START_MAP=False

    def map(self):
        '''映射'''
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if key_list[event.button] in self.key_map:
                    print(key_list[event.button],self.key_map[key_list[event.button]])
                    keyboard.press(self.key_map[key_list[event.button]])
                    keyboard.release(self.key_map[key_list[event.button]])
            elif event.type == pygame.JOYHATMOTION:
                x, y = event.value
                if key_list[(x,y)] in self.key_map:
                    print(key_list[(x,y)],self.key_map[key_list[(x,y)]])
                    self.last_key=self.key_map[key_list[(x,y)]]
                    keyboard.press(self.key_map[key_list[(x,y)]])
                if x == 0 and y == 0:
                    print('stop')
                    keyboard.release(self.last_key)
    def constant_click(self):
        '''连续点击'''
        if self.radioButton.isChecked():
            self.spinBox.setReadOnly(False)
        else:
            self.spinBox.setReadOnly(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
