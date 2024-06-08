import os
import pygame
import random

# 初始化pygame
pygame.init()

# 设置音频播放的目录
audio_dir = 'E:\sizu_guosai\onnx\yuyin'

# 获取目录下的所有音频文件
audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith(('.wav', '.mp3', '.ogg'))]

# 如果有音频文件，随机选择一个文件并播放
if audio_files:
    # 选择一个随机音频文件
    file_path = audio_files[2]

    # 加载音频文件
    pygame.mixer.music.load(file_path)

    # 播放音频文件
    pygame.mixer.music.play()

    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)