from PyQt5.QtCore import QTime

from core.utils.const import REST_TIME

class TimeState:
    """定义时间状态
    - short_time: 短周期 | 记录每个短周期学习时间。
    - total_time: 总周期 | 默认设置为90分钟,所有短周期累计。
    - rest_time: 休息周期 | 默认设置为10秒,在短周期中,每3~5分钟就休息一个周期。
    """
    def __init__(self):
        self.short_time = QTime(0, 0, 0)
        self.total_time = QTime(0, 0, 0) 
        self.rest_time = QTime(0, 0, REST_TIME)

    # 时间递增逻辑
    def increment(self):
        self.short_time = self.short_time.addSecs(1)
        self.total_time = self.total_time.addSecs(1)

    # 短周期重置逻辑
    def reset_short(self):
        self.short_time = QTime(0, 0, 0)

    # 长周期重置逻辑
    def reset_all(self):
        self.reset_short()
        self.total_time = QTime(0, 0, 0)

    def get_current_time(self, show_short):
        return self.short_time if show_short else self.total_time