import sys
from PyQt5.QtWidgets import QApplication

from widget.timer.timer_ball import TimerBall
from widget.rest.rest_overlay import RestOverlay

from core.time.time_state import TimeState
from core.time.time_logic import TimerLogic
from core.sound.sound_player import SoundPlayer

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 设置应用不在最后一个窗口关闭时退出
    app.setQuitOnLastWindowClosed(False)

    # 初始化状态和逻辑
    sound_player = SoundPlayer()
    time_state = TimeState()
    time_logic = TimerLogic(time_state, sound_player)
    rest_overlay = RestOverlay(time_state, time_logic)

    # 创建 UI 组件
    window = TimerBall(time_state, time_logic, rest_overlay)
    
    # 设置回调函数
    time_logic.set_callbacks(
        callback_pause=window.on_timer_pause,
        callback_resume=window.on_timer_resume,
        callback_update_ui=window.on_timer_update,
        callback_rest_start=window.on_rest_start,
        callback_rest_end=window.on_rest_end
    )

    sys.exit(app.exec_())