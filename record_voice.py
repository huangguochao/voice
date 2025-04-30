# record_voice.py (改进版)
import sounddevice as sd
import soundfile as sf
import numpy as np
import time

def list_input_devices():
    """获取所有输入设备"""
    devices = sd.query_devices()
    input_devices = [{"id": i, "name": d['name']} 
                   for i, d in enumerate(devices) 
                   if d['max_input_channels'] > 0]
    return input_devices

def validate_device(device_id):
    """验证设备ID有效性"""
    devices = sd.query_devices()
    if device_id < 0 or device_id >= len(devices):
        raise ValueError("设备ID超出范围")
    if devices[device_id]['max_input_channels'] == 0:
        raise ValueError("选择的设备不是输入设备")
    return True

def record_audio(filename, duration=5, fs=16000, device_id=None):
    """核心录音函数"""
    try:
        # 设置设备参数
        sd.check_input_settings(
            device=device_id,
            channels=1,
            dtype='float32',
            samplerate=fs
        )
        
        print(f"\n将在3秒后开始录音（总时长{duration}秒）...")
        for i in range(3, 0, -1):
            print(f"{i}...", end=' ', flush=True)
            time.sleep(1)
        print("\n开始录音！")
        
        # 执行录音
        recording = sd.rec(
            int(duration * fs),
            samplerate=fs,
            channels=1,
            device=device_id,
            blocking=True
        )
        
        # 验证录音数据
        if np.max(np.abs(recording)) < 0.001:  # 检测静音
            raise ValueError("未检测到有效音频输入")
        
        sf.write(filename, recording, fs)
        return True
    except sd.PortAudioError as e:
        raise RuntimeError(f"音频设备错误: {str(e)}")
    except sf.LibsndfileError as e:
        raise IOError(f"文件保存失败: {str(e)}")

def main():
    """主程序"""
    try:
        print("=== 专业级音频录制程序 ===")
        print("提示：请使用管理员权限运行本程序")
        
        devices = list_input_devices()
        if not devices:
            print("❌ 未找到可用的输入设备！")
            print("可能原因：")
            print("1. 麦克风未正确连接")
            print("2. 驱动程序未安装")
            return

        print("\n可用输入设备：")
        for dev in devices:
            print(f"[{dev['id']}] {dev['name']}")

        device_id = int(input("\n请输入麦克风设备ID: "))
        validate_device(device_id)

        filename = input("输入保存文件名（默认：my_voice.wav）: ") or "my_voice.wav"
        duration = int(input("输入录音时长（秒，建议5-10）: ") or 5)

        print("\n请准备好后朗读以下文本：")
        print("+"*40)
        print("红鲤鱼与绿鲤鱼与驴，12345，67890，Hello World!")
        print("+"*40)

        if record_audio(filename, duration=duration, fs=16000, device_id=device_id):
            print(f"\n✅ 录音成功！文件已保存到：{filename}")
            print("文件验证：")
            print(f"- 时长：{duration}秒")
            print("- 格式：16kHz WAV 单声道")
            print("- 建议用媒体播放器检查文件")
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        print("故障排查：")
        print("1. 检查麦克风是否被其他程序占用")
        print("2. 尝试更换USB接口（如果是外置麦克风）")
        print("3. 在系统设置中测试麦克风")

if __name__ == "__main__":
    main()
