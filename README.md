# voice
用于学习声音与文本之间的转化处理操作

# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple torch==2.0.1  torchaudio==2.0.2  soundfile==0.12.1  resemblyzer==0.1.4   TTS==0.22.0  --prefer-binary

（最终目标，录制个人声音分析音色，仅根据文字生成个人讲话的音频。）

1) cn_text_to_wav.py  根据中文文本生成语音wav文件

2) wav_to_cn_text.py  将wav中文语音文件转化成文本

3) record_voice.py 打开麦克风录制个人声音保存为wav文件
   
4) praat.py 提取声音特征 
