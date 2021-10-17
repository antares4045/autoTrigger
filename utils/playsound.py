import sounddevice as sd
import soundfile as sf


def playsound(path, blocking=False):
    data, fs = sf.read(path)
    sd.play(data, fs)
    if blocking:
        sd.wait()