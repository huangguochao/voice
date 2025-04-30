import pyttsx3  # 需要安装：pip install pyttsx3
import time

def cn_text_to_wav(text, filename, rate=200):
    """
    使用本地语音引擎生成中文WAV文件
    注意：需要系统已安装中文语音包（Windows自带，Linux需手动安装）
    
    :param text: 要转换的中文文本
    :param filename: 输出文件名（必须.wav结尾）
    :param rate: 语速（默认200，正常范围150-300）
    """
    try:
        # 初始化引擎
        engine = pyttsx3.init()
        
        # 设置语音参数
        engine.setProperty('rate', rate)          # 语速
        engine.setProperty('volume', 0.9)         # 音量0.0-1.0
        
        # 查找中文语音引擎（Windows示例ID）
        voices = engine.getProperty('voices')
        for voice in voices:
            # 中文语音通常包含'ZH'或'Chinese'标识
            if 'ZH' in voice.id or 'Chinese' in voice.name:
                engine.setProperty('voice', voice.id)
                print(f'使用语音引擎：{voice.name}')
                break
        
        # 生成语音文件
        engine.save_to_file(text, filename)
        engine.runAndWait()
        
        print(f'生成成功：{filename} ({len(text)}字)')
        
    except Exception as e:
        print(f'生成失败：{str(e)}')

# 使用示例
cn_text_to_wav(
    text="当前系统温度42℃，风扇转速每分钟2000转，运行状态正常。",
    filename="output_pyttsx3.wav",
    rate=180
)
