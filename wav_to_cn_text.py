from vosk import Model, KaldiRecognizer
import wave
import json
import os

def vosk_asr(wav_path, model_path=r"E:\models\vosk-model-cn-0.22"):
    """
    离线中文语音识别（需下载中文模型）
    模型下载：https://alphacephei.com/vosk/models
    """
    # 验证模型路径
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"未找到Vosk中文模型，请确认路径: {model_path}")
    
    # 加载模型
    model = Model(model_path)
    
    # 初始化识别器
    recognizer = KaldiRecognizer(model, 16000)

    # 读取音频文件
    with wave.open(wav_path, "rb") as wf:
        # 验证音频格式
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
            raise ValueError("音频格式需要是单声道16位PCM格式")
            
        # 分块读取并识别
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                pass

    # 获取最终结果
    result = json.loads(recognizer.FinalResult())
    return result["text"]
    

# 使用示例
text = vosk_asr(r".\output_pyttsx3.wav")
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(text)
