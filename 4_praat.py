import librosa
import numpy as np

y, sr = librosa.load("my_voice.wav", sr=16000)

# 提取基频
f0 = librosa.pyin(y, fmin=80, fmax=400)[0]
np.savetxt("pitch.txt", f0)

# 提取梅尔特征
mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=26)
np.savetxt("mel.csv", mel.T, delimiter=",")
