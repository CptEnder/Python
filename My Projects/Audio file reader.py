"""
Created on Thu 04 Jun 16:40 2020
Finished on
@author: Cpt.Ender
                                  """
from numpy import fft
import matplotlib.pyplot as plt
import sounddevice as sd
from pydub import AudioSegment
import time

filename = 'Sources\\Los_Angelenos.mp3'
sound = AudioSegment.from_mp3(filename)
data = sound.get_array_of_samples()
chunk = 8 * 1024

f = sound.frame_rate
duration = int(sound.duration_seconds + 1)

freq_fft = []
for i in range(int(sound.frame_count() / chunk)):
    data_chunk = data[i * chunk:(i + 1) * chunk]
    temp = abs(fft.fft(data_chunk))
    freq_fft.append(temp[0:f // 2])

sd.play(data[::2], f)
start_time = time.time()
dt = duration / int(sound.frame_count() / chunk)
for f_fft in freq_fft:
    tik = time.time()
    plt.clf()
    plt.semilogx(f_fft[::4])
    plt.xlim(10, 1000)
    # plt.pause(abs(dt-(time.time()-tik)))
    plt.pause(1 / f)
    print(time.time() - tik, dt - (time.time() - tik))
    time.sleep(abs(dt - (time.time() - tik)))

print(f'Total duration:{time.time() - start_time} seconds')
