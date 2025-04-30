# voice_synthesizer.py
# pip install numpy scipy soundfile librosa
# voice_synthesizer.py (修正版)
# #python voice_synthesizer.py -b input.txt -c output.wav
import librosa  # 必须添加
import numpy as np
import soundfile as sf
from scipy import signal
from scipy.io import wavfile

def load_features(pitch_path, mel_path):
    """加载预提取的特征"""
    pitch = np.loadtxt(pitch_path)
    mel = np.loadtxt(mel_path, delimiter=",").T
    return pitch, mel

def text_to_speech(text, pitch, mel, sr=16000):
    """改进后的语音合成逻辑"""
    # ...（保持之前的基频处理部分不变）...

    # 4. 梅尔频谱处理（修复形状问题）
    n_mels, n_frames = mel.shape
    mel_fb = librosa.filters.mel(sr=sr, n_fft=512, n_mels=n_mels)
    
    # 生成幅度谱（转置对齐STFT格式）
    mag = np.dot(mel.T, mel_fb).T  # 形状变为 (n_freq, n_frames)
    
    # 初始化相位（与mag形状一致）
    phase = 2 * np.pi * np.random.rand(*mag.shape)
    stft = mag * np.exp(1j*phase)

    # 5. Griffin-Lim迭代（修复形状一致性）
    for _ in range(32):
        # STFT逆变换+正变换保持形状
        audio = librosa.istft(stft, hop_length=256)
        stft_new = librosa.stft(audio, n_fft=512, hop_length=256)
        
        # 保持相位更新时的形状一致性
        stft = mag * np.exp(1j * np.angle(stft_new))
    audio = librosa.istft(stft)
    
    # 6. 后处理
    audio = librosa.effects.preemphasis(audio, coef=0.97)
    audio = np.tanh(audio * 3) * 0.8
    
    return audio

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", required=True)
    parser.add_argument("-c", required=True)
    args = parser.parse_args()
    
    pitch, mel = load_features("pitch.txt", 
                              "mel.csv")
    
    with open(args.b, "r", encoding="utf-8") as f:
        text = f.read().strip()
    
    audio = text_to_speech(text, pitch, mel)
    sf.write(args.c, audio, 16000)
    print(f"✅ 合成完成：{args.c}")
