from PyQt5.QtCore import QTimer

from core.time.time_state import TimeState
from core.sound.sound_player import SoundPlayer

from core.utils.const import FOCUS_LIMIT_SECONDS, REST_TIME, REMIND_THRESHOLD

import random


class TimerLogic:
    def __init__(self, state: TimeState, sound_player: SoundPlayer):
        # Timer 状态
        self.state = state
        self.running = False
        self.resting = False
        self.rest_bell_played = False

        # Timer 默认时间设置
        self.focus_limit_seconds = FOCUS_LIMIT_SECONDS
        self.rest_lower_time = 3 * 60
        self.rest_upper_time = 5 * 60
        self.rest_time_value = REST_TIME
        self.remind_threshold = REMIND_THRESHOLD
        self.next_bell_seconds = self._random_interval()
        self.last_bell_seconds = 0

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)

        # 播放器
        self.sound_player = sound_player if sound_player else None

    # 操作回调
    def set_callbacks(self, 
                      callback_pause, 
                      callback_resume, 
                      callback_update_ui, 
                      callback_rest_start, 
                      callback_rest_end,
                      callback_remind):
        self.callback_pause = callback_pause
        self.callback_resume = callback_resume
        self.callback_update_ui = callback_update_ui
        self.callback_rest_start = callback_rest_start
        self.callback_rest_end = callback_rest_end
        self.callback_remind = callback_remind

    # 随机数产生下一次休息时间
    def _random_interval(self):
        return random.randint(self.rest_lower_time, self.rest_upper_time)
    
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
        """时间更新逻辑(Timer 每秒触发一次)"""
        if self.resting:
            # 处于休息周期
            if self.state.rest_time.minute() > 0 or self.state.rest_time.second() > 0:
                self.state.rest_time = self.state.rest_time.addSecs(-1)
            else:
                # rest_time 变成 00:00, 退出休息
                self.resting = False
                self.rest_bell_played = False
                self.state.rest_time.setHMS(0, 0, self.rest_time_value)
                if self.callback_rest_end:
                    self.callback_rest_end()
        else:
            # 处于学习周期
            self.state.increment()
            current_seconds = self.state.total_time.hour() * 3600 + self.state.total_time.minute() * 60 + self.state.total_time.second()

            ### 提醒阈值
            if self.focus_limit_seconds - current_seconds == self.remind_threshold:
                if self.callback_remind:
                    self.callback_remind()

            ### 长休息临界值
            if current_seconds >= self.focus_limit_seconds:
                self.pause()

                # 默认长休息20分钟
                # TODO 休息 20 分钟锁屏还是太变态了一点 ~, 这里将锁屏逻辑替换为悬浮时钟显示逻辑
                self.state.rest_time.setHMS(0, 20, 0)
                self.resting = True
                self.rest_bell_played = False
                if self.callback_rest_start:
                    self.callback_rest_start()
                if self.callback_pause:
                    self.callback_pause()
                return

            # 短休息随机值
            if current_seconds - self.last_bell_seconds >= self.next_bell_seconds:
                self.last_bell_seconds = current_seconds
                self.resting = True
                self.rest_bell_played = False
                self.state.rest_time.setHMS(0, 0, self.rest_time_value)
                self.callback_rest_start()
                self.next_bell_seconds = self._random_interval()
                self.callback_pause()

        # 只在进入休息的 tick 播放一次
        if self.resting and not self.rest_bell_played:
            if self.sound_player:
                self.sound_player.play()
            self.rest_bell_played = True

        # 每次 tick 都更新界面
        if self.callback_update_ui:
            self.callback_update_ui()