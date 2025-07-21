import os
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

from core.time.time_state import TimeState
from core.time.time_logic import TimerLogic
from core.utils.utils import get_image_list

class RestOverlay(QWidget):
    def __init__(self, state: TimeState, logic: TimerLogic):
        super().__init__()

        self.state = state
        self.logic = logic

        # 屏幕设置
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        self.setWindowState(Qt.WindowFullScreen)
        self.setAttribute(Qt.WA_TranslucentBackground, False)

        # 读取并随机选择背景图片
        base_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(base_dir, '../../assets/rest')
        images_dir = os.path.normpath(images_dir)
        image_list = get_image_list(images_dir)
        if image_list:
            import random
            image_file = os.path.join(images_dir, random.choice(image_list))
        else:
            # Default
            image_file = os.path.join(images_dir, 'bg03.jpg')
        
        # 设置图片覆盖逻辑
        self.bg_label = QLabel(self)
        pixmap = QPixmap(image_file)
        self.bg_label.setPixmap(pixmap)
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(self.rect())

        # 设置文字显示逻辑
        self.time_label = self.set_label(
            "",
            "color:red;font-size:100px;font-family:'Consolas','Courier New',monospace;font-weight:bold;background:transparent;",
            1
        )
        self.text_label_1 = self.set_label(
            "休息时间😄",
            "color:white;font-size:60px;font-weight:bold;background:rgba(0,0,0,0.5);"
            "border-radius:20px;padding:10px 30px;",
            1
        )
        self.text_label_2 = self.set_label(
            "不要忘记喝水🥛💦",
            "color:white;font-size:48px;font-weight:bold;background:rgba(0,0,0,0.5);"
            "border-radius:20px;padding:8px 24px;",
            2
        )

        w, h = self.width(), self.height()
        self.time_label.setGeometry(self.rect())
        self.text_label_1.setGeometry(700, 300, 560, 180)
        self.text_label_2.setGeometry(720, 600, 500, 200)

        # 设置休息周期时钟
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rest_time)
        
    def set_label(self, content: str, style: str, pos: int):
        text_label = QLabel(content, self)
        text_label.setStyleSheet(style)
        if pos == 1:
            text_label.setAlignment(Qt.AlignCenter) # 水平垂直居中
        elif pos == 2:
            text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 左对齐垂直居中
        elif pos == 3:
            text_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)  # 右下角
        return text_label
    
    # ——————————————————————————————————————————————————————————— #
    #                          回调方法                            #
    # ——————————————————————————————————————————————————————————— #
    def showFullScreen(self):
        super().showFullScreen()
        self.timer.start(1000)
        self.update_rest_time()

    def hide(self):
        self.timer.stop()
        super().hide()

    def update_rest_time(self):
        t = self.state.rest_time
        self.time_label.setText(f"{t.minute():02d}:{t.second():02d}")