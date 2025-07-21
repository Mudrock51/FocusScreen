from PyQt5.QtMultimedia import QSound

from core.utils.utils import resource_path, get_sound_list

import os
import random

class SoundPlayer:
    def __init__(self):
        # 随机提示音目录
        self.sound_dir = resource_path("src/assets/wav")
        # 随机提示音集合
        self.sound_list = get_sound_list(self.sound_dir)

    def play(self):
        """播放随机提示音"""
        if os.path.exists(self.sound_dir):
            sound_path = os.path.join(self.sound_dir, random.choice(self.sound_list))
            QSound.play(sound_path)
        else:
            QSound.play()