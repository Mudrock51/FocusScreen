import os
import sys

def resource_path(relative_path):
    """获取资源文件的绝对路径, 兼容打包后和开发环境"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def get_file_normpath(path: str):
    """基于当前文件的目标文件路径"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(base_dir, path)
    target_path = os.path.normpath(target_path)
    return target_path

def get_sound_list(sound_path):
    return [
        s for s in os.listdir(sound_path)
        if s.lower().endswith(('.wav'))
    ]

def get_image_list(image_path):
    # 支持获取 jpg/png/bmp 等格式的图片数量
    return [
        f for f in os.listdir(image_path)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))
    ]