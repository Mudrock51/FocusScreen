import os

def get_file_normpath(path: str):
    """基于当前文件的目标文件路径"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(base_dir, path)
    target_path = os.path.normpath(target_path)
    return target_path

def get_image_list(image_path):
    # 支持获取 jpg/png/bmp 等格式的图片数量
    return [
        f for f in os.listdir(image_path)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))
    ]