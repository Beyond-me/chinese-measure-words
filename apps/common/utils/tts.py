# -*- coding: utf-8 -*-
# @Time    : 2026/5/27 08:52
# @Author  : lihaizhen
# @File    : tts.py
# @Software: PyCharm
# @Desc    :

# common/utils/tts.py
import os
from gtts import gTTS
from django.conf import settings

def generate_audio(word: str, lang='zh'):
    filename = f'media/audio/{lang}/{word}.mp3'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    tts = gTTS(word, lang=lang)
    tts.save(filename)
    return filename

def generate_tts_audio(text: str, lang: str = 'zh') -> str:
    """
    生成 TTS 音频文件
    :param text: 要朗读的文本
    :param lang: zh / en
    :return: 相对路径（可直接存入 FileField）
    """
    if not text:
        return ''

    safe_text = text.strip().replace('/', '_')
    filename = f'{safe_text}.mp3'
    relative_path = f'audio/{lang}/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # 避免重复生成
    if not os.path.exists(full_path):
        tts = gTTS(text=text, lang=lang)
        tts.save(full_path)

    return relative_path