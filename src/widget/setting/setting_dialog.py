from PyQt5.QtWidgets import QLabel, QDialog, QFormLayout, QSpinBox, QPushButton, QHBoxLayout

from core.utils.const import FOCUS_LIMIT_SECONDS, REST_TIME, REMIND_THRESHOLD

class SettingDialog(QDialog):
    def __init__(
            self, 
            focus_seconds=FOCUS_LIMIT_SECONDS, 
            remind_threshold=REMIND_THRESHOLD,
            rest_lower=3*60, 
            rest_upper=5*60, 
            rest_time=REST_TIME, 
            parent=None
        ):
        super().__init__(parent)
        self.setWindowTitle("专注设置")
        self.setFixedSize(340, 170)
        layout = QFormLayout(self)

        ### 专注总时长
        # QHBoxLayout 基于 horizontal(水平) 排版
        focus_layout = QHBoxLayout()
        self.focus_min = QSpinBox(self)
        self.focus_min.setRange(0, 240)
        self.focus_min.setValue(focus_seconds // 60)
        self.focus_sec = QSpinBox(self)
        self.focus_sec.setRange(0, 59)
        self.focus_sec.setValue(focus_seconds % 60)
        # 添加组件, 实现横向排版
        focus_layout.addWidget(self.focus_min)
        focus_layout.addWidget(QLabel("分:"))
        focus_layout.addWidget(self.focus_sec)
        focus_layout.addWidget(QLabel("秒"))
        # 在 SettingDialog 页面下作为一个新的 Row 添加上去
        layout.addRow("专注总时长：", focus_layout)

        ### 专注提醒阈值
        remind_layout = QHBoxLayout()
        self.remind_min = QSpinBox(self)
        self.remind_min.setRange(1, 20)
        self.remind_min.setValue(remind_threshold // 60)
        self.remind_sec = QSpinBox(self)
        self.remind_sec.setRange(0, 59)
        self.remind_sec.setValue(remind_threshold % 60)
        remind_layout.addWidget(self.remind_min)
        remind_layout.addWidget(QLabel("分:"))
        remind_layout.addWidget(self.remind_sec)
        remind_layout.addWidget(QLabel("秒"))
        layout.addRow("专注提醒阈值：", remind_layout)

        # 专注时间下限
        lower_layout = QHBoxLayout()
        self.lower_min = QSpinBox(self)
        self.lower_min.setRange(0, 60)
        self.lower_min.setValue(rest_lower // 60)
        self.lower_sec = QSpinBox(self)
        self.lower_sec.setRange(0, 59)
        self.lower_sec.setValue(rest_lower % 60)
        lower_layout.addWidget(self.lower_min)
        lower_layout.addWidget(QLabel("分:"))
        lower_layout.addWidget(self.lower_sec)
        lower_layout.addWidget(QLabel("秒"))
        layout.addRow("专注时间下限：", lower_layout)

        # 专注时间上限
        upper_layout = QHBoxLayout()
        self.upper_min = QSpinBox(self)
        self.upper_min.setRange(0, 120)
        self.upper_min.setValue(rest_upper // 60)
        self.upper_sec = QSpinBox(self)
        self.upper_sec.setRange(0, 59)
        self.upper_sec.setValue(rest_upper % 60)
        upper_layout.addWidget(self.upper_min)
        upper_layout.addWidget(QLabel("分:"))
        upper_layout.addWidget(self.upper_sec)
        upper_layout.addWidget(QLabel("秒"))
        layout.addRow("专注时间上限：", upper_layout)

        # 休息时间
        rest_layout = QHBoxLayout()
        self.rest_sec = QSpinBox(self)
        self.rest_sec.setRange(10, 30)
        self.rest_sec.setValue(rest_time)
        rest_layout.addWidget(self.rest_sec)
        rest_layout.addWidget(QLabel("秒"))
        layout.addRow("设置休息时间:", rest_layout)

        # 按钮
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("保存", self)
        self.cancel_btn = QPushButton("取消", self)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addRow(btn_layout)

        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def get_settings(self):
        focus_limit_seconds = self.focus_min.value() * 60 + self.focus_sec.value()
        remind_threshold = self.remind_min.value() * 60 + self.remind_sec.value()
        rest_lower_time = self.lower_min.value() * 60 + self.lower_sec.value()
        rest_upper_time = self.upper_min.value() * 60 + self.upper_sec.value()
        rest_time = self.rest_sec.value()
        return {
            "focus_limit_seconds": focus_limit_seconds,
            "remind_threshold": remind_threshold,
            "rest_lower_time": rest_lower_time,
            "rest_upper_time": rest_upper_time,
            "rest_time": rest_time
        }