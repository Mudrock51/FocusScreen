import os
from PyQt5.QtWidgets import QWidget, QMenu, QAction, QSystemTrayIcon, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QCursor, QIcon
from PyQt5.QtCore import Qt, QTimer, QTime

from core.time.time_state import TimeState
from core.time.time_logic import TimerLogic
from core.utils.const import FOCUS_LIMIT_SECONDS, REST_TIME

from widget.rest.rest_overlay import RestOverlay
from widget.setting.setting_dialog import SettingDialog

# - TODO (1)悬浮框 | 右键「关闭」按键的逻辑设计与实现 
# - TODO (2)实现「休息周期」下的全屏页面覆盖
# - TODO (3)响铃时间(Belling)计算逻辑存在问题 | 设计算法完成修改 

class TimerBall(QWidget):
    def __init__(self, state: TimeState, logic: TimerLogic, overlay: RestOverlay):
        super().__init__()

        # Timer 初始化
        self.state = state
        self.logic = logic
        self.overlay = overlay

        # TimerBall 初始化
        self.show_short = True
        self.alt_pressed = False
        self.hover = False

        self.drag_position = None
        self.setMouseTracking(True)


        # 时钟组件构建
        self.setFixedSize(60, 60)
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.create_tray()

        # 动画逻辑
        self.display_mode_timer = QTimer()
        self.display_mode_timer.setInterval(300)
        self.display_mode_timer.setSingleShot(True)
        self.display_mode_timer.timeout.connect(self.repaint)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.repaint)
        self.update_timer.start(1000)

        self.show()

    # ——————————————————————————————————————————————————————————— #
    #                          绘制组件                            #
    # ——————————————————————————————————————————————————————————— #
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 根据是否在休息选择显示的时间
        if self.logic.resting:
            # 休息时显示倒计时
            time = self.state.rest_time
            rest_seconds = time.minute() * 60 + time.second()
            progress = 1.0 - (rest_seconds / (20 * 60 if rest_seconds > 600 else 10))  # 倒计时进度
            # 休息时使用不同的颜色方案
            base_color = QColor(255, 200, 200)  # 浅红色
            target_color = QColor(255, 100, 100)  # 深红色
        else:
            # 正常学习时间显示
            time = self.state.get_current_time(self.show_short)
            sec = time.minute() * 60 + time.second()
            progress = min(sec / (20 * 60 if self.show_short else 90 * 60), 1.0)
            # 背景颜色
            base_color = QColor(255, 255, 255) if self.show_short else QColor(173, 216, 230)
            target_color = QColor(160, 160, 160) if self.show_short else QColor(30, 144, 255)

        r = int(base_color.red() + (target_color.red() - base_color.red()) * progress)
        g = int(base_color.green() + (target_color.green() - base_color.green()) * progress)
        b = int(base_color.blue() + (target_color.blue() - base_color.blue()) * progress)

        painter.setBrush(QColor(r, g, b))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())

        # 时间文本
        painter.setPen(Qt.black)
        painter.setFont(QFont('Arial', 14))
        time_text = time.toString("mm:ss")
        if self.logic.resting:
            time_text = "休息 " + time_text
        painter.drawText(self.rect(), Qt.AlignCenter, time_text)

        # 鼠标悬浮显示按钮（开始/暂停）
        if self.hover and not self.logic.resting:  # 休息时不显示控制按钮
            symbol = "▶️" if not self.logic.running else "⏸️"
            painter.setFont(QFont('Arial', 12))
            painter.drawText(self.rect(), Qt.AlignBottom | Qt.AlignHCenter, symbol)


    def create_tray(self):
        """创建系统托盘"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, '../../assets/icon-app.jpg')
        icon_path = os.path.normpath(icon_path)

        # 创建托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icon_path))

        # 创建托盘菜单
        tray_menu = QMenu()
        
        show_action = QAction("显示计时器⏱", self)
        show_action.triggered.connect(lambda: self.show_timer())
        hide_action = QAction("隐藏计时器⏱", self)
        hide_action.triggered.connect(lambda: self.hide_timer())
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(lambda: self.quit_app())

        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # 显示托盘图标
        self.tray_icon.show()
        self.tray_icon.showMessage(
            "专注计时器", 
            "计时器已启动，右键托盘图标查看选项",
            QSystemTrayIcon.Information,
            2000
        )


    def show_menu(self):
        """右键功能栏"""
        menu = QMenu(self)

        setting_action = QAction("设置", self)
        setting_action.triggered.connect(lambda: self.open_setting())

        reset_short = QAction("重置短周期", self)
        reset_short.triggered.connect(lambda: self.state.reset_short())

        reset_all = QAction("重置整个周期", self)
        reset_all.triggered.connect(lambda: self.state.reset_all())

        hide_action = QAction("隐藏到系统托盘", self)
        hide_action.triggered.connect(lambda: self.close())

        quit_action = QAction("退出", self)
        quit_action.triggered.connect(lambda: self.quit_app())

        menu.addAction(setting_action)
        menu.addSeparator()
        menu.addAction(reset_short)
        menu.addAction(reset_all)
        menu.addSeparator()
        menu.addAction(hide_action)
        menu.addSeparator()
        menu.addAction(quit_action)
        menu.exec_(QCursor.pos())

    # ——————————————————————————————————————————————————————————— #
    #                          回调方法                            #
    # ——————————————————————————————————————————————————————————— #

    def tray_icon_activated(self, reason):
        """托盘图标激活事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_timer()

    def on_timer_pause(self):
        """计时器暂停时的回调"""
        self.repaint()

    def on_timer_resume(self):
        """计时器恢复时的回调"""
        self.repaint()

    def on_timer_update(self):
        """计时器更新时的回调"""
        self.repaint()

    def on_rest_start(self):
        """激活休息周期"""
        self.overlay.showFullScreen()

    def on_rest_end(self):
        """结束休息周期"""
        self.overlay.hide()

    def show_timer(self):
        """显示计时器"""
        self.show()
        self.activateWindow()
        self.raise_()

    def hide_timer(self):
        """隐藏计时器"""
        self.hide()

    def open_setting(self):
        """打开设置"""
        dlg = SettingDialog(
            focus_seconds=self.logic.focus_limit_seconds,
            rest_lower=self.logic.rest_lower_time,
            rest_upper=self.logic.rest_upper_time,
            rest_time=self.logic.rest_time_value
        )
        if dlg.exec_():
            settings = dlg.get_settings()
            self.logic.focus_limit_seconds = settings["focus_limit_seconds"]
            self.logic.rest_lower_time = settings["rest_lower_time"]
            self.logic.rest_upper_time = settings["rest_upper_time"]
            self.logic.rest_time_value = settings["rest_time"]
            self.state.rest_time = QTime(0, 0, self.logic.rest_time_value)
            self.logic.next_bell_seconds = self.logic._random_interval()

    def quit_app(self):
        """完全退出应用"""
        if hasattr(self, 'logic') and self.logic:
            self.logic.pause()

        # 停止ui更新计时器
        if hasattr(self, 'update_timer'):
            self.update_timer.stop()
        if hasattr(self, 'display_mode_timer'):
            self.display_mode_timer.stop()

        # 隐藏托盘图标
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
            
        # 退出应用
        QApplication.instance().quit()

    # ——————————————————————————————————————————————————————————— #
    #                        重载时钟逻辑                           #
    # ——————————————————————————————————————————————————————————— #

    def mouseMoveEvent(self, e):
        """重载鼠标拖动事件"""
        if self.drag_position and self.alt_pressed:
            self.move(e.globalPos() - self.drag_position)

    def mousePressEvent(self, e):
        """重载鼠标点击事件"""
        if e.button() == Qt.LeftButton:
            if self.alt_pressed:
                self.drag_position = e.globalPos() - self.frameGeometry().topLeft()
                
            else:
                # 左键点击切换计时器状态
                self.logic.toggle()
        elif e.button() == Qt.RightButton:
            # 右键显示菜单
            self.show_menu()
    
    def mouseReleaseEvent(self, e):
        """重载鼠标释放事件"""
        self.drag_position = None

    def wheelEvent(self, e):
        """重载滚轮事件"""
        self.show_short = not self.show_short
        self.display_mode_timer.start()

    def enterEvent(self, e):
        """启动事件"""
        self.hover = True
        self.repaint()

    def leaveEvent(self, e):
        """离开事件"""
        self.hover = False
        self.repaint()

    def closeEvent(self, event):
        """窗口关闭事件"""
        if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
            self.hide()
            event.ignore()  # 忽略关闭事件，改为隐藏
        else:
            event.accept()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Alt:
            self.alt_pressed = True

    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Alt:
            self.alt_pressed = False

    def close(self):
        """关闭计时器球(隐藏)"""
        self.hide_timer()
        if hasattr(self, 'tray_icon'):
            self.tray_icon.showMessage(
                "专注计时器", 
                "计时器已隐藏到系统托盘",
                QSystemTrayIcon.Information,
                2000
            )
