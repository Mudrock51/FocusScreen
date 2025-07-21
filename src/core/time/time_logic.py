from PyQt5.QtCore import QTimer
from core.time.time_state import TimeState
import random


class TimerLogic:
    def __init__(self, state: TimeState, sound_player=None):
        # Timer 状态
        self.state = state
        self.running = False
        self.resting = False

        # Timer 默认时间设置
        self.focus_limit_seconds = 90 * 60
        self.next_bell_seconds = self._random_interval()
        self.last_bell_seconds = 0

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)

        # 播放器
        self.sound_player = sound_player

    # 操作回调
    def set_callbacks(self, callback_pause, callback_resume, callback_update_ui, callback_rest_start, callback_rest_end):
        self.callback_pause = callback_pause
        self.callback_resume = callback_resume
        self.callback_update_ui = callback_update_ui
        self.callback_rest_start = callback_rest_start
        self.callback_rest_end = callback_rest_end

    # 随机数产生下一次休息时间
    def _random_interval(self):
        return random.randint(3, 5) # Testing
        # return random.randint(3 * 60, 5 * 60)
    
    def start(self):
        if not self.running:
            self.running = True
            self.timer.start(1000) # 每秒触发一次 tick()

    def pause(self):
        self.running = False
        self.timer.stop()

    def toggle(self):
        if self.running:
            self.pause()
            self.callback_pause()
        else:
            self.start()
            self.callback_resume()

    def tick(self):
        """时间更新逻辑(Timer 每秒触发一次)
        """
        if self.resting:
            # 处于长休息周期
            # QTime.addSecs(-1) 倒计时1秒
            self.state.rest_time = self.state.rest_time.addSecs(-1)
            if self.state.rest_time.second() <= 0:
                # 休息结束
                self.resting = False
                self.state.rest_time.setHMS(0, 0, 10)
                self.callback_rest_end()
                self.callback_resume()
        else:
            # 处于学习周期
            self.state.increment()
            current_seconds = self.state.total_time.minute() * 60 + self.state.total_time.second()

            # 长休息临界值
            if current_seconds >= self.focus_limit_seconds:
                self.pause()
                self.state.short_time.setHMS(0, 20, 0)
                self.state.total_time.setHMS(0, 20, 0)
                self.resting = True
                self.callback_pause()
                return
            
            # 短休息随机值
            if current_seconds - self.last_bell_seconds >= self.next_bell_seconds:
                
                self.last_bell_seconds = current_seconds
                self.resting = True
                self.state.rest_time.setHMS(0, 0, 10)

                # 切换休息页面
                self.callback_rest_start()

                # 下一次响铃随机数
                self.next_bell_seconds = self._random_interval()

                # 响铃
                if self.sound_player:
                    self.sound_player.play()
                self.callback_pause()
        
        # 每次tick都更新UI
        if hasattr(self, 'callback_update_ui'):
            self.callback_update_ui()
