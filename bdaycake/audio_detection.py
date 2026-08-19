import pyaudio
import numpy as np
import pythonturtle as turtle

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

THRESHOLD = 17500
STOP_THRESHOLD = 17501

def is_sound(data):
    audio_data = np.frombuffer(data, dtype = np.int16)
    rms = np.sqrt(np.mean(audio_data.astype(np.float64)**2))
    return rms > THRESHOLD, rms

def cake():
    print("Cake")

def main():
    p = pyaudio.PyAudio()

    stream = p.open(format = FORMAT, 
                    channels = CHANNELS, 
                    rate = RATE, 
                    input = True, 
                    frames_per_buffer = CHUNK)

    print("Listening (strg+c zum Beenden)")

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow = False)
            sound, rms = is_sound(data)
            if rms > STOP_THRESHOLD:
                status = cake() if sound else ""
                break



    except KeyboardInterrupt:
        print("\nBeende")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()

